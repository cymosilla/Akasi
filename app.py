from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# from ui.cgmacros import (
#     render_time_series_section,
#     render_feature_summary_section,
#     render_correlations_section
# )
'''
    This is for the Streamlit visual app for users to be able to interact with the data. 
    List of variables:
        Bone Density
        Orientation
        Radiation

'''

st.set_page_config(page_title="Akasi Dashboard", layout="wide")
st.title("CGMacros: Time Series + Metabolic Associations")

PROJECT_ROOT = Path(__file__).resolve().parent

CGMACROS_ROOT = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)

CGMACROS_DATA_PATH = (
    Path(__file__).parent
    / "data"
    / "preprocessed"
    / "cgmacros-time-series-res.csv"
)

# Takes cgmacros-time-series-res.csv
def cgmacros_preprocessed():
    df = pd.read_csv(CGMACROS_DATA_PATH)
    st.title("CGM Physiological Analysis")
    fig, ax = plt.subplots()

    ax.hist(df["Libre_mean"].dropna(), bins=15)

    ax.set_xlabel("Mean Glucose")
    ax.set_ylabel("Subjects")

    st.pyplot(fig)
    st.write(df.head())

# Takes bio.csv
def cgmacros_raw_bio():
    ts = pd.read_csv(CGMACROS_ROOT/"bio.csv")

    ts["Time (t)"] = pd.to_datetime(ts["Time (t)"])

    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(
        ts["Time (t)"],
        ts["LDL"],
        ts["Insulin"],
        ts["Triglycerides"],
    )

    ax.set_ylabel("Glucose")
    st.pyplot(fig)  

cgmacros_preprocessed()
cgmacros_raw_bio()