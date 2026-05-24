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
    The bed rest studies are abundant with data, but there is a lack of documentation on how to read some of the files.
    
'''
)
def ares_actigraphy_ME():
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