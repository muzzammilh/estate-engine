
from django import forms

from .models import Message, TenancyContract


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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

        return cleaned_data


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }
