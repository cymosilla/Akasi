from pathlib import Path
import pandas as pd
import plotly.express as px # New interactive chart, see how it goes
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.ares_echo_long_analysis import (
    load_cf_avg,
    get_primary_metric_labels,
    filter_metric,
    compute_summary,
    PRIMARY_METRICS,
)
from src.analysis.ares_echo_bayesian import (
    fit_bayesian_metric,
)

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


st.title("NASA Standard Measures Bed Rest Campaigns")    
st.header("What does \"bed rest\" mean?")

st.markdown(
    '''
    Getting paid to lay in bed all day may sound amazing. But this is no ordinary bed.
    To simulate spaceflight effects without being in space, bed rest involves a 6-degree tilt towards the head.
    This shows how fluids (blood, mucuous, earwax, lymphatic fluid, etc.) behave in a microgravity environment.
    Due to the body's orientation, it creates a sense that there is a lack of gravity. But the body feels the effects.
    Muscles start to atrophize, bones can become less dense, intracranial pressure can increase, peristalsis can also be affected. 
    '''
)

st.header("What can this do for Artemis II?")
st.markdown(
    '''
    Outside of the microgravity effects, my intention of selecting this one next was to try & relate peristalsis data from CGMacros with bed resting & differentiate glucose levels & heart rhythms.
    The bed rest studies are abundant with data, but there is a lack of documentation on how to read some of the files. What's left is still some pretty useful data.
    Actigraphy - 


'''
)

# Sleep it off trajectory 
def plot_eepy_traj(df):
    plot_df = df.sort_values(["Subject", "BR_Day"])

    fig = px.line(
        plot_df,
        x="BR_Day",
        y="sleep_efficiency",
        color="Subject",
        title="Sleep Efficiency by Subject",
        labels={
            "BR_Day": "Bed Rest Day",
            "sleep_efficiency": "Sleep Efficiency (%)",
        },
    )

    fig.update_layout(height=600,legend_title="Subject")

    st.plotly_chart(fig, use_container_width=True)
    st.write(df.groupby("Subject").size().reset_index(name="n_rows"))
    st.write(df.groupby("Subject")["sleep_efficiency"].agg(["count", "min", "max"]))

# Sleep mean
def plot_eepy_effmean(df):

    summary = df.groupby("BR_Day")["sleep_efficiency"].agg(mean="mean",std="std",count="count").reset_index()

    summary["se"] = summary["std"]/np.sqrt(summary["count"])
    summary["lower"] = summary["mean"] -1.96 * summary["se"]
    summary["upper"] = summary["mean"]+  1.96 * summary["se"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=summary["BR_Day"],
            y=summary["upper"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
        )
    )

    fig.update_layout(
        title="Average Sleep Efficiency Across Bed Rest",
        xaxis_title="Bed Rest Day",
        yaxis_title="Sleep Efficiency (%)",
        height=600,
    )

    st.plotly_chart(fig,use_container_width=True)


# Efficiency based on phases
def plot_eepy_effPhase(df):

    phase_summary = df.groupby("Test_Phase")["sleep_efficiency"].mean().reset_index()
    fig = px.bar(
        phase_summary,
        x="Test_Phase",
        y="sleep_efficiency",
        title="Average Sleep Efficiency by Test Phase",
        labels={"Test_Phase": "Test Phase","sleep_efficiency": "Sleep Efficiency (%)"},
        text_auto=".1f",
    )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

def plot_medication_effect(df):
    med_summary = df.groupby("any_sleep_med")["sleep_efficiency"].mean().reset_index()

    # med_summary = (
    #     df.groupby("any_sleep_med")["sleep_efficiency"]
    #     .svd()
    #     .reset_index()
    # )

    med_summary["Medication"] = med_summary["any_sleep_med"].map({0: "No Medication",1: "Medication Used",})

    fig = px.bar(
        med_summary,
        x="Medication",
        y="sleep_efficiency",
        title="Average Sleep Efficiency by Medication Use",
        text_auto=".1f",
        labels={"sleep_efficiency": "Sleep Efficiency (%)"},
    )

    fig.update_layout(height=500,showlegend=False,)
    st.plotly_chart(fig,use_container_width=True)

def ares_actigraphy_ME():
    st.header("ARES Actigraphy Mixed Effects")
    df = pd.read_csv(ANALYZED_PATH / "ares-actigraphy-mixedeffects.csv")
    st.subheader("Model COE")
    st.dataframe(df, use_container_width=True) # Take up entire width of page
    # Attempt at Forest GGDM
    st.subheader("COE estimates")
    plot_df = df[~df["term"].str.contains("Group Var", na=False)]
    st.scatter_chart(data=plot_df, x="coefficient", y="term")
    # Sig Terms
    st.subheader("Significant effects")
    sig = df[df["p_value"] < 0.05]
    st.dataframe(sig, use_container_width=True)
    actigraphy_df = pd.read_csv(ANALYZED_PATH / "ares-actigraphy-clean.csv")
    st.subheader("Subject Trajectories")
    plot_eepy_traj(actigraphy_df)
    st.subheader("Mean Trends")
    plot_eepy_effmean(actigraphy_df)
    st.subheader("Sleep Efficiency by Phase")
    plot_eepy_effPhase(actigraphy_df)
    st.subheader("Medication Effect")
    plot_medication_effect(actigraphy_df)


def test():
    df = load_cf_avg()
    print(df["Test"].sort_values().unique())

def ares():
    # Dropdown time
    methods = {"Actigraphy Mixed Effects": ares_actigraphy_ME,
               # Add other methods here
               }

    selected = st.selectbox("Select Analysis",list(methods.keys()))
    # selected[methods]()
    methods[selected]()

ares()