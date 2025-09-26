from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import Order


class OrderForm(forms.ModelForm):
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
        # Ensure the select widget is used for country
        widgets = {
            "country": CountrySelectWidget(
                attrs={
                    "class": "form-control stripe-style-input",
                    "id": "id_country",
                }
            )
        }

    def __init__(self, *args, **kwargs):
        """
        Add placeholders/classes, remove labels, set autofocus.
        Keep country as a SELECT (no placeholder on selects).
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "postcode": "Postal Code",
            "town_or_city": "Town or City",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2",
            "county": "County / State",
        }

        # Make sure the widget is CountrySelectWidget even if overridden elsewhere
        if not isinstance(self.fields["country"].widget, CountrySelectWidget):
            self.fields["country"].widget = CountrySelectWidget(
                attrs={"class": "form-control stripe-style-input", "id": "id_country"}
            )

        # Nice blank label for country
        self.fields["country"].empty_label = "Select a country *"

        # Autofocus first text field
        self.fields["full_name"].widget.attrs["autofocus"] = True

        for name, field in self.fields.items():
            # Placeholders on inputs only (selects generally ignore placeholder)
            if name != "country":
                placeholder = placeholders.get(name, "")
                if field.required and placeholder:
                    placeholder = f"{placeholder} *"
                if placeholder:
                    field.widget.attrs["placeholder"] = placeholder

            # Shared classes
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " stripe-style-input").strip()

            # Hide labels (crispy will render nicely)
            field.label = False
