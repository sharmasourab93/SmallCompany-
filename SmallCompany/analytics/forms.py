from upload.models import DriverDetails
from django import forms


class HomeForm(forms.Form):

    driver = forms.ModelChoiceField(queryset=
                                    DriverDetails.objects.all()\
                                    .order_by('serial_id'))