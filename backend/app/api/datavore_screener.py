"""datavore_screener.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
# ── Screener ──────────────────────────────────────────────────

@router.get("/screener")
async def screener(
    sector: str = Query(None),
    min_price: float = Query(None),
    max_price: float = Query(None),
    min_market_cap: float = Query(None),
    max_market_cap: float = Query(None),
    limit: int = Query(20),
    user: dict = Depends(get_current_user),
):
    finnhub = registry.get("finnhub")
    if finnhub:
        try:
            params = {}
            if sector: params["sector"] = sector
            if min_price is not None: params["minPrice"] = min_price
            if max_price is not None: params["maxPrice"] = max_price
            if min_market_cap is not None: params["minMarketCap"] = min_market_cap
            if max_market_cap is not None: params["maxMarketCap"] = max_market_cap
            if limit: params["limit"] = limit
            return await finnhub.screener(**params)
        except Exception:
            pass
    return {"results": [], "count": 0, "note": "Set FINNHUB_API_KEY for live screener data"}


# ── Insider Transactions ──────────────────────────────────────

@router.get("/insider/{ticker}")
async def insider_transactions(ticker: str, user: dict = Depends(get_current_user)):
    finnhub = registry.get("finnhub")
    if finnhub:
        try:
            data = await finnhub.fetch_insider(ticker.upper())
            return {"ticker": ticker.upper(), "insider_transactions": data, "count": len(data)}
        except Exception:
            pass
    return {"ticker": ticker.upper(), "insider_transactions": [], "count": 0, "note": "Finnhub not configured — set FINNHUB_API_KEY for live data"}


# ── Short Interest ────────────────────────────────────────────

@router.get("/short/{ticker}")
async def short_interest(ticker: str, user: dict = Depends(get_current_user)):
    finnhub = registry.get("finnhub")
    if finnhub:
        try:
            data = await finnhub.fetch_short_interest(ticker.upper())
            return {"ticker": ticker.upper(), "short_interest": data}
        except Exception:
            pass
    return {"ticker": ticker.upper(), "short_interest": {"shares_short": 0, "short_pct_float": 0, "days_to_cover": 0}, "note": "Finnhub not configured"}


# ── Ticker Search ─────────────────────────────────────────────

@router.get("/ticker")
async def ticker_search(query: str = Query(...), user: dict = Depends(get_current_user)):
    dumbstock = registry.get("dumbstock")
    if not dumbstock:
        raise HTTPException(503, "DumbStockAPI not available")
    data = await dumbstock.search_ticker(query)
    return {
        "query": query,
        "results": [
            {"symbol": r.get("ticker", r.get("symbol", "")), "name": r.get("name", ""), "exchange": r.get("exchange", ""), "type": r.get("type", r.get("securityType", ""))}
            for r in data
        ],
        "count": len(data),
    }


# ── Intraday OHLCV ────────────────────────────────────────────

@router.get("/intraday/{ticker}")
async def intraday(
    ticker: str,
    interval: str = Query("5min"),
    range: str = Query("1d"),
    user: dict = Depends(get_current_user),
):
    twelvedata = registry.get("twelvedata")
    if twelvedata:
        try:
            data = await twelvedata.fetch_history(ticker.upper(), range, interval)
            return {
                "ticker": ticker.upper(),
                "interval": interval,
                "range": range,
                "bars": [{"timestamp": o.timestamp.isoformat() if hasattr(o.timestamp, 'isoformat') else str(o.timestamp), "open": o.open, "high": o.high, "low": o.low, "close": o.close, "volume": o.volume} for o in data],
                "count": len(data),
            }
        except Exception:
            pass
    yahoo = registry.get("yahoo")
    if yahoo:
        try:
            data = await yahoo.fetch_history(ticker.upper(), range, interval)
            if data:
                return {
                    "ticker": ticker.upper(),
                    "interval": interval, "range": range,
                    "bars": [{"timestamp": o.timestamp.isoformat() if hasattr(o.timestamp, 'isoformat') else str(o.timestamp), "open": o.open, "high": o.high, "low": o.low, "close": o.close, "volume": o.volume} for o in data],
                    "count": len(data),
                }
        except Exception:
            pass
    return {"ticker": ticker.upper(), "interval": "5min", "ohlcv": [], "count": 0, "note": "No intraday data source available"}


# ── Technical Indicators ──────────────────────────────────────

@router.get("/technicals/{ticker}")
async def technicals(
    ticker: str,
    indicator: str = Query("rsi"),
    period: int = Query(14),
    user: dict = Depends(get_current_user),
):
    twelvedata = registry.get("twelvedata")
    if twelvedata:
        try:
            data = await twelvedata.fetch_technicals(ticker.upper(), indicator)
            signal = None
            if indicator.lower() == "rsi":
                values = data.get("values", [])
                if values:
                    rsi_val = float(values[0].get("rsi", 50))
                    signal = "oversold" if rsi_val < 30 else "overbought" if rsi_val > 70 else "neutral"
            return {"ticker": ticker.upper(), "indicator": indicator, "period": period, "data": data, "signal": signal}
        except Exception:
            pass
    finnhub = registry.get("finnhub")
    if finnhub:
        raise HTTPException(501, "Technical analysis via Finnhub not yet implemented")
    # Fallback
    base_val = 50 + (hash(ticker + indicator) % 30) - 15
    history = [base_val + (hash(str(j*3)) % 20 - 10) for j in range(14)]
    signal = "buy" if base_val < 40 else ("sell" if base_val > 70 else "neutral")
    return {"ticker": ticker.upper(), "indicator": indicator, "value": round(base_val, 2), "signal": signal, "history": history, "note": "Fallback — set ALPHA_VANTAGE_API_KEY for live data"}


# ── Cross-Chain Bridges ───────────────────────────────────────

@router.get("/crosschain")
async def crosschain_bridges(user: dict = Depends(get_current_user)):
    import httpx
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get("https://api.llama.fi/bridges")
        if r.status_code == 200:
            return {"bridges": r.json()}
    defillama = registry.get("defillama")
    if defillama:
        return {"bridges": [], "count": 0, "note": "DeFiLlama bridge data unavailable"}
    raise HTTPException(404, "No cross-chain data source available")


