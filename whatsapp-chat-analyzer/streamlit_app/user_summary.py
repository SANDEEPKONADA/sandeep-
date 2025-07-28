import pandas as pd

def generate_user_summary(df):
    """
    Generates a summary for each user including:
    - Total messages sent
    - Average message length
    - Media/shared content stats
    """
    if 'Sender' not in df.columns or 'Message' not in df.columns:
        return pd.DataFrame()

    summary = df.groupby("Sender").agg(
        total_messages=pd.NamedAgg(column="Message", aggfunc="count"),
        avg_message_length=pd.NamedAgg(column="Message", aggfunc=lambda x: round(x.str.len().mean(), 2)),
        total_media=pd.NamedAgg(column="Message", aggfunc=lambda x: x.str.contains("<Media omitted>").sum())
    ).reset_index()

    return summary
