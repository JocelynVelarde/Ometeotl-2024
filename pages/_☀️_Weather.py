from api.day_counts import *
from streamlit.components.v1 import html
from api.atmospheric import *
from api.temperature import *
from api.weather_params import *
from api.health import *
from streamlit_calendar import calendar
from algorithms.gpt_analysis import get_gpt_prompt_response
from algorithms.whatsapp import WhatsappSender
from api.credentials_fetcher import Credentials
from api.mongo_connection import *
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

lat, lon = Credentials.get_latlon()
city, region, country = Credentials.get_location_by_ip()
token = Credentials.fetch_token()

st.image('assets/weather.jpg', use_column_width=True)

st.title(f'☀️ Weather for {city}, {region}, {country}')

st.write('This page allows you to view and explore the various weather parameters for your location.')
st.write('We are fully **compromised** on making your crops grow better and healthier knowing the weather conditions, analysis and interpretation.')

st.divider()

st.subheader('Step 1: Make sure to have your location activated')
st.write('This will allow us to provide you with the most accurate weather data for your location.')

st.subheader('Step 2: Select a prediction date from calendar')
st.write('Note that the forecast is available for the next 35 days. In case you selected a past date, then the actual data from those days will be shown.')

st.subheader('Step 3: Explore the weather parameters')
st.write('Once you have selected a date, you can explore the various weather parameters available for that date being fetched in real time.')

st.subheader('Step 4: Generate a brief analysis')
st.write('The majority of weather widgets contain a button **Generate brief analysis**. This button will generate a brief analysis of the data fetched for that specific parameter.')
st.write('With this easy interpretation, you can understand the data better and make better decisions for your crops.')

