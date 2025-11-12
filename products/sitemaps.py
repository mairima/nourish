from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    # Return all products
    def items(self):
        return Product.objects.all()

    # Return last modified date
    def lastmod(self, obj):
        return getattr(obj, "updated_on", None)


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    # Return static page names
    def items(self):
        return ["home", "products", "about", "contact"]

    # Reverse URL for each static page
    def location(self, item):
        return reverse(item)
