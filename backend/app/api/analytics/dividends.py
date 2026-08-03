from fastapi import APIRouter, Depends, Query
from typing import Optional
import logging
from datetime import datetime

from app.middleware.auth import get_current_user
from app.services.analytics._yf import get_info as yf_info

router = APIRouter(prefix="/dividends", tags=["Dividends"])
logger = logging.getLogger(__name__)


@router.get("/calendar")
async def api_dividend_calendar(
    tickers: str = Query("AAPL,MSFT,JNJ,PG,KO,XOM", description="Comma-separated tickers"),
    user: dict = Depends(get_current_user),
):
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    results = []
    total_income = 0.0

    for ticker in ticker_list:
        try:
            info = await yf_info(ticker) or {}
        except Exception:
            info = {}

        div_yield = float(info.get("dividendYield") or 0)
        div_rate = float(info.get("dividendRate") or 0)
        price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 100)

        annual_income = div_rate if div_rate > 0 else price * div_yield
        total_income += annual_income

        results.append({
            "ticker": ticker,
            "price": round(price, 2),
            "dividend_yield_pct": round(div_yield * 100, 2),
            "annual_dividend": round(div_rate, 2),
            "ex_date": info.get("exDividendDate"),
            "estimated_quarterly": round(annual_income / 4, 2),
        })

    return {
        "tickers": len(results),
        "total_annual_income": round(total_income, 2),
        "total_quarterly_income": round(total_income / 4, 2),
        "monthly_income": round(total_income / 12, 2),
        "holdings": results,
        "date": datetime.now().isoformat(),
    }


@router.get("/{ticker}")
async def api_dividend_info(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    info = {}
    try:
        info = await yf_info(ticker) or {}
    except Exception:
        pass

    return {
        "ticker": ticker.upper(),
        "dividend_yield": round(float(info.get("dividendYield") or 0) * 100, 2),
        "dividend_rate": round(float(info.get("dividendRate") or 0), 2),
        "payout_ratio": round(float(info.get("payoutRatio") or 0) * 100, 1),
        "ex_dividend_date": info.get("exDividendDate"),
        "last_dividend_date": info.get("lastDividendDate"),
        "five_year_avg_yield": round(float(info.get("fiveYearAvgDividendYield") or 0) * 100, 2),
        "trailing_annual_yield": round(float(info.get("trailingAnnualDividendYield") or 0) * 100, 2),
    }
