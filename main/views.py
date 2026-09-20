from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Projects, Academic

from main.forms import ProjectForm

def show_main(request):
    context = {
        "name": "Rama",
        "full_name" : "Narendra Rama Prawira",
        "npm": "2506606490",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student who is passionate about his interest on game development"
            "and web/app development. Always eager to improve my skills and learn new technologies up forward."
        ),
    }
    return render(request, "index.html", context)

def show_academic(request):
    context = {
            "name": "Rama",
            "academic_list": Academic.objects.all(),
        }
    return render(request, 'academic.html', context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rama",
        "projects_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Project added!")
        return redirect("main:show_projects")

    context = {
        "name": "Rama",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Projects.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")