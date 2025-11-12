from django.urls import path
from . import views
from .webhooks import webhook as stripe_webhook

app_name = "checkout"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path(
        "checkout_success/<order_number>/",
        views.checkout_success,
        name="checkout_success",
    ),
    path(
        "cache_checkout_data/",
        views.cache_checkout_data,
        name="cache_checkout_data",
    ),
    path("apply-discount/", views.apply_discount, name="apply_discount"),
    path("wh/", stripe_webhook, name="webhook"),
    path(
        "order_history/<order_number>/",
        views.order_history,
        name="order_history",
    ),
]
