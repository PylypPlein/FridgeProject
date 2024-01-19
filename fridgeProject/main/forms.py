from django import forms
from .models import Fridge, Product

class FridgeForm(forms.ModelForm):
    class Meta:
        model = Fridge
        fields = ['name', 'brand', 'model', 'capacity']

class ProductManageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category','quantity']  # Exclude 'quantity' from the form fields

class FridgeProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['quantity']  # Include 'quantity' for associating quantity when adding to a fridge
