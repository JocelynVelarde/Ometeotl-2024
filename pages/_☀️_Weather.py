import streamlit as st
import matplotlib.pyplot as plt
from api.day_counts import fetch_vegetation_days, fetch_heating_days, fetch_extremely_hot_days, fetch_tropical_nights, fetch_frost_days, fetch_rain_days
from streamlit.components.v1 import html
from api.weather_params import fetch_weather_description, fetch_fog, fetch_snow_cover
from api.health import fetch_pollen_concentration, fetch_pollen_warning
from streamlit_calendar import calendar

import api.location_fetcher as get_location
import pandas as pd

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

lat, lon = get_location.get_latlon()
location = get_location.get_location_by_ip()

st.title('Weather for ' + location)

container = st.container(border=True)

calendar_options = {
    "editable": "true",
    "selectable": "true",
}

selected_date = ""

with st.container(border=True, key='calendar'):
    st.subheader('📅 Select a prediction date')
    calendar = calendar(options=calendar_options)

    if "dateClick" in calendar:
        selected_date = calendar["dateClick"]["date"]
        st.write(f'Selected date: {selected_date}')

container.subheader('📍 My location')
# Ensure latitude and longitude are floats
location_df = pd.DataFrame({
    'lat': [float(lat)],
    'lon': [float(lon)]
})

# Display the map with the point
container.map(location_df, zoom=15)

if selected_date:
    with st.container(border=True, key='vegetation_days'):
        st.subheader('🥬 Vegetation days')
        st.write('This parameter returns the number of vegetation days (days on which the mean temperature was above 5°C) since the 1st of January.')
        data = fetch_vegetation_days(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='heating_days'):
        st.subheader('☀️ Heating days')
        st.write('This parameter returns the number of heating days (days for which the 24h-mean is less than 15°C, or the number of days buildings need to be heated) since the 1st of January.')
        data = fetch_heating_days(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='extremely_hot_days'):
        st.subheader('🔥 Extremely hot days')
        st.write('This parameter returns the number of extremely hot days (days on which the maximum temperature at 2m exceeds 35°C) since the 1st of January.')
        data = fetch_extremely_hot_days(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='tropical_nights'):
        st.subheader('🌴 Tropical nights')
        st.write('This parameter returns the number of tropical nights (days for which the 24-hour minimum temperature was greater than 20°C) since the 1st of January.')
        data = fetch_tropical_nights(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='frost_days'):
        st.subheader('❄️ Frost days')
        st.write('This parameter indicates the count of frost days, which are days when the temperature fell below 0 degrees Celsius, since the 1st of January. The count of frost days corresponds to the count of freezing days in the United States.')
        data = fetch_frost_days(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='rain_days'):
        st.subheader('🌧️ Rain days')
        st.write('This parameter returns the number of rain days (days on which at least 0.1 mm of rain fell) since 1st of January.')
        data = fetch_rain_days(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='weather_description'):
        st.subheader('🌦️ Weather description')
        st.write('This parameter provides an automated text snipped describing the general weather state of the queried day. It is currently available in English, German, French and Italian.')
        data = fetch_weather_description(date=selected_date)
        html(data, width=500, height=200)

    with st.container(border=True, key='fog'):
        st.subheader('🌫️ Fog')
        st.write('Show if there is any fog expected during the next six hours.')
        data = fetch_fog(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='snow_cover'):
        st.subheader('⛄️ Snow cover')
        st.write('Gives the probability for a location/region being covered by snow. The probability is determined by combining information about temperatures at different altitudes and precipitation predictions.')
        data = fetch_snow_cover(date=selected_date)
        html(data, width=500, height=400)
    
    with st.container(border=True, key='pollen_concentration'):
        st.subheader('🌼 Pollen concentration')
        st.write('Gives the total pollen concentration in grains per cubic meter.')
        data = fetch_pollen_concentration(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='pollen_warning'):
        st.subheader('💐 Pollen warning')
        st.write('The pollen warning returns warning levels for different types of pollen loads. The warning levels are based on the pollen concentration in the air.')
        data = fetch_pollen_warning(date=selected_date)
        html(data, width=500, height=400)

st.button('Refresh')