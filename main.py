import streamlit as st
import pandas as pd
import numpy as np

st.title("Execute um aplicativo Streamlit no Google Colab Notebook")
st.subheader('By Gabrielle Desireé')

x= st.slider("X", 1,20, 1)
chart_data = pd.DataFrame(
    np.random.randn(x, 3),
    columns=['a', 'b', 'c'])

st.area_chart(chart_data)
