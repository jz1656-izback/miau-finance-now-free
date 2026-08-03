import re
from datetime import datetime, timedelta
from typing import Optional

from app.cache_utils import cached
from app.services.analytics import news as news_service


def _score_text_vader(text: str) -> float:
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(text)["compound"]
    except ImportError:
        try:
            from textblob import TextBlob
            return TextBlob(text).sentiment.polarity
        except ImportError:
            pass
    words = text.lower().split()
    positive = {"up", "gain", "bullish", "outperform", "growth", "surge", "beat", "positive", "profit", "strong", "upgrade", "buy", "rally", "boost", "optimistic", "rising", "momentum", "breakthrough"}
    negative = {"down", "loss", "bearish", "underperform", "decline", "drop", "miss", "negative", "loss", "weak", "downgrade", "sell", "crash", "fall", "slump", "risk", "warning", "downturn", "debt", "cut"}
    pos_count = sum(1 for w in words if w in positive)
    neg_count = sum(1 for w in words if w in negative)
    total = pos_count + neg_count
    if total == 0:
        return 0.0
    return (pos_count - neg_count) / total


def _classify(score: float) -> str:
    if score >= 0.15:
        return "bullish"
    elif score <= -0.15:
        return "bearish"
    return "neutral"


@cached(ttl=300, prefix="sentiment")
async def analyze_ticker_sentiment(ticker: str, days: int = 7) -> dict:
    articles = await news_service.company_news(ticker, limit=50)
    cutoff = datetime.now() - timedelta(days=days)
    scored = []
    for art in articles:
        published = art.get("published_at")
        if published:
            try:
                pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if pub_dt < cutoff:
                    continue
            except (ValueError, TypeError):
                pass
        title = art.get("title", "")
        summary = art.get("summary", "")
        combined = f"{title} {summary}"
        score = _score_text_vader(combined)
        scored.append({
            "title": title,
            "summary": summary[:200] if summary else "",
            "publisher": art.get("publisher", ""),
            "link": art.get("link", ""),
            "published_at": published,
            "sentiment_score": round(score, 4),
            "classification": _classify(score),
        })

    if not scored:
        return {
            "ticker": ticker,
            "overall_score": 0.0,
            "classification": "neutral",
            "article_count": 0,
            "articles": [],
        }

    avg_score = sum(a["sentiment_score"] for a in scored) / len(scored)
    return {
        "ticker": ticker,
        "overall_score": round(avg_score, 4),
        "classification": _classify(avg_score),
        "article_count": len(scored),
        "articles": sorted(scored, key=lambda x: abs(x["sentiment_score"]), reverse=True)[:10],
    }


@cached(ttl=300, prefix="sentiment_market")
async def analyze_market_sentiment(days: int = 1) -> dict:
    articles = await news_service.yahoo_finance_news("", limit=50)
    cutoff = datetime.now() - timedelta(days=days)
    scored = []
    for art in articles:
        published = art.get("published_at")
        if published:
            try:
                pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                if pub_dt < cutoff:
                    continue
            except (ValueError, TypeError):
                pass
        title = art.get("title", "")
        summary = art.get("summary", "")
        combined = f"{title} {summary}"
        score = _score_text_vader(combined)
        scored.append({
            "title": title,
            "summary": summary[:200] if summary else "",
            "source": art.get("publisher", ""),
            "link": art.get("link", ""),
            "published_at": published,
            "sentiment_score": round(score, 4),
            "classification": _classify(score),
        })

    if not scored:
        return {
            "overall_score": 0.0,
            "classification": "neutral",
            "article_count": 0,
            "articles": [],
        }

    avg_score = sum(a["sentiment_score"] for a in scored) / len(scored)
    bullish = sum(1 for a in scored if a["classification"] == "bullish")
    bearish = sum(1 for a in scored if a["classification"] == "bearish")
    neutral = sum(1 for a in scored if a["classification"] == "neutral")

    return {
        "overall_score": round(avg_score, 4),
        "classification": _classify(avg_score),
        "article_count": len(scored),
        "breakdown": {"bullish": bullish, "bearish": bearish, "neutral": neutral},
        "articles": sorted(scored, key=lambda x: abs(x["sentiment_score"]), reverse=True)[:10],
    }
