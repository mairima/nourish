from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    """Newsletter Form for submission"""
    class Meta:
        model = Newsletter
        fields = "__all__"