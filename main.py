from src.youtube_collector import collect_feedback
from src.ai_analyzer import analyze_all_comments
from src.report_generator import generate_report

def run_agent():
    print("=" * 50)
    print("  SENSITHAPTICS FEEDBACK AUTOMATION AGENT")
    print("=" * 50)

    # Step 1 — Collect YouTube feedback
    print("\nSTEP 1 — Collecting YouTube feedback...")
    search_queries = [
        "SensitHaptics sim racing review",
        "sim racing haptics hardware review",
        "direct drive haptics sim racing 2024"
    ]
    videos, comments = collect_feedback(
        search_queries,
        max_videos=3,
        max_comments=20
    )

    if not comments:
        print("No comments found. Check your YouTube API key.")
        return

    # Step 2 — Analyse with AI
    print("\nSTEP 2 — Analysing comments with AI...")
    analyzed = analyze_all_comments(comments, max_comments=30)

    if not analyzed:
        print("Analysis failed. Check your setup.")
        return

    # Step 3 — Generate report
    print("\nSTEP 3 — Generating report...")
    csv_path, summary = generate_report(analyzed)

    print("\nAGENT COMPLETE")
    print(f"Report saved to: {csv_path}")

if __name__ == "__main__":
    run_agent()