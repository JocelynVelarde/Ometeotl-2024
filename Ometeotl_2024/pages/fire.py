"""The fire map page."""

from ..templates import template
from Ometeotl_2024.components.map import fire_map

import reflex as rx


@template(route="/fire", title="Fire")
def fire() -> rx.Component:
    """The fire map page.

    Returns:
        The UI for the fire map page.
    """
    return rx.vstack(
        rx.heading("Fire map", size="5"),
        fire_map(),
        spacing="8",
        width="100%",
    )
