from upload.models import DriverDetails, FuelType
from django import forms


class DriverSpendForm(forms.Form):
    
    CHOICES = [
        ('0', 'Show All Records'),
        ('1', 'Show Total Spend By Month/Year')
        ]
        
    driver = forms.ModelChoiceField(
        queryset=DriverDetails.objects.all(),
        empty_label="Select Driver"
        )
    by_month = forms.ChoiceField(choices=CHOICES,
                                 widget=forms.RadioSelect)


class FuelSpendForm(forms.Form):
    fuel_spend = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        empty_label="Select Fuel",
        )
