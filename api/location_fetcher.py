import requests

def get_location() -> tuple:
    response = requests.get('https://ipinfo.io')

    data = response.json()

    if 'loc' in data:
        lat, lon = data['loc'].split(',')
        print(f"Latitude: {lat}, Longitude: {lon}")
        return lat, lon
    else:
        print("Could not retrieve location data.")
        return '', ''