import reflex as rx

def Buttons() -> rx.Component:
    """The buttons component.

    Returns:
        The UI for the buttons component.
    """
    return rx.grid(
        rx.button("Message support with agent", id="buttonAgent"),
        rx.button("Message support with AI", id="buttonAI"),
        rx.button("Call support with agent", id="buttonCall"),
    columns="3",
    spacing="4",
    width="100%",
)


