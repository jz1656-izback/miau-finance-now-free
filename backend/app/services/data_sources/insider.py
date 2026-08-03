import asyncio
import httpx
from datetime import datetime
from typing import Optional

from app.services.data_sources.sec_edgar import _get_cik, _rate_limit, _fetch_with_retry, SEC_HEADERS, SUBMISSIONS_URL

FORM_TYPES = {"3", "4", "5"}


async def get_insider_trades(ticker: str, limit: int = 50) -> dict:
    cik = await _get_cik(ticker)
    if not cik:
        return {"ticker": ticker, "error": "CIK not found for ticker", "trades": []}

    async with httpx.AsyncClient(timeout=15) as client:
        data = await _fetch_with_retry(client, SUBMISSIONS_URL.format(cik))
        if not data:
            return {"ticker": ticker, "error": "Could not fetch insider data", "trades": []}

    company_name = data.get("name", ticker)
    recent_filings = data.get("filings", {}).get("recent", {})
    if not recent_filings:
        return {"ticker": ticker, "company_name": company_name, "trades": []}

    forms = recent_filings.get("form", [])
    filing_dates = recent_filings.get("filingDate", [])
    accession_numbers = recent_filings.get("accessionNumber", [])
    primary_docs = recent_filings.get("primaryDocument", [])

    trades = []
    insider_trade_types = {"4": "Buy", "4/A": "Buy"}

    for i, form in enumerate(forms):
        if form in FORM_TYPES:
            acc_num = accession_numbers[i] if i < len(accession_numbers) else ""
            doc = primary_docs[i] if i < len(primary_docs) else ""
            raw_cik = cik.lstrip("0")
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{raw_cik}/{acc_num.replace('-', '')}/{doc}"

            trade = {
                "filing_date": filing_dates[i] if i < len(filing_dates) else "",
                "transaction_date": "",
                "insider_name": "",
                "title": "",
                "transaction_type": "Buy" if form == "4" else "Sell",
                "shares": 0,
                "price": 0.0,
                "value": 0.0,
                "form_type": form,
                "filing_url": filing_url,
            }
            trades.append(trade)

            if len(trades) >= limit:
                break

    return {
        "ticker": ticker,
        "company_name": company_name,
        "trades": trades,
        "as_of": datetime.now().isoformat(),
        "source": "SEC EDGAR",
        "note": "Detailed transaction data (prices, shares) available from parsed HTML/XML filings",
    }
