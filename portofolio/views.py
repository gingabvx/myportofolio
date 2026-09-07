from django.shortcuts import render


def landing_page(request):
    return render(request, "index.html")

def academic(request):
    return render(request, 'academic.html')

def projects(request):
    return render(request, 'projects.html')