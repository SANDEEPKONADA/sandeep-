import pandas as pd

def get_chat_stats(df):
    # Total messages
    num_messages = df.shape[0]

    # Total words
    total_words = df['Message'].apply(lambda x: len(str(x).split())).sum()

    # Media shared
    media_shared = df[df['Message'].str.strip() == '<Media omitted>'].shape[0]

    # Links shared
    links_shared = df['Message'].str.count(r'http[s]?://').sum()

    # Messages per user (for bar chart)
    messages_per_user = df['Sender'].value_counts()

    # Unique participants
    participants = df['Sender'].nunique()

    return {
        'total_messages': num_messages,
        'total_words': total_words,
        'media_shared': media_shared,
        'links_shared': links_shared,
        'messages_per_user': messages_per_user,
        'participants': participants   # ✅ added
    }
