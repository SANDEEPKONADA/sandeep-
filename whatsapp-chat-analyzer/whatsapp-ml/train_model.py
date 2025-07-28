# train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Load data
df = pd.read_csv("labeled_chats.csv")

# Step 1: Drop missing or empty rows
df = df.dropna(subset=["Message", "Sentiment"])
df["Message"] = df["Message"].astype(str).str.strip()
df = df[df["Message"] != ""]  # Remove empty strings

# Step 2: (Optional) Remove duplicates
df = df.drop_duplicates(subset=["Message", "Sentiment"])

# Step 3: Confirm messages are not all stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
df = df[~df["Message"].isin(ENGLISH_STOP_WORDS)]

# Step 4: Check again
if df.empty:
    raise ValueError("❌ No valid training data left after cleaning.")

# Features and labels
X = df["Message"]
y = df["Sentiment"]

# Step 5: Define and train model
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english")),
    ("clf", MultinomialNB())
])

model.fit(X, y)

# Step 6: Save model
joblib.dump(model, "sentiment_model.pkl")
print("✅ Model trained and saved as 'sentiment_model.pkl'")
