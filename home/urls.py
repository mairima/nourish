from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-conditions/", views.terms_conditions, name="terms_conditions"),
]
