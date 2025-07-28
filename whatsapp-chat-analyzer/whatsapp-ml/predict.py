# whatsapp-ml/predict.py
import joblib

# Load the saved sentiment model
try:
    model = joblib.load("sentiment_model.pkl")
except FileNotFoundError:
    print("❌ Model file 'sentiment_model.pkl' not found. Please train the model first.")
    exit(1)

def predict_sentiment(text: str) -> str:
    if not text.strip():
        return "⚠️ Empty input"
    return model.predict([text])[0]

# Run interactively
if __name__ == "__main__":
    print("🔮 Sentiment Prediction (type 'exit' to quit)\n")
    while True:
        user_input = input("Enter message: ").strip()
        if user_input.lower() == "exit":
            break
        sentiment = predict_sentiment(user_input)
        print("Predicted Sentiment:", sentiment, "\n")
