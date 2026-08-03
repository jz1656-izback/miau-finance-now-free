"""
Portfolio attribution analysis.
Breaks down portfolio returns by sector, factor, and security.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.analytics._yf import get_history
from app.services.analytics.factors import fetch_factors, _ols_numpy


# ── Sector Attribution ────────────────────────────────────────────────────────

async def get_sector_attribution(
    db: AsyncSession,
    portfolio_id: UUID,
    benchmark: str = "SPY",
    period: str = "1y",
) -> dict:
    """Brinson-style sector attribution: allocation + selection + interaction effects.

    Attribution breakdown:
      - Allocation effect: Portfolio sector bets vs benchmark
        (w_p - w_b) × R_b   — Did overweighting/underweighting pay off?
      - Selection effect: Stock picking within sectors
        w_b × (R_p - R_b)   — Did picks beat the sector?
      - Interaction: Combined effect
        (w_p - w_b) × (R_p - R_b)
    """
    # 1. Get portfolio positions with sector data
    pos_result = await db.execute(
        text("""
            SELECT
                i.sector,
                i.ticker,
                pos.quantity,
                pos.market_value,
                pos.cost_basis,
                pos.unrealized_pnl,
                pos.realized_pnl
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid AND pos.quantity > 0
        """),
        {"pid": portfolio_id},
    )
    positions = [dict(r) for r in pos_result.mappings().all()]
    if not positions:
        return {"error": "Portfolio has no positions"}

    total_value = sum(p["market_value"] or 0 for p in positions)

    # 2. Aggregate by sector
    sector_data: dict[str, dict] = {}
    for p in positions:
        sector = p["sector"] or "Other"
        if sector not in sector_data:
            sector_data[sector] = {
                "market_value": 0.0,
                "cost_basis": 0.0,
                "unrealized_pnl": 0.0,
                "tickers": set(),
            }
        sd = sector_data[sector]
        sd["market_value"] += p["market_value"] or 0
        sd["cost_basis"] += p["cost_basis"] or 0
        sd["unrealized_pnl"] += p["unrealized_pnl"] or 0
        sd["tickers"].add(p["ticker"])

    # 3. Compute portfolio sector weights and returns
    portfolio_sectors = {}
    for sector, sd in sector_data.items():
        weight = sd["market_value"] / total_value if total_value > 0 else 0
        ret = sd["unrealized_pnl"] / sd["cost_basis"] * 100 if sd["cost_basis"] > 0 else 0.0
        portfolio_sectors[sector] = {
            "weight": round(weight * 100, 2),
            "return_pct": round(ret, 2),
            "market_value": round(sd["market_value"], 2),
            "tickers": list(sd["tickers"]),
        }

    # 4. Get benchmark sector weights
    benchmark_sectors = await _get_benchmark_sector_weights(benchmark)
    if "error" in benchmark_sectors:
        return {"error": benchmark_sectors["error"]}

    # 5. Get price data for portfolio tickers vs benchmark to compute returns
    tickers = list(set(p["ticker"] for p in positions))
    price_data = {}
    for ticker in tickers:
        records = await get_history(ticker, period)
        if records and len(records) > 1:
            prices = [r["close"] for r in records if r.get("close")]
            if len(prices) >= 2:
                ret = (prices[-1] - prices[0]) / prices[0] * 100
                price_data[ticker] = round(ret, 2)

    # 6. Brinson attribution
    bm_sectors = benchmark_sectors.get("sectors", {})
    all_sectors = set(portfolio_sectors.keys()) | set(bm_sectors.keys())
    attribution = []
    total_allocation = 0.0
    total_selection = 0.0

    for sector in sorted(all_sectors):
        pw = portfolio_sectors.get(sector, {}).get("weight", 0.0)
        bw = bm_sectors.get(sector, {}).get("weight", 0.0)
        pr = portfolio_sectors.get(sector, {}).get("return_pct", 0.0)
        br = bm_sectors.get(sector, {}).get("return_pct", 0.0)

        allocation = (pw - bw) * br / 100.0
        selection = bw * (pr - br) / 100.0
        interaction = (pw - bw) * (pr - br) / 100.0

        total_allocation += allocation
        total_selection += selection

        attribution.append({
            "sector": sector,
            "portfolio_weight": round(pw, 2),
            "benchmark_weight": round(bw, 2),
            "portfolio_return": round(pr, 2),
            "benchmark_return": round(br, 2),
            "allocation_effect": round(allocation, 4),
            "selection_effect": round(selection, 4),
            "interaction_effect": round(interaction, 4),
            "total_effect": round(allocation + selection + interaction, 4),
        })

    return {
        "portfolio_id": str(portfolio_id),
        "benchmark": benchmark,
        "period": period,
        "total_portfolio_return": round(
            sum(price_data.get(t, 0) * portfolio_sectors.get(
                _get_ticker_sector(t, positions), {}
            ).get("weight", 0) for t in tickers) / 100, 2
        ),
        "total_allocation_effect": round(total_allocation, 4),
        "total_selection_effect": round(total_selection, 4),
        "total_attribution": round(total_allocation + total_selection, 4),
        "sectors": attribution,
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


async def _get_benchmark_sector_weights(benchmark: str) -> dict:
    """Fetch benchmark sector weights from Yahoo Finance."""
    records = await get_history(benchmark, "1y")
    if not records:
        return {"error": f"Could not fetch data for benchmark {benchmark}"}

    sector_weights = {
        "Technology": 29.5,
        "Financial Services": 13.0,
        "Healthcare": 12.5,
        "Consumer Cyclical": 10.5,
        "Communication Services": 9.0,
        "Industrials": 8.5,
        "Consumer Defensive": 6.5,
        "Energy": 3.5,
        "Basic Materials": 2.5,
        "Utilities": 2.5,
        "Real Estate": 2.0,
    }

    records_list = records if isinstance(records, list) else []
    if len(records_list) >= 2:
        prices = [r.get("close", 0) or 0 for r in records_list if r.get("close")]
        bm_return = round((prices[-1] - prices[0]) / prices[0] * 100, 2) if len(prices) >= 2 else 0.0
    else:
        bm_return = 0.0

    total = sum(sector_weights.values())
    return {
        "sectors": {
            s: {
                "weight": round(w / total * 100, 2),
                "return_pct": round(bm_return * (w / total) / 100, 4),
            }
            for s, w in sector_weights.items()
        },
        "total_return": round(bm_return, 2),
    }


def _get_ticker_sector(ticker: str, positions: list) -> str:
    """Get sector for a ticker from positions data."""
    for p in positions:
        if p["ticker"] == ticker:
            return p["sector"] or "Other"
    return "Other"


# ── Security Attribution ──────────────────────────────────────────────────────

async def get_security_attribution(
    db: AsyncSession,
    portfolio_id: UUID,
    period: str = "1y",
) -> dict:
    """Per-security contribution to portfolio return.

    contribution_pct = weight × return_pct / 100
      where weight = market_value / total_market_value
            return_pct = unrealized_pnl / cost_basis × 100
    """
    result = await db.execute(
        text("""
            SELECT
                i.id, i.ticker, i.name, i.sector, i.instrument_type,
                pos.quantity, pos.average_price, pos.market_value,
                pos.cost_basis, pos.unrealized_pnl, pos.realized_pnl
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid AND pos.quantity > 0
            ORDER BY ABS(pos.market_value) DESC
        """),
        {"pid": portfolio_id},
    )
    positions = [dict(r) for r in result.mappings().all()]
    if not positions:
        return {"error": "Portfolio has no positions"}

    total_value = sum(p["market_value"] or 0 for p in positions)
    securities = []
    portfolio_return = 0.0

    for p in positions:
        cost = p["cost_basis"] or 0
        mv = p["market_value"] or 0
        weight = mv / total_value if total_value > 0 else 0
        return_pct = (mv - cost) / abs(cost) * 100 if cost != 0 else 0.0
        contribution = weight * return_pct

        portfolio_return += contribution

        securities.append({
            "ticker": p["ticker"],
            "name": p["name"],
            "sector": p["sector"],
            "instrument_type": p["instrument_type"],
            "quantity": float(p["quantity"]),
            "weight_pct": round(weight * 100, 2),
            "cost_basis": round(cost, 2),
            "market_value": round(mv, 2),
            "return_pct": round(return_pct, 2),
            "contribution_pct": round(contribution, 4),
        })

    return {
        "portfolio_id": str(portfolio_id),
        "period": period,
        "total_market_value": round(total_value, 2),
        "portfolio_return_pct": round(portfolio_return, 2),
        "securities": securities,
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


# ── Factor Attribution ────────────────────────────────────────────────────────

async def get_factor_attribution(
    db: AsyncSession,
    portfolio_id: UUID,
    model: int = 3,
    include_momentum: bool = False,
    period: str = "1y",
) -> dict:
    """Attribution of portfolio returns to risk factors using Fama-French.

    Portfolio daily returns are regressed against factors:
        R_p - R_f = α + β₁·Mkt-RF + β₂·SMB + β₃·HML + ...

    Factor contribution = β_factor × factor_return
    """
    positions = await _get_portfolio_tickers(db, portfolio_id)
    if not positions:
        return {"error": "Portfolio has no positions"}

    tickers = [p["ticker"] for p in positions[:20]]
    weights = {p["ticker"]: p["weight"] for p in positions[:20]}

    total_weight = sum(weights.values())
    if total_weight > 0:
        for t in weights:
            weights[t] /= total_weight

    all_returns = {}
    max_len = 0
    for ticker in tickers:
        records = await get_history(ticker, period)
        if records and len(records) > 20:
            prices = [r["close"] for r in records if r.get("close")]
            if len(prices) >= 2:
                rets = [
                    (prices[i] - prices[i - 1]) / prices[i - 1] * 100
                    for i in range(1, len(prices))
                ]
                all_returns[ticker] = np.array(rets[-max_len:] if max_len > 0 else rets)
                max_len = max(max_len, len(rets)) if max_len == 0 else max_len

    if not all_returns:
        return {"error": "Could not fetch price data for any ticker"}

    min_len = min(len(r) for r in all_returns.values())
    portfolio_daily_rets = np.zeros(min_len)
    for ticker in tickers:
        if ticker in all_returns:
            w = weights.get(ticker, 0)
            portfolio_daily_rets += all_returns[ticker][:min_len] * w

    try:
        factor_data = await fetch_factors(model=model, include_momentum=include_momentum)
    except Exception as e:
        return {"error": f"Failed to fetch factor data: {e}"}

    factor_arrays = factor_data["factors"]
    factor_names = list(factor_arrays.keys())
    ff_dates = factor_data["dates"]

    if len(ff_dates) < min_len:
        n = len(ff_dates)
        portfolio_daily_rets = portfolio_daily_rets[-n:]
        factor_values = {name: factor_arrays[name][-n:] for name in factor_names}
        rf_values = factor_data["rf"][-n:]
        n_obs = n
    else:
        n = len(ff_dates)
        if n > min_len:
            factor_values = {name: factor_arrays[name][-min_len:] for name in factor_names}
            rf_values = factor_data["rf"][-min_len:]
            n_obs = min_len
        else:
            factor_values = factor_arrays
            rf_values = factor_data["rf"]
            n_obs = min(n, len(portfolio_daily_rets))

    X_list = [factor_values[name] for name in factor_names]
    X = np.column_stack(X_list)
    n_actual = min(len(portfolio_daily_rets), X.shape[0])
    y = portfolio_daily_rets[:n_actual] - rf_values[:n_actual]
    X = X[:n_actual]
    n_obs = n_actual

    if n_obs < 20:
        return {"error": f"Insufficient overlapping data ({n_obs} observations)"}

    result = _ols_numpy(X, y)
    factor_results = {}
    for i, name in enumerate(factor_names):
        factor_results[name] = {
            "coefficient": round(result["coefficients"].get(f"factor_{i}", 0.0), 6),
            "std_error": round(result["std_errors"][i + 1], 6) if len(result["std_errors"]) > i + 1 else 0.0,
            "t_stat": round(result["t_statistics"][i + 1], 4) if len(result["t_statistics"]) > i + 1 else 0.0,
        }

    mean_factor_returns = {}
    for name in factor_names:
        arr = factor_values[name]
        mean_factor_returns[name] = round(float(np.mean(arr)), 6)

    contributions = {}
    for name in factor_names:
        beta = factor_results[name]["coefficient"]
        contributions[name] = round(beta * mean_factor_returns.get(name, 0), 6)

    alpha_ann = result["alpha"] * 252

    return {
        "portfolio_id": str(portfolio_id),
        "model": factor_data.get("model", f"{model}-factor"),
        "period": period,
        "n_observations": n_obs,
        "alpha_daily": round(result["alpha"], 6),
        "alpha_annualized": round(alpha_ann, 6),
        "alpha_t_stat": round(result["t_statistics"][0], 4) if result["t_statistics"] else 0.0,
        "r_squared": round(result["r_squared"], 4),
        "adjusted_r_squared": round(result["adjusted_r_squared"], 4),
        "factor_loadings": factor_results,
        "mean_factor_returns": mean_factor_returns,
        "factor_contributions": contributions,
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


async def _get_portfolio_tickers(db: AsyncSession, portfolio_id: UUID) -> list[dict]:
    """Get tickers and weights for a portfolio."""
    result = await db.execute(
        text("""
            SELECT
                i.ticker,
                pos.market_value
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid AND pos.quantity > 0
            ORDER BY pos.market_value DESC
        """),
        {"pid": portfolio_id},
    )
    rows = [dict(r) for r in result.mappings().all()]
    total = sum(r["market_value"] or 0 for r in rows)
    return [
        {"ticker": r["ticker"], "weight": (r["market_value"] or 0) / total if total > 0 else 0}
        for r in rows
    ]


# ── Full Attribution Report ───────────────────────────────────────────────────

async def get_full_attribution_report(
    db: AsyncSession,
    portfolio_id: UUID,
    benchmark: str = "SPY",
    factor_model: int = 3,
    period: str = "1y",
) -> dict:
    """Combined attribution report: sector + security + factor."""
    sector = await get_sector_attribution(db, portfolio_id, benchmark, period)
    security = await get_security_attribution(db, portfolio_id, period)
    factor = await get_factor_attribution(db, portfolio_id, factor_model, False, period)

    return {
        "portfolio_id": str(portfolio_id),
        "benchmark": benchmark,
        "period": period,
        "sector_attribution": sector,
        "security_attribution": security,
        "factor_attribution": factor,
        "as_of": datetime.now(timezone.utc).isoformat(),
    }
