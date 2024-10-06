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

def get_location_by_ip() -> tuple:
    response = requests.get('https://ipinfo.io')

    data = response.json()

    if 'city' in data:
        city = data['city']
        region = data['region']
        country = data['country']
        return city, region, country
    else:
        print("Could not retrieve location data.")
        return '', '', ''
