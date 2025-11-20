from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return getattr(obj, "updated_on", None)

    def location(self, obj):
        return reverse("products:product_detail", args=[obj.id])


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            "home",                 # home page
            "products:products",    # product list page
            "contact:index",        # contact.urls → name="index"
            "faqs:index",           # FAQ page
        ]

    def location(self, item):
        return reverse(item)
