# pyrefly: ignore [missing-import]
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentService:

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str):
        if text is None or text.strip() == "":
            return {
                "sentiment": "Neutral",
                "compound": 0.0,
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0
            }

        score = self.analyzer.polarity_scores(text)
        compound = score["compound"]

        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "sentiment": sentiment,
            "compound": compound,
            "positive": score["pos"],
            "neutral": score["neu"],
            "negative": score["neg"]
        }

    def analyze_bulk(self, texts):
        return [self.analyze_text(text) for text in texts]

    def repository_sentiment(self, texts):
        if not texts:
            return {
                "overall_sentiment": "Neutral",
                "average_score": 0
            }

        scores = [self.analyze_text(text)["compound"] for text in texts]
        avg = sum(scores) / len(scores)

        if avg >= 0.05:
            sentiment = "Positive"
        elif avg <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "overall_sentiment": sentiment,
            "average_score": round(avg, 3)
        }