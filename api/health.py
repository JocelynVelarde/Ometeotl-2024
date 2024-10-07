import requests
import streamlit as st

def fetch_pollen_warning_image(date: str, lat: float, lon: float, token: str):
    date = date[:-13] + '12Z'
    api_url = f'https://api.meteomatics.com/{date}P1D:PT1H/grass_pollen_warning:idx/51.23693,10.13906/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_pollen_warning_csv(date: str, lat: float, lon: float, token: str):
    date = date[:-13] + '12Z'
    api_url = f'https://api.meteomatics.com/{date}P1D:PT1H/grass_pollen_warning:idx/51.23693,10.13906/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode('utf-8')
    except requests.RequestException as e:
        return f"API request failed: {e}"
    

def fetch_land_usage(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}/land_usage:idx/46,7.3_45.5,7.8:0.001,0.001/png?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        st.image(response.content)
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_open_water_body(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}/is_open_water_body:idx/scandinavia:0.05,0.05/png?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        st.image(response.content)
    except requests.RequestException as e:
        return f"API request failed: {e}"
