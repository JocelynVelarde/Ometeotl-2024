# This parameter returns the number of vegetation days (days on which the mean temperature was above 5°C) since the 1st of January.

import reflex as rx
from flask import Flask, render_template_string
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import json
import io
from ..templates import template
from ..backend.api import make_api_request


class VegetationState(rx.State):
    vegetation_days_data: str = ""
    loading: bool = False
    running: bool = False
    _n_tasks: int = 0

    @rx.background
    async def fetch_vegetation_days_data(self):
        async with self:
            if self._n_tasks > 0:
                return

            self._n_tasks += 1
            self.loading = True

        response = make_api_request('GET', 'https://api.meteomatics.com/2024-10-06T00:00:00ZP35D:P1D/vegetation_days:d/47.412164,9.340652/html?access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2IjoxLCJ1c2VyIjoidmVsYXJkZV9qb2NlbHluIiwiaXNzIjoibG9naW4ubWV0ZW9tYXRpY3MuY29tIiwiZXhwIjoxNzI4MTgzMjM3LCJzdWIiOiJhY2Nlc3MifQ.RATZwXDjd3VIgSITT9e4jmrz3IGYW9njTAk-sChsdNtatLR9QQKH7r6_dQjVOd0M_l__qhDEJhmufaasFOD9ng')
        print(response.content)
        
        
        #image = Image.open(io.BytesIO(response.content))
        #image.save('output.png')
        async with self:
            self.vegetation_days_data = response.content.decode("utf-8")
            self.loading = False
            self._n_tasks -= 1

    def toggle_fetching(self):
        self.running = not self.running
        if self.running:
            return VegetationState.fetch_vegetation_days_data

    def clear_vegetation_days_data(self):
        self.vegetation_days_data = ""

def vegation_days() -> rx.Component:
    """The vegetation days component.

    Returns:
        The UI for the vegetation days component.
    """
    return rx.card(
        rx.vstack(
            rx.button(
                rx.cond(~VegetationState.loading, "Fetch Vegetation Days Data", "Loading..."),
                on_click=VegetationState.toggle_fetching,
            ),
            rx.button(
                "Clear Data",
                on_click=VegetationState.clear_vegetation_days_data,
            ),
            rx.cond(
                VegetationState.vegetation_days_data != [],
                rx.html(VegetationState.vegetation_days_data),
            ),
            #rx.image(src="/output.png", width="100px", height="auto"),
            rx.text("The number of vegetation days (days on which the mean temperature was above 5°C) since the 1st of January."),
            spacing="8",
            width="100%",
        ),
        padding="16px",
        shadow="md",
        border_radius="8px",
    )


