"""
Nourish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, StaticViewSitemap

sitemaps_dict = {
    "products": ProductSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("newsletter/", include("newsletter.urls")),
    path("", include("home.urls")),
    path("products/", include(("products.urls", "products"), namespace="products")),
    path("bag/", include("bag.urls")),
    path("checkout/", include(("checkout.urls", "checkout"), namespace="checkout")),
    path("profiles/", include("profiles.urls")),
    path("contact/", include("contact.urls")),
    path("faqs/", include(("faqs.urls", "faqs"), namespace="faqs")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# Correct custom error handler
handler404 = 'nourish.views.handler404'
