from ..templates import template
from ..backend.credentials_state import CredentialsState

import reflex as rx

@template(route="/credentials", title="Credentials")
def credentials() -> rx.Component:
    return rx.cond(
            CredentialsState.lat != "",
            rx.hstack(
                rx.text(f"Latitude: {CredentialsState.lat}"),
                rx.text(" "),
                rx.text(f"Longitude: {CredentialsState.lon}"),
                rx.text(" "),
                rx.text(f"Access Token: {CredentialsState.access_token}"),
            ),
        )