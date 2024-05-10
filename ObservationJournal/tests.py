from django.test import TestCase
from django import forms
from .forms import ObservationForm
from Identification.models import SnakeSpecies
from django.core.files.uploadedfile import SimpleUploadedFile

# Seamus 
class ObservationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.

        This method is used to create test data for the test case. It creates two instances of the `SnakeSpecies` model
        with different common names and scientific names.

        Args:
            cls: The class object.

        Returns:
            None
        """

        # Setup test data using the correct field names
        SnakeSpecies.objects.create(common_name="Rattlesnake", scientific_name="Crotalus horridus")
        SnakeSpecies.objects.create(common_name="Cobra", scientific_name="Naja naja")

    def test_form_initialization(self):
        """
        Test the initialization and widget configuration of the form.

        This method creates an instance of the ObservationForm and asserts that the widget
        configuration of the form fields is as expected. It checks that the 'species' field
        is a Select widget with the class 'form-control', and that the 'observation' and
        'observation_pic' fields have the class 'form-control' and 'form-control-file'
        respectively.

        """

        form = ObservationForm()
        self.assertIsInstance(form.fields['species'].widget, forms.Select)
        self.assertEqual(form.fields['species'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['observation'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['observation_pic'].widget.attrs['class'], 'form-control-file')

    def test_field_configuration(self):
        """
        Test the configuration of form fields.

        This test checks the configuration of the fields in the ObservationForm.
        It verifies that the 'species' field is required, is an instance of
        forms.ModelChoiceField, and has a queryset with a length of 2.
        """

        form = ObservationForm()
        self.assertTrue(form.fields['species'].required)
        self.assertIsInstance(form.fields['species'], forms.ModelChoiceField)
        self.assertEqual(len(form.fields['species'].queryset), 2)

    def test_form_validation_valid_data(self):
        """
        Test form validation with valid data.

        This method tests the validation of the ObservationForm with valid data.
        It creates a valid_data dictionary containing the necessary data for the form,
        including a valid SnakeSpecies object, an observation description, and a test image.
        The form is then instantiated with the valid_data and checked if it is valid.

        Returns:
            None
        """

        species = SnakeSpecies.objects.first()
        valid_data = {
            'species': species.id,
            'observation': 'Seen near the lake',
            'observation_pic': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        }
        form = ObservationForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_form_validation_invalid_data(self):
        """Test form validation with invalid data.

        This test case checks the form validation when invalid data is provided.
        It creates a dictionary `invalid_data` with invalid values for the form fields.
        The `species` field is set to `None`, which should be invalid as it is required.
        The `observation` field is set to an empty string, which should also be invalid.
        The `ObservationForm` is then instantiated with the `invalid_data`.
        The test asserts that the form is not valid and that the `species` and `observation`
        fields have errors in the form.
        """

        invalid_data = {
            'species': None,  # This should be invalid as species is required
            'observation': '',  # Empty observation should also be invalid
        }
        form = ObservationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('species', form.errors)
        self.assertIn('observation', form.errors)

    def test_form_saves_correctly(self):
        """
        Test that a valid form can be saved correctly.

        This test verifies that a valid form can be saved correctly by creating a test data dictionary
        with the required form fields and submitting it to the ObservationForm. It then checks if the
        form is valid and proceeds to save the form data. Finally, it asserts that the saved observation
        has the expected species and observation values.
        """
        
        species = SnakeSpecies.objects.first()
        data = {
            'species': species.id,
            'observation': 'Seen in the woods',
            'observation_pic': SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        }
        form = ObservationForm(data=data)
        if form.is_valid():
            observation = form.save(commit=False)
            self.assertEqual(observation.species.common_name, species.common_name)
            self.assertEqual(observation.observation, 'Seen in the woods')
