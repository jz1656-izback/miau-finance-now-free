from datetime import datetime
from typing import Optional
from app.services.analytics._yf import get_info, get_history


async def company_financials(ticker: str) -> dict:
    info = await get_info(ticker)
    if not info:
        return {"ticker": ticker, "error": "No data"}
    if info.get("error"):
        return {"ticker": ticker, "error": info["error"]}

    ap = info.get("assetProfile", {})
    fd = info.get("financialData", {})
    ks = info.get("defaultKeyStatistics", {})
    sd = info.get("summaryDetail", {})

    result = {
        "ticker": ticker,
        "name": (fd.get("shortName", {}) or {}).get("raw", ticker) if isinstance(fd.get("shortName"), dict) else fd.get("shortName", ticker),
        "sector": ap.get("sector", ""),
        "industry": ap.get("industry", ""),
        "employees": ap.get("fullTimeEmployees", 0),
        "description": (ap.get("longBusinessSummary", "") or "")[:500],
        "website": ap.get("website", ""),
        "as_of": datetime.now().isoformat(),
    }

    def get_val(obj, key):
        if isinstance(obj, dict):
            v = obj.get(key, {})
            if isinstance(v, dict):
                return v.get("raw")
            return v
        return None

    # CEO from assetProfile.companyOfficers (prefer the Chief Executive).
    ceo = ""
    officers = ap.get("companyOfficers") or []
    if isinstance(officers, list):
        for off in officers:
            title = (off.get("title") or "") if isinstance(off, dict) else ""
            if "chief executive" in title.lower() or title.strip().upper() in {"CEO", "PRESIDENT & CEO", "PRESIDENT AND CEO"}:
                ceo = off.get("name", "") if isinstance(off, dict) else ""
                break
        if not ceo and officers and isinstance(officers[0], dict):
            ceo = officers[0].get("name", "")
    result["ceo"] = ceo

    # HQ location as a display string.
    parts = [ap.get("address1", ""), ap.get("city", ""), ap.get("state", ""), ap.get("country", "")]
    result["hq"] = ", ".join(p for p in parts if p)

    total_rev = get_val(fd, "totalRevenue")
    if total_rev is not None:
        result["totalRevenue"] = round(float(total_rev), 2) if isinstance(total_rev, (int, float)) else total_rev

    valuation = {}
    for k in ["marketCap", "enterpriseValue", "trailingPE", "forwardPE", "pegRatio",
              "priceToBook", "priceToSalesTrailing12Months", "enterpriseToRevenue", "enterpriseToEbitda",
              "beta"]:
        v = get_val(ks, k) or get_val(fd, k)
        if v is not None:
            valuation[k] = round(float(v), 4) if isinstance(v, (int, float)) else v
    # Frontend map panels read flat fields; expose a priceToSales alias too.
    if "priceToSalesTrailing12Months" in valuation:
        valuation["priceToSales"] = valuation["priceToSalesTrailing12Months"]
    if valuation:
        result["valuation"] = valuation
        result.update(valuation)

    health = {}
    for k in ["quickRatio", "currentRatio", "debtToEquity", "returnOnEquity", "returnOnAssets",
              "profitMargins", "operatingMargins", "revenueGrowth", "earningsGrowth"]:
        v = get_val(fd, k)
        if v is not None:
            health[k] = round(float(v), 4) if isinstance(v, (int, float)) else v
    if health:
        result["financial_health"] = health
        result.update(health)

    dividends = {}
    for k in ["dividendYield", "dividendRate", "payoutRatio"]:
        v = get_val(sd, k)
        if v is not None:
            dividends[k] = v
    if dividends:
        result["dividends"] = dividends
        result.update(dividends)

    price_targets = {}
    for k in ["targetMeanPrice", "targetHighPrice", "targetLowPrice", "numberOfAnalystOpinions"]:
        v = get_val(fd, k)
        if v is not None:
            price_targets[k] = v
    rec = get_val(fd, "recommendationKey")
    if rec:
        price_targets["recommendation"] = rec
        price_targets["recommendationKey"] = rec
    if price_targets:
        result["price_targets"] = price_targets
        result.update(price_targets)

    return result


async def earnings_calendar(ticker: str) -> dict:
    records = await get_history(ticker, "1y")
    if not records:
        return {"ticker": ticker, "error": "No data"}
    return {"ticker": ticker, "note": "Detailed earnings data available via financial statements", "records": len(records)}
