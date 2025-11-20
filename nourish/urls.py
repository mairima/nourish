"""Nourish URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

# Correct sitemap imports (from home, not products)
from home.sitemaps import ProductSitemap, StaticViewSitemap

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
    path("bag/", include(("bag.urls", "bag"), namespace="bag")),
    path(
        "checkout/",
        include(("checkout.urls", "checkout"), namespace="checkout"),
    ),
    path("profiles/", include("profiles.urls")),
    path("contact/", include("contact.urls")),
    path("faqs/", include(("faqs.urls", "faqs"), namespace="faqs")),
    path("newsletter/", include("newsletter.urls")),

    # Dynamic Sitemap
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps_dict},
        name="django.contrib.sitemaps.views.sitemap",
    ),

    # robots.txt served from templates
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
        name="robots_txt",
    ),
]

# Error handlers
handler404 = "nourish.views.handler404"
handler500 = "home.views.error_500"
