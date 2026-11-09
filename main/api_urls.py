from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    # Projects
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),

    # Academic
    path("academic/", api_views.academic_list, name="academic-list"),
    path("academic/<uuid:academic_id>/", api_views.academic_detail, name="academic-detail"),
    path("academic/<uuid:academic_id>/star/", api_views.academic_star, name="academic-star"),
]
