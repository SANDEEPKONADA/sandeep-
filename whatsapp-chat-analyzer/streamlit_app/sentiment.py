from textblob import TextBlob

def analyze_sentiment(df):
    # Compute polarity
    df["Polarity"] = df["Message"].fillna("").apply(lambda x: TextBlob(x).sentiment.polarity)
    
    # Classify sentiment
    def classify_sentiment(score):
        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"
    
    df["Sentiment"] = df["Polarity"].apply(classify_sentiment)
    
    return df
