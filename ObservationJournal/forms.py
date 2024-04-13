from django import forms
from .models import UserObservation

from Identification.models import SnakeSpecies

class ObservationForm(forms.ModelForm):
    species = forms.ModelChoiceField(queryset=SnakeSpecies.objects.all(), required=True)
    class Meta:
        model = UserObservation
        fields = ['observation', 'observation_pic', 'species']