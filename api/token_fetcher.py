import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_token() -> str:
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    # Create the basic authentication header
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Make the GET request
    try:
        response = requests.get('https://login.meteomatics.com/api/v1/token', headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        token = data['access_token']
        print('token', token)
        return token
    except requests.exceptions.RequestException as err:
        print('something went wrong', err)
        return ''