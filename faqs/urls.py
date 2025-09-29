# faqs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.faqs, name="faqs"),
    path("add_faq", views.add_faq, name="add_faq"),
    path("update_faq/<int:id>/", views.update_faq, name="update_faq"),
    path("delete_faq/<int:id>/", views.delete_faq, name="delete_faq"),
]