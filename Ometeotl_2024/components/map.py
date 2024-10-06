import reflex as rx

import plotly.graph_objects as go
import pandas as pd

# Read data from a csv
z_data = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv"
)

fig = go.Figure(data=[go.Surface(z=z_data.values)])
fig.update_traces(
    contours_z=dict(
        show=True,
        usecolormap=True,
        highlightcolor="limegreen",
        project_z=True,
    )
)
fig.update_layout(
    scene_camera_eye=dict(x=1.87, y=0.88, z=-0.64),
    margin=dict(l=65, r=50, b=65, t=90),
)

    

def fire_map() -> rx.Component:
    """The fire maps component.

    Returns:
        The UI for the fire maps component.
    """
    return rx.center(
        rx.plotly(data=fig),
    )



