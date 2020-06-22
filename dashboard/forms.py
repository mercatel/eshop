from django import forms

from shop.models import Product, ImageProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = ImageProduct
        fields = '__all__'

