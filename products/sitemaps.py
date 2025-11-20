from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        """
        Return ordered queryset to avoid the
        UnorderedObjectListWarning with pagination.
        """
        return Product.objects.all().order_by("id")

    def lastmod(self, obj):
        """
        Return last modified timestamp if available.
        """
        return getattr(obj, "updated_on", None)

    def location(self, obj):
        """
        Use the canonical product URL from the model.
        """
        return obj.get_absolute_url()


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        """
        Named URL patterns to include in the static sitemap.
        Ensure these names exist in your project.
        """
        return [
            "home",             # home page
            "products",         # all products list page
            "contact:index",    # contact app (urls.py name="index")
            "faqs:index",       # FAQ page
        ]

    def location(self, item):
        return reverse(item)
