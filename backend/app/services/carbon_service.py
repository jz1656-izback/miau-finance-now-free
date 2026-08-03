"""Carbon footprint service — intensity calculation, portfolio footprint, benchmark comparison."""

import logging
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

INDUSTRY_BENCHMARKS: dict[str, dict[str, float]] = {
    "Technology": {"intensity": 15.0, "scope1": 5.0, "scope2": 8.0, "scope3": 80.0},
    "Energy": {"intensity": 250.0, "scope1": 40.0, "scope2": 25.0, "scope3": 35.0},
    "Healthcare": {"intensity": 20.0, "scope1": 8.0, "scope2": 10.0, "scope3": 82.0},
    "Financial": {"intensity": 5.0, "scope1": 2.0, "scope2": 3.0, "scope3": 95.0},
    "Consumer Cyclical": {"intensity": 45.0, "scope1": 12.0, "scope2": 18.0, "scope3": 70.0},
    "Consumer Defensive": {"intensity": 35.0, "scope1": 10.0, "scope2": 15.0, "scope3": 75.0},
    "Industrials": {"intensity": 85.0, "scope1": 20.0, "scope2": 25.0, "scope3": 55.0},
    "Basic Materials": {"intensity": 180.0, "scope1": 30.0, "scope2": 30.0, "scope3": 40.0},
    "Real Estate": {"intensity": 25.0, "scope1": 8.0, "scope2": 12.0, "scope3": 80.0},
    "Utilities": {"intensity": 300.0, "scope1": 45.0, "scope2": 35.0, "scope3": 20.0},
    "Communication": {"intensity": 10.0, "scope1": 3.0, "scope2": 5.0, "scope3": 92.0},
}

PARIS_ALIGNMENT_REDUCTION_PCT = 7.6


