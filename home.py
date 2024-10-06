import streamlit as st
import pandas as pd
import numpy as np

if 'phone_number' not in st.session_state:
    with open("phone.txt", 'r') as file:
        text = file.read()
    st.session_state.phone_number = text
    
st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.title(':rainbow[Welcome to Crop Connect 📒]')

