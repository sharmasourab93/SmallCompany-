from upload.models import DriverDetails, FuelType
from upload.models import PurchaseRecord
from django.db.models.functions import ExtractYear, ExtractMonth
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


class SpendByTimeForm(forms.Form):
    extract_year = PurchaseRecord.objects\
        .annotate(year=ExtractYear('dated'))\
        .distinct().values_list('year').all()
    extract_month = PurchaseRecord.objects\
        .annotate(month=ExtractMonth('dated'))\
        .distinct().values_list('month').all()
    
    year = forms.ModelChoiceField(queryset=extract_year,
                                  empty_label="Select Year",
                                  required=True)
    month = forms.ModelChoiceField(queryset=extract_month,
                                   empty_label="Select Month",
                                   required=False)
