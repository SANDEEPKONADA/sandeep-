import streamlit as st
import pandas as pd
import os

from chat_parser import parse_chat
from chat_stats import get_chat_stats
from file_upload import handle_uploaded_file
from user_summary import generate_user_summary
from download_utils import download_button
from sentiment import analyze_sentiment
from visualizations import plot_message_distribution, plot_hourly_activity

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.title("📊 WhatsApp Chat Analyzer")

uploaded_files = st.file_uploader(
    "📂 Upload one or more WhatsApp chats (`.txt` or `.csv`)", 
    type=["txt", "csv"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_dfs = []

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_type = os.path.splitext(file_name)[-1].lower()

        if file_type == ".csv":
            try:
                df = pd.read_csv(uploaded_file)
                if {'Date', 'Sender', 'Message'}.issubset(df.columns):
                    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                    df.dropna(subset=["Date", "Sender", "Message"], inplace=True)
                    all_dfs.append(df)
                else:
                    st.warning(f"⚠️ CSV '{file_name}' does not have required columns: Date, Sender, Message")
            except Exception as e:
                st.error(f"❌ Error reading CSV '{file_name}': {e}")
        elif file_type == ".txt":
            parsed_df = parse_chat(uploaded_file)
            if parsed_df is not None and not parsed_df.empty:
                all_dfs.append(parsed_df)
            else:
                st.warning(f"⚠️ Could not parse chat from '{file_name}'")
        else:
            st.warning(f"Unsupported file format: {file_name}")

    if not all_dfs:
        st.error("❌ No valid chat files parsed.")
    else:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        st.success(f"✅ Parsed {len(all_dfs)} file(s), total messages: {len(combined_df)}")

        with st.expander("📄 Uploaded Files"):
            for f in uploaded_files:
                st.markdown(f"- {f.name}")

        with st.expander("🔍 Preview Combined Chat Data"):
            st.dataframe(combined_df.head(100), use_container_width=True)

        # Overview stats
        st.subheader("📈 Chat Overview")
        stats = get_chat_stats(combined_df)
        cols = st.columns(4)
        cols[0].metric("Total Messages", stats.get('total_messages', 0))
        cols[1].metric("Media Shared", stats.get('media_shared', 0))
        cols[2].metric("Links Shared", stats.get('links_shared', 0))
        cols[3].metric("Participants", stats.get('participants', 0))

        # Messages per user
        if 'messages_per_user' in stats:
            st.subheader("📊 Messages per User")
            st.bar_chart(stats['messages_per_user'])

        # User summary
        st.subheader("👥 User Summary")
        summary_df = generate_user_summary(combined_df)
        st.dataframe(summary_df, use_container_width=True)

        # Sentiment analysis
        st.subheader("🧠 Sentiment Analysis")
        sentiment_df = analyze_sentiment(combined_df)
        st.dataframe(sentiment_df[["Sender", "Message", "Polarity", "Sentiment"]].head(100), use_container_width=True)

        # Download
        st.subheader("⬇️ Download Analyzed CSV")
        download_button(sentiment_df, filename="chat_analysis.csv")

        # Visualizations
        st.subheader("📊 Visual Insights")
        plot_message_distribution(combined_df)
        plot_hourly_activity(combined_df)
