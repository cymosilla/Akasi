import streamlit as st
import pandas as pd
import numpy as np

from ui.cgmacros import (
    render_time_series_section,
    render_feature_summary_section,
    render_correlations_section
)
'''
    This is for the Streamlit visual app for users to be able to interact with the data. 
    List of variables:
        Bone Density
        Orientation
        Radiation

'''

st.set_page_config(page_title="Akasi Dashboard", layout="wide")
st.title("CGMacros: Time Series + Metabolic Associations")

render_time_series_section()
st.divider()
render_feature_summary_section()
st.divider()
render_correlations_section()