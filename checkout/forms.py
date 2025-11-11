from django import forms
from django_countries import countries
from .widgets import SafeCountrySelectWidget
from .models import Order


class OrderForm(forms.ModelForm):
    """Form for creating or updating an order."""

    class Meta:
        model = Order
        fields = (
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "town_or_city",
            "postcode",
            "country",
            "county",
        )
        widgets = {
            "country": SafeCountrySelectWidget(
                attrs={
                    "class": "form-control stripe-style-input",
                    "id": "id_country",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with safe country widget and valid choices."""
        super().__init__(*args, **kwargs)

        field = self.fields["country"]

        # Ensure safe widget is used
        if not isinstance(field.widget, SafeCountrySelectWidget):
            field.widget = SafeCountrySelectWidget(
                attrs={
                    "class": "form-control stripe-style-input",
                    "id": "id_country",
                }
            )

        # Remove empty label and apply concrete country list
        if hasattr(field, "empty_label"):
            field.empty_label = None

        concrete = [("", "Select a country *")] + list(countries)
        field.choices = concrete
        field.widget.choices = concrete

        if hasattr(field.widget, "_choices"):
            field.widget._choices = concrete

        # Add placeholders and styling if needed
        # for name, f in self.fields.items():
        #     f.widget.attrs["class"] = "form-control stripe-style-input"
