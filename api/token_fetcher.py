import requests
import base64
import streamlit as st

def fetch_token() -> str:
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
        print(token)
        return token
    except requests.exceptions.RequestException as err:
        return err