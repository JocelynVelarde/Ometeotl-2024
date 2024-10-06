"""The weather page."""

import base64
from PIL import Image
import io
from ..templates import template
from ..backend.api import make_api_request

import reflex as rx


class WeatherState(rx.State):
    weather_data: str = ""
    loading: bool = False
    running: bool = False
    _n_tasks: int = 0

    @rx.background
    async def fetch_weather_data(self):
        async with self:
            if self._n_tasks > 0:
                return

            self._n_tasks += 1
            self.loading = True

        
        response = make_api_request('GET', 'https://api.meteomatics.com/2024-10-05T12:00:00Z/t_2m:C/90,-180_-90,180:600x400/png?access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2IjoxLCJ1c2VyIjoidmVsYXJkZV9qb2NlbHluIiwiaXNzIjoibG9naW4ubWV0ZW9tYXRpY3MuY29tIiwiZXhwIjoxNzI4MTc1OTI1LCJzdWIiOiJhY2Nlc3MifQ.hbHKbiq_RMYos3ZDO90n8vxQRcDb-Sxl2COYFTWIRBT2xNBMtN_c4bMngzu9yail-PUGcqY6b-xIY85NV1-ifg')
        image = Image.open(io.BytesIO(response.content))
        image.save('output.png')
        async with self:
            self.weather_data = response.content
            self.loading = False
            self._n_tasks -= 1

    def toggle_fetching(self):
        self.running = not self.running
        if self.running:
            return WeatherState.fetch_weather_data

    def clear_weather_data(self):
        self.weather_data = ""


@template(route="/weather", title="Weather")
def weather() -> rx.Component:
    """The weather page.

    Returns:
        The UI for the weather page.
    """
    return rx.vstack(
        rx.heading("Weather", size="5"),
        rx.button(
            rx.cond(~WeatherState.loading, "Fetch Weather Data", "Loading..."),
            on_click=WeatherState.toggle_fetching,
        ),
        rx.button(
            "Clear Data",
            on_click=WeatherState.clear_weather_data,
        ),
        rx.cond(
            WeatherState.weather_data != "",
            rx.text(WeatherState.weather_data),
            
        ),
        rx.image(src="/output.png", width="100px", height="auto"),
        spacing="8",
        width="100%",
    )