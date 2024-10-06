import streamlit as st

st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.markdown('# :green[Farmer Assistant]')

st.write("Select a support method, and we'll gladly assist you!")

col1, col2, col3 = st.columns(3)

st.divider()

r1, r2, r3 = False, False, False

with col1:
    r1 = st.button("Message AI for support")

with col2:
    r2 = st.button("Message agent for support")

with col3:
    r3 = st.button("Call agent for support")


with st.container():
    st.chat_input("Type your message here...")