from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Contact Form for submission"""
    class Meta:
        model = Contact
        exclude = ("sent",)
