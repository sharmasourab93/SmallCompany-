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

    # TODO: Tips for Adding One URL One View and dynamic outputs
    # Driver Form to accept Optional Year and optional Month
    

class FuelSpendForm(forms.Form):
    CHOICES = [
        ('0', 'Show All Records'),
        ('1', 'Show Total Spend By Month/Year')
        ]
    
    fuel_spend = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        empty_label="Select Fuel",
        )
    by_time = forms.ChoiceField(choices=CHOICES,
                                widget=forms.RadioSelect)

    # TODO: Tips for Adding One URL One View and dynamic outputs
    # Fuel Form to accept Optional Year and optional Month
