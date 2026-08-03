from typing import Optional
import asyncio
import logging

logger = logging.getLogger(__name__)


async def run_scenario(
    ticker: str,
    portfolio_id: Optional[str] = None,
    shocks: Optional[list[dict]] = None,
) -> dict:
    from app.services.analytics._yf import get_info as yf_info
    from app.services.analytics.valuation import calculate_wacc

    info = await yf_info(ticker) if ticker else {}
    price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 100)
    beta_val = float(info.get("beta") or 1.0)

    scenarios = []
    if not shocks:
        shocks = [
            {"label": "Bear Case (-20%)", "shock": -0.20, "beta_mult": 1.0},
            {"label": "Mild Dip (-10%)", "shock": -0.10, "beta_mult": 0.7},
            {"label": "Base Case (0%)", "shock": 0.0, "beta_mult": 0.3},
            {"label": "Bull Case (+10%)", "shock": 0.10, "beta_mult": 0.7},
            {"label": "Melt Up (+20%)", "shock": 0.20, "beta_mult": 1.0},
            {"label": "Black Swan (-40%)", "shock": -0.40, "beta_mult": 2.0},
        ]

    for s in shocks:
        shock_pct = s["shock"]
        beta_mult = s.get("beta_mult", 1.0)
        shocked_price = price * (1 + shock_pct * beta_mult)
        pct_change = (shocked_price / price - 1) * 100

        scenarios.append({
            "label": s["label"],
            "original_price": round(price, 2),
            "shocked_price": round(shocked_price, 2),
            "change_pct": round(pct_change, 1),
            "beta": beta_val,
        })

    try:
        wacc_data = await calculate_wacc(ticker)
        wacc = wacc_data.get("wacc", 0.08)
    except Exception:
        wacc = 0.08

    return {
        "ticker": ticker.upper(),
        "current_price": round(price, 2),
        "beta": beta_val,
        "wacc": round(wacc, 2),
        "scenarios": scenarios,
        "worst_case": min(s["shocked_price"] for s in scenarios),
        "best_case": max(s["shocked_price"] for s in scenarios),
        "drawdown_risk": round((min(s["shocked_price"] for s in scenarios) / price - 1) * 100, 1),
    }


async def portfolio_scenario(
    tickers: list[str],
    weights: Optional[list[float]] = None,
    market_shock: float = -0.10,
) -> dict:
    from app.services.analytics._yf import get_info as yf_info

    if not weights:
        weights = [1.0 / len(tickers)] * len(tickers)

    results = []
    total_current = 0
    total_shocked = 0

    for i, ticker in enumerate(tickers):
        try:
            info = await yf_info(ticker)
            price = float(info.get("currentPrice") or 100)
            beta = float(info.get("beta") or 1.0)
        except Exception:
            price = 100
            beta = 1.0

        weight = weights[i]
        shocked_price = price * (1 + market_shock * beta)
        total_current += price * weight
        total_shocked += shocked_price * weight

        results.append({
            "ticker": ticker.upper(),
            "weight_pct": round(weight * 100, 1),
            "current_price": round(price, 2),
            "shocked_price": round(shocked_price, 2),
            "impact_pct": round((shocked_price / price - 1) * 100, 1),
            "beta": beta,
        })

    portfolio_change = (total_shocked / total_current - 1) * 100 if total_current > 0 else 0

    return {
        "market_shock_pct": round(market_shock * 100, 1),
        "portfolio_change_pct": round(portfolio_change, 2),
        "holdings": results,
        "summary": (
            f"Under a {market_shock * 100:.0f}% market shock, "
            f"your portfolio would change by {portfolio_change:+.2f}%. "
            f"The beta-weighted impact varies per holding."
        ),
    }
