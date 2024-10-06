from geopy.geocoders import Photon

import requests

def get_latlon() -> tuple:
    response = requests.get('https://ipinfo.io')

    data = response.json()

    if 'loc' in data:
        lat, lon = data['loc'].split(',')
        return lat, lon
    else:
        print("Could not retrieve location data.")
        return '', ''

def get_location_by_ip():
    lat, lon = get_latlon()

    # Use Geopy to convert latitude and longitude to a human-readable address
    geolocator = Photon(user_agent="measurements")
    location = geolocator.reverse(f"{lat}, {lon}", language="en")

    return location.address
