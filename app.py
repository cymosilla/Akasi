from pathlib import Path
import pandas as pd
import plotly.express as px # New interactive chart, see how it goes
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.analysis.cgmacros_scatter_plot import get_bio_data
from src.analysis.cgmacros_timeseries import get_subjects, prepare_timeseries_data

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
    / "raw"
    / "PhysioNet"
    / "cgmacros-scientific-dataset-nutrition-diet-monitoring-1.0.0"
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
    df = pd.read_csv(ANALYZED_PATH / "cgmacros-summary-res.csv")
    st.title("CGM Physiological Analysis")
    metric = st.selectbox(
        "Select Metric",
        [
            "Libre_mean",
            "Dexcom_mean",
        ]
    )
    df[metric] = pd.to_numeric(df[metric], errors="coerce")
    fig = px.histogram(df,x=metric, nbins=20, marginal="box",title=f"Distribution of {metric}")

    st.plotly_chart(fig,use_container_width=True)
    if "subject" in df.columns:
        fig2 = px.scatter(df,x="subject", y=metric,hover_data=df.columns,title=f"{metric} by Subject")
        st.plotly_chart(fig2,use_container_width=True)
    st.dataframe(df,use_container_width=True)

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
        title=f"{marker} by Subject",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    # col1, col2, col3 = st.columns([1, 2, 1])
    col1, col2 = st.columns(2)
    with col2:
        st.plotly_chart(fig, use_container_width=True)
    with col1:
        st.markdown("### Interpretation test")
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

# Spent like 30 minutes on PATH
def test():
    bio = pd.read_csv(CGMACROS_ROOT / "bio.csv")
    bio.columns = bio.columns.str.strip()
    print(bio.columns.tolist())
#     print("\n\n\n\n\nNEW")
#     print(CGMACROS_ROOT / "bio.csv")
#     p = CGMACROS_ROOT / "bio.csv"
#     print("bio csv path:", p)
#     print("exists:", p.exists())
#     print("is_file:", p.is_file())

def cgmacros_timeseries_per():
    bio = pd.read_csv(CGMACROS_ROOT / "bio.csv")
    st.sidebar.header("Filters")
    min_age = int(bio["Age"].min())
    max_age = int(bio["Age"].max())

    age_range = st.sidebar.slider(
        "Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age),
    )
    gender_options = sorted(bio["Gender"].dropna().unique())
    selected_genders = st.sidebar.multiselect("Gender",options=gender_options,default=gender_options)
    subjects = get_subjects(age_range=age_range, genders=selected_genders)
    # subject = st.selectbox("Subject",range(1, 50))
    subject = st.sidebar.selectbox("Subject", subjects)
    # Remove .astype if figured out
    subject_info = bio[bio["subject"].astype(str) == str(subject)].iloc[0]    
    st.subheader(f"Subject {subject:03d}")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Age",int(subject_info["Age"]))
    col2.metric("Gender",subject_info["Gender"],)
    col3.metric("BMI",round(subject_info["BMI"], 1))
    col4.metric("Weight",subject_info["Body weight"])
    col5.metric("Height",subject_info["Height"])

    full_data = prepare_timeseries_data(subject)
    timestamps = full_data["glucose"]["Timestamp"]
    min_date = timestamps.min().date()
    max_date = timestamps.max().date()
    st.subheader("Date Range")
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = min_date
        end_date = max_date

    data = prepare_timeseries_data(subject, start_date=start_date, end_date=end_date)

    # Meals
    meal_colors = {
        "Breakfast": "orange",
        "Lunch": "green",
        "Dinner": "blue",
        "Snacks": "white",
    }
    #glucose up next
    glucose_fig = go.Figure()
    # Libre
    glucose_fig.add_trace(
        go.Scatter(
            x=data["glucose"]["Timestamp"],
            y=data["glucose"]["Libre GL"],
            mode="lines",name="Libre GL"
        )
    )
    # Dexcom
    glucose_fig.add_trace(
        go.Scatter(x=data["glucose"]["Timestamp"],
                   y=data["glucose"]["Dexcom GL"],
                   mode="lines", name="Dexcom GL"
        )
    )

    for _, meal in data["meals"].iterrows():
        glucose_fig.add_vline( # Verifical lines on plot
            x= meal["Timestamp"],
            line_color=meal_colors.get(meal["Meal Type"],"gray"),
            opacity=0.25, # XXX: Comment out, gray might be too light
        )
    glucose_fig.update_layout(
        title="Glucose Timeline", xaxis_title="Time", yaxis_title="Glucose", height=500)
    
    st.plotly_chart(glucose_fig, use_container_width=True)


    # Heart rate
    # Activity (MET)
    # Add different colors for meals somehow
# cgmacros_summary_plot()
# cgmacros_raw_bio()
# ares_actigraphy_ME()
cgmacros_timeseries_per()
