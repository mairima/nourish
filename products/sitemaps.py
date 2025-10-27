from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_on  # or your last modified field

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['home', 'products', 'about', 'contact']  # your static page names

    def location(self, item):
        return reverse(item)
