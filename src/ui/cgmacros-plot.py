import streamlit as st
import matplotlib.pyplot as plt

def plot_time_series_matplotlib(df, col, title):
    df2 = df.dropna(subset=["Timestamp", col]).sort_values("Timestamp")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df2["Timestamp"], df2[col], linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(col)
    fig.autofmt_xdate()
    return fig

fig = plot_time_series_matplotlib(df, col, f"{source} GL - Participant {sid}")
st.pyplot(fig, use_container_width=True)
plt.close(fig)