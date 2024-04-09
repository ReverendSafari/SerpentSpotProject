# forms.py in your Django app

from django import forms
from .models import State

class StateForm(forms.Form):
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Select a State")
