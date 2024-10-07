import requests
import base64
import streamlit as st
import ipinfo

class Credentials:
    lat: str = None
    lon: str = None
    token: str = None

    def get_latlon() -> tuple:
        
        if Credentials.lat is not None and Credentials.lon is not None:
            return Credentials.lat, Credentials.lon
        
        handler = ipinfo.getHandler(access_token=st.secrets["Ipinfo"]["ACCESS_TOKEN"])

        data =  handler.getDetails().details

        if 'loc' in data:
            lat, lon = data.get('loc').split(',')
            print(f"Latitude: {lat}, Longitude: {lon}")

            Credentials.lat = lat
            Credentials.lon = lon
            return lat, lon
        else:
            print("Could not retrieve location data.")
            return '', ''

    def get_location_by_ip() -> tuple:
        handler = ipinfo.getHandler(access_token=st.secrets["Ipinfo"]["ACCESS_TOKEN"])
        data =  handler.getDetails().details

        if 'city' in data:
            city = data['city']
            region = data['region']
            country = data['country']
            return city, region, country
        else:
            print("Could not retrieve location data.")
            return '', '', ''

    def fetch_token() -> str:
        
        if Credentials.token is not None:
            return Credentials.token

        username = st.secrets["username"]
        password = st.secrets["password"]

        # Create the basic authentication header
        credentials = f"{username}:{password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }
        
        # Make the GET request
        try:
            response = requests.get('https://login.meteomatics.com/api/v1/token', headers=headers)
            response.raise_for_status()
            data = response.json()
            token = data['access_token']
            Credentials.token = token
            return token
        except requests.exceptions.RequestException as err:
            return err