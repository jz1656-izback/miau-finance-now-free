"""
Pairs trading analysis service.

Detects cointegrated pairs using the Rust engine (Engle-Granger,
ADF test, half-life computation, z-score signals).
"""

from __future__ import annotations

import numpy as np
from datetime import datetime, timezone
from app.services.analytics._yf import get_history

try:
    from miau_analytics._core import pairs_analysis as _rust_pairs
    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


SIGNAL_LABELS = {
    -1: "SHORT spread (sell B, buy A)",
    0: "NEUTRAL",
    1: "LONG spread (buy B, sell A)",
}


async def analyze_pair(
    ticker_a: str,
    ticker_b: str,
    lookback: int = 20,
    period: str = "2y",
) -> dict:
    """Analyze a pair of tickers for cointegration and trading signals.

    Parameters
    ----------
    ticker_a, ticker_b : str
        The two tickers to analyze as a potential pair.
    lookback : int
        Rolling window for z-score computation.
    period : str
        Historical data period.

    Returns
    -------
    dict with cointegration test, spread, z-scores, signals.
    """
    # Fetch both price series concurrently
    import asyncio
    results = await asyncio.gather(
        get_history(ticker_a, period),
        get_history(ticker_b, period),
    )
    records_a, records_b = results

    if not records_a or len(records_a) < 30:
        return {"error": f"Insufficient data for {ticker_a}"}
    if not records_b or len(records_b) < 30:
        return {"error": f"Insufficient data for {ticker_b}"}

    closes_a = [r["close"] for r in records_a if r.get("close")]
    closes_b = [r["close"] for r in records_b if r.get("close")]

    min_len = min(len(closes_a), len(closes_b))
    if min_len < 30:
        return {"error": "Insufficient overlapping data"}

    prices_a = np.array(closes_a[:min_len], dtype=np.float64)
    prices_b = np.array(closes_b[:min_len], dtype=np.float64)

    if _HAS_RUST:
        result = dict(_rust_pairs(prices_a, prices_b, lookback))
        if "error" in result:
            return result

        spread = np.array(result["spread"])
        z_scores = np.array(result["z_scores"])
        current_z = result["current_z_score"]
    else:
        return {"error": "Rust extension not available for pairs analysis"}

    # Generate recent trading signals
    signals = []
    prev_signal = 0
    for i in range(max(lookback, len(z_scores) - 30), len(z_scores)):
        z = z_scores[i]
        sig = 0
        if z > 2.0:
            sig = -1
        elif z < -2.0:
            sig = 1
        elif abs(z) < 0.5:
            sig = 0

        if sig != prev_signal:
            date_idx = i + 1  # +1 because spread starts after regression
            date = records_a[min(date_idx, len(records_a) - 1)].get("date", "")[:10] if date_idx < len(records_a) else ""
            signals.append({
                "date": date,
                "z_score": round(float(z), 2),
                "signal": sig,
                "action": SIGNAL_LABELS.get(sig, "HOLD"),
            })
            prev_signal = sig

    # Summary stats
    non_zero_z = z_scores[lookback:]
    z_mean = float(np.mean(non_zero_z))
    z_std = float(np.std(non_zero_z))

    # Correlation
    log_a = np.log(prices_a[prices_a > 0])
    log_b = np.log(prices_b[prices_b > 0])
    min_corr = min(len(log_a), len(log_b))
    correlation = float(np.corrcoef(log_a[:min_corr], log_b[:min_corr])[0, 1]) if min_corr > 1 else 0.0

    return {
        "pair": {"a": ticker_a, "b": ticker_b},
        "n_observations": len(spread),
        "hedge_ratio": round(result["hedge_ratio"], 4),
        "alpha": round(result["alpha"], 4),
        "half_life_days": round(result["half_life"], 1),
        "adf_statistic": round(result["adf_statistic"], 4),
        "adf_pvalue": round(result["adf_pvalue"], 4),
        "is_cointegrated": result["is_cointegrated"],
        "correlation": round(correlation, 4),
        "current_z_score": round(current_z, 2),
        "current_signal": SIGNAL_LABELS.get(result["signal"], "NEUTRAL"),
        "spread_stats": {
            "mean": round(float(np.mean(spread)), 4),
            "std": round(float(np.std(spread)), 4),
            "min": round(float(np.min(spread)), 4),
            "max": round(float(np.max(spread)), 4),
            "current": round(float(spread[-1]), 4) if len(spread) > 0 else 0.0,
        },
        "z_score_stats": {
            "mean": round(z_mean, 2),
            "std": round(z_std, 2),
            "min": round(float(np.min(non_zero_z)), 2),
            "max": round(float(np.max(non_zero_z)), 2),
        },
        "recent_signals": signals[-10:],
        "as_of": datetime.now(timezone.utc).isoformat(),
    }
