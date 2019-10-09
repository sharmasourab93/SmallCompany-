from django import forms
from .models import Document


class UpdateForm(forms.Form):
    DATE_INPUT_FORMATS = ['%d-%m-%Y']
    
    FUEL_OPTIONS = (
        (1, 'CNG'),
        (2, 'PETROL'),
        (3, 'DIESEL'),
        (4, 'HYDROGEN'),
        (5, 'LIQUID NITROGEN'),
        (6, 'BIODIESEL')
        )
    
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
