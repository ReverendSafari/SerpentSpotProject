from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.utils import timezone
from datetime import timedelta

# @ Safari
# Resources used:
# https://developers.google.com/maps/documentation/javascript/overview
# https://www.inaturalist.org/pages/api+reference
# (I was going to link a GPT chat that helped me with both API's but I accidentally leaked my API key in the chat)


"""
Pulls observations from the iNaturalist API based on a taxon ID, latitude, longitude, radius, and date range.

Args:
    taxon_id: The taxon ID of the species to search for.
    latitude: The latitude of the location to search around.
    longitude: The longitude of the location to search around.
    radius: The radius around the location to search within.
    date_range: The range of dates to search within (e.g., '6m' for 6 months).
    page: The page of results to fetch (default is 1).

Returns:
    dict: The JSON response from the API.
"""
def fetch_observations(taxon_id, latitude, longitude, radius, date_range, page=1):
    url = "https://api.inaturalist.org/v1/observations"
    today = timezone.now().date()
    start_date = None
    if date_range == "6m":
        start_date = today - timedelta(days=182)
    elif date_range == "1y":
        start_date = today - timedelta(days=365)
    elif date_range == "5y":
        start_date = today - timedelta(days=5*365)

    params = {
        'taxon_id': taxon_id,
        'lat': latitude,
        'lng': longitude,
        'radius': radius,
        'd1': start_date.isoformat() if start_date else None,
        'geo': 'true',
        'per_page': 200,  # Maximum typically allowed by APIs
        'page': page
    }
    print("Making API Call to:", url, "With parameters:", params)
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

"""
Unused function to handle pagination of API results.
"""
# def handle_pagination(taxon_id, latitude, longitude, radius, date_range):
#     page = 1
#     all_observations = []
#     while True:
#         data = fetch_observations(taxon_id, latitude, longitude, radius, date_range, page)
#         if data and data.get('results'):
#             all_observations.extend(data['results'])
#             page += 1
#             if len(data['results']) < 200:  # If fewer than 200 results, last page
#                 break
#         else:
#             break
#     return all_observations


"""
Renders the template, and fetches observations if the request is a GET with the required parameters.
(Also passed in our API key)

Args:
    request: The request object.

Returns:
    render object: The render object for the map html template, and a JSON response of observations if it is a get request
    
"""
def map_view(request):
    
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    }

    print("Request received:", request.GET)
    if request.method == 'GET' and 'latitude' in request.GET:
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        radius = request.GET.get('radius')
        date_range = request.GET.get('date_range', 'all')  # default to 'all'
        taxon_id = 85553  # Example taxon ID for snakes

        data = fetch_observations(taxon_id, latitude, longitude, radius, date_range)
        if data:
            observations = [{
                'common_name': obs['taxon'].get('preferred_common_name', 'Unknown'),
                'scientific_name': obs['taxon'].get('name', 'No scientific name'),
                'coordinates': obs['geojson']['coordinates']
            } for obs in data.get('results', []) if 'geojson' in obs and 'taxon' in obs]
            return JsonResponse({'observations': observations})
        else:
            return JsonResponse({'error': 'Failed to fetch data'}, status=500)
    else:
        return render(request, 'map.html', context)