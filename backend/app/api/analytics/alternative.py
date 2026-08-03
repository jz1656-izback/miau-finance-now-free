from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.analytics.alternative import FREDProvider, SentimentProvider

router = APIRouter(tags=["Analytics - Alternative Data"])

@router.get("/macro/{series_id}")
async def get_macro_data(series_id: str, user: dict = Depends(get_current_user)):
    data = await FREDProvider.get_series(series_id)
    return {"series": series_id, "data": data}

@router.get("/sentiment/{ticker}")
async def get_sentiment(ticker: str, user: dict = Depends(get_current_user)):
    data = await SentimentProvider.get_sentiment(ticker)
    return {"ticker": ticker, "sentiment": data}