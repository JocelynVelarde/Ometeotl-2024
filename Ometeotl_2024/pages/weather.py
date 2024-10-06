"""The weather page."""

from ..templates import template
from Ometeotl_2024.components.vegetation_days import vegation_days


import reflex as rx

@template(route="/weather", title="Weather")
def weather() -> rx.Component:
    """The weather page.

    Returns:
        The UI for the weather page.
    """
    return rx.vstack(
        rx.heading("Weather", size="5"),
        vegation_days(),
        spacing="8",
        width="100%",
    )