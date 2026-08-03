from fastapi import APIRouter, Query
from app.services.analytics import sentiment as sentiment_service

router = APIRouter()

TICKER_PATTERN = r"^[A-Za-z0-9]{1,10}$"


@router.get("/sentiment")
async def ticker_sentiment(
    ticker: str = Query("AAPL", pattern=TICKER_PATTERN, max_length=10),
    days: int = Query(7, ge=1, le=365),
):
    return await sentiment_service.analyze_ticker_sentiment(ticker.upper(), days)


@router.get("/sentiment/market")
async def market_sentiment(
    days: int = Query(1, ge=1, le=30),
):
    return await sentiment_service.analyze_market_sentiment(days)
