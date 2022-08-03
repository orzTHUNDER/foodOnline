from django import forms
from vendor.models import Vendor


class VendorForm(forms.ModelForm): #inheriting from forms.ModelForm
    class Meta:
        model = Vendor  #giiving model name
        fields = ['vendor_name', 'vendor_license']