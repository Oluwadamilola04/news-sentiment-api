from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()
analyzer = SentimentIntensityAnalyzer()

IMPACT_KEYWORDS = ["crash", "surge", "rate hike", "recession", "plunge", "rally", "crisis", "default"]

class Headline(BaseModel):
    headline: str

@app.post("/analyze")
def analyze(data: Headline):
    scores = analyzer.polarity_scores(data.headline)
    compound = scores["compound"]

    if compound >= 0.5:
        sentiment = "positive"
    elif compound <= -0.5:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    matched = [kw for kw in IMPACT_KEYWORDS if kw in data.headline.lower()]

    return {
        "sentiment": sentiment,
        "confidence": abs(compound),
        "impact_keywords": matched
    }
