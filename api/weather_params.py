import requests
import api.token_fetcher as fetch_token
import api.location_fetcher as get_location

token = fetch_token.fetch_token()
lat, lon = get_location.get_location()

def fetch_weather_description(date: str):
    api_url = f'https://api.meteomatics.com/{date}/weather_text_en:str/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        return f"API request failed: {e}"