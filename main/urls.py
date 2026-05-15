from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects_all, name="projects"),
    path("contact/", views.contact_submit, name="contact_submit"),
]
