# whatsapp-ml/batch_predict.py
import pandas as pd
import joblib

# Load model
model = joblib.load("sentiment_model.pkl")

# Load messages
df = pd.read_csv("labeled_chats.csv")

# Predict on messages that don't have sentiment yet
unlabeled = df[df["Sentiment"].isna() | (df["Sentiment"] == "")]
if unlabeled.empty:
    print("✅ All messages already labeled.")
else:
    predictions = model.predict(unlabeled["Message"])
    df.loc[unlabeled.index, "Sentiment"] = predictions
    df.to_csv("predicted_chats.csv", index=False)
    print(f"✅ Predictions saved to 'predicted_chats.csv' with {len(predictions)} newly labeled messages.")
