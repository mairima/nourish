from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit/", views.profile, name="profile_edit"),
    path('order_history/<order_number>', views.order_history, name='order_history'),
]