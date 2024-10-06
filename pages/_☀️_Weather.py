import streamlit as st
import matplotlib.pyplot as plt
from api.day_counts import *
from streamlit.components.v1 import html
from api.atmospheric import fetch_convective_categories, fetch_thunderstorm_probabilities, fetch_rime_probability
from api.temperature import fetch_windchill
from api.weather_params import *
from api.health import *
from streamlit_calendar import calendar
from algorithms.gpt_analysis import get_gpt_prompt_response

import api.location_fetcher as get_location
import pandas as pd

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

lat, lon = get_location.get_latlon()
city, region, country = get_location.get_location_by_ip()

st.title(f'Weather for {city}, {region}, {country}')

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
        if st.button("Generate brief analysis", key='vegetation_days_button'):
            res = fetch_vegetation_days_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='heating_days'):
        st.subheader('☀️ Heating days')
        st.write('This parameter returns the number of heating days (days for which the 24h-mean is less than 15°C, or the number of days buildings need to be heated) since the 1st of January.')
        data = fetch_heating_days(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='heating_days_button'):
            res = fetch_heating_days_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='extremely_hot_days'):
        st.subheader('🔥 Extremely hot days')
        st.write('This parameter returns the number of extremely hot days (days on which the maximum temperature at 2m exceeds 35°C) since the 1st of January.')
        data = fetch_extremely_hot_days(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='extremely_hot_days_button'):
            res = fetch_extremely_hot_days_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='rime_probability'):
        st.subheader('🌨️ Rime probability')
        st.write('This parameter describes the probability of rime occurrence. It is given in a range from 0 to 100% and is based on surface temperature (0m), dew point temperature, wind speed and global radiation.')
        fetch_rime_probability(date=selected_date)

    with st.container(border=True, key='tropical_nights'):
        st.subheader('🌴 Tropical nights')
        st.write('This parameter returns the number of tropical nights (days for which the 24-hour minimum temperature was greater than 20°C) since the 1st of January.')
        data = fetch_tropical_nights(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='tropical_nights_button'):
            res = fetch_tropical_nights_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='windchill'):
        st.subheader('🌬️ Windchill')
        st.write('Show the windchill and the temperature at a height of 2 meters for the next five days.')
        data = fetch_windchill(date=selected_date)
        html(data, width=500, height=400)

    with st.container(border=True, key='frost_days'):
        st.subheader('❄️ Frost days')
        st.write('This parameter indicates the count of frost days, which are days when the temperature fell below 0 degrees Celsius, since the 1st of January. The count of frost days corresponds to the count of freezing days in the United States.')
        data = fetch_frost_days(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='frost_days_button'):
            res = fetch_frost_days_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='rain_days'):
        st.subheader('🌧️ Rain days')
        st.write('This parameter returns the number of rain days (days on which at least 0.1 mm of rain fell) since 1st of January.')
        data = fetch_rain_days(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='rain_days_button'):
            res = fetch_rain_days_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='thunderstorm_probabilities'):
        st.subheader('⚡️ Thunderstorm probabilities')
        st.write('Gives the probability of a thunderstorm to occur.')
        fetch_thunderstorm_probabilities(date=selected_date)

    with st.container(border=True, key='weather_description'):
        st.subheader('🌦️ Weather description')
        st.write('This parameter provides an automated text snipped describing the general weather state of the queried day. It is currently available in English, German, French and Italian.')
        data = fetch_weather_description(date=selected_date)
        data = get_gpt_prompt_response(prompt=data, system_message="Format the following text into better sentences for the user.")
        st.write("#### Forecast")
        st.write(data)

    with st.container(border=True, key='fog'):
        st.subheader('🌫️ Fog')
        st.write('Show if there is any fog expected during the next six hours.')
        data = fetch_fog(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='fog_button'):
            res = fetch_fog_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='snow_cover'):
        st.subheader('⛄️ Snow cover')
        st.write('Gives the probability for a location/region being covered by snow. The probability is determined by combining information about temperatures at different altitudes and precipitation predictions.')
        data = fetch_snow_cover(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='snow_cover_button'):
            res = fetch_snow_cover_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)

    with st.container(border=True, key='Snow drift'):
        st.subheader('❄️ Snow drift')
        st.write('The snow drift parameter describes how strong snow is carried over the surface due to environmental factors such as wind speed. The index ranges from 0 to 6 with higher values indicating a higher amount of fresh snow being transported because of high wind speeds.')
        data = fetch_snow_cover(date=selected_date)

    with st.container(border=True, key='pollen_warning'):
        st.subheader('💐 Pollen warning')
        st.write('The pollen warning returns warning levels for different types of pollen loads. The warning levels are based on the pollen concentration in the air.')
        data = fetch_pollen_warning_image(date=selected_date)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='pollen_warning_button'):
            res = fetch_pollen_warning_csv(date=selected_date)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            st.write(get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph."),)
            
    with st.container(border=True, key='land_usage'):
        st.subheader('🏞️ Land usage')
        st.write('The return values are integer codes, examples above are 512 for inland water bodies and 112 for discontinuous urban fabric.')
        st.write('Please consult https://www.eea.europa.eu/data-and-maps/data/clc-2006-raster-3/corine-land-cover-classes-and/clc_legend.csv for a table of the codes.')
        fetch_land_usage(date=selected_date)
  
    with st.container(border=True, key='Open water body'):
        st.subheader('🌊 Open water body')
        st.write('This index tells you if a coordinate is located within a water body or on land. The index is either 1 for water bodies or 0 for land.')
        fetch_open_water_body(date=selected_date)

    with st.container(border=True, key='convective categories'):
        st.subheader('⛈️ Convective categories')
        st.write('Convective categories denote the convective potential of clouds. A high category (category 3 and above) indicates the potential for strong convection and the development of thunderstorm clouds.')
        fetch_convective_categories(date=selected_date)

st.button('Refresh')