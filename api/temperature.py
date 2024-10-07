import requests
import streamlit as st

def fetch_windchill(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P5D:PT1H/windchill:C,t_2m:C/{lat},{lon}/html?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"

def fetch_windchill_csv(date: str, lat: float, lon: float, token: str):
    api_url = f'https://api.meteomatics.com/{date}P5D:PT1H/windchill:C,t_2m:C/{lat},{lon}/csv?access_token={token}'
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        return response.content.decode("utf-8")
    except requests.RequestException as e:
        return f"API request failed: {e}"


