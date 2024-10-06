import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.image('assets/farmer.png')

st.title('🌦️ Welcome to Crop Connect!')

st.divider()

st.subheader("We are here to help you with your farming needs")
st.write("**Crop Connect** is a platform that provides you with the tools to help you manage your farm.")

st.write("Here are some of the features we offer:")
st.write("✨ Use of **computer vision** and **models** to analyze images of your crops")
st.write("✨ Weather **forecasting** for the next 35 days using real time data fetching")
st.write("✨ Soil and fire risk analysis using **machine learning** models and **satellite data**")
st.write("✨ **WhatsApp notifications** for weather alerts using authenticated **Twilio API**")
st.write("✨ Real time help with **LLM** for farming questions using images as **knowledge base**")

st.divider()
# Create a grid of 4 rows and 2 columns
rows = 4
columns = 2

for row in range(rows):
    cols = st.columns(columns)
    for col_index, col in enumerate(cols):
        with col:
            container = st.container(border=True)
            with container:
                if row == 0 and col_index == 0:
                    st.write("☀️ **Weather**")
                    st.write("1. Using your location provide a weather forecast for the next 35 days.")
                    st.write("2. Visualize historical weather data.")
                    st.write("3. Provide weather alerts trough WhatsApp.")
                    st.write("4. Generate individual data interpretation for easier approach.")
                    st.button("Go to: ☀️ Weather")
                elif row == 0 and col_index == 1:
                    st.write("🌾 **Crop**")
                    st.write("1. Add coordinates of farm positions with an image too.")
                    st.write("2. You can also upload image of crop, seed, fruit, vegetable to obtain state (healthy, ripe, mold...).")
                    st.write("3. Insights on crop health, plant illness, pests and more are generated.")
                    st.button("Go to: 🌾 Crop")
                elif row == 1 and col_index == 0:
                    st.write("🏡 **My Farm**")
                    st.write("1. In base of the coordinates and images uploaded, you can see the farm overview.")
                    st.write("2. Nice tile display in meters of your farm.")
                    st.write("3. See individual details of each plot such 🚜as ripeness, weeds, helthy plants, water...")
                    st.write("4. The grid will color itself like a heatmap to view overall farm performance for each variable.")
                    st.button("Go to: 🏡 My Farm")
                elif row == 1 and col_index == 1:
                    st.write("🌱 **Soil**")
                elif row == 2 and col_index == 0:
                    st.write("💬 **WhatsApp Notifications**")
                    st.write("1. Setup WhatsApp notifications for weather alerts.")
                    st.write("2. Add your number for updates.")
                    st.write("3. Initial setup to join the chat with Twilio setup.")
                    st.button("Go to: 💬 WhatsApp Notifications")
                elif row == 2 and col_index == 1:
                    st.write("📄 **Instructions**")
                elif row == 3 and col_index == 0:
                    st.write("🔥 **Fire**")
                elif row == 3 and col_index == 1:
                    st.write("🚜 **Farmer**")
                    st.write("1. Upload images of your crop, seed, fruit, vegetable to answer questions.")
                    st.write("2. Ask questions about farming and get answers.")
                    st.write("3. Real time help with AI chat")
                    st.write("2. Add your number for updates.")
                    st.button("Go to: 🚜 Farmer")
                   


