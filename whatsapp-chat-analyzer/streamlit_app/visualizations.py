import altair as alt
import pandas as pd
import streamlit as st

def plot_message_distribution(df):
    if 'Sender' not in df.columns:
        st.warning("Sender column missing.")
        return

    sender_count = df['Sender'].value_counts().reset_index()
    sender_count.columns = ['Sender', 'Message Count']

    chart = alt.Chart(sender_count).mark_bar().encode(
        x=alt.X('Sender', sort='-y'),
        y='Message Count',
        tooltip=['Sender', 'Message Count']
    ).properties(
        title='Messages per User',
        width=600
    )
    st.altair_chart(chart, use_container_width=True)

def plot_hourly_activity(df):
    if 'Date' not in df.columns:
        st.warning("Date column missing.")
        return

    df['Hour'] = df['Date'].dt.hour
    hourly = df.groupby('Hour').size().reset_index(name='Messages')

    chart = alt.Chart(hourly).mark_line(point=True).encode(
        x='Hour:O',
        y='Messages:Q',
        tooltip=['Hour', 'Messages']
    ).properties(
        title='Hourly Message Activity',
        width=600
    )
    st.altair_chart(chart, use_container_width=True)

# ✅ This must exist for app.py to import successfully
def plot_visualizations(df):
    st.markdown("### 📊 Message Distribution")
    plot_message_distribution(df)

    st.markdown("### ⏰ Hourly Activity")
    plot_hourly_activity(df)
