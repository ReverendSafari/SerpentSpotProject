from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.utils import timezone
from datetime import timedelta

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

def handle_pagination(taxon_id, latitude, longitude, radius, date_range):
    page = 1
    all_observations = []
    while True:
        data = fetch_observations(taxon_id, latitude, longitude, radius, date_range, page)
        if data and data.get('results'):
            all_observations.extend(data['results'])
            page += 1
            if len(data['results']) < 200:  # If fewer than 200 results, last page
                break
        else:
            break
    return all_observations

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