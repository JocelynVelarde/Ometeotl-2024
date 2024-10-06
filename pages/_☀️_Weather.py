import streamlit as st
import matplotlib.pyplot as plt
from api.day_counts import fetch_vegetation_days, fetch_heating_days, fetch_extremely_hot_days
from streamlit.components.v1 import html
from streamlit_calendar import calendar

import api.location_fetcher as get_location
import pandas as pd

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

lat, lon = get_location.get_location()

st.date_input('Date Input', value=pd.to_datetime('2021-01-01'))

st.title('Weather for ' + str(lat) + ', ' + str(lon))
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


st.button('Refresh')