from transformers import pipeline
import re

print("Loading AI model... (first time takes 1 minute to download)")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Model loaded!")

HAPTICS_KEYWORDS = [
    "haptic", "vibration", "feedback", "rumble", "feel", "immersive",
    "realistic", "tactile", "response", "sensation", "force", "texture"
]

HARDWARE_KEYWORDS = [
    "build quality", "hardware", "device", "pedal", "wheel", "seat",
    "mount", "cable", "setup", "installation", "compatibility"
]

SOFTWARE_KEYWORDS = [
    "software", "app", "driver", "update", "bug", "crash", "interface",
    "settings", "configuration", "firmware", "support"
]

PRICE_KEYWORDS = [
    "price", "expensive", "cheap", "worth", "value", "cost",
    "money", "affordable", "overpriced", "budget"
]

def extract_features(comment_text):
    """Extract mentioned features from comment."""
    text_lower = comment_text.lower()
    features = []
    if any(k in text_lower for k in HAPTICS_KEYWORDS):
        features.append("haptic feedback")
    if any(k in text_lower for k in HARDWARE_KEYWORDS):
        features.append("build quality")
    if any(k in text_lower for k in SOFTWARE_KEYWORDS):
        features.append("software")
    if any(k in text_lower for k in PRICE_KEYWORDS):
        features.append("price")
    return features if features else ["general"]

def extract_pain_points(comment_text, sentiment):
    """Extract pain points from negative comments."""
    if sentiment == "Positive":
        return []
    text_lower = comment_text.lower()
    pain_points = []
    if any(k in text_lower for k in ["crash", "bug", "broken", "issue", "problem", "error"]):
        pain_points.append("software issues")
    if any(k in text_lower for k in ["expensive", "overpriced", "costly", "price"]):
        pain_points.append("high price")
    if any(k in text_lower for k in ["difficult", "hard", "complicated", "setup"]):
        pain_points.append("difficult setup")
    if any(k in text_lower for k in ["slow", "delay", "lag", "latency"]):
        pain_points.append("latency issues")
    if any(k in text_lower for k in ["quality", "cheap", "plastic", "flimsy"]):
        pain_points.append("build quality concerns")
    return pain_points if pain_points else ["general dissatisfaction"]

def generate_insight(comment_text, sentiment, features):
    """Generate a short insight from the comment."""
    text = comment_text[:150]
    feature_str = features[0] if features else "the product"
    if sentiment == "Positive":
        return f"User praises {feature_str} — {text[:80]}..."
    elif sentiment == "Negative":
        return f"User critical of {feature_str} — {text[:80]}..."
    else:
        return f"User neutral about {feature_str} — {text[:80]}..."

def analyze_comment(comment_text, video_title):
    """Analyze a single comment using local AI model."""
    # Run sentiment analysis
    result = sentiment_pipeline(comment_text[:512])[0]

    raw_sentiment = result["label"]
    confidence = result["score"]

    # Map to our format
    if raw_sentiment == "POSITIVE":
        sentiment = "Positive"
        score = round(5 + (confidence * 5))
    else:
        sentiment = "Negative"
        score = round(5 - (confidence * 5))
        score = max(1, score)

    features = extract_features(comment_text)
    pain_points = extract_pain_points(comment_text, sentiment)
    insight = generate_insight(comment_text, sentiment, features)

    return {
        "sentiment": sentiment,
        "score": score,
        "features_mentioned": features,
        "pain_points": pain_points,
        "key_insight": insight
    }

def analyze_all_comments(comments, max_comments=50):
    """Analyze a batch of comments."""
    results = []
    comments_to_analyze = comments[:max_comments]

    for i, comment in enumerate(comments_to_analyze):
        print(f"Analyzing comment {i+1}/{len(comments_to_analyze)}...")
        try:
            analyzed = analyze_comment(
                comment["comment"],
                comment.get("video_title", "Unknown")
            )
            result = {
                "video_title": comment.get("video_title", ""),
                "channel": comment.get("channel", ""),
                "comment": comment["comment"][:200],
                "likes": comment.get("likes", 0),
                **analyzed
            }
            results.append(result)
        except Exception as e:
            print(f"Error on comment {i+1}: {e}")
            continue

    return results

if __name__ == "__main__":
    test_comments = [
        {
            "comment": "The haptic feedback on this is incredible, feels so realistic during cornering!",
            "video_title": "SensitHaptics Review 2024",
            "channel": "SimRacingGarage",
            "likes": 45
        },
        {
            "comment": "Way too expensive for what you get. The software keeps crashing.",
            "video_title": "SensitHaptics Review 2024",
            "channel": "SimRacingGarage",
            "likes": 12
        },
        {
            "comment": "Decent product overall but setup was complicated for beginners.",
            "video_title": "SensitHaptics Setup Guide",
            "channel": "SimRacingPro",
            "likes": 8
        }
    ]

    results = analyze_all_comments(test_comments)
    for r in results:
        print(f"\nSentiment: {r['sentiment']} | Score: {r['score']}/10")
        print(f"Features: {r['features_mentioned']}")
        print(f"Pain points: {r['pain_points']}")
        print(f"Insight: {r['key_insight']}")
