import logging
import httpx
from typing import Optional, List, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class FREDProvider:
    """Fetch macro data from FRED API"""
    BASE_URL = "https://api.stlouisfed.org/fred"

    @classmethod
    async def get_series(cls, series_id: str) -> List[Dict]:
        if not settings.fred_api_key:
            return []
        
        url = f"{cls.BASE_URL}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": settings.fred_api_key,
            "file_type": "json"
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json().get("observations", [])
            logger.error(f"FRED API error for {series_id}: {resp.status_code}")
            return []

class SentimentProvider:
    """Aggregator for sentiment data from NewsAPI and Alpha Vantage"""
    
    @classmethod
    async def get_sentiment(cls, ticker: str) -> Dict[str, Any]:
        results = {"news_sentiment": [], "market_sentiment": {}}
        
        # 1. NewsAPI Sentiment (Simplified: count headlines)
        if settings.news_api_key:
            async with httpx.AsyncClient(timeout=10) as client:
                url = "https://newsapi.org/v2/everything"
                params = {"q": ticker, "apiKey": settings.news_api_key, "pageSize": 5}
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    results["news_sentiment"] = resp.json().get("articles", [])
        
        # 2. Alpha Vantage Sentiment
        if settings.alpha_vantage_api_key:
            async with httpx.AsyncClient(timeout=10) as client:
                url = "https://www.alphavantage.co/query"
                params = {
                    "function": "NEWS_SENTIMENT",
                    "ticker": ticker,
                    "apikey": settings.alpha_vantage_api_key
                }
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    results["market_sentiment"] = resp.json()
        
        return results


