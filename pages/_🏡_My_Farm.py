import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)


st.image('assets/farm.jpg', use_column_width=True)

st.title('🏡 Farm overview')

st.write('This page allows you to view the different coordinates and location on your farm and see individual details of each plot.')

st.divider()

rows = st.number_input('Select height of your farm (m)', min_value=1, step=1)
columns = st.number_input('Select width of your farm (m)', min_value=1, step=1)

if st.button('Generate farm'):
    st.success('Farm generated successfully!')

    # Generate the grid
    for row in range(int(rows)):
        cols = st.columns(int(columns))
        for col_index, col in enumerate(cols):
            with col:
                if st.button("🌾", key=f"{row}-{col_index}"):
                    st.write(f"Clicked on cell ({row+1}, {col_index+1})")