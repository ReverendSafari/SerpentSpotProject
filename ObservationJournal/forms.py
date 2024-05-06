from django import forms
from .models import UserObservation
from Identification.models import SnakeSpecies

class ObservationForm(forms.ModelForm):
    """
    A form for creating or updating user observations.

    This form is used to collect information about a user's observation, including the observation text,
    an optional observation picture, and the species of snake observed.

    Attributes:
        species (forms.ModelChoiceField): A field for selecting the species of snake observed.
        observation (forms.CharField): A field for entering the observation text.
        observation_pic (forms.ImageField): A field for uploading an observation picture.

    """

    species = forms.ModelChoiceField( # A field for selecting the species of snake observed
        queryset=SnakeSpecies.objects.all(), # The queryset for the field is all snake species
        required=True, # The field is required
        widget=forms.Select(attrs={'class': 'form-control'}) # Add the 'form-control' class to the field
    )

    class Meta:
        model = UserObservation # The UserObservation model that the form is associated with
        fields = ['observation', 'observation_pic', 'species'] # The fields that will be displayed in the form
        widgets = { # Add hidden input fields for latitude and longitude
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the ObservationForm.

        This method adds Bootstrap classes to the form fields to enhance the user interface.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """

        super(ObservationForm, self).__init__(*args, **kwargs) # Call the parent class constructor
        self.fields['observation'].widget.attrs.update({'class': 'form-control'}) # Add the 'form-control' class to the observation field
        self.fields['observation_pic'].widget.attrs.update({'class': 'form-control-file'}) # Add the 'form-control-file' class to the observation_pic field
