from pathlib import Path
import pandas as pd
import plotly.express as px # New interactive chart, see how it goes
# import plotly.graph_objects as go # No go
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.analysis.cgmacros_scatter_plot import get_bio_data
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

ANALYZED_PATH = (
    PROJECT_ROOT
    / "data"
    / "analyzed"
)

CGMACROS_ROOT = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
    / "CGMacros_dateshifted365"
    / "CGMacros"
)

ARES_ACTIGRAPHY_ROOT = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "BRSMACT_Campaign_1_Actigraphy"
    / "BRSMACT_Campaign_1_Actigraphy"
)

# Takes cgmacros-time-series-res.csv
def cgmacros_summary_plot():
    df = pd.read_csv(ANALYZED_PATH / "cgmacros-time-series-res.csv")
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
        bio[col] = pd.to_numeric(bio[col], errors="coerce")

    marker = st.selectbox("Select Biomarker", biomarkers)

    bio = bio.dropna(subset=[marker])

    st.markdown(f"### {marker} by Subject")

    fig = px.scatter(
        bio,
        x="subject",
        y=marker,
        hover_data=bio.columns,
        title=f"{marker} by Subject"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Biomarker Relationships")

    x_var = st.selectbox(
        "Compare Against",
        [
            "Age",
            "BMI",
            "HDL",
            "Cholesterol",
            "Triglycerides",
            "Insulin"
        ],
        index=0
    )
    # Implementing px properly over matplotlib
    rel_df = bio.dropna(subset=[x_var, marker])

    fig2 = px.scatter(rel_df,x=x_var,y=marker, hover_data=["subject"], trendline="ols",title=f"{x_var} vs {marker}")
    st.plotly_chart(fig2,use_container_width=True)
    st.markdown(f"### Distribution of {marker}")

    fig3 = px.histogram(bio,x=marker,nbins=20,title=f"{marker} Distribution")
    st.plotly_chart(fig3,use_container_width=True)
    st.markdown("### Summary Statistics")
    st.dataframe(bio[[marker]].describe().T,use_container_width=True)

def ares_actigraphy_ME():
    st.header("ARES Bed Rest")
    # Dropdown time
    datasets = {"Actigraphy Mixed Effects" : "ares-actigraphy-mixedeffects.csv"}
    selected = st.selectbox("Select Model", list(datasets.keys()))
    df = pd.read_csv(ANALYZED_PATH / datasets[selected])
    st.subheader("Model COE")
    st.dataframe(df, use_container_width=True) # Take up entire width of page
    # Attempt at Forest GGDM
    st.subheader("COE estimates")
    plot_df = df[~df["term"].str.contains("Group Var", na=False)]
    st.scatter_chart(data=plot_df, x="coefficient", y="term")
    # Sig Terms
    st.subheader("Sig Fx")
    sig = df[df["p_value"] < 0.05]
    st.dataframe(sig, use_container_width=True)
    #Interpret
    st.subheader("Interpretation")

cgmacros_summary_plot()
cgmacros_raw_bio()
ares_actigraphy_ME()