st.subheader('Step 5: WhatsApp notifications')
st.write('Make sure to have your phone added on our notification system to receive the latest weather updates and alerts for your location.')
st.write('You can add your number on the following page: 💬[WhatsApp Notifications](https://crop-connector.streamlit.app/Whatsapp_Notifications)')

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
        data = fetch_vegetation_days(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='vegetation_days_button'):
            res = fetch_vegetation_days_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")
            
            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)
                
                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='heating_days'):
        st.subheader('☀️ Heating days')
        st.write('This parameter returns the number of heating days (days for which the 24h-mean is less than 15°C, or the number of days buildings need to be heated) since the 1st of January.')
        data = fetch_heating_days(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='heating_days_button'):
            res = fetch_heating_days_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='extremely_hot_days'):
        st.subheader('🔥 Extremely hot days')
        st.write('This parameter returns the number of extremely hot days (days on which the maximum temperature at 2m exceeds 35°C) since the 1st of January.')
        data = fetch_extremely_hot_days(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='extremely_hot_days_button'):
            res = fetch_extremely_hot_days_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='rime_probability'):
        st.subheader('🌨️ Rime probability')
        st.write('This parameter describes the probability of rime occurrence. It is given in a range from 0 to 100% and is based on surface temperature (0m), dew point temperature, wind speed and global radiation.')
        fetch_rime_probability(date=selected_date, lat=lat, lon=lon, token=token)

    with st.container(border=True, key='tropical_nights'):
        st.subheader('🌴 Tropical nights')
        st.write('This parameter returns the number of tropical nights (days for which the 24-hour minimum temperature was greater than 20°C) since the 1st of January.')
        data = fetch_tropical_nights(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='tropical_nights_button'):
            res = fetch_tropical_nights_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='windchill'):
        st.subheader('🌬️ Windchill')
        st.write('Show the windchill and the temperature at a height of 2 meters for the next five days.')
        data = fetch_windchill(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='windchill_button'):
            res = fetch_windchill_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='frost_days'):
        st.subheader('❄️ Frost days')
        st.write('This parameter indicates the count of frost days, which are days when the temperature fell below 0 degrees Celsius, since the 1st of January. The count of frost days corresponds to the count of freezing days in the United States.')
        data = fetch_frost_days(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='frost_days_button'):
            res = fetch_frost_days_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='rain_days'):
        st.subheader('🌧️ Rain days')
        st.write('This parameter returns the number of rain days (days on which at least 0.1 mm of rain fell) since 1st of January.')
        data = fetch_rain_days(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='rain_days_button'):
            res = fetch_rain_days_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='thunderstorm_probabilities'):
        st.subheader('⚡️ Thunderstorm probabilities')
        st.write('Gives the probability of a thunderstorm to occur.')
        fetch_thunderstorm_probabilities(date=selected_date, lat=lat, lon=lon, token=token)

    with st.container(border=True, key='weather_description'):
        st.subheader('🌦️ Weather description')
        st.write('This parameter provides an automated text snipped describing the general weather state of the queried day. It is currently available in English, German, French and Italian.')
        data = fetch_weather_description(date=selected_date, lat=lat, lon=lon, token=token)
        data = get_gpt_prompt_response(prompt=data, system_message="Format the following text into better sentences for the user.")
        st.write("#### Forecast")
        st.write(data)

    with st.container(border=True, key='fog'):
        st.subheader('🌫️ Fog')
        st.write('Show if there is any fog expected during the next six hours.')
        data = fetch_fog(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='fog_button'):
            res = fetch_fog_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='snow_cover'):
        st.subheader('⛄️ Snow cover')
        st.write('Gives the probability for a location/region being covered by snow. The probability is determined by combining information about temperatures at different altitudes and precipitation predictions.')
        data = fetch_snow_cover(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='snow_cover_button'):
            res = fetch_snow_cover_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='Snow drift'):
        st.subheader('❄️ Snow drift')
        st.write('The snow drift parameter describes how strong snow is carried over the surface due to environmental factors such as wind speed. The index ranges from 0 to 6 with higher values indicating a higher amount of fresh snow being transported because of high wind speeds.')
        fetch_snow_drift(date=selected_date, lat=lat, lon=lon, token=token)
        if st.button("Generate brief analysis", key='snow_drift_button'):
            res = fetch_snow_drift_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='pollen_warning'):
        st.subheader('💐 Pollen warning')
        st.write('The pollen warning returns warning levels for different types of pollen loads. The warning levels are based on the pollen concentration in the air.')
        data = fetch_pollen_warning_image(date=selected_date, lat=lat, lon=lon, token=token)
        html(data, width=500, height=400)
        if st.button("Generate brief analysis", key='pollen_warning_button'):
            res = fetch_pollen_warning_csv(date=selected_date, lat=lat, lon=lon, token=token)
            s = "Analyze the following csv data and provide a detailed analysis."
            st.write("#### Analysis")
            response = get_gpt_prompt_response(prompt=s + res, system_message="Analyze the following csv data and provide a brief analysis in a single paragraph. At the end write out an alert message for the most important thing analyzed. Write this alert message and start it with the word ‘ALERT’")

            if "ALERT:" in response:
                pre_alert_text = response.split("ALERT:", 1)[0].strip()
                alert_text = response.split("ALERT:", 1)[1].strip()
                
                st.write(pre_alert_text)

                decoded_data = json.loads(get_all_data('numberData', 'number'))

                for entry in decoded_data:
                    phone_number = entry.get("phone_number")
                    WhatsappSender.send_message(phone_number, alert_text)

    with st.container(border=True, key='land_usage'):
        st.subheader('🏞️ Land usage')
        st.write('The return values are integer codes, examples above are 512 for inland water bodies and 112 for discontinuous urban fabric.')
        st.write('Please consult https://www.eea.europa.eu/data-and-maps/data/clc-2006-raster-3/corine-land-cover-classes-and/clc_legend.csv for a table of the codes.')
        fetch_land_usage(date=selected_date, lat=lat, lon=lon, token=token)
  
    with st.container(border=True, key='Open water body'):
        st.subheader('🌊 Open water body')
        st.write('This index tells you if a coordinate is located within a water body or on land. The index is either 1 for water bodies or 0 for land.')
        fetch_open_water_body(date=selected_date, lat=lat, lon=lon, token=token)

    with st.container(border=True, key='convective categories'):
        st.subheader('⛈️ Convective categories')
        st.write('Convective categories denote the convective potential of clouds. A high category (category 3 and above) indicates the potential for strong convection and the development of thunderstorm clouds.')
        fetch_convective_categories(date=selected_date, lat=lat, lon=lon, token=token)

st.button('Refresh')