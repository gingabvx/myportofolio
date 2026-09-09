from django.shortcuts import render


def show_main(request):
    return render(request, "index.html")

def show_academic(request):
    return render(request, 'academic.html')

def show_projects(request):
    return render(request, 'projects.html')