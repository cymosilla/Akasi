import streamlit as st
import pandas as pd
import numpy as np

'''
    This is for the Streamlit visual app for users to be able to interact with the data. 
    List of variables:
        Bone Density
        Orientation
        Radiation
        
'''
st.title("Akasi Dashboard")
st.write("Adjust the sliders below to see how gravity affects biological systems.")


# Syntax: st.sidebar.slider("Label", min_value, max_value, default_value)
gravity_level = st.sidebar.slider("Bone Density over time", 0.0, 1.0, 0.1)
