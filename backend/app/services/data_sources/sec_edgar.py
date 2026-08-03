import asyncio
import logging
import httpx
import random
from datetime import datetime
from typing import Optional

from app.cache_utils import cached

logger = logging.getLogger(__name__)

CIK_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{}.json"
USER_AGENT = "Miau Finance Research miau@miau.finance"

SEC_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

_last_request_time = 0.0


async def _rate_limit():
    global _last_request_time
    now = asyncio.get_event_loop().time()
    elapsed = now - _last_request_time
    if elapsed < 0.1:
        await asyncio.sleep(0.1 - elapsed)
    _last_request_time = asyncio.get_event_loop().time()


async def _fetch_with_retry(
    client: httpx.AsyncClient, url: str, max_retries: int = 3
) -> Optional[dict]:
    for attempt in range(max_retries):
        try:
            await _rate_limit()
            r = await client.get(url, headers=SEC_HEADERS, timeout=15)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                wait = 2 ** attempt
                await asyncio.sleep(wait)
                continue
            return None
        except (httpx.TimeoutException, httpx.RequestError):
            if attempt == max_retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)
    return None


async def _get_cik(ticker: str) -> Optional[str]:
    async with httpx.AsyncClient(timeout=15) as client:
        await _rate_limit()
        try:
            r = await client.get(CIK_URL, headers=SEC_HEADERS, timeout=15)
            if r.status_code != 200:
                return None
            mapping = r.json()
            ticker_upper = ticker.upper()
            for item in mapping.values():
                if item.get("ticker") == ticker_upper:
                    cik = str(item["cik_str"])
                    return cik.zfill(10)
            return None
        except Exception as e:
            logger.debug(f"SEC EDGAR CIK lookup failed for {ticker}: {e}")
            return None


def _generate_mock_filings(ticker: str, filing_types: list[str], limit: int) -> list[dict]:
    """Generate mock SEC filings when the API is unavailable."""
    mock_filings = []
    base_date = datetime.now()
    for i in range(min(limit, 20)):
        form = filing_types[i % len(filing_types)]
        filing_date = base_date.replace(year=base_date.year - (i // 4), month=((base_date.month - i - 1) % 12) + 1)
        mock_filings.append({
            "filing_type": form,
            "company_name": f"{ticker.upper()} Corp",
            "filing_date": filing_date.strftime("%Y-%m-%d"),
            "description": f"{form} filing for {ticker.upper()} Corp",
            "filing_url": f"https://www.sec.gov/Archives/edgar/data/0000000000/0000000000-25-000001/{form.lower()}.htm",
        })
    return mock_filings


@cached(ttl=3600, prefix="filings")
async def get_filings(
    ticker: str, filing_types: Optional[list[str]] = None, limit: int = 20
) -> dict:
    if filing_types is None:
        filing_types = ["10-K", "10-Q", "8-K"]

    cik = await _get_cik(ticker)
    if not cik:
        # Return mock data when CIK lookup fails (API unavailable or unknown ticker)
        return {
            "ticker": ticker,
            "company_name": f"{ticker.upper()} Corp",
            "filings": _generate_mock_filings(ticker, filing_types, limit),
            "as_of": datetime.now().isoformat(),
            "source": "SEC EDGAR (mock data)",
            "note": "CIK not found or SEC API unavailable. Returning mock filings.",
        }

    async with httpx.AsyncClient(timeout=15) as client:
        data = await _fetch_with_retry(client, SUBMISSIONS_URL.format(cik))
        if not data:
            return {
                "ticker": ticker,
                "company_name": f"{ticker.upper()} Corp",
                "filings": _generate_mock_filings(ticker, filing_types, limit),
                "as_of": datetime.now().isoformat(),
                "source": "SEC EDGAR (mock data)",
                "note": "SEC API unavailable. Returning mock filings.",
            }

    company_name = data.get("name", ticker)
    recent_filings = data.get("filings", {}).get("recent", {})
    if not recent_filings:
        return {
            "ticker": ticker,
            "company_name": company_name,
            "filings": _generate_mock_filings(ticker, filing_types, limit),
            "as_of": datetime.now().isoformat(),
            "source": "SEC EDGAR (mock data)",
            "note": "No filings found. Returning mock filings.",
        }

    forms = recent_filings.get("form", [])
    dates = recent_filings.get("filingDate", [])
    descriptions = recent_filings.get("primaryDocument", [])
    accession_numbers = recent_filings.get("accessionNumber", [])

    results = []
    for i, form in enumerate(forms):
        if form in filing_types:
            acc_num = accession_numbers[i] if i < len(accession_numbers) else ""
            doc = descriptions[i] if i < len(descriptions) else ""
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_num.replace('-', '')}/{doc}"
            results.append({
                "filing_type": form,
                "company_name": company_name,
                "filing_date": dates[i] if i < len(dates) else "",
                "description": f"{form} filing for {company_name}",
                "filing_url": filing_url,
            })
            if len(results) >= limit:
                break

    return {
        "ticker": ticker,
        "company_name": company_name,
        "filings": results,
        "as_of": datetime.now().isoformat(),
        "source": "SEC EDGAR",
    }
