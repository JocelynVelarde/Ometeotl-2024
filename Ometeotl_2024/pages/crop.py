from ..templates import template
from Ometeotl_2024.components.upload import ImageUploadComponent
import reflex as rx

@template(route="/crop", title="Crop")
def crop() -> rx.Component:
    """The crop page.

    Returns:
        The UI for the crop page.
    """
    return rx.vstack(
        rx.heading("Crop", size="5"),
        ImageUploadComponent(),
        spacing="8",
        width="100%",
    )