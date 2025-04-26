from typing import Dict
import joblib
import os

class SentimentAnalyzer:
    def __init__(self):
        """
        Load trained sentiment classifier from a pickle file.
        Adjusts pathing to work reliably regardless of run location.
        """
        current_dir = os.path.dirname(__file__)  # Get path to this file
        model_path = os.path.join(current_dir, "sentiment_model.pkl")  # Absolute-safe path
        self.model = joblib.load(model_path)

    def analyze(self, text: str) -> Dict[str, str]:
        """
        Predict sentiment using trained ML model.
        Returns a dictionary with:
            - sentiment: 'positive', 'neutral', or 'negative'
            - is_frustrated: True if sentiment is negative
        """
        sentiment = self.model.predict([text])[0]
        print(f"[🧠 ML Sentiment] {text.strip()} → {sentiment}")
        return {
            "sentiment": sentiment,
            "is_frustrated": sentiment == "negative"
        }

    def get_response_tone(self, sentiment: Dict[str, str]) -> str:
        """
        Maps sentiment to a conversational tone.
        """
        tone = "neutral"  # default

        if sentiment.get("is_frustrated"):
            tone = "empathetic"
        elif sentiment.get("sentiment") == "positive":
            tone = "positive"
        elif sentiment.get("sentiment") == "negative":
            tone = "reassuring"

        print(f"[🎯 Tone] Using tone: {tone}")
        return tone
