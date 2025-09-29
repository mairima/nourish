from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    """FAQs Form for submission"""
    class Meta:
        model = FAQ
        fields = "__all__"
