from django import forms
from .models import UserProfile
from django_countries.widgets import CountrySelectWidget

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "default_phone_number",
            "default_country",
            "default_postcode",
            "default_town_or_city",
            "default_street_address1",
            "default_street_address2",
            "default_county",
        ]
        widgets = {
            "default_country": CountrySelectWidget(),
        }
