from django import forms
from .models import NewsletterSubscription


class NewsletterForm(forms.ModelForm):
    """Newsletter Form for submission"""
    class Meta:
        model = NewsletterSubscription
        fields = ['email']