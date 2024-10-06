import streamlit as st
import matplotlib.pyplot as plt
import api.location_fetcher as get_location
from api.day_counts import fetch_vegetation_days, fetch_heating_days, fetch_extremely_hot_days
from streamlit.components.v1 import html
import pandas as pd

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

lat, lon = get_location.get_location()



st.title('Weather for ' + str(lat) + ', ' + str(lon))
container = st.container(border=True)



container.subheader('📍 My location')
# Ensure latitude and longitude are floats
location_df = pd.DataFrame({
    'lat': [float(lat)],
    'lon': [float(lon)]
})

# Display the map with the point
container.map(location_df, zoom=15)


with st.container(border=True, key='vegetation_days'):
    st.subheader('🥬 Vegetation days')
    st.write('This parameter returns the number of vegetation days (days on which the mean temperature was above 5°C) since the 1st of January.')
    data = fetch_vegetation_days()
    html(data, width=500, height=400)

with st.container(border=True, key='heating_days'):
    st.subheader('☀️ Heating days')
    st.write('This parameter returns the number of heating days (days for which the 24h-mean is less than 15°C, or the number of days buildings need to be heated) since the 1st of January.')
    data = fetch_heating_days()
    html(data, width=500, height=400)

with st.container(border=True, key='extremely_hot_days'):
    st.subheader('🔥 Extremely hot days')
    st.write('This parameter returns the number of extremely hot days (days on which the maximum temperature at 2m exceeds 35°C) since the 1st of January.')
    data = fetch_extremely_hot_days()
    html(data, width=500, height=400)


st.button('Refresh')