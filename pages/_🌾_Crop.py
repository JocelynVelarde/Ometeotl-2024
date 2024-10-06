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
st.write("Upload or take an image to analyze the crop and get detailed information. Some of the detected features include: crop type, health, plant illness, pests and more.")

st.divider()

st.subheader('Step 1: Set coordinates')
st.write("Set the coordinates of the area you want to analyze in the input fields.")
st.write("\n\n")

st.subheader('Step 2: Upload image')
st.markdown('Upload an image of the crop you want to analyze by clicking on _Browse files_ below. The image should be clear and focused on the crop.')
st.write("or")
st.markdown('Click on _Enable Camera_ button below and then click on _Take Photo_ to take a picture of the crop directly from your device.')
st.write("\n\n")

st.subheader('Step 3: Wait for results')
st.markdown('As soon as the image is uploaded, the analysis will start and take a few seconds to complete. Once the results are available, they will be displayed below.')

st.divider()

# Coordinates input
st.subheader('Coordinates')
col1, col2 = st.columns(2)
x1, y1 = 0, 0
with col1:
    x1 = st.number_input("X", value=0)
    y1 = st.number_input("Y", value=0)

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


if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    image_pil = Image.open(uploaded_file)
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image, data = CropAnalyzer.analyze_image(image_cv, x1, y1)
    interpreted_info = CropAnalyzer.interpret_data(data)
    # WhatsappSender.send_message(st.session_state.phone_number, interpreted_info)
    
    st.success("Analysis complete, scroll down below to see the results.")
    st.divider()
    st.header("Results")
    #Handle data - funcion Rossi
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption="Results", use_column_width=True)
    st.markdown(interpreted_info)
