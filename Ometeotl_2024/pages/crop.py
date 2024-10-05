from ..templates import template
from ..components.upload import render as ImageUploadComponxent
import reflex as rx

@template(route="/crop", title="Crop")
def crop() -> rx.Component:
    """The crop page.

    Returns:
        The UI for the crop page.
    """
    return rx.vstack(
        rx.heading("Crop", size="5"),
        ImageUploadComponxent(),
        spacing="8",
        width="100%",
    )