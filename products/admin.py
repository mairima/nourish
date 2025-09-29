# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def image_preview(self, obj):
        url = obj.static_image_url if obj.image_filename else (obj.image_url or '')
        if not url:
            return '-'
        return format_html('<img src="{}" style="height:40px; width:auto;" />', url)
    image_preview.short_description = 'Image'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
