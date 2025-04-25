from transformers import pipeline
from data_store import save_entry, get_entries

sentiment_analyzer = pipeline("sentiment-analysis")
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def analyze_text(text):
    sentiment = sentiment_analyzer(text)[0]
    emotion = emotion_classifier(text)[0][0]
    return {
        "sentiment": sentiment["label"],
        "sentiment_score": round(sentiment["score"], 3),
        "emotion": emotion["label"],
        "emotion_score": round(emotion["score"], 3),
    }
