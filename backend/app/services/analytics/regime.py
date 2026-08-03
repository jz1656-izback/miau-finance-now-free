"""
Market regime detection service using Hidden Markov Models.

Detects latent market regimes (Bull, Bear, Sideways, High Volatility)
from historical return data using a Rust-accelerated HMM with
log-domain forward-backward and Viterbi decoding.
"""

from __future__ import annotations

import numpy as np
from datetime import datetime, timezone
from app.services.analytics._yf import get_history

try:
    from miau_analytics._core import hmm_regime_detection as _rust_hmm
    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False

REGIME_LABELS = {
    0: "Bull",
    1: "Bear",
    2: "Sideways",
    3: "High Volatility",
}


async def detect_regimes(
    ticker: str,
    n_states: int = 3,
    n_iter: int = 50,
    period: str = "2y",
) -> dict:
    """Run HMM regime detection for a ticker.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.
    n_states : int
        Number of hidden regimes (default 3: Bull, Bear, Sideways).
    n_iter : int
        EM iterations (default 50).
    period : str
        Historical data period (default "2y").

    Returns
    -------
    dict with regime classifications, statistics, and transition matrix.
    """
    records = await get_history(ticker, period)
    if not records or len(records) < 30:
        return {"error": f"Insufficient price data for {ticker}"}

    closes = [r["close"] for r in records if r.get("close")]
    if len(closes) < 30:
        return {"error": "Insufficient closing price data"}

    prices = np.array(closes, dtype=np.float64)
    log_returns = np.diff(np.log(prices))

    if _HAS_RUST:
        result = dict(_rust_hmm(log_returns, n_states, n_iter))
        if "error" in result:
            return result
        states = np.array(result["states"])
        state_probs = np.array(result["state_probs"])
        trans = np.array(result["transition"])
        means = np.array(result["means"])
        stds = np.array(result["stds"])
        log_likelihood = result["log_likelihood"]
    else:
        # Pure Python fallback would go here
        return {"error": "Rust extension not available for HMM"}

    # Sort states by mean return for consistent labeling
    order = np.argsort(means)[::-1]  # highest mean first (Bull → Sideways → Bear)
    label_map = {old: new for new, old in enumerate(order)}
    sorted_states = np.array([label_map[s] for s in states])

    # Build regime distribution
    regime_counts = {}
    for s in range(n_states):
        label = REGIME_LABELS.get(s, f"Regime {s}")
        mask = sorted_states == s
        regime_counts[label] = {
            "count": int(mask.sum()),
            "pct": round(float(mask.mean() * 100), 1),
            "mean_return": round(float(means[order[s]]), 6),
            "volatility": round(float(stds[order[s]]), 6),
        }

    # Current regime
    current_state = int(sorted_states[-1])
    current_label = REGIME_LABELS.get(current_state, f"Regime {current_state}")
    # Reshape state_probs to (n, k) and get last row
    probs_2d = np.array(state_probs).reshape(-1, n_states) if len(np.array(state_probs).shape) == 1 else np.array(state_probs)
    current_prob = float(probs_2d[-1, order[current_state]]) if probs_2d.shape[1] > order[current_state] else 0.0

    # Regime changes
    changes = []
    for t in range(1, len(sorted_states)):
        if sorted_states[t] != sorted_states[t - 1]:
            changes.append({
                "date": records[t].get("date", "")[:10],
                "from": REGIME_LABELS.get(int(sorted_states[t - 1]), f"R{int(sorted_states[t-1])}"),
                "to": REGIME_LABELS.get(int(sorted_states[t]), f"R{int(sorted_states[t])}"),
                "index": t,
            })

    return {
        "ticker": ticker,
        "n_states": n_states,
        "n_observations": len(log_returns),
        "date_range": {
            "start": records[0].get("date", "")[:10],
            "end": records[-1].get("date", "")[:10],
        },
        "log_likelihood": round(log_likelihood, 2),
        "current_regime": {
            "state": current_state,
            "label": current_label,
            "probability": round(current_prob, 4),
        },
        "regimes": regime_counts,
        "regime_changes": changes[:20],  # last 20 changes
        "transition_matrix": trans.tolist(),
        "state_sequence": sorted_states.tolist(),
        "state_probabilities": state_probs.tolist(),
        "as_of": datetime.now(timezone.utc).isoformat(),
    }
