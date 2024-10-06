from PIL import Image
from algorithms.gpt_analysis import get_image_analysis, get_gpt_prompt_response

import streamlit as st

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)

st.markdown('# :green[Farmer Assistant]')

st.write("Select a support method, and we'll gladly assist you!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.session_state["state"] = "chat"

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

uploaded_images = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, label_visibility="hidden")

if uploaded_images:
    # Convert single file to list for uniform processing
    if not isinstance(uploaded_images, list):
        uploaded_images = [uploaded_images]

    for image in uploaded_images:
        image_pil = Image.open(image)
        st.image(image_pil, caption="Uploaded Image", use_column_width=True)

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message(name="user").write(prompt)

    if uploaded_images:
        image_pil_list = [Image.open(img) for img in uploaded_images]  # Open all images
        analysis_result = get_image_analysis(image_pil_list, prompt)

        st.session_state.messages.append({"role": "assistant", "content": analysis_result})
        st.chat_message("assistant").write(analysis_result)
    else:
        gpt_response = get_gpt_prompt_response(prompt)

        st.session_state.messages.append({"role": "assistant", "content": gpt_response})
        st.chat_message("assistant").write(gpt_response)

if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]