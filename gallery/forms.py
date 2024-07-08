from django import forms
from django.forms import modelformset_factory

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']


ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)


DocFormSet = modelformset_factory(Image, form=ImageForm, extra=0, max_num=2, min_num=2)
