import requests
import api.token_fetcher as fetch_token
import api.location_fetcher as get_latlon
import streamlit as st

token = fetch_token.fetch_token()
lat, lon = get_latlon.get_latlon()

def fetch_pollen_warning(date: str):
    date = date[:-13] + '12Z'
    # https://api.meteomatics.com/2024-10-06T12ZP1D:PT1H/grass_pollen_warning:idx/51.23693,10.13906/html
    api_url = f'https://api.meteomatics.com/{date}P1D:PT1H/grass_pollen_warning:idx/51.23693,10.13906/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
    

def fetch_open_water_body(date: str):
    # https://api.meteomatics.com/2024-10-06T18:00:00Z/land_usage:idx/46,7.3_45.5,7.8:0.001,0.001/html 
    # # https://api.meteomatics.com/2024-10-06T18:00:00Z/is_in_shadow:idx/46,7.3_45.5,7.8:0.001,0.001/html   
    api_url = f'https://api.meteomatics.com/2024-10-06T00:00:00Z/is_open_water_body:idx/scandinavia:0.05,0.05/png?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        st.image(response.content)
        return st.success("Open water body image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_land_usage(date: str):
    # https://api.meteomatics.com/2024-10-06T18:00:00Z/land_usage:idx/46,7.3_45.5,7.8:0.001,0.001/html 
    # # https://api.meteomatics.com/2024-10-06T18:00:00Z/is_in_shadow:idx/46,7.3_45.5,7.8:0.001,0.001/html   
    api_url = f'https://api.meteomatics.com/{date}/land_usage:idx/46,7.3_45.5,7.8:0.001,0.001/png?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        st.image(response.content)
        return st.success("Land usage image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
