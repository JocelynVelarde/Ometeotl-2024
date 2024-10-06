"""The soil page."""

from ..templates import template
from Ometeotl_2024.components.card import card
from Ometeotl_2024.components.funnel import funnel_simple

import reflex as rx


@template(route="/soil", title="Soil")
def soil() -> rx.Component:
    """The soil page.

    Returns:
        The UI for the soil page.
    """
    return rx.vstack(
        rx.heading("Soil information", size="5"),
        card(rx.hstack(
            rx.hstack(
                rx.icon("user-round-search", size=20),
                rx.text("Soil Analytics", size="4", weight="medium"),
                align="center",
                spacing="2",
            ),
            align="center",
            width="100%",
            justify="between",
        ),),
        card(rx.text("Soil Type: Loam", size="4"),),
        funnel_simple(),
        spacing="8",
        width="100%",

    )
