"""Direct Yahoo Finance API access via httpx (no yfinance dependency)."""
import asyncio
import functools
import logging
import random
import time

import httpx
import json
from datetime import datetime
from typing import Any, Callable, Optional

from app.cache_utils import cached

logger = logging.getLogger(__name__)

def retry_with_jitter(
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> Callable:
    """Decorator that retries an async function with exponential backoff + jitter.

    Args:
        max_retries: Maximum number of retry attempts. Default 3.
        base_delay: Base delay in seconds. Default 1.0.

    Usage:
        @retry_with_jitter(max_retries=3, base_delay=1.0)
        async def fetch_something(url: str) -> dict:
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc = None
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, base_delay)
                        logger.warning(
                            f"Retry {attempt + 1}/{max_retries} for {func.__name__}: {e}. "
                            f"Waiting {delay:.2f}s"
                        )
                        await asyncio.sleep(delay)
            if last_exc is None:
                raise RuntimeError(f"{func.__name__} failed without exception")
            raise last_exc
        return wrapper
    return decorator


YF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def _make_client(timeout: float = 12.0, **kwargs) -> httpx.AsyncClient:
    """Build an httpx client pinned to IPv4.

    Yahoo's AAAA records (2a00:...) sit outside many local IPv6 scopes and
    silently hang, blowing past the connect timeout inside long-running
    server processes. Binding to 0.0.0.0 forces IPv4, which always works.
    """
    transport = httpx.AsyncHTTPTransport(local_address="0.0.0.0")
    return httpx.AsyncClient(timeout=timeout, transport=transport, headers=YF_HEADERS, **kwargs)


@cached(ttl=60, prefix="price")
async def get_price(ticker: str) -> dict:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d"
    async with _make_client() as client:
        r = await client.get(url)
        if r.status_code != 200:
            return {"ticker": ticker, "error": f"HTTP {r.status_code}"}
        data = r.json()
        results = data.get("chart", {}).get("result", [])
        if not results:
            return {"ticker": ticker, "error": "No data"}
        result = results[0]
        meta = result.get("meta", {})
        quotes = result.get("indicators", {}).get("quote", [{}])[0]
        closes = quotes.get("close", [])
        opens = quotes.get("open", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        volumes = quotes.get("volume", [])
        timestamps = result.get("timestamp", [])

        closes = [c for c in closes if c is not None]
        if not closes:
            return {"ticker": ticker, "error": "No price data"}

        price = closes[-1]
        prev = closes[-2] if len(closes) >= 2 else price
        return {
            "ticker": ticker,
            "price": round(price, 4),
            "prev_close": round(prev, 4),
            "change": round(price - prev, 4),
            "change_pct": round((price - prev) / prev * 100, 2),
            "high": round(highs[-1], 4) if highs and highs[-1] else round(price, 4),
            "low": round(lows[-1], 4) if lows and lows[-1] else round(price, 4),
            "volume": int(volumes[-1]) if volumes and volumes[-1] else 0,
            "as_of": datetime.now().isoformat(),
        }


@cached(ttl=3600, prefix="history")
async def get_history(ticker: str, range_str: str = "6mo", interval: str = "1d") -> list:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={range_str}&interval={interval}"
    async with _make_client() as client:
        r = await client.get(url)
        if r.status_code != 200:
            return []
        data = r.json()
        results = data.get("chart", {}).get("result", [])
        if not results:
            return []
        result = results[0]
        quotes = result.get("indicators", {}).get("quote", [{}])[0]
        closes = quotes.get("close", [])
        opens = quotes.get("open", [])
        highs = quotes.get("high", [])
        lows = quotes.get("low", [])
        volumes = quotes.get("volume", [])
        timestamps = result.get("timestamp", [])

        n = len(timestamps)
        records = []
        for i in range(n):
            if i < len(closes) and closes[i] is not None:
                records.append({
                    "date": datetime.fromtimestamp(timestamps[i]).isoformat(),
                    "open": round(opens[i], 4) if i < len(opens) and opens[i] else 0,
                    "high": round(highs[i], 4) if i < len(highs) and highs[i] else 0,
                    "low": round(lows[i], 4) if i < len(lows) and lows[i] else 0,
                    "close": round(closes[i], 4),
                    "volume": int(volumes[i]) if i < len(volumes) and volumes[i] else 0,
                })
        return records


_crumb_lock = asyncio.Lock()
_crumb_state: dict = {}


async def _get_crumb(force: bool = False) -> tuple[str, dict]:
    """Obtain a Yahoo crumb + session cookie (required for quoteSummary since 2025).

    Yahoo now 401s quoteSummary requests without a crumb. The crumb is minted
    per-session: fc.yahoo.com sets the A3 cookie, then /v1/test/getcrumb returns
    the crumb bound to that cookie. We cache both in-memory for 1 hour.

    Returns:
        (crumb, extra_headers) where extra_headers carries the Cookie header.
    """
    global _crumb_state
    now = time.time()
    if not force and _crumb_state and (now - _crumb_state.get("ts", 0)) < 3600:
        return _crumb_state["crumb"], {"Cookie": _crumb_state["cookie"]}
    async with _crumb_lock:
        if not force and _crumb_state and (now - _crumb_state.get("ts", 0)) < 3600:
            return _crumb_state["crumb"], {"Cookie": _crumb_state["cookie"]}
        try:
            async with _make_client(follow_redirects=True) as client:
                await client.get("https://fc.yahoo.com")
                r = await client.get(
                    "https://query1.finance.yahoo.com/v1/test/getcrumb",
                    headers={"Accept": "text/plain"},
                )
                crumb = r.text.strip()
                cookie = "; ".join(f"{c.name}={c.value}" for c in client.cookies.jar)
                if crumb and cookie:
                    _crumb_state = {"crumb": crumb, "cookie": cookie, "ts": now}
                    return crumb, {"Cookie": cookie}
        except Exception as e:
            logger.warning(f"Failed to fetch Yahoo crumb: {e}")
    return "", {}


@cached(ttl=86400, prefix="info")
async def get_info(ticker: str) -> dict:
    crumb, extra_headers = await _get_crumb()
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile%2CfinancialData%2CdefaultKeyStatistics%2CsummaryDetail%2Cprice"
    if crumb:
        url += f"&crumb={crumb}"
    headers = {**YF_HEADERS, **extra_headers}
    async with _make_client() as client:
        r = await client.get(url, headers=headers)
        if r.status_code != 200:
            return {"ticker": ticker, "error": f"HTTP {r.status_code}"}
        try:
            data = r.json()
            results = data.get("quoteSummary", {}).get("result", [])
            if not results:
                return {"ticker": ticker, "error": "Empty result"}
            qs = results[0]
            if not qs:
                return {"ticker": ticker, "error": "Empty result"}
            result = {}
            for module_key in ["assetProfile", "financialData", "defaultKeyStatistics", "summaryDetail", "price"]:
                module = qs.get(module_key, {})
                if module and isinstance(module, dict) and len(module) > 0:
                    result[module_key] = module
            return result if result else {"ticker": ticker, "error": "No modules returned"}
        except Exception as e:
            return {"ticker": ticker, "error": f"Parse error: {str(e)[:100]}"}


async def get_sector_etfs() -> dict:
    sectors = {
        "XLF": "Financials", "XLK": "Technology", "XLE": "Energy",
        "XLV": "Healthcare", "XLI": "Industrials", "XLP": "Consumer Staples",
        "XLY": "Consumer Discretionary", "XLB": "Materials", "XLU": "Utilities",
        "XLRE": "Real Estate",
    }
    gainers, losers = [], []
    for ticker, name in sectors.items():
        try:
            p = await get_price(ticker)
            if "price" in p:
                item = {"ticker": ticker, "name": name, "change_pct": p.get("change_pct", 0), "price": p.get("price", 0)}
                if p.get("change_pct", 0) >= 0:
                    gainers.append(item)
                else:
                    losers.append(item)
        except Exception as e:
            logger.warning(f"Failed to fetch sector ETF {ticker}: {e}")
    gainers.sort(key=lambda x: x["change_pct"], reverse=True)
    losers.sort(key=lambda x: x["change_pct"])
    return {"top_gainers": gainers[:10], "top_losers": losers[:10], "as_of": datetime.now().isoformat()}


_SEMAPHORE = asyncio.Semaphore(5)


async def fetch_prices(tickers: list[str]) -> list[dict]:
    """Fetch prices for multiple tickers concurrently using asyncio.gather.

    Each ticker is fetched independently; errors are captured per ticker
    rather than failing the entire batch.

    Args:
        tickers: List of stock ticker symbols.

    Returns:
        List of price dicts (one per ticker), in the same order as input.
    """
    async def _fetch_one(ticker: str) -> dict:
        try:
            return await get_price(ticker)
        except Exception as e:
            logger.error(f"Failed to fetch price for {ticker}: {e}")
            return {"ticker": ticker, "error": str(e)}

    tasks = [_fetch_one(t) for t in tickers]
    return await asyncio.gather(*tasks)


async def fetch_sector_etfs() -> dict:
    """Fetch sector ETF performance with concurrent requests limited by semaphore.

    Uses asyncio.Semaphore(5) to limit concurrent outbound requests,
    then classifies results into gainers and losers sorted by change_pct.

    Returns:
        Dict with 'top_gainers', 'top_losers', and 'as_of' timestamp.
    """
    sectors = {
        "XLF": "Financials", "XLK": "Technology", "XLE": "Energy",
        "XLV": "Healthcare", "XLI": "Industrials", "XLP": "Consumer Staples",
        "XLY": "Consumer Discretionary", "XLB": "Materials", "XLU": "Utilities",
        "XLRE": "Real Estate",
    }
    gainers, losers = [], []

    async def _fetch(ticker: str, name: str) -> None:
        async with _SEMAPHORE:
            try:
                p = await get_price(ticker)
                if "price" in p:
                    item = {"ticker": ticker, "name": name, "change_pct": p.get("change_pct", 0), "price": p.get("price", 0)}
                    if p.get("change_pct", 0) >= 0:
                        gainers.append(item)
                    else:
                        losers.append(item)
            except Exception as e:
                logger.warning(f"Failed to fetch sector ETF {ticker}: {e}")

    await asyncio.gather(*[_fetch(t, n) for t, n in sectors.items()])
    gainers.sort(key=lambda x: x["change_pct"], reverse=True)
    losers.sort(key=lambda x: x["change_pct"])
    return {"top_gainers": gainers[:10], "top_losers": losers[:10], "as_of": datetime.now().isoformat()}
