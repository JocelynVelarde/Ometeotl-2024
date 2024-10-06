import requests
import api.token_fetcher as fetch_token
import api.location_fetcher as get_location

token = fetch_token.fetch_token()
lat, lon = get_location.get_latlon()

def fetch_vegetation_days(date: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/vegetation_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_heating_days(date: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/heating_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_extremely_hot_days(date: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/desert_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_tropical_nights():
    api_url = "https://api.meteomatics.com/2024-10-06T00:00:00ZP35D:P1D/tropical_nights:d/" + lat + "," + lon + "/html?access_token=" + token
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