class AlphaVantageProvider:
    """Technical indicators, sector performance, FX from Alpha Vantage (free tier: 25 req/day)."""

    BASE = "https://www.alphavantage.co/query"

    INDICATORS = {
        "SMA": "simple moving average", "EMA": "exponential moving average",
        "WMA": "weighted moving average", "DEMA": "double exponential moving average",
        "TEMA": "triple exponential moving average", "TRIMA": "triangular moving average",
        "KAMA": "Kaufman adaptive moving average", "MAMA": "MESA adaptive moving average",
        "T3": "T3 moving average", "RSI": "relative strength index",
        "MACD": "MACD", "ADX": "average directional movement index",
        "ADXR": "average directional movement index rating",
        "APO": "absolute price oscillator", "PPO": "percentage price oscillator",
        "MOM": "momentum", "ROC": "rate of change", "ROCR": "rate of change ratio",
        "AROON": "aroon", "AROONOSC": "aroon oscillator",
        "MFI": "money flow index", "TRIX": "triple exponential average",
        "ULTOSC": "ultimate oscillator", "DX": "directional movement index",
        "MINUS_DI": "minus directional indicator", "PLUS_DI": "plus directional indicator",
        "MINUS_DM": "minus directional movement", "PLUS_DM": "plus directional movement",
        "BBANDS": "bollinger bands", "MIDPOINT": "midpoint", "MIDPRICE": "midprice",
        "SAR": "parabolic SAR", "TRANGE": "true range", "ATR": "average true range",
        "NATR": "normalized average true range", "AD": "chaikin A/D line",
        "ADOSC": "chaikin A/D oscillator", "OBV": "on balance volume",
        "HT_TRENDLINE": "Hilbert dominant cycle", "HT_SINE": "Hilbert sine wave",
        "HT_TRENDMODE": "Hilbert trend mode", "HT_PHASOR": "Hilbert phasor",
        "HT_DCPERIOD": "Hilbert dominant cycle period", "HT_DCPHASE": "Hilbert phase",
        "STOCH": "stochastic oscillator", "STOCHF": "stochastic fast",
        "STOCHRSI": "stochastic RSI", "WILLR": "williams %R",
    }

    SECTOR_INDICATORS = [
        "Real Estate", "Financials", "Healthcare", "Technology",
        "Consumer Discretionary", "Consumer Staples", "Energy",
        "Industrials", "Materials", "Utilities", "Communication Services",
    ]

    @classmethod
    async def fetch_technical(cls, ticker: str, indicator: str = "RSI", interval: str = "daily", time_period: int = 14, series_type: str = "close") -> dict:
        """Fetch a single technical indicator for a ticker."""
        if not settings.alpha_vantage_api_key:
            return {"error": "ALPHA_VANTAGE_API_KEY not configured", "available_indicators": list(cls.INDICATORS.keys())}
        indicator = indicator.upper()
        if indicator not in cls.INDICATORS:
            return {"error": f"Unknown indicator '{indicator}'", "available_indicators": list(cls.INDICATORS.keys())}
        params = {"function": indicator, "symbol": ticker.upper(), "interval": interval, "apikey": settings.alpha_vantage_api_key}
        if indicator in ("SMA", "EMA", "WMA", "DEMA", "TEMA", "TRIMA", "KAMA", "MAMA", "T3", "RSI", "STOCHRSI"):
            params["time_period"] = time_period
            params["series_type"] = series_type
        if indicator in ("BBANDS",):
            params["time_period"] = time_period
            params["series_type"] = series_type
            params["nbdevup"] = 2
            params["nbdevdn"] = 2
        if indicator in ("STOCH", "STOCHF"):
            params["fastkperiod"] = time_period
            params["slowkperiod"] = 3
            params["slowdperiod"] = 3
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(cls.BASE, params=params)
                if r.status_code != 200:
                    return {"error": f"Alpha Vantage returned {r.status_code}"}
                data = r.json()
                if "Technical Analysis" in data:
                    return {"ticker": ticker.upper(), "indicator": indicator, "interval": interval, "data": data["Technical Analysis"]}
                if "Error Message" in data:
                    return {"error": data["Error Message"]}
                return data
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    async def fetch_sector_performance(cls) -> list[dict]:
        """Sector performance (real-time) — free endpoint, no key needed for basic."""
        if not settings.alpha_vantage_api_key:
            return [{"sector": s, "performance_pct": 0} for s in cls.SECTOR_INDICATORS]
        params = {"function": "SECTOR", "apikey": settings.alpha_vantage_api_key}
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(cls.BASE, params=params)
                if r.status_code != 200:
                    return [{"sector": s, "performance_pct": 0} for s in cls.SECTOR_INDICATORS]
                data = r.json()
                today = data.get("Rank A: Real-Time Performance", {})
                return [{"sector": s.replace("_", " "), "performance_pct": float(today.get(s, 0))} for s in today]
        except Exception:
            return [{"sector": s, "performance_pct": 0} for s in cls.SECTOR_INDICATORS]

    @classmethod
    async def fetch_fx(cls, from_currency: str = "EUR", to_currency: str = "USD") -> dict:
        """Real-time FX rate."""
        if not settings.alpha_vantage_api_key:
            return {"from": from_currency, "to": to_currency, "rate": 0}
        params = {"function": "CURRENCY_EXCHANGE_RATE", "from_currency": from_currency.upper(), "to_currency": to_currency.upper(), "apikey": settings.alpha_vantage_api_key}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(cls.BASE, params=params)
                if r.status_code != 200:
                    return {"from": from_currency, "to": to_currency, "rate": 0}
                data = r.json().get("Realtime Currency Exchange Rate", {})
                return {"from": from_currency.upper(), "to": to_currency.upper(), "rate": float(data.get("5. Exchange Rate", 0)), "bid": float(data.get("8. Bid Price", 0)), "ask": float(data.get("9. Ask Price", 0)), "updated": data.get("6. Last Refreshed", "")}
        except Exception:
            return {"from": from_currency, "to": to_currency, "rate": 0}

    @classmethod
    async def list_indicators(cls) -> dict:
        """List all available technical indicators."""
        return {"count": len(cls.INDICATORS), "indicators": list(cls.INDICATORS.keys()), "descriptions": cls.INDICATORS}
