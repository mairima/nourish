# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def image_preview(self, obj):
        """
        Show a small preview of the product image in admin.
        Uses unified image_url property from the Product model.
        """
        if not obj.image_url:
            return '-'
        return format_html('<img src="{}" style="height:40px; width:auto;" />', obj.image_url)
    image_preview.short_description = 'Image'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')
