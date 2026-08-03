"""ESG scoring service — fetch, cache, and compute ESG scores."""

import logging
from datetime import date
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import EsgScore
from app.services.analytics._yf import get_info as yf_info

logger = logging.getLogger(__name__)


async def fetch_esg_score(ticker: str, db: AsyncSession) -> dict[str, Any]:
    """Return ESG score for a ticker. Checks DB cache first, falls back to live fetch."""
    stmt = select(EsgScore).where(EsgScore.ticker == ticker.upper()).order_by(EsgScore.retrieved_at.desc()).limit(1)
    result = await db.execute(stmt)
    cached = result.scalars().first()
    if cached:
        return _row_to_dict(cached)

    score = await _fetch_from_provider(ticker)
    if score.get("total_score") is not None:
        await _save_score(ticker, score, db)
    return score


async def get_portfolio_esg(portfolio_id: str, db: AsyncSession) -> dict[str, Any]:
    """Compute weighted ESG score for an entire portfolio."""
    positions = await db.execute(
        text("""
            SELECT i.ticker, p.quantity, p.market_value
            FROM positions p
            JOIN instruments i ON i.id = p.instrument_id
            WHERE p.portfolio_id = :pid AND p.quantity > 0
        """),
        {"pid": portfolio_id},
    )
    rows = positions.mappings().all()
    if not rows:
        return {"portfolio_id": portfolio_id, "error": "No positions found", "weighted_score": None}

    total_value = sum(float(r["market_value"]) for r in rows)
    if total_value <= 0:
        return {"portfolio_id": portfolio_id, "error": "Portfolio value is zero", "weighted_score": None}

    weighted = Decimal("0.0")
    esg_scores = []
    for r in rows:
        ticker = r["ticker"]
        weight = float(r["market_value"]) / total_value
        score = await fetch_esg_score(ticker, db)
        ts = score.get("total_score")
        if ts is not None:
            weighted += Decimal(str(ts)) * Decimal(str(weight))
            esg_scores.append({"ticker": ticker, "total_score": ts, "weight_pct": round(weight * 100, 2)})

    return {
        "portfolio_id": portfolio_id,
        "weighted_score": round(float(weighted), 2) if esg_scores else None,
        "holdings_scored": len(esg_scores),
        "holdings_total": len(rows),
        "scores": esg_scores,
    }


async def screen_tickers(
    db: AsyncSession,
    min_total: Optional[float] = None,
    max_controversy: Optional[float] = None,
    min_environmental: Optional[float] = None,
    min_social: Optional[float] = None,
    min_governance: Optional[float] = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Screen tickers by ESG criteria. Returns latest score per ticker."""
    conditions = []
    if min_total is not None:
        conditions.append(f"total_score >= {min_total}")
    if max_controversy is not None:
        conditions.append(f"controversy_score <= {max_controversy}")
    if min_environmental is not None:
        conditions.append(f"environmental_score >= {min_environmental}")
    if min_social is not None:
        conditions.append(f"social_score >= {min_social}")
    if min_governance is not None:
        conditions.append(f"governance_score >= {min_governance}")

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    rows = await db.execute(
        text(f"""
            SELECT DISTINCT ON (ticker) ticker, total_score, environmental_score,
                   social_score, governance_score, controversy_score, rating
            FROM esg_scores
            {where}
            ORDER BY ticker, retrieved_at DESC
            LIMIT :limit
        """),
        {"limit": limit},
    )
    return [dict(r) for r in rows.mappings().all()]


def _row_to_dict(score: EsgScore) -> dict[str, Any]:
    return {
        "ticker": score.ticker,
        "total_score": float(score.total_score) if score.total_score else None,
        "environmental_score": float(score.environmental_score) if score.environmental_score else None,
        "social_score": float(score.social_score) if score.social_score else None,
        "governance_score": float(score.governance_score) if score.governance_score else None,
        "controversy_score": float(score.controversy_score) if score.controversy_score else None,
        "percentile": float(score.percentile) if score.percentile else None,
        "rating": score.rating,
        "source": score.source,
        "retrieved_at": str(score.retrieved_at) if score.retrieved_at else None,
    }


async def _fetch_from_provider(ticker: str) -> dict[str, Any]:
    """Fetch ESG data from Yahoo Finance."""
    try:
        info = await yf_info(ticker.upper()) or {}
    except Exception as e:
        logger.warning("ESG fetch failed for %s: %s", ticker, e)
        return {"ticker": ticker.upper(), "error": str(e)}

    esg_data = info.get("esgScores", {}) or {}
    return {
        "ticker": ticker.upper(),
        "total_score": esg_data.get("totalEsg"),
        "environmental_score": esg_data.get("environmentScore"),
        "social_score": esg_data.get("socialScore"),
        "governance_score": esg_data.get("governanceScore"),
        "controversy_score": 0,  # Yahoo doesn't provide controversy percentile directly
        "percentile": esg_data.get("percentile"),
        "rating": esg_data.get("rating"),
        "source": "yahoo",
    }


async def _save_score(ticker: str, score: dict[str, Any], db: AsyncSession) -> None:
    entry = EsgScore(
        ticker=ticker.upper(),
        total_score=score.get("total_score"),
        environmental_score=score.get("environmental_score"),
        social_score=score.get("social_score"),
        governance_score=score.get("governance_score"),
        controversy_score=score.get("controversy_score", 0),
        percentile=score.get("percentile"),
        rating=score.get("rating"),
        source=score.get("source", "yahoo"),
    )
    db.add(entry)
    await db.commit()
