import reflex as rx
from Ometeotl_2024 import styles


def card(*children, **props) -> rx.Component:
    return rx.card(
        *children,
        box_shadow=styles.box_shadow_style,
        size="3",
        width="100%",
        **props,
    )
