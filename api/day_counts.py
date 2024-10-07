import requests

def fetch_vegetation_days(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/vegetation_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_vegetation_days_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/vegetation_days:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"


def fetch_heating_days(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/heating_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_heating_days_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/heating_days:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_extremely_hot_days(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/desert_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_extremely_hot_days_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/desert_days:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_tropical_nights(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/tropical_nights:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_tropical_nights_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/tropical_nights:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_frost_days(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/frost_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
       
def fetch_frost_days_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/frost_days:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_rain_days(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/rain_days:d/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_rain_days_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P35D:P1D/rain_days:d/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
