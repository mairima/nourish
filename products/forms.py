from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=ClearableFileInput()
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        self.fields['category'].choices = friendly_names

        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
