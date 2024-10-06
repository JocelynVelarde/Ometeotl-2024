from ..templates import template
from Ometeotl_2024.components.button import Buttons

import reflex as rx

@template(route="/farmer", title="Farmer")
def farmer() -> rx.Component:
    """The farmer page.

    Returns:
        The UI for the farmer page.
    """
    return rx.vstack(
        rx.heading("Farmer Assistant", size="5"),
        Buttons(),
        spacing="8",
        width="100%",
    )