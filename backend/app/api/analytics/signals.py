from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import signals as signals_service

router = APIRouter()


@router.get("/generate")
async def generate(ticker: str = "AAPL", period: str = "6mo"):
    return await signals_service.generate_signals(ticker, period)


@router.get("/backtest")
async def backtest(
    ticker: str = "AAPL",
    strategy: str = "sma_cross",
    short_window: int = 20,
    long_window: int = 50,
    initial_capital: float = 100000,
    period: str = "2y",
):
    return await signals_service.backtest_strategy(
        ticker, strategy, short_window, long_window, initial_capital, period,
    )


@router.get("/multi")
async def multi_signal(tickers: str = Query("AAPL,MSFT,GOOGL,AMZN,TSLA", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100), period: str = "3mo"):
    t_list = [t.strip() for t in tickers.split(",")]
    results = {}
    for t in t_list:
        results[t] = await signals_service.generate_signals(t, period)
    return {"signals": results}
