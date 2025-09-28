from django import forms
from django_countries import countries
from .widgets import SafeCountrySelectWidget   # <-- use your safe widget
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "street_address1", "street_address2",
            "town_or_city", "postcode", "country", "county",
        )
        widgets = {
            "country": SafeCountrySelectWidget(
                attrs={"class": "form-control stripe-style-input", "id": "id_country"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make sure the safe widget is actually in use
        f = self.fields["country"]
        if not isinstance(f.widget, SafeCountrySelectWidget):
            f.widget = SafeCountrySelectWidget(
                attrs={"class": "form-control stripe-style-input", "id": "id_country"}
            )

        # Avoid BlankChoiceIterator: no empty_label; set concrete choices
        if hasattr(f, "empty_label"):
            f.empty_label = None
        concrete = [("", "Select a country *")] + list(countries)
        f.choices = concrete
        f.widget.choices = concrete
        if hasattr(f.widget, "_choices"):
            f.widget._choices = concrete

        # (rest of your placeholder/class logic)
