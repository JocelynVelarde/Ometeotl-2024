
from ..backend.token_fetcher import fetch_token
import reflex as rx
import requests

class CredentialsState(rx.State):
    lat: str = ""
    lon: str = ""
    running: bool = False
    access_token: str = ""

    @rx.background
    async def fetch_credentials(self):
        response = requests.get('https://ipinfo.io')

        data = response.json()

        if 'loc' in data:
            lat, lon = data['loc'].split(',')
            print(f"Latitude: {lat}, Longitude: {lon}")
        else:
            print("Could not retrieve location data.")
        
        token = fetch_token()

        async with self:
            self.lat = lat
            self.lon = lon
            self.access_token = token

    def toggle_fetching(self):
        self.running = not self.running
        if self.running:
            return CredentialsState.fetch_credentials

    def clear_credentials(self):
        self.lat = ""
        self.lon = ""