from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import market_data
from app.services.analytics import data_sources

router = APIRouter()

TICKER_PATTERN = r"^[A-Za-z0-9]{1,10}$"
COIN_PATTERN = r"^[a-zA-Z0-9_-]{1,30}$"


@router.get("/live")
async def live_prices(
    tickers: str = Query("AAPL,MSFT,GOOGL,AMZN,TSLA,SPY,QQQ", pattern=r"^[A-Za-z0-9,]{1,200}$"),
    live: bool = Query(False, description="Bypass cache and fetch live data"),
):
    t_list = [t.strip().upper() for t in tickers.split(",")]
    return await market_data.fetch_live_prices(t_list, force_live=live)


@router.get("/historical/{ticker}")
async def historical(
    ticker: str,
    period: str = Query("6mo", pattern=r"^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"),
    interval: str = Query("1d", pattern=r"^(1m|2m|5m|15m|30m|60m|90m|1h|1d|5d|1wk|1mo|3mo)$"),
):
    return await market_data.fetch_historical(ticker.upper(), period, interval)


@router.get("/movers")
async def movers():
    return await market_data.get_market_movers()


@router.get("/crypto/historical")
async def crypto_historical(
    coin: str = Query("bitcoin", pattern=COIN_PATTERN, max_length=30),
    days: int = Query(30, ge=1, le=3650),
):
    return await data_sources.coingecko_historical(coin, days)


@router.get("/sectors")
async def sectors():
    return await data_sources.sector_performance()


@router.get("/crypto")
async def crypto(
    coin: str = Query("bitcoin", pattern=COIN_PATTERN, max_length=30),
):
    return await data_sources.coingecko_coin_price(coin)


@router.get("/crypto/top")
async def crypto_top(
    limit: int = Query(20, ge=1, le=250),
):
    return await data_sources.coingecko_top_coins(limit)


@router.get("/crypto/market")
async def crypto_market():
    return await data_sources.coingecko_market()


@router.get("/crypto/fear-greed")
async def fear_greed():
    return await data_sources.bitcoin_fear_greed_index()


@router.get("/forex")
async def forex(
    base: str = Query("USD", pattern=r"^[A-Z]{3}$", max_length=3),
    targets: Optional[str] = Query(None, pattern=r"^[A-Z,]{3,60}$", max_length=60),
):
    t_list = targets.split(",") if targets else None
    return await data_sources.exchange_rate(base.upper(), t_list)


@router.get("/indicators")
async def indicators():
    return await data_sources.us_indicators()
