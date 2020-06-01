from upload.models import DriverDetails
from django import forms


class DriverSpendForm(forms.Form):

    driver = forms.ModelChoiceField(
        queryset=DriverDetails.objects.all())
    

class FuelSpendForm(forms.Form):
    fuel_spend = forms.ModelChoiceField(
        queryset=DriverDetails.objects.all()
        )
