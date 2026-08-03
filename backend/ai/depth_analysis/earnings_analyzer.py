import logging
from typing import Optional

logger = logging.getLogger(__name__)

TRANSCRIPTS = {
    "AAPL": {
        "quarter": "Q1 2026",
        "date": "2026-01-30",
        "eps_actual": 2.40,
        "eps_estimate": 2.35,
        "revenue_actual_b": 124.3,
        "revenue_estimate_b": 121.8,
        "highlights": [
            "iPhone revenue $69.1B, above consensus of $67.5B",
            "Services revenue hit all-time high of $26.3B, +14% YoY",
            "Installed base surpassed 2.3B active devices",
            "Board authorized additional $90B share buyback",
            "AI features driving iPhone upgrade cycle",
        ],
        "guidance": {
            "next_quarter_revenue_b": "90-95",
            "margin_pct": "46-47",
            "key_drivers": ["AI rollout", "China demand", "Services growth"],
        },
        "sentiment": "bullish",
        "call_duration_min": 68,
        "analyst_questions": 12,
    },
    "MSFT": {
        "quarter": "Q2 2026",
        "date": "2026-01-28",
        "eps_actual": 3.23,
        "eps_estimate": 3.18,
        "revenue_actual_b": 69.0,
        "revenue_estimate_b": 67.5,
        "highlights": [
            "Azure revenue +22% YoY, AI services contributing 8ppts",
            "Microsoft 365 Copilot subscribers grew 150% QoQ",
            "Commercial cloud annualized revenue exceeded $135B",
            "GitHub revenue passed $2B annual run rate",
            "LinkedIn revenue +12%, session growth +18%",
        ],
        "guidance": {
            "next_quarter_revenue_b": "71-73",
            "margin_pct": "70-71",
            "key_drivers": ["AI monetization", "Cloud migration", "Copilot expansion"],
        },
        "sentiment": "bullish",
        "call_duration_min": 72,
        "analyst_questions": 15,
    },
    "TSLA": {
        "quarter": "Q4 2025",
        "date": "2026-01-29",
        "eps_actual": 0.73,
        "eps_estimate": 0.65,
        "revenue_actual_b": 25.7,
        "revenue_estimate_b": 24.9,
        "highlights": [
            "Deliveries 495,570, above consensus of 480,000",
            "Cybertruck production ramp reached 2,500/week",
            "Energy storage deployments +110% YoY to 11.8 GWh",
            "FSD v13 released to wide fleet, intervention miles improved 5x",
            "Gross margin ex-RFX improved to 18.5%",
        ],
        "guidance": {
            "next_quarter_revenue_b": "26-28",
            "margin_pct": "18-20",
            "key_drivers": ["Cybertruck ramp", "Energy storage", "FSD monetization"],
        },
        "sentiment": "neutral",
        "call_duration_min": 55,
        "analyst_questions": 10,
    },
}


async def analyze_transcript(ticker: str) -> dict:
    t = TRANSCRIPTS.get(ticker.upper())
    if not t:
        return {"ticker": ticker.upper(), "error": "No transcript available"}
    surprise_eps = round((t["eps_actual"] - t["eps_estimate"]) / t["eps_estimate"] * 100, 1) if t["eps_estimate"] else 0
    return {
        "ticker": ticker.upper(),
        "quarter": t["quarter"],
        "date": t["date"],
        "headline": f"{ticker.upper()} {t['quarter']} Earnings",
        "eps_actual": t["eps_actual"],
        "eps_estimate": t["eps_estimate"],
        "eps_surprise_pct": surprise_eps,
        "revenue_actual_b": t["revenue_actual_b"],
        "revenue_estimate_b": t["revenue_estimate_b"],
        "revenue_surprise_pct": round((t["revenue_actual_b"] - t["revenue_estimate_b"]) / t["revenue_estimate_b"] * 100, 1),
        "highlights": t["highlights"],
        "guidance": t["guidance"],
        "sentiment": t["sentiment"],
        "call_duration_min": t["call_duration_min"],
        "analyst_questions": t["analyst_questions"],
        "verdict": "BEAT" if surprise_eps > 0 else "MISS",
    }


async def compare_earnings(tickers: list[str]) -> list[dict]:
    results = []
    for t in tickers:
        analysis = await analyze_transcript(t)
        if "error" not in analysis:
            results.append(analysis)
    return results


async def earnings_calendar() -> list[dict]:
    return [
        {"ticker": "AAPL", "date": "2026-04-24", "quarter": "Q2 2026", "eps_estimate": 2.30, "revenue_estimate_b": 118.5},
        {"ticker": "MSFT", "date": "2026-04-22", "quarter": "Q3 2026", "eps_estimate": 3.35, "revenue_estimate_b": 72.0},
        {"ticker": "GOOGL", "date": "2026-04-23", "quarter": "Q1 2026", "eps_estimate": 2.10, "revenue_estimate_b": 85.2},
        {"ticker": "AMZN", "date": "2026-04-24", "quarter": "Q1 2026", "eps_estimate": 1.20, "revenue_estimate_b": 158.0},
        {"ticker": "TSLA", "date": "2026-04-22", "quarter": "Q1 2026", "eps_estimate": 0.55, "revenue_estimate_b": 22.8},
    ]


async def get_sentiment_summary(ticker: str) -> dict:
    t = TRANSCRIPTS.get(ticker.upper())
    if not t:
        return {"error": "No data"}
    positive_keywords = ["growth", "record", "above", "expansion", "momentum", "adoption"]
    keyword_hits = sum(1 for h in t["highlights"] for kw in positive_keywords if kw.lower() in h.lower())
    return {
        "ticker": ticker.upper(),
        "overall_sentiment": t["sentiment"],
        "confidence": "high" if len(t["highlights"]) >= 4 else "medium",
        "positive_signals": keyword_hits,
        "highlight_count": len(t["highlights"]),
        "analyst_engagement": t["analyst_questions"],
    }
