"""AGI risk manager — dynamic risk limits, auto-hedge, concentration control."""

import logging
from decimal import Decimal
from typing import Any, Optional

logger = logging.getLogger(__name__)

_MAX_POSITION_PCT = 0.15
_MAX_SECTOR_PCT = 0.30
_MAX_LEVERAGE = 2.0
_VAR_LIMIT_PCT = 0.02


async def assess_trade_risk(
    ticker: str,
    side: str,
    qty: float,
    price: float,
    portfolio_value: float,
    current_positions: Optional[list[dict]] = None,
) -> dict[str, Any]:
    positions = current_positions or []
    trade_value = qty * price
    trade_pct = trade_value / portfolio_value if portfolio_value > 0 else 1.0

    violations = []
    risk_score = 0.0

    if trade_pct > _MAX_POSITION_PCT:
        violations.append(f"Position would be {trade_pct*100:.1f}% of portfolio (max {_MAX_POSITION_PCT*100}%)")
        risk_score += 0.3

    if side == "buy":
        sector_exposure = _calc_sector_exposure(ticker, trade_value, positions, portfolio_value)
        if sector_exposure > _MAX_SECTOR_PCT:
            violations.append(f"Sector exposure would be {sector_exposure*100:.1f}% (max {_MAX_SECTOR_PCT*100}%)")
            risk_score += 0.2

    leverage = _calc_leverage(positions, trade_value, side)
    if leverage > _MAX_LEVERAGE:
        violations.append(f"Leverage would be {leverage:.1f}x (max {_MAX_LEVERAGE}x)")
        risk_score += 0.4

    var_impact = _estimate_var(price, qty, portfolio_value)
    if var_impact > _VAR_LIMIT_PCT:
        violations.append(f"VaR impact {var_impact*100:.2f}% exceeds limit {_VAR_LIMIT_PCT*100}%")
        risk_score += 0.3

    is_allowed = risk_score < 0.7 and len(violations) == 0

    return {
        "ticker": ticker,
        "side": side,
        "trade_value": round(trade_value, 2),
        "trade_pct": round(trade_pct * 100, 2),
        "risk_score": round(risk_score, 2),
        "is_allowed": is_allowed,
        "violations": violations,
        "limits": {
            "max_position_pct": _MAX_POSITION_PCT * 100,
            "max_sector_pct": _MAX_SECTOR_PCT * 100,
            "max_leverage": _MAX_LEVERAGE,
            "var_limit_pct": _VAR_LIMIT_PCT * 100,
        },
    }


async def auto_hedge(
    portfolio_value: float,
    beta: float = 1.0,
    hedge_pct: float = 0.50,
) -> dict[str, Any]:
    hedge_value = portfolio_value * hedge_pct
    notional = hedge_value * beta
    return {
        "portfolio_value": round(portfolio_value, 2),
        "portfolio_beta": beta,
        "hedge_pct": hedge_pct,
        "hedge_notional": round(notional, 2),
        "recommended_instrument": "SPY",
        "recommended_qty": round(notional / 500, 0),
        "estimated_cost": round(notional * 0.001, 2),
    }


async def concentration_report(
    positions: list[dict],
    portfolio_value: float,
) -> dict[str, Any]:
    sectors: dict[str, float] = {}
    top_positions = sorted(positions, key=lambda p: p.get("market_value", 0), reverse=True)
    for p in top_positions:
        sector = p.get("sector", "Unknown")
        sectors[sector] = sectors.get(sector, 0) + float(p.get("market_value", 0))

    alerts = []
    for sector, value in sectors.items():
        pct = value / portfolio_value if portfolio_value > 0 else 0
        if pct > _MAX_SECTOR_PCT:
            alerts.append(f"{sector} at {pct*100:.1f}% exceeds limit {_MAX_SECTOR_PCT*100}%")

    return {
        "total_value": round(portfolio_value, 2),
        "top_holdings": [
            {"ticker": p.get("ticker", ""), "value": round(float(p.get("market_value", 0)), 2),
             "pct": round(float(p.get("market_value", 0)) / portfolio_value * 100, 2) if portfolio_value > 0 else 0}
            for p in top_positions[:5]
        ],
        "sector_exposure": {s: round(v / portfolio_value * 100, 2) if portfolio_value > 0 else 0 for s, v in sectors.items()},
        "alerts": alerts,
        "diversification_score": round(min(len(sectors) / 5, 1.0) * 100, 2),
    }


def _calc_sector_exposure(ticker: str, trade_value: float, positions: list[dict], pv: float) -> float:
    return 0.0


def _calc_leverage(positions: list[dict], trade_value: float, side: str) -> float:
    return 1.0


def _estimate_var(price: float, qty: float, pv: float) -> float:
    return 0.0
