from django import forms
from .models import UserObservation

class ObservationForm(forms.ModelForm):
    class Meta:
        model = UserObservation
        fields = ['observation', 'observation_pic']