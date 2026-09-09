from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path('projects/', views.show_projects, name='show_projects'),
    path('academic/', views.show_academic, name='show_academic'), 
]