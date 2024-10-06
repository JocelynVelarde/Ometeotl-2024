import requests

def fetch_weather_description(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}/weather_text_en:str/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.text
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_fog(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}PT6H:PT1H/visibility:km,is_fog_1h:idx/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_fog_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}PT6H:PT1H/visibility:km,is_fog_1h:idx/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_snow_cover(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}/prob_snow_cover:p/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_snow_cover_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}/prob_snow_cover:p/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
