"""Green finance API — renewable energy ETFs, green bonds, sustainable funds."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/green", tags=["Green Finance"])

RENEWABLE_ENERGY_ETFS = [
    {"ticker": "ICLN", "name": "iShares Global Clean Energy ETF", "category": "clean_energy", "region": "global", "aum_b": 5.2, "expense_ratio": 0.40, "esg_score_min": 60},
    {"ticker": "TAN", "name": "Invesco Solar ETF", "category": "solar", "region": "global", "aum_b": 2.8, "expense_ratio": 0.67, "esg_score_min": 55},
    {"ticker": "FAN", "name": "First Trust Global Wind Energy ETF", "category": "wind", "region": "global", "aum_b": 1.1, "expense_ratio": 0.60, "esg_score_min": 65},
    {"ticker": "PBW", "name": "Invesco WilderHill Clean Energy ETF", "category": "clean_energy", "region": "US", "aum_b": 1.5, "expense_ratio": 0.61, "esg_score_min": 50},
    {"ticker": "QCLN", "name": "First Trust NASDAQ Clean Edge Green Energy ETF", "category": "clean_energy", "region": "US", "aum_b": 1.3, "expense_ratio": 0.58, "esg_score_min": 55},
    {"ticker": "ACES", "name": "ALPS Clean Energy ETF", "category": "clean_energy", "region": "US", "aum_b": 0.6, "expense_ratio": 0.55, "esg_score_min": 50},
    {"ticker": "RNRG", "name": "Global X Renewable Energy Producers ETF", "category": "clean_energy", "region": "global", "aum_b": 0.4, "expense_ratio": 0.65, "esg_score_min": 60},
    {"ticker": "SMOG", "name": "VanEck Low Carbon Energy ETF", "category": "clean_energy", "region": "global", "aum_b": 0.3, "expense_ratio": 0.61, "esg_score_min": 55},
    {"ticker": "HYDR", "name": "Global X Hydrogen ETF", "category": "hydrogen", "region": "global", "aum_b": 0.2, "expense_ratio": 0.50, "esg_score_min": 50},
    {"ticker": "BATT", "name": "Amplify Lithium & Battery Technology ETF", "category": "battery", "region": "global", "aum_b": 0.8, "expense_ratio": 0.59, "esg_score_min": 45},
    {"ticker": "LIT", "name": "Global X Lithium & Battery Tech ETF", "category": "battery", "region": "global", "aum_b": 3.1, "expense_ratio": 0.75, "esg_score_min": 45},
    {"ticker": "CTEC", "name": "Global X CleanTech ETF", "category": "cleantech", "region": "global", "aum_b": 0.1, "expense_ratio": 0.50, "esg_score_min": 55},
]

GREEN_BONDS = [
    {"isin": "XS1234567890", "name": "EU Green Bond 2026", "issuer": "European Union", "currency": "EUR", "coupon": 2.5, "maturity": "2026-12-15", "rating": "AAA", "use_of_proceeds": "renewable_energy"},
    {"isin": "XS2345678901", "name": "World Bank Green Bond 2028", "issuer": "World Bank", "currency": "USD", "coupon": 3.0, "maturity": "2028-06-30", "rating": "AAA", "use_of_proceeds": "climate_adaptation"},
    {"isin": "XS3456789012", "name": "Apple Green Bond 2029", "issuer": "Apple Inc.", "currency": "USD", "coupon": 2.8, "maturity": "2029-09-15", "rating": "AA+", "use_of_proceeds": "clean_energy"},
    {"isin": "XS4567890123", "name": "Enel Green Bond 2027", "issuer": "Enel SpA", "currency": "EUR", "coupon": 3.5, "maturity": "2027-03-20", "rating": "BBB+", "use_of_proceeds": "renewable_energy"},
    {"isin": "XS5678901234", "name": "Iberdrola Green Bond 2030", "issuer": "Iberdrola SA", "currency": "EUR", "coupon": 3.2, "maturity": "2030-11-01", "rating": "A-", "use_of_proceeds": "wind_energy"},
    {"isin": "XS6789012345", "name": "Toyota Green Bond 2028", "issuer": "Toyota Motor Corp", "currency": "JPY", "coupon": 1.8, "maturity": "2028-04-30", "rating": "AA", "use_of_proceeds": "hybrid_vehicles"},
    {"isin": "XS7890123456", "name": "BNP Paribas Green Bond 2027", "issuer": "BNP Paribas", "currency": "EUR", "coupon": 2.0, "maturity": "2027-08-15", "rating": "A+", "use_of_proceeds": "green_buildings"},
    {"isin": "XS8901234567", "name": "China Green Bond 2029", "issuer": "China Development Bank", "currency": "CNY", "coupon": 3.8, "maturity": "2029-01-20", "rating": "A", "use_of_proceeds": "renewable_energy"},
]

SUSTAINABLE_FUNDS = [
    {"ticker": "ESGU", "name": "iShares ESG Aware MSCI USA ETF", "category": "esg_aware", "region": "US", "aum_b": 12.5, "expense_ratio": 0.15, "esg_score_avg": 75},
    {"ticker": "ESGD", "name": "iShares ESG Aware MSCI EAFE ETF", "category": "esg_aware", "region": "developed_ex_us", "aum_b": 6.8, "expense_ratio": 0.20, "esg_score_avg": 70},
    {"ticker": "ESGE", "name": "iShares ESG Aware MSCI EM ETF", "category": "esg_aware", "region": "emerging", "aum_b": 3.2, "expense_ratio": 0.25, "esg_score_avg": 60},
    {"ticker": "SUSL", "name": "iShares ESG MSCI USA Leaders ETF", "category": "esg_leaders", "region": "US", "aum_b": 2.1, "expense_ratio": 0.10, "esg_score_avg": 85},
    {"ticker": "USXF", "name": "iShares ESG Advanced MSCI USA ETF", "category": "esg_advanced", "region": "US", "aum_b": 1.5, "expense_ratio": 0.10, "esg_score_avg": 90},
    {"ticker": "NZUS", "name": "iShares Net Zero Paris Aligned MSCI USA ETF", "category": "paris_aligned", "region": "US", "aum_b": 0.5, "expense_ratio": 0.10, "esg_score_avg": 88},
    {"ticker": "VOTE", "name": "Engine No. 1 Transform Climate ETF", "category": "climate", "region": "US", "aum_b": 0.3, "expense_ratio": 0.50, "esg_score_avg": 82},
    {"ticker": "ETHO", "name": "Etho Climate Leadership US ETF", "category": "climate", "region": "US", "aum_b": 0.2, "expense_ratio": 0.45, "esg_score_avg": 80},
    {"ticker": "DSI", "name": "iShares MSCI KLD400 Social ETF", "category": "social", "region": "US", "aum_b": 3.5, "expense_ratio": 0.25, "esg_score_avg": 78},
]

CATEGORY_MAP = {
    "clean_energy": "Clean Energy",
    "solar": "Solar Energy",
    "wind": "Wind Energy",
    "hydrogen": "Hydrogen Fuel",
    "battery": "Battery & Storage",
    "cleantech": "Clean Technology",
    "renewable_energy": "Renewable Energy",
    "climate_adaptation": "Climate Adaptation",
    "hybrid_vehicles": "Hybrid & Electric Vehicles",
    "green_buildings": "Green Buildings",
    "esg_aware": "ESG Aware",
    "esg_leaders": "ESG Leaders",
    "esg_advanced": "ESG Advanced",
    "paris_aligned": "Paris Aligned",
    "climate": "Climate Solutions",
    "social": "Social Impact",
}


@router.get("/renewable-energy")
async def list_renewable_energy(
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by region (US, global, developed_ex_us, emerging)"),
    min_esg_score: Optional[int] = Query(None, ge=0, le=100, description="Minimum ESG score"),
):
    results = list(RENEWABLE_ENERGY_ETFS)
    if category:
        results = [e for e in results if e["category"] == category]
    if region:
        results = [e for e in results if e["region"] == region]
    if min_esg_score is not None:
        results = [e for e in results if e["esg_score_min"] >= min_esg_score]
    return {
        "count": len(results),
        "results": results,
        "categories": {k: v for k, v in CATEGORY_MAP.items() if any(e["category"] == k for e in RENEWABLE_ENERGY_ETFS)},
    }


@router.get("/bonds")
async def list_green_bonds(
    currency: Optional[str] = Query(None, description="Filter by currency (USD, EUR, JPY, CNY)"),
    min_rating: Optional[str] = Query(None, description="Minimum rating (e.g. A, BBB)"),
    use_of_proceeds: Optional[str] = Query(None, description="Filter by use of proceeds category"),
):
    results = list(GREEN_BONDS)
    if currency:
        results = [b for b in results if b["currency"] == currency.upper()]
    if min_rating:
        rating_order = {"AAA": 0, "AA+": 1, "AA": 2, "AA-": 3, "A+": 4, "A": 5, "A-": 6, "BBB+": 7, "BBB": 8}
        min_val = rating_order.get(min_rating.upper(), 99)
        results = [b for b in results if rating_order.get(b["rating"], 99) <= min_val]
    if use_of_proceeds:
        results = [b for b in results if b["use_of_proceeds"] == use_of_proceeds]
    return {"count": len(results), "results": results, "total_issuers": len(set(b["issuer"] for b in results))}


@router.get("/funds")
async def list_sustainable_funds(
    category: Optional[str] = Query(None, description="Filter by category"),
    region: Optional[str] = Query(None, description="Filter by region"),
    min_esg_score: Optional[int] = Query(None, ge=0, le=100, description="Minimum average ESG score"),
):
    results = list(SUSTAINABLE_FUNDS)
    if category:
        results = [f for f in results if f["category"] == category]
    if region:
        results = [f for f in results if f["region"] == region]
    if min_esg_score is not None:
        results = [f for f in results if f["esg_score_avg"] >= min_esg_score]
    return {"count": len(results), "results": results}


@router.get("/overview")
async def green_finance_overview():
    return {
        "renewable_energy_etfs": len(RENEWABLE_ENERGY_ETFS),
        "green_bonds": len(GREEN_BONDS),
        "sustainable_funds": len(SUSTAINABLE_FUNDS),
        "total_aum_etfs_b": round(sum(e["aum_b"] for e in RENEWABLE_ENERGY_ETFS), 1),
        "total_aum_funds_b": round(sum(f["aum_b"] for f in SUSTAINABLE_FUNDS), 1),
        "categories_available": list(CATEGORY_MAP.values()),
    }
