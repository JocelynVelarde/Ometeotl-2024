import requests
import api.token_fetcher as fetch_token
import api.location_fetcher as get_latlon
import streamlit as st

token = fetch_token.fetch_token()
lat, lon = get_latlon.get_latlon()

def fetch_convective_categories(date: str):
    api_url = f'https://api.meteomatics.com/{date}/convective_categories_1h:idx/60,-12_35,30:0.05,0.05/png?access_token={token}'
    try:
        response = requests.get(api_url)
        st.image(response.content)
        response.raise_for_status() 
        return st.success("Convective categories image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_thunderstorm_probabilities(date: str):
    
    api_url = f'https://api.meteomatics.com/{date}/prob_tstorm_1h:p/70,-15_35,30:0.1,0.1/png?access_token={token}'
    try:
        response = requests.get(api_url)
        st.image(response.content)
        response.raise_for_status() 
        return st.success("Convective categories image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_rime_probability(date: str):  
    api_url = f'https://api.meteomatics.com/{date}/prob_rime:p/53.5,7.5_51,11.5:0.01,0.01/png?access_token={token}'
    try:
        response = requests.get(api_url)
        st.image(response.content)
        response.raise_for_status() 
        return st.success("Rime probability image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    
def fetch_snow_drift(date: str):  
    api_url = f'https://api.meteomatics.com/{date}/snow_drift:idx/54,8.5_51,14.9:0.025,0.025/png?access_token={token}'
    try:
        response = requests.get(api_url)
        st.image(response.content)
        response.raise_for_status() 
        return st.success("Snow drift image displayed.")
    except requests.RequestException as e:
        return f"API request failed: {e}"
    


