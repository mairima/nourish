"""Nourish URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, StaticViewSitemap

# Sitemap dictionary
sitemaps_dict = {
    "products": ProductSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    # Admin and authentication
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),

    # Core apps
    path("", include("home.urls")),
    path(
        "products/",
        include(("products.urls", "products"), namespace="products"),
    ),
    path("bag/", include("bag.urls")),
    path(
        "checkout/",
        include(("checkout.urls", "checkout"), namespace="checkout"),
    ),
    path("profiles/", include("profiles.urls")),
    path("contact/", include("contact.urls")),
    path("faqs/", include(("faqs.urls", "faqs"), namespace="faqs")),
    path("newsletter/", include("newsletter.urls")),

    # Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

# 404 error handler
handler404 = "nourish.views.handler404"
