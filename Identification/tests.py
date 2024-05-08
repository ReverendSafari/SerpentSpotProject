
from django.test import TestCase, Client
from django.urls import reverse
from django.forms import ModelChoiceField
from .forms import StateForm
from .models import State, SnakeSpecies

"""
UNIT TESTS
Trying to get basic tests surrounding the models, views, and our form
Not meant to be entirely comprehensive just a starting point to ensure basic functionality

"""
# @ Safari (Whole file)

#Test our models
class ModelTests(TestCase):
    def test_create_state(self):
        state = State.objects.create(name="Florida", abbreviation="FL")
        self.assertEqual(state.name, "Florida")
        self.assertEqual(state.abbreviation, "FL")

    def test_create_snake_species(self):
        state = State.objects.create(name="California", abbreviation="CA")
        snake = SnakeSpecies.objects.create(
            common_name="Garter Snake",
            scientific_name="Thamnophis sirtalis",
            description="A common non-venomous snake found throughout North America.",
            venomous=False
        )
        snake.states.add(state)
        self.assertEqual(snake.common_name, "Garter Snake")
        self.assertTrue(snake.states.filter(name="California").exists())

#Test our views
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.state = State.objects.create(name="Nevada", abbreviation="NV")
        self.snake = SnakeSpecies.objects.create(
            common_name="Copperhead",
            scientific_name="Agkistrodon contortrix",
            description="A venomous species found in the Eastern United States.",
            venomous=True
        )
        self.snake.states.add(self.state)

    def test_select_state_view_no_state(self):
        response = self.client.get(reverse('id_view'))  # Updated view name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'id.html')
        self.assertIn('the USA', response.context['selected_state_name'])

    def test_select_state_view_with_state(self):
        url = reverse('id_view') + '?state=' + str(self.state.id)  # Updated view name
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.state.name, response.context['selected_state_name'])
        self.assertIn(self.snake.common_name, response.context['species'][0]['common_name'])

    def test_render_education_view(self):
        response = self.client.get(reverse('education_view'))  # Updated view name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')

#Test our form (singular lol)
class StateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        State.objects.create(name="California", abbreviation="CA")
        State.objects.create(name="Texas", abbreviation="TX")

    def test_state_field_label(self):
        form = StateForm()
        self.assertEqual(form.fields['state'].label, None)

    def test_state_field_queryset(self):
        form = StateForm()
        self.assertEqual(form.fields['state'].queryset.count(), 2)
        self.assertIsInstance(form.fields['state'], ModelChoiceField)
        self.assertTrue(form.fields['state'].queryset.filter(name="California").exists())
        self.assertTrue(form.fields['state'].queryset.filter(name="Texas").exists())

    def test_form_validity_with_valid_data(self):
        form = StateForm(data={'state': State.objects.get(name="California").id})
        self.assertTrue(form.is_valid())

    def test_form_validity_without_data(self):
        form = StateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('state', form.errors)

"""
INTEGREATION TESTS
Not a lot going on in this app so just testing our ID page seems fair
"""

#Testing basic user iteraction with the ID page
class UserInteractionTests(TestCase):
    def setUp(self):
        # Create test data for states and species
        self.state_ca = State.objects.create(name="California", abbreviation="CA")
        self.state_tx = State.objects.create(name="Texas", abbreviation="TX")
        self.snake_ca = SnakeSpecies.objects.create(
            common_name="California Kingsnake",
            scientific_name="Lampropeltis getula californiae",
            description="Commonly found in California.",
            venomous=False
        )
        self.snake_ca.states.add(self.state_ca)
        self.snake_tx = SnakeSpecies.objects.create(
            common_name="Texas Ratsnake",
            scientific_name="Pantherophis obsoletus",
            description="Commonly found in Texas.",
            venomous=False
        )
        self.snake_tx.states.add(self.state_tx)
        self.client = Client()

    def test_user_submits_form_without_selecting_state(self):
        # User submits the form without selecting a state
        response = self.client.get(reverse('id_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('the USA', response.content.decode())  # Default selection info
        # Check if all species are listed when no state is selected
        self.assertIn('California Kingsnake', response.content.decode())
        self.assertIn('Texas Ratsnake', response.content.decode())
