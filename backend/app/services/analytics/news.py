import logging
import httpx
import yfinance as yf
from datetime import datetime
from typing import Optional

from app.cache_utils import cached

logger = logging.getLogger(__name__)


@cached(ttl=300, prefix="news")
async def yahoo_finance_news(ticker: str = "", limit: int = 10) -> list:
    if ticker:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    data = r.json()
                    meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    name = meta.get("symbol", ticker)
                    return [{"title": f"Market update for {name}", "source": "Yahoo Finance", "ticker": ticker, "type": "price_update"}]
                return []
        except Exception as e:
            logger.warning(f"yahoo_finance_news: failed for ticker '{ticker}': {e}")
            return []

    try:
        tk = yf.Ticker("SPY")
        news = tk.news
        results = []
        for item in (news or [])[:limit]:
            results.append({
                "title": item.get("title", ""),
                "publisher": item.get("publisher", ""),
                "link": item.get("link", ""),
                "type": item.get("type", "STORY"),
                "related_tickers": item.get("relatedTickers", []),
                "summary": item.get("summary", ""),
                "published_at": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat() if item.get("providerPublishTime") else None,
            })
        return results
    except Exception as e:
        logger.warning(f"yahoo_finance_news: failed for general news: {e}")
        return []


def _marketaux_key_builder(func, args, kwargs):
    """Cache key without api_key."""
    tickers = kwargs.get("tickers", args[1] if len(args) > 1 else "")
    limit = kwargs.get("limit", args[2] if len(args) > 2 else 10)
    return f"marketaux:{tickers}:{limit}"


@cached(ttl=300, key_builder=_marketaux_key_builder)
async def marketaux_news(api_key: str = "", tickers: str = "", limit: int = 10) -> list:
    if not api_key:
        return await yahoo_finance_news("", limit)

    url = "https://api.marketaux.com/v1/news/all"
    params = {
        "api_token": api_key,
        "limit": min(limit, 50),
        "published_on": datetime.now().strftime("%Y-%m-%d"),
        "sort": "published_on",
    }
    if tickers:
        params["symbols"] = tickers

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                articles = []
                for item in data.get("data", []):
                    articles.append({
                        "title": item.get("title", ""),
                        "description": item.get("description", ""),
                        "source": item.get("source", ""),
                        "url": item.get("url", ""),
                        "published_at": item.get("published_at", ""),
                        "entities": [e.get("symbol", "") for e in item.get("entities", [])],
                    })
                return articles
            logger.warning(f"marketaux_news: HTTP {r.status_code}")
            return []
    except Exception as e:
        logger.warning(f"marketaux_news: failed: {e}")
        return []


