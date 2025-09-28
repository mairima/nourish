from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit/", views.profile_edit, name="profile_edit"),
]
