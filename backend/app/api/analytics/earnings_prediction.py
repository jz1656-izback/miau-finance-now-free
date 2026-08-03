from fastapi import APIRouter, Depends, HTTPException
from app.services.analytics.earnings_prediction import (
    fetch_earnings,
    predict_earnings,
)

router = APIRouter()


@router.get("/{ticker}")
async def get_earnings_prediction(ticker: str):
    ticker = ticker.upper()
    try:
        result = await predict_earnings(ticker)
        if "error" in result:
            raise HTTPException(404, result["error"])
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/{ticker}/history")
async def get_earnings_history(ticker: str):
    ticker = ticker.upper()
    data = await fetch_earnings(ticker)
    if not data:
        raise HTTPException(404, f"No earnings data found for {ticker}")
    return {"ticker": ticker, "earnings": data}
