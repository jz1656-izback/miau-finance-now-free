from fastapi import APIRouter, Query
import httpx
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/treasury-yield")
async def treasury_yield():
    async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
        results = {}
        for name, ticker in [("10y", "^TNX"), ("30y", "^TYX"), ("5y", "^FVX"), ("2y", "^IRX"), ("13w", "^BANK")]:
            try:
                r = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1mo&interval=1d",
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                if r.status_code == 200:
                    data = r.json()
                    meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    price = meta.get("regularMarketPrice")
                    prev = meta.get("previousClose")
                    if price:
                        change = None
                        if prev and float(prev) != 0:
                            change = round(float(price) - float(prev), 2)
                        results[name] = {
                            "yield": round(float(price), 2),
                            "change": change,
                        }
            except (httpx.RequestError, ValueError, KeyError, IndexError) as e:
                logger.warning(f"Failed to fetch treasury yield {name} ({ticker}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error fetching treasury yield {name}: {e}", exc_info=True)
        return results


@router.get("/commodities")
async def commodities():
    async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
        results = {}
        for name, ticker in [("Gold", "GC=F"), ("Silver", "SI=F"), ("Copper", "HG=F"), ("Crude Oil", "CL=F"), ("Natural Gas", "NG=F"), ("Corn", "ZC=F"), ("Wheat", "ZW=F")]:
            try:
                r = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1mo&interval=1d",
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                if r.status_code == 200:
                    data = r.json()
                    meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    price = meta.get("regularMarketPrice")
                    prev = meta.get("previousClose")
                    if price:
                        change_pct = None
                        if prev and float(prev) != 0:
                            change_pct = round((float(price) - float(prev)) / float(prev) * 100, 2)
                        results[name] = {
                            "price": round(float(price), 2),
                            "change_pct": change_pct,
                        }
            except (httpx.RequestError, ValueError, KeyError, IndexError) as e:
                logger.warning(f"Failed to fetch commodity {name} ({ticker}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error fetching commodity {name}: {e}", exc_info=True)
        return results


@router.get("/market-breadth")
async def market_breadth():
    async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
        indices = {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "DOW": "^DJI", "RUSSELL 2000": "^RUT", "VIX": "^VIX"}
        results = {}
        for name, ticker in indices.items():
            try:
                r = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1mo&interval=1d",
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                if r.status_code == 200:
                    meta = r.json().get("chart", {}).get("result", [{}])[0].get("meta", {})
                    price = meta.get("regularMarketPrice")
                    prev = meta.get("previousClose")
                    if price:
                        change_pct = None
                        if prev and float(prev) != 0:
                            change_pct = round((float(price) - float(prev)) / float(prev) * 100, 2)
                        results[name] = {
                            "value": round(float(price), 2),
                            "change_pct": change_pct,
                        }
            except (httpx.RequestError, ValueError, KeyError, IndexError) as e:
                logger.warning(f"Failed to fetch market breadth {name} ({ticker}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error fetching market breadth {name}: {e}", exc_info=True)
        return results


@router.get("/correlation")
async def correlation(tickers: str = Query("AAPL,MSFT,GOOGL,AMZN,TSLA", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100)):
    from app.services.analytics._yf import get_history
    import pandas as pd
    import numpy as np

    t_list = [t.strip() for t in tickers.split(",")]
    prices = {}
    for t in t_list:
        records = await get_history(t, "1y")
        if records:
            prices[t] = [r["close"] for r in records if r.get("close")]

    if len(prices) < 2:
        return {"error": "Need at least 2 tickers"}

    df = pd.DataFrame(prices).pct_change().dropna()
    corr = df.corr().round(4)
    return {
        "tickers": t_list,
        "correlation_matrix": corr.to_dict(),
        "as_of": datetime.now().isoformat(),
    }


@router.get("/gainers-losers")
async def gainers_losers():
    from app.services.analytics import market_data
    return await market_data.get_market_movers()