class CarbonService:

    @staticmethod
    async def get_carbon_data(db: AsyncSession, ticker: str) -> Optional[dict]:
        result = await db.execute(
            text("""
                SELECT ticker, scope1_tons, scope2_tons, scope3_tons, total_tons,
                       intensity_per_revenue, year, source, retrieved_at
                FROM carbon_footprints
                WHERE ticker = :ticker
                ORDER BY year DESC
                LIMIT 1
            """),
            {"ticker": ticker.upper()},
        )
        row = result.mappings().first()
        if not row:
            return None
        return dict(row)

    @staticmethod
    async def get_carbon_history(db: AsyncSession, ticker: str, limit: int = 5) -> list[dict]:
        result = await db.execute(
            text("""
                SELECT ticker, scope1_tons, scope2_tons, scope3_tons, total_tons,
                       intensity_per_revenue, year
                FROM carbon_footprints
                WHERE ticker = :ticker
                ORDER BY year DESC
                LIMIT :limit
            """),
            {"ticker": ticker.upper(), "limit": limit},
        )
        return [dict(r) for r in result.mappings().all()]

    @staticmethod
    async def calculate_intensity(db: AsyncSession, ticker: str) -> Optional[dict]:
        data = await CarbonService.get_carbon_data(db, ticker)
        if not data:
            return None

        industry = await CarbonService._get_industry(db, ticker)
        benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["Technology"])

        intensity = float(data.get("intensity_per_revenue", 0))
        historical = await CarbonService.get_carbon_history(db, ticker, 3)
        yoy_change = None
        if len(historical) >= 2:
            older = float(historical[-1].get("intensity_per_revenue", 0))
            current = float(historical[0].get("intensity_per_revenue", 0))
            if older > 0:
                yoy_change = ((current - older) / older) * 100

        return {
            "ticker": ticker.upper(),
            "industry": industry,
            "emissions": {
                "scope1_tons": float(data.get("scope1_tons", 0)),
                "scope2_tons": float(data.get("scope2_tons", 0)),
                "scope3_tons": float(data.get("scope3_tons", 0)),
                "total_tons": float(data.get("total_tons", 0)),
            },
            "intensity_per_revenue": intensity,
            "industry_benchmark": benchmark["intensity"],
            "intensity_vs_benchmark_pct": ((intensity - benchmark["intensity"]) / benchmark["intensity"] * 100) if benchmark["intensity"] > 0 else 0,
            "yoy_change_pct": yoy_change,
            "year": data.get("year"),
        }

    @staticmethod
    async def portfolio_footprint(db: AsyncSession, portfolio_id: str) -> Optional[dict]:
        positions = await db.execute(
            text("""
                SELECT i.ticker, p.quantity, p.market_value, p.currency
                FROM positions p
                JOIN instruments i ON i.id = p.instrument_id
                WHERE p.portfolio_id = :pid AND p.quantity > 0
            """),
            {"pid": portfolio_id},
        )
        pos_rows = positions.mappings().all()
        if not pos_rows:
            return None

        portfolio_value = sum(float(r["market_value"] or 0) for r in pos_rows)
        total_scope1 = total_scope2 = total_scope3 = 0.0
        ticker_details = []

        for pos in pos_rows:
            ticker = pos["ticker"]
            weight = float(pos["market_value"] or 0) / portfolio_value if portfolio_value > 0 else 0
            carbon = await CarbonService.get_carbon_data(db, ticker)
            if carbon:
                s1 = float(carbon.get("scope1_tons", 0)) * weight
                s2 = float(carbon.get("scope2_tons", 0)) * weight
                s3 = float(carbon.get("scope3_tons", 0)) * weight
                total_scope1 += s1
                total_scope2 += s2
                total_scope3 += s3
                ticker_details.append({
                    "ticker": ticker,
                    "weight_pct": round(weight * 100, 2),
                    "intensity": float(carbon.get("intensity_per_revenue", 0)),
                })

        ticker_details.sort(key=lambda x: x["intensity"], reverse=True)

        return {
            "portfolio_id": portfolio_id,
            "total_emissions_tons": {
                "scope1": round(total_scope1, 2),
                "scope2": round(total_scope2, 2),
                "scope3": round(total_scope3, 2),
                "total": round(total_scope1 + total_scope2 + total_scope3, 2),
            },
            "portfolio_value": round(portfolio_value, 2),
            "largest_emitters": ticker_details[:5],
            "num_holdings_with_data": len(ticker_details),
        }

    @staticmethod
    async def benchmark_comparison(db: AsyncSession, portfolio_id: str) -> Optional[dict]:
        footprint = await CarbonService.portfolio_footprint(db, portfolio_id)
        if not footprint:
            return None

        total_emissions = footprint["total_emissions_tons"]["total"]
        portfolio_value = footprint["portfolio_value"]
        intensity = (total_emissions / portfolio_value * 1_000_000) if portfolio_value > 0 else 0

        spy_benchmark = 85.0
        paris_target = spy_benchmark * (1 - PARIS_ALIGNMENT_REDUCTION_PCT / 100)
        required_reduction = ((intensity - paris_target) / intensity * 100) if intensity > 0 else 0

        return {
            "portfolio_id": portfolio_id,
            "carbon_intensity_per_million": round(intensity, 2),
            "spy_benchmark_intensity": spy_benchmark,
            "vs_spy_pct": round(((intensity - spy_benchmark) / spy_benchmark * 100), 1) if spy_benchmark > 0 else 0,
            "paris_alignment_target": round(paris_target, 2),
            "annual_reduction_needed_pct": round(PARIS_ALIGNMENT_REDUCTION_PCT, 1),
            "reduction_to_meet_target_pct": round(max(0, required_reduction), 1),
        }

    @staticmethod
    async def _get_industry(db: AsyncSession, ticker: str) -> str:
        try:
            result = await db.execute(
                text("SELECT sector FROM instruments WHERE ticker = :ticker"),
                {"ticker": ticker.upper()},
            )
            row = result.mappings().first()
            if row and row["sector"]:
                for known in INDUSTRY_BENCHMARKS:
                    if known.lower() in row["sector"].lower():
                        return known
                if any(w in row["sector"].lower() for w in ["tech", "software", "semi"]):
                    return "Technology"
                if any(w in row["sector"].lower() for w in ["bank", "financ", "insur"]):
                    return "Financial"
                if any(w in row["sector"].lower() for w in ["energy", "oil", "gas"]):
                    return "Energy"
                if any(w in row["sector"].lower() for w in ["health", "pharma", "bio"]):
                    return "Healthcare"
                if any(w in row["sector"].lower() for w in ["industri", "manufact"]):
                    return "Industrials"
                if any(w in row["sector"].lower() for w in ["material", "chemical", "mining"]):
                    return "Basic Materials"
                if any(w in row["sector"].lower() for w in ["util"]):
                    return "Utilities"
                if any(w in row["sector"].lower() for w in ["real", "estate"]):
                    return "Real Estate"
                if any(w in row["sector"].lower() for w in ["consumer", "retail"]):
                    return "Consumer Cyclical"
                if any(w in row["sector"].lower() for w in ["communicat", "media", "telecom"]):
                    return "Communication"
        except Exception:
            pass
        return "Technology"
