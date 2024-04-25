from django.test import TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        """
        Test the status code of the home view.

        This method sends a GET request to the 'home_view' URL and checks if the response
        status code is equal to 200 (HTTP OK). This ensures that the home view is accessible
        and returns a successful response.

        """
        response = self.client.get(reverse('home_view'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the home view uses the correct template.
        """
        response = self.client.get(reverse('home_view'))
        self.assertTemplateUsed(response, 'homepage.html')
