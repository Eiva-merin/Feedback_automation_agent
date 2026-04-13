# SensitHaptics Feedback Automation Agent

An AI-powered automation agent that collects YouTube comments about 
sim racing haptics hardware, analyses sentiment and extracts product 
insights automatically — eliminating hours of manual research.

## What it does
1. Searches YouTube for sim racing haptics reviews
2. Collects comments from top videos automatically
3. Runs AI sentiment analysis on every comment
4. Generates a structured report with actionable insights

## Sample Output
- Collected 175 real comments across 9 YouTube videos
- Identified top praised features: haptic feedback, build quality
- Identified top pain points: price, software issues, setup complexity
- Generated CSV report + text summary automatically

## Tech Stack
Python · YouTube Data API v3 · HuggingFace Transformers · 
DistilBERT · pandas · python-dotenv

## How to Run
```bash
pip install -r requirements.txt
python main.py
```

## Output
- `reports/feedback_report_[timestamp].csv` — full analysis
- `reports/summary_[timestamp].txt` — executive summary

## Real World Use Case
Automates competitor and product feedback monitoring for hardware 
startups — replacing manual YouTube research with an intelligent 
pipeline that runs on demand.