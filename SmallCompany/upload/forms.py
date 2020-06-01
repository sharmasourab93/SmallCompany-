from django import forms
from .models import Document
import datetime


FUEL_OPTIONS = (
        (1, 'CNG'),
        (2, 'PETROL'),
        (3, 'DIESEL'),
        (4, 'HYDROGEN'),
        (5, 'LIQUID NITROGEN'),
        (6, 'BIODIESEL'))


class UpdateForm(forms.Form):
    DATE_INPUT_FORMATS = ['%d-%m-%Y']
    
    fuel = forms.ChoiceField(choices=FUEL_OPTIONS)
    date = forms.DateField(widget=forms.SelectDateWidget)
    volume = forms.DecimalField(max_digits=5)
    driver_id = forms.CharField(max_length=10)
    
    
class UploadForm(forms.ModelForm):
    # To Bulk Upload from a file
    
    # file = forms.FileField(label="Select a file")
    
    class Meta:
        model = Document
        fields = ('description', 'document')


class PriceUpdateForm(forms.Form):
    fuel = forms.ChoiceField(choices=FUEL_OPTIONS)
    date = forms.DateTimeField(initial=datetime.datetime
                               .now().strftime('%d-%m-%Y %H:%M:%S %p'))
    price = forms.DecimalField(max_digits=5,
                               decimal_places=2)
    
    
class DriverEnrollmentForm(forms.Form):
    name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    registered_on = forms.DateField(input_formats=['%d-%m-%Y %H:%M:%S %p'],
                                    initial=datetime.datetime
                                    .now().strftime('%d-%m-%Y %H:%M:%S %p'))
    serial_id = forms.CharField(max_length=6)