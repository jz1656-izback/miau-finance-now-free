from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import fundamentals as fundamentals_service
from app.services.data_sources import sec_edgar
from app.services.data_sources import insider

router = APIRouter()


@router.get("/{ticker}")
async def company_overview(ticker: str):
    return await fundamentals_service.company_financials(ticker)


@router.get("/{ticker}/earnings")
async def earnings(ticker: str):
    return await fundamentals_service.earnings_calendar(ticker)


@router.get("/{ticker}/filings")
async def sec_filings(
    ticker: str,
    filing_types: Optional[str] = Query(None, description="Comma-separated filing types (10-K,10-Q,8-K)"),
    limit: int = Query(20, ge=1, le=100),
):
    types_list = [t.strip() for t in filing_types.split(",")] if filing_types else None
    return await sec_edgar.get_filings(ticker, filing_types=types_list, limit=limit)


@router.get("/{ticker}/insider-trades")
async def insider_trades(
    ticker: str,
    limit: int = Query(50, ge=1, le=200),
):
    return await insider.get_insider_trades(ticker, limit=limit)
