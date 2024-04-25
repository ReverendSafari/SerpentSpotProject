from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json
from . import views

"""
UNIT TESTS 
Not a very backend heavy app, we are mainly concerned with testing our API call and our JSON response in the map view
"""


class MapViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('map_view')

    @patch('requests.get')
    def test_fetch_observations_successful(self, mock_get):
        # Setup mock
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{'taxon': {'preferred_common_name': 'Garter Snake', 'name': 'Thamnophis sirtalis'}, 'geojson': {'coordinates': [10, 10]}}]
        }
        
        # Call function
        response = views.fetch_observations(85553, '10', '10', '10', '6m')
        self.assertIsNotNone(response)
        self.assertEqual(len(response['results']), 1)
        self.assertEqual(response['results'][0]['taxon']['preferred_common_name'], 'Garter Snake')

    @patch('requests.get')
    def test_fetch_observations_api_failure(self, mock_get):
        # Setup mock
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        
        # Call function
        response = views.fetch_observations(85553, '10', '10', '10', '6m')
        self.assertIsNone(response)

    def test_map_view_get_with_params(self):
        with patch('requests.get') as mock_get:
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'results': [{'taxon': {'preferred_common_name': 'Garter Snake', 'name': 'Thamnophis sirtalis'}, 'geojson': {'coordinates': [10, 10]}}]
            }
            response = self.client.get(self.url, {'latitude': '10', 'longitude': '10', 'radius': '10', 'date_range': '6m'})
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertIn('observations', data)
            self.assertEqual(len(data['observations']), 1)
            self.assertEqual(data['observations'][0]['common_name'], 'Garter Snake')

    def test_map_view_get_without_params(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map.html')

