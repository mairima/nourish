from django.contrib import admin

from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin configuration for the FAQ model."""
    list_display = ("question",)
