from django import forms
from .models import *


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['Full_name', 'Description']

        widgets = {
            'Имя': forms.TextInput(attrs={'class': 'form-control'}),
            'Описание': forms.Textarea(attrs={'class': 'form-control'}),
        }
