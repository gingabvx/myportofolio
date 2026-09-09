from django.shortcuts import render

from main.models import Projects


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
    return render(request, 'academic.html')

def show_projects(request):
    context = {
        "name": "Rama",
        "projects_list": Projects.objects.all(),
    }
    return render(request, 'projects.html', context)