from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Projects, Academic

from main.forms import ProjectForm, AcademicForm

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

# ACADEMIC FUNCTION

def show_academic(request):
    json_response = get_academics_json(request)
    
    academics = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    academic_list = [item.object for item in academics]
    query = request.GET.get("q", "").strip()

    context = {
        "name": "Rama",
        "academic_list": academic_list,
        "search_query": query,
    }
    return render(request, "academic.html", context)

def create_academic(request):
    form = AcademicForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat akademik baru berhasil ditambahkan!")
        return redirect("main:show_academic")

    context = {
        "name": "Rama",
        "form": form,
        "form_title": "Add Academic Record",
        "button_text": "Add Academic",
    }
    return render(request, "academic_form.html", context)

def edit_academic(request, academic_id):
    academic = get_object_or_404(Academic, pk=academic_id)
    form = AcademicForm(request.POST or None, instance=academic)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Riwayat akademik berhasil diperbarui!")
        return redirect("main:show_academic")

    context = {
        "name": "Rama",
        "form": form,
        "form_title": f"Edit {academic.institution}",
        "button_text": "Save Changes",
    }
    return render(request, "academic_form.html", context)

def delete_academic(request, academic_id):
    academic = get_object_or_404(Academic, pk=academic_id)

    if request.method == "POST":
        academic.delete()
        messages.success(request, "Riwayat akademik berhasil dihapus!")
        return redirect("main:show_academic")

    return redirect("main:show_academic")

def get_academics_json(request):
    query = request.GET.get("q", "").strip()
    academics = Academic.objects.all()

    if query:
        academics = academics.filter(institution__icontains=query)

    academic_json = serializers.serialize("json", academics)
    return HttpResponse(academic_json, content_type="application/json")

# PROJECTS FUNCTION

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
    title_query = request.GET.get("institution", "").strip()
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