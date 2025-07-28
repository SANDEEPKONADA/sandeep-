# whatsapp-ml/extract_messages.py
import re
import pandas as pd

def extract_messages(file_path):
    # Regex: Match lines like `29/12/24, 16:43 - Sandy: some message`
    pattern = r"^\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} - (.*?): (.*)"
    messages = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                message = match.group(2).strip()
                if message and message != "<Media omitted>":
                    messages.append(message)

    if not messages:
        print("❌ No messages found. Check the chat format.")
        return

    df = pd.DataFrame(messages, columns=["Message"])
    df["Sentiment"] = ""  # You will manually label this
    df.to_csv("labeled_chats.csv", index=False)
    print(f"✅ Extracted {len(df)} messages. Now open 'labeled_chats.csv' and label the 'Sentiment' column.")

# Call the function
extract_messages("chat.txt")  # Replace with your actual file name if different
