import streamlit as st
import matplotlib.pyplot as plt
from algorithms.digitalTwinEx import *

st.set_page_config(
    page_title="Crop Connect",
    page_icon="🪴",
)


st.image('assets/farm.jpg', use_column_width=True)

st.title('🏡 Farm overview')

st.write('This page allows you to view the different coordinates and location on your farm and see individual details of each plot.')

st.divider()

#dimension = st.number_input('Select the dimension of your farm (m)', min_value=1, max_value= 5, step=1) - 1

e = Example(30, 10)
e.time_analysis()

st.write("(1) Ripeness, (2) Weed number, (3) Healthy plant number, (4) Water level, (5) Leaf type count")
dimension = st.slider('Select the dimension of your farm. ', min_value=1, max_value=5, step=1) - 1


matrix = e.farm.get_dimension(dimension=dimension).tolist()


for i in range(10):
    cols = st.columns(20)
    for col_index, col in enumerate(cols):
        with col:
            if dimension == 0:
                    
                if matrix[i][col_index] <= 0:
                    st.write("🔵")
                elif matrix[i][col_index] > 0 and matrix[i][col_index] <= 1.5:
                    st.write("🟢")
                elif matrix[i][col_index] > 1.5:
                    st.write("🔴")

            elif dimension == 1 or dimension == 2 or dimension == 4:
                st.write(int(matrix[i][col_index]))
            elif dimension == 3:
                if matrix[i][col_index] <= 0:
                    st.write("🔵")
                elif matrix[i][col_index] > 0 and matrix[i][col_index] <= 1.5:
                    st.write("🟢")
                elif matrix[i][col_index] > 1.5:
                    st.write("🔴")

    st.divider()

if dimension == 0:
    st.write('🔵 - Healthy plants'
        '\n🟢 - Healthy plants'
        '\n🔴 - Weed')
elif dimension == 3:
    st.write('🔵 - Dry'
    '\n🟢 - Healthy plants'
    '\n🔴 - Overwatered')
