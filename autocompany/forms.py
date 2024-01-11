# myapp/forms.py

from django import forms
from .models import SampleTable

class SampleModelForm(forms.ModelForm):
    class Meta:
        model = SampleTable
        fields = ['name', 'description']
