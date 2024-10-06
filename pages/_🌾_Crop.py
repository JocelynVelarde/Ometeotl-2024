import streamlit as st
from algorithms.crop_analyzer import CropAnalyzer
from algorithms.whatsapp import WhatsappSender
import cv2
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.title('Crops analysis')
st.write("Analyze crops through an image")

st.divider()


# File upload section
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Camera input
# uploaded_file = st.camera_input("Capture a picture")

# Initialize session state for camera enabled
if 'camera_enabled' not in st.session_state:
    st.session_state.camera_enabled = False

# Button to enable camera
if st.session_state.camera_enabled == False:
    if st.button("Enable Camera"):
        st.session_state.camera_enabled = True

# Display camera input only if the camera is enabled
if st.session_state.camera_enabled:
    picture = st.camera_input("Capture a picture")


    # If a picture is taken, display it
    if picture is not None:
        st.image(picture, caption='Captured Image', use_column_width=True)

    # Button to cancel/disable camera input
    if st.button("Cancel Camera"):
        st.session_state.camera_enabled = False
# Inform the user if the camera is disabled
if not st.session_state.camera_enabled:
    st.write("Camera is not enabled.")

# # Display message if camera is disabled
# if not st.session_state.camera_enabled:
#     st.write("Camera is not enabled.")

# if picture is not None:
#     # To read file as bytes
#     st.image(picture, caption='Captured Image', use_column_width=True)
# st.write(st.session_state.phone_number)

# Display the file details after uploading
if uploaded_file is not None:
    st.write(f"Uploaded file: {uploaded_file.name}")

    image_pil = Image.open(uploaded_file)
    image_np = np.array(image_pil)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image, data = CropAnalyzer.analyze_image(image_cv, 1, 2)
    
    WhatsappSender.send_message(st.phone_number, data)
    
    #Handle data - funcion Rossi
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption="Results", use_column_width=True)
    st.success("Analysis complete")

# Display the image