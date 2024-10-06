import streamlit as st

st.set_page_config(
        page_title="Crop Connect",
        page_icon="🪴",
)

st.markdown('# :green[Farmer Assistant]')

st.write("Select a support method, and we'll gladly assist you!")

col1, col2, col3 = st.columns(3)

st.divider()

with col1:
    st.button("Message AI for support")

with col2:
    st.button("Message agent for support")

with col3:
    st.button("Call agent for support")

with st.container():
    st.write("Or, you can check out the weather widgets below!")