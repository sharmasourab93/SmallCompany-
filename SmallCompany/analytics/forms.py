from upload.models import DriverDetails, FuelType
from django import forms


class DriverSpendForm(forms.Form):
        
    driver = forms.ModelChoiceField(
        queryset=DriverDetails.objects.all(),
        empty_label="Select Driver"
        )
    

class FuelSpendForm(forms.Form):
    fuel_spend = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        empty_label="Select Fuel",
        )
