"""ESG data source — fetches ESG scores from Yahoo Finance."""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

YF_ESG_URL = "https://query2.finance.yahoo.com/v1/finance/esgChart"


async def fetch_esg_score(ticker: str) -> Optional[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{YF_ESG_URL}/{ticker}")
            if resp.status_code == 200:
                data = resp.json()
                esg = data.get("esgChart", {}).get("result", [{}])[0] if data.get("esgChart") else {}
                if esg.get("totalEsg"):
                    return {
                        "ticker": ticker.upper(),
                        "total_score": esg["totalEsg"].get("raw"),
                        "environmental_score": esg.get("environmentalScore", {}).get("raw"),
                        "social_score": esg.get("socialScore", {}).get("raw"),
                        "governance_score": esg.get("governanceScore", {}).get("raw"),
                        "percentile": esg.get("percentile", {}).get("raw"),
                        "rating": esg.get("rating"),
                    }
    except Exception as e:
        logger.warning("ESG fetch failed for %s: %s", ticker, e)
    return None
