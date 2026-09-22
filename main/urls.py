from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("projects/add/", views.create_project, name="create_project"),
    path('projects/', views.show_projects, name='show_projects'),
    path("projects/<uuid:project_id>/delete/", views.delete_project, name="delete_project"),
    path("api/projects/", views.get_projects_json, name="get_projects_json"),

    # Academic Routes
    path('academic/', views.show_academic, name='show_academic'),
    path('academic/add/', views.create_academic, name='create_academic'),
    path('academic/<uuid:academic_id>/edit/', views.edit_academic, name='edit_academic'),
    path('academic/<uuid:academic_id>/delete/', views.delete_academic, name='delete_academic'),
    path("api/academic/", views.get_academics_json, name="get_academics_json"),
]