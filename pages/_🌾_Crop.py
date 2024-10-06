import streamlit as st
from algorithms.crop_analyzer import CropAnalyzer
from algorithms.whatsapp import WhatsappSender
import cv2
import numpy as np
from PIL import Image
from datetime import datetime


if 'phone_number' not in st.session_state:
    with open("phone.txt", 'r') as file:
        text = file.read()
    st.session_state.phone_number = text


# Page configuration
st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.title('Crops analysis')
st.write("Analyze crops through an image and get detailed information.")

st.divider()


# File upload section
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Camera input
if 'camera_enabled' not in st.session_state:
    st.session_state.camera_enabled = False

if st.session_state.camera_enabled == False:
    if st.button("Enable Camera"):
        st.session_state.camera_enabled = True

if st.session_state.camera_enabled:
    picture = st.camera_input("Capture a picture")

    if picture is not None:
        st.image(picture, caption='Captured Image', use_column_width=True)

    if st.button("Cancel Camera"):
        st.session_state.camera_enabled = False

if not st.session_state.camera_enabled:
    st.write("Camera is not enabled.")

if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    image_pil = Image.open(uploaded_file)
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image, data = CropAnalyzer.analyze_image(image_cv, 1, 2)
    interpreted_info = CropAnalyzer.interpret_data(data)
    # WhatsappSender.send_message(st.session_state.phone_number, interpreted_info)
    
    st.success("Analysis complete")
    st.divider()
    st.header("Results")
    #Handle data - funcion Rossi
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption="Results", use_column_width=True)
    st.markdown(interpreted_info)
