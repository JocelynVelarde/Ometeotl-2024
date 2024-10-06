import streamlit as st
import matplotlib.pyplot as plt
import datetime
from api.vegetation_days import fetch_vegetation_days
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

st.title('Weather widgets depending on your location')
# Fetch data
st.divider()

st.subheader('Vegetation days')
data = fetch_vegetation_days()
html(data, width=500, height=400)

st.divider()