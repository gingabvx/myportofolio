from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("projects/add/", views.create_project, name="create_project"),
    path('projects/', views.show_projects, name='show_projects'),
    path('academic/', views.show_academic, name='show_academic'),
    
    path("api/projects/", views.get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", views.delete_project, name="delete_project")

]