import requests
import api.token_fetcher as fetch_token
import api.location_fetcher as get_latlon
import streamlit as st

token = fetch_token.fetch_token()
lat, lon = get_latlon.get_latlon()

def fetch_windchill(date: str):
    api_url = f'https://api.meteomatics.com/{date}P5D:PT1H/windchill:C,t_2m:C/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"


