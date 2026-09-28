from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import datetime

from main.models import Projects, Academic

from main.forms import ProjectForm, AcademicForm

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rama",
        "full_name": "Narendra Rama Prawira",
        "npm": "2506606490",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
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


@login_required(login_url="/login/") 
def create_academic(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = AcademicForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Academic Record Added!")
        return redirect("main:show_academic")

    context = {
        "name": "Rama",
        "form": form,
        "form_title": "Add Academic Record",
        "button_text": "Add Academic",
    }
    return render(request, "academic_form.html", context)

@login_required(login_url="/login/") 
def edit_academic(request, academic_id):
    if not request.user.is_superuser:
            raise PermissionDenied
    
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

@login_required(login_url="/login/") 
def delete_academic(request, academic_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

    academic_json = serializers.serialize("json", academics, use_natural_foreign_keys=True)
    return HttpResponse(academic_json, content_type="application/json")

@login_required(login_url="/login/")
def toggle_star_academic(request, academic_id):
    academic = get_object_or_404(Academic, pk=academic_id)

    if request.method == "POST":
        if request.user in academic.starred_by.all():
            academic.starred_by.remove(request.user)
        else:
            academic.starred_by.add(request.user)

    return redirect("main:show_academic")


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

@login_required(login_url="/login/") 
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    projects = get_object_or_404(Projects, pk=project_id)

    if request.method == "POST":
        if request.user in projects.starred_by.all():
            projects.starred_by.remove(request.user)
        else:
            projects.starred_by.add(request.user)

    return redirect("main:show_projects")

# Auth

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Rama",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rama",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

