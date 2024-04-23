import requests

def fetch_observations(taxon_id, latitude, longitude, radius):
    # API endpoint for observations
    url = "https://api.inaturalist.org/v1/observations"
    
    # Define the parameters for the API request
    params = {
        'taxon_id': taxon_id,
        'lat': latitude,
        'lng': longitude,
        'radius': radius,
        'geo': 'true'  # Ensure that only georeferenced observations are returned
    }
    
    # Send the request to the iNaturalist API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data: HTTP", response.status_code)
        return None

def extract_observation_data(observations):
    # Initialize a list to store observation data
    observation_data = []

    if observations and 'results' in observations:
        for observation in observations['results']:
            if 'geojson' in observation and 'taxon' in observation:
                # Extract desired data
                obs_data = {
                    'common_name': observation['taxon'].get('preferred_common_name', 'Unknown'),
                    'scientific_name': observation['taxon'].get('name', 'No scientific name'),
                    'coordinates': observation['geojson']['coordinates']
                }
                observation_data.append(obs_data)
    return observation_data

# Example usage
taxon_id = 85553  # ID for snakes
latitude = 27.3361  # Example latitude
longitude = -82.5307  # Example longitude
radius = 10  # Search within 10 kilometers

# Fetch observations
observations_data = fetch_observations(taxon_id, latitude, longitude, radius)

# Extract and print observation data
extracted_data = extract_observation_data(observations_data)
for data in extracted_data:
    print(f"Common Name: {data['common_name']}, Scientific Name: {data['scientific_name']}, Coordinates: {data['coordinates']}")
