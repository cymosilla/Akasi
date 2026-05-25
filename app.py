import streamlit as st

st.set_page_config(page_title="Akasi",layout="wide")

pg = st.navigation(
    [
        st.Page("pages/Home.py", title="Akasi Home", icon="🏠"),
        st.Page("pages/1_CGMacros.py",title="CGMacros",icon="🥢"),
        st.Page("pages/2_Ares.py",title="ARES",icon="🛌"),
        st.Page("pages/3_FutureDatasets.py",title="Future Datasets", icon="⌛")
    ]
)

pg.run()