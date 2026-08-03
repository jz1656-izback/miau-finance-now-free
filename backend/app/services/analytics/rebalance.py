"""Portfolio rebalancing engine — drift detection, target allocation, trade generation."""

import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

DRIFT_THRESHOLD = Decimal("0.05")


@dataclass
class Holding:
    ticker: str
    market_value: Decimal
    weight: Decimal
    target_weight: Decimal = Decimal("0")


@dataclass
class RebalanceTrade:
    ticker: str
    side: str
    value: Decimal
    current_weight: Decimal
    target_weight: Decimal

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticker": self.ticker,
            "side": self.side,
            "value": round(float(self.value), 2),
            "current_weight_pct": round(float(self.current_weight * 100), 2),
            "target_weight_pct": round(float(self.target_weight * 100), 2),
        }


async def get_portfolio_holdings(portfolio_id: str, db: AsyncSession) -> list[Holding]:
    rows = await db.execute(
        text("""
            SELECT i.ticker, p.market_value
            FROM positions p
            JOIN instruments i ON i.id = p.instrument_id
            WHERE p.portfolio_id = :pid AND p.quantity > 0
        """),
        {"pid": portfolio_id},
    )
    holdings = []
    total = Decimal("0")
    raw = [dict(r) for r in rows.mappings().all()]
    for r in raw:
        mv = Decimal(str(r.get("market_value", 0) or 0))
        if mv > 0:
            total += mv
            holdings.append(Holding(ticker=r["ticker"], market_value=mv, weight=Decimal("0")))
    for h in holdings:
        h.weight = h.market_value / total if total > 0 else Decimal("0")
    return holdings


async def detect_drift(portfolio_id: str, db: AsyncSession, threshold: float = 0.05) -> dict[str, Any]:
    """Detect portfolio allocations that deviate from equal-weight targets beyond threshold."""
    holdings = await get_portfolio_holdings(portfolio_id, db)
    if not holdings:
        return {"portfolio_id": portfolio_id, "error": "No positions found", "drifted": []}

    n = len(holdings)
    target = Decimal("1") / Decimal(str(n))
    for h in holdings:
        h.target_weight = target

    drifted = []
    for h in holdings:
        diff = abs(h.weight - h.target_weight)
        if diff > Decimal(str(threshold)):
            drifted.append({
                "ticker": h.ticker,
                "current_weight_pct": round(float(h.weight * 100), 2),
                "target_weight_pct": round(float(h.target_weight * 100), 2),
                "drift_pct": round(float(diff * 100), 2),
                "action": "overweight" if h.weight > h.target_weight else "underweight",
            })

    return {
        "portfolio_id": portfolio_id,
        "total_value": round(float(sum(h.market_value for h in holdings)), 2),
        "holdings": len(holdings),
        "drifted_count": len(drifted),
        "drifted": sorted(drifted, key=lambda x: x["drift_pct"], reverse=True),
        "threshold_pct": threshold * 100,
    }


async def generate_rebalance_plan(portfolio_id: str, db: AsyncSession) -> dict[str, Any]:
    drift = await detect_drift(portfolio_id, db)
    if drift.get("error"):
        return drift

    total = Decimal(str(drift["total_value"]))
    holdings = await get_portfolio_holdings(portfolio_id, db)
    n = len(holdings)
    target = Decimal("1") / Decimal(str(n))

    trades: list[RebalanceTrade] = []
    summary_sell = Decimal("0")
    summary_buy = Decimal("0")

    for h in holdings:
        diff = h.weight - target
        if abs(diff) <= DRIFT_THRESHOLD:
            continue
        trade_value = abs(diff) * total
        if diff > 0:
            summary_sell += trade_value
            trades.append(RebalanceTrade(h.ticker, "sell", trade_value, h.weight, target))
        else:
            summary_buy += trade_value
            trades.append(RebalanceTrade(h.ticker, "buy", trade_value, h.weight, target))

    total_turnover = summary_sell + summary_buy
    return {
        "portfolio_id": portfolio_id,
        "total_value": round(float(total), 2),
        "holdings": n,
        "trades": [t.to_dict() for t in trades],
        "summary": {
            "sell_count": sum(1 for t in trades if t.side == "sell"),
            "buy_count": sum(1 for t in trades if t.side == "buy"),
            "total_turnover": round(float(total_turnover), 2),
            "turnover_pct": round(float(total_turnover / total * 100), 2) if total > 0 else 0,
        },
    }


async def set_target_allocations(
    portfolio_id: str, targets: dict[str, float], db: AsyncSession
) -> dict[str, Any]:
    holdings = await get_portfolio_holdings(portfolio_id, db)
    if not holdings:
        return {"portfolio_id": portfolio_id, "error": "No positions found"}

    total_target = sum(targets.values())
    if total_target <= 0:
        return {"error": "Target allocations must sum to > 0"}

    normalized = {t: Decimal(str(v)) / Decimal(str(total_target)) for t, v in targets.items()}

    total_value = sum(h.market_value for h in holdings)
    trades: list[RebalanceTrade] = []
    summary_buy = Decimal("0")
    summary_sell = Decimal("0")

    for h in holdings:
        tgt = normalized.get(h.ticker, Decimal("0"))
        diff = h.weight - tgt
        if abs(diff) <= DRIFT_THRESHOLD:
            continue
        trade_value = abs(diff) * total_value
        if diff > 0:
            summary_sell += trade_value
            trades.append(RebalanceTrade(h.ticker, "sell", trade_value, h.weight, tgt))
        else:
            summary_buy += trade_value
            trades.append(RebalanceTrade(h.ticker, "buy", trade_value, h.weight, tgt))

    missing_tickers = [t for t in targets if t not in {h.ticker for h in holdings}]
    for t in missing_tickers:
        tgt = normalized[t]
        trade_value = tgt * total_value
        if trade_value > 0:
            trades.append(RebalanceTrade(t, "buy", trade_value, Decimal("0"), tgt))
            summary_buy += trade_value

    return {
        "portfolio_id": portfolio_id,
        "total_value": round(float(total_value), 2),
        "holdings": len(holdings),
        "target_tickers": len(targets),
        "trades": [t.to_dict() for t in trades],
        "summary": {
            "sell_count": sum(1 for t in trades if t.side == "sell"),
            "buy_count": sum(1 for t in trades if t.side == "buy"),
            "total_turnover": round(float(summary_sell + summary_buy), 2),
            "turnover_pct": round(float((summary_sell + summary_buy) / total_value * 100), 2) if total_value > 0 else 0,
        },
    }
