from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']     #fields which render inside the form(on html)
        #other fields in caetgory gets automatically assigned