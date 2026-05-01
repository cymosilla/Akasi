from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.analysis.cgmacros_scatter_plot import get_bio_data

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
st.title("Akasi Dashboard")

PROJECT_ROOT = Path(__file__).resolve().parent

CGMACROS_ROOT = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)

CGMACROS_ANALYZED_PATH = (
    PROJECT_ROOT
    / "data"
    / "analyzed"
    / "cgmacros-time-series-res.csv"
)

# Takes cgmacros-time-series-res.csv
def cgmacros_timeseries_plot():
    df = pd.read_csv(CGMACROS_ANALYZED_PATH)
    st.title("CGM Physiological Analysis")
    fig, ax = plt.subplots()

    ax.hist(df["Libre_mean"].dropna(), bins=15)

    ax.set_xlabel("Mean Glucose")
    ax.set_ylabel("Subjects")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.pyplot(fig)
    st.write(df.head())

# Takes bio.csv, time series would not work here
def cgmacros_raw_bio():

    st.subheader("CGMacros Bio Data")
    # XXX: Remember to write desc here about why this is impt
    bio = get_bio_data()
    biomarkers = [
        "LDL (Cal)",
        "HDL",
        "Cholesterol",
        "Triglycerides",
        "Insulin"
    ]

    for col in biomarkers:
        bio[col] = pd.to_numeric(
            bio[col],
            errors="coerce"
        )

    marker = st.selectbox(
        "Select Biomarker",
        biomarkers
    )

    bio = bio.dropna(subset=[marker])

    # Huge plot (to prove a point)
    st.markdown(f"### {marker} by Subject")

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.scatter(
        bio["subject"],
        bio[marker]
    )

    ax.set_xlabel("Subject")
    ax.set_ylabel(marker)

    st.pyplot(fig)

    # Subplots
    st.markdown("### Biomarker Relationships")

    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        ax1.scatter(
            bio["Age"],
            bio[marker]
        )
        ax1.set_title(f"Age vs {marker}")
        ax1.set_xlabel("Age")
        ax1.set_ylabel(marker)
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        ax2.scatter(
            bio["BMI"],
            bio[marker]
        )
        ax2.set_title(f"BMI vs {marker}")
        ax2.set_xlabel("BMI")
        ax2.set_ylabel(marker)
    # Add HDL 

        st.pyplot(fig2)
cgmacros_timeseries_plot()
cgmacros_raw_bio()