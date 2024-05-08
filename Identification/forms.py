# forms.py in your Django app
#@ Safari
from django import forms
from .models import State

# Create a form to select a state
class StateForm(forms.Form):
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Select a State")
