from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import news as news_service

router = APIRouter()


@router.get("/market")
async def market_news(ticker: str = "", limit: int = 10):
    return await news_service.yahoo_finance_news(ticker, limit)


@router.get("/company/{ticker}")
async def company_news(ticker: str, limit: int = 10):
    return await news_service.company_news(ticker, limit)


@router.get("/batch")
async def batch_news(tickers: str = Query("AAPL,MSFT,GOOGL,AMZN,TSLA", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100), limit: int = Query(5, ge=1, le=50)):
    t_list = [t.strip() for t in tickers.split(",")]
    return await news_service.ticker_news_batch(t_list, limit)
