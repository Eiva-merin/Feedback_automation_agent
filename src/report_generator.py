import pandas as pd
from datetime import datetime
import os

def generate_report(analyzed_comments, output_dir="reports"):
    """Generate a structured CSV report and text summary."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save full CSV
    df = pd.DataFrame(analyzed_comments)
    csv_path = f"{output_dir}/feedback_report_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    print(f"CSV saved: {csv_path}")

    # Generate summary
    summary = generate_summary(df, timestamp, output_dir)
    return csv_path, summary

def generate_summary(df, timestamp, output_dir):
    """Generate a human readable summary report."""

    total = len(df)
    avg_score = df["score"].mean()

    sentiment_counts = df["sentiment"].value_counts()
    positive = sentiment_counts.get("Positive", 0)
    negative = sentiment_counts.get("Negative", 0)
    neutral  = sentiment_counts.get("Neutral", 0)

    # Top features mentioned
    all_features = []
    for features in df["features_mentioned"]:
        if isinstance(features, list):
            all_features.extend(features)
    feature_freq = pd.Series(all_features).value_counts().head(5)

    # Top pain points
    all_pain = []
    for pain in df["pain_points"]:
        if isinstance(pain, list):
            all_pain.extend(pain)
    pain_freq = pd.Series(all_pain).value_counts().head(5)

    # Top insights from most liked comments
    top_insights = df.nlargest(5, "likes")[["video_title", "key_insight", "likes"]]

    summary = f"""
=====================================
  SENSITHAPTICS FEEDBACK REPORT
  Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
=====================================

OVERVIEW
--------
Total comments analysed : {total}
Average sentiment score : {avg_score:.1f} / 10
Positive comments       : {positive} ({positive/total*100:.1f}%)
Negative comments       : {negative} ({negative/total*100:.1f}%)
Neutral comments        : {neutral}  ({neutral/total*100:.1f}%)

TOP PRAISED FEATURES
--------------------
{feature_freq.to_string() if not feature_freq.empty else 'None identified'}

TOP PAIN POINTS / COMPLAINTS
-----------------------------
{pain_freq.to_string() if not pain_freq.empty else 'None identified'}

TOP INSIGHTS (most liked comments)
------------------------------------"""

    for _, row in top_insights.iterrows():
        summary += f"\n• [{row['likes']} likes] {row['key_insight']}"

    summary += "\n\n====================================="

    # Save summary
    summary_path = f"{output_dir}/summary_{timestamp}.txt"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(summary)
    print(f"\nSummary saved: {summary_path}")
    return summary

if __name__ == "__main__":
    test_data = [
        {"video_title": "Test", "channel": "TestChan", "comment": "Great product",
         "likes": 10, "sentiment": "Positive", "score": 8,
         "features_mentioned": ["haptic feedback", "software"],
         "pain_points": [], "key_insight": "Haptic feedback is highly praised"},
        {"video_title": "Test", "channel": "TestChan", "comment": "Too expensive",
         "likes": 5, "sentiment": "Negative", "score": 3,
         "features_mentioned": ["price"], "pain_points": ["expensive", "buggy software"],
         "key_insight": "Price point is a major concern for buyers"}
    ]
    generate_report(test_data)