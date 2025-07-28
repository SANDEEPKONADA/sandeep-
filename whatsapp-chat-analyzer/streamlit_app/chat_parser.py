import pandas as pd
import re

def parse_chat(file):
    if file.name.endswith('.csv'):
        try:
            df = pd.read_csv(file)
            required_columns = {"Date", "Sender", "Message"}
            if required_columns.issubset(df.columns):
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df.dropna(subset=["Date", "Sender", "Message"], inplace=True)
                return df
            else:
                return None
        except Exception:
            return None

    try:
        lines = file.read().decode("utf-8", errors="ignore").splitlines()
    except Exception:
        return None

    data = []

    # ✅ Pattern 1: Android/Export
    pattern_android = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?:\s?[APMapm]{2})?) - (.*?): (.*)$'
    )

    # ✅ Pattern 2: iPhone/Desktop (with square brackets)
    pattern_iphone = re.compile(
        r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}(?::\d{2})?\s?[APMapm]{2})\] (.*?): (.*)$'
    )

    current_msg = ""
    current_date = None
    current_time = None
    current_sender = None

    for line in lines:
        match = pattern_android.match(line) or pattern_iphone.match(line)
        if match:
            if current_msg and current_sender:
                timestamp = pd.to_datetime(f"{current_date} {current_time}", dayfirst=True, errors="coerce")
                data.append({
                    "Date": timestamp,
                    "Sender": current_sender.strip(),
                    "Message": current_msg.strip()
                })
            current_date, current_time, current_sender, current_msg = match.groups()
        else:
            current_msg += "\n" + line.strip()

    # Last message
    if current_msg and current_sender:
        timestamp = pd.to_datetime(f"{current_date} {current_time}", dayfirst=True, errors="coerce")
        data.append({
            "Date": timestamp,
            "Sender": current_sender.strip(),
            "Message": current_msg.strip()
        })

    df = pd.DataFrame(data)
    if {"Date", "Sender", "Message"}.issubset(df.columns):
        df.dropna(subset=["Date", "Sender", "Message"], inplace=True)
        return df
    else:
        return None
