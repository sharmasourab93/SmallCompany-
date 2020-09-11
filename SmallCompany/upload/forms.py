from django import forms
from .models import Document
from .models import DriverDetails, FuelType
from django.contrib.auth.forms import forms
from django.contrib.auth import authenticate
from datetime import date


FUEL_OPTIONS = (
        (1, 'CNG'),
        (2, 'PETROL'),
        (3, 'DIESEL'),
        (4, 'HYDROGEN'),
        (5, 'LIQUID NITROGEN'),
        (6, 'BIODIESEL'))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                               max_length=100)

    def login(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        return user
        
        
class UploadForm(forms.ModelForm):
    # To Bulk Upload from a file
    
    # file = forms.FileField(label="Select a file")
    
    class Meta:
        model = Document
        fields = ('description', 'document')


class PriceUpdateForm(forms.Form):
    fuel = forms.ChoiceField(choices=FUEL_OPTIONS)
    date = forms.DateField(input_formats=['%d-%m-%Y'],
                           initial=date.today)
    price = forms.DecimalField(max_digits=5,
                               decimal_places=2)
    
    
class DriverEnrollmentForm(forms.Form):
    name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=200)
    registered_on = forms.DateField(input_formats=['%d-%m-%Y'],
                                    initial=date.today)
    serial_id = forms.CharField(max_length=6)
    
    
class PurchaseUpdateForm(forms.Form):

    price = forms.DecimalField()
    volume = forms.DecimalField()
    dated = forms.DateField(initial=date.today)
    driver_id = forms.ModelChoiceField(
        queryset=DriverDetails.objects.all(),
        empty_label="Select Driver"
        )
    fuel_type = forms.ModelChoiceField(
        queryset=FuelType.objects.all(),
        empty_label="Select Fuel"
        )
