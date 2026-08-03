from datetime import datetime
from typing import Optional
from app.services.analytics._yf import get_price, get_history, get_sector_etfs
from app.services.analytics import data_sources
from app.services.data_quality import check_price_quality, parallel_fetch, DataQualityError


CHONK_URL = "http://localhost:8765"

async def _chonk_get(tickers: list[str]) -> Optional[dict]:
    """Try to get prices from Miau DatChonk service first."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=3) as client:
            param = ",".join(tickers)
            r = await client.get(f"{CHONK_URL}/prices?tickers={param}")
            if r.status_code == 200:
                data = r.json()
                if data.get("data"):
                    return data
    except Exception:
        pass
    return None

async def fetch_live_prices(tickers: list[str], force_live: bool = False) -> dict:
    from app.services.data.cache import data_cache

    # Miau DatChonk: check chonk service first (unless force_live)
    if not force_live:
        chonk_data = await _chonk_get(tickers)
        if chonk_data and chonk_data.get("data"):
            result = {}
            for t, p in chonk_data["data"].items():
                p["name"] = t
                result[t] = p
            return {"data": result, "as_of": datetime.now().isoformat(), "source": "chonk"}
        
        # Fallback to local in-memory cache
        cached = {}
        misses = []
        for t in tickers:
            entry = data_cache.get("yahoo", "price", t)
            if entry:
                cached[t] = entry
            else:
                misses.append(t)
        if cached and not misses:
            result = {}
            for t, p in cached.items():
                p["name"] = t
                result[t] = p
            return {"data": result, "as_of": datetime.now().isoformat(), "source": "chonk"}
        tickers = misses

    async def fetch_one(t: str) -> tuple[str, dict]:
        p = await get_price(t)
        warning = check_price_quality(p, source=f"yfinance:{t}")
        if warning:
            p["quality_warning"] = warning
        return t, p

    results = await parallel_fetch(tickers, fetch_one, semaphore_limit=5, label="live_prices")
    data = {}
    for t, p in results:
        if "error" in p:
            data[t] = {"ticker": t, "error": p["error"]}
        else:
            p["name"] = t
            data[t] = p
    return {"data": data, "as_of": datetime.now().isoformat()}


async def fetch_historical(ticker: str, period: str = "6mo", interval: str = "1d") -> dict:
    range_map = {"1mo": "1mo", "3mo": "3mo", "6mo": "6mo", "1y": "1y", "2y": "2y", "5y": "5y"}
    yf_range = range_map.get(period, "6mo")
    try:
        records = await get_history(ticker, yf_range, interval)
        if not records:
            return {"ticker": ticker, "error": "No data", "records": []}
        return {"ticker": ticker, "name": ticker, "records": records, "as_of": datetime.now().isoformat()}
    except Exception as e:
        return {"ticker": ticker, "error": str(e)[:100], "records": []}


async def get_market_movers() -> dict:
    try:
        return await get_sector_etfs()
    except Exception as e:
        return {"error": str(e)[:100]}
