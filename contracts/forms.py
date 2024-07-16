
from django import forms

from .models import TenancyContract


class DateInput(forms.DateInput):
    input_type = 'date'


class TenancyContractForm(forms.ModelForm):

    class Meta:
        model = TenancyContract
        fields = ['unit', 'tenant', 'owner', 'start_date', 'end_date', 'rent_agreed', 'active']
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
        }
