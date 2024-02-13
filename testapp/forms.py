from django import forms
from django.forms import ModelForm
from .models import *

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('word',)
        labels = {
            'word': '',  # Set the label for the 'word' field to an empty string
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = '__all__'
        widgets = {
            'startdate': DateInput(),
            'enddate': DateInput()
        }
        labels = {
            'startdate': '',
            'enddate': ''
        }