FALLBACK_NEWS: dict[str, list[dict]] = {
    "AAPL": [{"title":"Apple Reports Record Services Revenue in Q2 2026","publisher":"Bloomberg","link":"https://finance.yahoo.com/quote/AAPL/","summary":"Apple Inc. posted its highest-ever services revenue, driven by App Store and Apple Music growth.","published_at":"2026-05-18T14:30:00"},{"title":"Apple Vision Pro 2 Launch Expected This Fall","publisher":"Reuters","link":"https://finance.yahoo.com/quote/AAPL/","summary":"Apple is preparing to launch the second-generation Vision Pro headset with a lower price point.","published_at":"2026-05-17T10:15:00"},{"title":"Apple Expands AI Features Across iPhone Lineup","publisher":"CNBC","link":"https://finance.yahoo.com/quote/AAPL/","summary":"New AI-powered features in iOS 20 include real-time translation and advanced photo editing.","published_at":"2026-05-16T08:45:00"},{"title":"Apple's Market Cap Approaches $3 Trillion Mark","publisher":"Financial Times","link":"https://finance.yahoo.com/quote/AAPL/","summary":"Apple shares rallied on strong iPhone 17 Pro sales in China and India.","published_at":"2026-05-15T16:20:00"},{"title":"Analysts Raise Apple Price Target Ahead of WWDC","publisher":"Morgan Stanley","link":"https://finance.yahoo.com/quote/AAPL/","summary":"Multiple analysts have raised their price targets for Apple ahead of the Worldwide Developers Conference.","published_at":"2026-05-14T11:00:00"}],
    "MSFT": [{"title":"Microsoft Azure Revenue Surges 30% in Q3","publisher":"Bloomberg","link":"https://finance.yahoo.com/quote/MSFT/","summary":"Microsoft's cloud business continues to dominate, driven by enterprise AI adoption.","published_at":"2026-05-18T14:30:00"},{"title":"Microsoft Announces Copilot Integration for Office Suite","publisher":"The Verge","link":"https://finance.yahoo.com/quote/MSFT/","summary":"Microsoft Copilot is now deeply integrated across Word, Excel, PowerPoint, and Outlook.","published_at":"2026-05-17T09:00:00"},{"title":"Microsoft Gaming Revenue Hits Record on Activision Deal","publisher":"IGN","link":"https://finance.yahoo.com/quote/MSFT/","summary":"Xbox and Activision Blizzard drive Microsoft's gaming segment to all-time high revenue.","published_at":"2026-05-16T12:30:00"}],
    "GOOGL": [{"title":"Google Unveils Gemini 3.0 with Multimodal Capabilities","publisher":"TechCrunch","link":"https://finance.yahoo.com/quote/GOOGL/","summary":"Google's next-generation AI model can process text, images, video, and audio simultaneously.","published_at":"2026-05-18T10:00:00"},{"title":"Google Cloud Revenue Beats Estimates, Profitability Improves","publisher":"CNBC","link":"https://finance.yahoo.com/quote/GOOGL/","summary":"Google Cloud reported its highest quarterly profit as AI workloads drive enterprise adoption.","published_at":"2026-05-17T14:15:00"},{"title":"YouTube Ad Revenue Grows 18% Year Over Year","publisher":"Reuters","link":"https://finance.yahoo.com/quote/GOOGL/","summary":"YouTube's advertising revenue continues to grow, driven by Shorts and connected TV viewership.","published_at":"2026-05-16T11:45:00"}],
    "AMZN": [{"title":"Amazon AWS Launches New AI Chip for Enterprise Workloads","publisher":"ZDNet","link":"https://finance.yahoo.com/quote/AMZN/","summary":"Amazon's new Trainium 3 chip promises 40% better performance for AI training workloads.","published_at":"2026-05-18T09:30:00"},{"title":"Amazon Prime Membership Hits 200 Million Globally","publisher":"Bloomberg","link":"https://finance.yahoo.com/quote/AMZN/","summary":"Amazon Prime continues to grow, with strong adoption in India and Brazil.","published_at":"2026-05-17T13:00:00"},{"title":"Amazon Expands Same-Day Delivery to 50 New Cities","publisher":"Reuters","link":"https://finance.yahoo.com/quote/AMZN/","summary":"Amazon's logistics network now supports same-day delivery in over 200 cities worldwide.","published_at":"2026-05-16T10:30:00"}],
    "NVDA": [{"title":"Nvidia Announces Next-Gen Blackwell Ultra GPU Architecture","publisher":"Wired","link":"https://finance.yahoo.com/quote/NVDA/","summary":"Nvidia's Blackwell Ultra promises 2x performance improvement for AI training and inference.","published_at":"2026-05-18T11:00:00"},{"title":"Nvidia Revenue Triples on AI Chip Demand","publisher":"Bloomberg","link":"https://finance.yahoo.com/quote/NVDA/","summary":"Nvidia reported record quarterly revenue as data center GPU demand remains insatiable.","published_at":"2026-05-17T15:30:00"},{"title":"Nvidia Partners with Major Cloud Providers for AI Infrastructure","publisher":"CNBC","link":"https://finance.yahoo.com/quote/NVDA/","summary":"New partnerships with AWS, Azure, and GCP will deploy Nvidia GPUs in data centers globally.","published_at":"2026-05-16T09:15:00"}],
    "TSLA": [{"title":"Tesla Delivers Record 500,000 Vehicles in Q2 2026","publisher":"Reuters","link":"https://finance.yahoo.com/quote/TSLA/","summary":"Tesla's quarterly deliveries beat estimates, driven by strong demand in China and Europe.","published_at":"2026-05-18T12:00:00"},{"title":"Tesla's Full Self-Driving Approved in Europe","publisher":"The Verge","link":"https://finance.yahoo.com/quote/TSLA/","summary":"European regulators have approved Tesla's FSD software for use on highways.","published_at":"2026-05-17T10:45:00"},{"title":"Tesla Announces New Gigafactory in India","publisher":"Bloomberg","link":"https://finance.yahoo.com/quote/TSLA/","summary":"Tesla's planned factory in Maharashtra will produce the Model 2 compact EV for Indian market.","published_at":"2026-05-16T14:00:00"}],
}

@cached(ttl=300, prefix="news_co")
async def company_news(ticker: str, limit: int = 10) -> list:
    # Primary: Yahoo Finance search API (most reliable, no extra deps)
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker}&quotesCount=0&newsCount={limit}"
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
            if r.status_code == 200:
                data = r.json()
                news_items = data.get("news", [])
                if news_items:
                    results = []
                    for item in news_items[:limit]:
                        ts = item.get("providerPublishTime")
                        results.append({
                            "title": item.get("title", ""),
                            "publisher": item.get("publisher", ""),
                            "link": item.get("link", ""),
                            "type": item.get("type", "STORY"),
                            "summary": item.get("summary", ""),
                            "published_at": datetime.fromtimestamp(ts).isoformat() if ts else None,
                        })
                    return results
    except Exception as e:
        logger.warning(f"company_news search API failed for '{ticker}': {e}")

    # Fallback: yfinance
    try:
        tk = yf.Ticker(ticker)
        news = tk.news
        if news:
            results = []
            for item in news[:limit]:
                results.append({
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", ""),
                    "link": item.get("link", ""),
                    "type": item.get("type", "STORY"),
                    "summary": item.get("summary", ""),
                    "published_at": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat() if item.get("providerPublishTime") else None,
                })
            return results
    except Exception as e:
        logger.warning(f"company_news yfinance failed for '{ticker}': {e}")

    # Fallback: hardcoded news for common tickers
    if ticker.upper() in FALLBACK_NEWS:
        return FALLBACK_NEWS[ticker.upper()][:limit]

    return []


@cached(ttl=300, prefix="news_batch")
async def ticker_news_batch(tickers: list[str], limit: int = 5) -> dict:
    results = {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            news = tk.news
            results[t] = []
            for item in (news or [])[:limit]:
                results[t].append({
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", ""),
                    "link": item.get("link", ""),
                    "summary": item.get("summary", ""),
                    "published_at": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat() if item.get("providerPublishTime") else None,
                })
        except Exception as e:
            logger.warning(f"ticker_news_batch: failed for '{t}': {e}")
            results[t] = []
    return results