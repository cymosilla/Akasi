from pathlib import Path
import pandas as pd
import plotly.express as px # New interactive chart, see how it goes
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANALYZED_PATH = (
    PROJECT_ROOT
    / "data"
    / "analyzed"
)

ARES_ACTIGRAPHY_ROOT = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "UTM-1-3Campaign"
    / "BRSMACT_Campaign_1_Actigraphy"
    / "BRSMACT_Campaign_1_Actigraphy"
)

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

ares_actigraphy_ME()