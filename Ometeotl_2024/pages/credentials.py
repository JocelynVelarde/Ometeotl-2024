
from ..templates import template

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
        
        async with self:
            self.lat = lat
            self.lon = lon

    def toggle_fetching(self):
        self.running = not self.running
        if self.running:
            return CredentialsState.fetch_credentials

    def clear_credentials(self):
        self.lat = ""
        self.lon = ""
def lot_button() -> rx.Component:
    return rx.button("Lot", style="primary", size="lg")

@template(route="/credentials", title="Credentials")
def credentials() -> rx.Component:
    return rx.vstack(
        rx.button(
            rx.cond(~CredentialsState.running, "Fetch Credentials", "Loading..."),
            on_click=CredentialsState.toggle_fetching,
        ),
        rx.cond(
            CredentialsState.lat != "",
            rx.hstack(
                rx.text(f"Latitude: {CredentialsState.lat}"),
                rx.text(" "),
                rx.text(f"Longitude: {CredentialsState.lon}"),
            ),
        ),
        rx.button(
            "Clear Credentials",
            on_click=CredentialsState.clear_credentials,
        ),
        spacing="8",
        width="100%",
    )