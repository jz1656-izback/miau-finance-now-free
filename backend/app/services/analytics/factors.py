"""
Fama-French factor analysis service.

Provides:
- 3-factor model: Market (Rm-Rf), SMB, HML
- 5-factor model: + RMW, CMA
- Plus Momentum (UMD) as optional extension

Data sourced from Prof. Ken French's data library via direct URL fetch
with optional Redis caching.
"""

from __future__ import annotations

import asyncio
import csv
import io
import logging
import re
import zipfile
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
import numpy as np

from app.services.analytics._yf import get_history

logger = logging.getLogger(__name__)

try:
    from miau_analytics._core import ols_regression as _rust_ols
    _HAS_RUST = True
except (ImportError, ModuleNotFoundError):
    _HAS_RUST = False

# ── Factor definitions ───────────────────────────────────────────────────────

FF_URLS = {
    3: "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_TXT.zip",
    5: "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_TXT.zip",
}

MOMENTUM_URL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_daily_TXT.zip"

FACTOR_NAMES_3 = ["Mkt-RF", "SMB", "HML"]
FACTOR_NAMES_5 = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
FACTOR_NAMES_MOM = ["MOM"]

HTTP_TIMEOUT = 30.0


# ── Data fetching ────────────────────────────────────────────────────────────


def _parse_ff_csv(text: str) -> dict[str, np.ndarray]:
    """Parse Ken French daily factor TXT into factor arrays.

    Format is space-delimited (not comma). Example:
      19260701    0.09   -0.25   -0.27    0.01
    """
    lines = text.strip().splitlines()
    # Find data start: first line matching YYYYMMDD
    data_start = 0
    for i, line in enumerate(lines):
        if re.match(r"^\d{6}", line.strip()):
            data_start = i
            break

    # Parse header line (line before data, space-delimited)
    header_line = lines[data_start - 1] if data_start > 0 else ""
    all_cols = header_line.strip().split()
    # Filter out empty strings and hyphens (used as placeholders)
    col_names = [h for h in all_cols if h and h != "-"]

    dates: list[str] = []
    values: list[list[float]] = []

    for line in lines[data_start:]:
        line = line.strip()
        if not line or not re.match(r"^\d{6}", line):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        dates.append(parts[0])
        row = []
        for v in parts[1:]:
            try:
                row.append(float(v) if v else 0.0)
            except ValueError:
                row.append(0.0)
        values.append(row)

    # All non-date columns are factor columns (including Mkt-RF)
    return {
        "dates": np.array(dates),
        "values": np.array(values, dtype=np.float64),
        "headers": col_names,
    }


def _extract_zip_bytes(content: bytes) -> str:
    """Extract the first .txt file from a ZIP archive and return its text."""
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        txt_files = [n for n in zf.namelist() if n.endswith(".txt")]
        if not txt_files:
            raise ValueError("No .txt file found in ZIP archive")
        # French's ZIP uses one txt file
        return zf.read(txt_files[0]).decode("utf-8-sig")


async def fetch_factors(
    model: int = 3,
    include_momentum: bool = False,
) -> dict:
    """Fetch Fama-French factor data from Ken French's data library (ZIP).

    Returns dict with 'dates', 'factors' (name→array), 'rf' (risk-free rate).
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        urls = [FF_URLS.get(model, FF_URLS[3])]
        if include_momentum:
            urls.append(MOMENTUM_URL)

        results = await asyncio.gather(*[client.get(u) for u in urls], return_exceptions=True)

        # Parse primary model
        if isinstance(results[0], Exception):
            raise results[0]  # type: ignore
        text = _extract_zip_bytes(results[0].content)
        parsed = _parse_ff_csv(text)

        factor_data: dict[str, np.ndarray] = {}
        for i, name in enumerate(parsed["headers"]):
            if i < parsed["values"].shape[1]:
                factor_data[name] = parsed["values"][:, i] / 100.0

        rf = factor_data.pop("RF", np.zeros(parsed["values"].shape[0]))

        # Parse momentum if requested
        if include_momentum and len(results) > 1 and not isinstance(results[1], Exception):
            mom_text = _extract_zip_bytes(results[1].content)
            mom_parsed = _parse_ff_csv(mom_text)
            if mom_parsed["values"].shape[1] >= 1:
                factor_data["MOM"] = mom_parsed["values"][:, 0] / 100.0

        return {
            "dates": parsed["dates"],
            "factors": factor_data,
            "rf": rf,
            "model": f"{model}-factor{' + Momentum' if include_momentum else ''}",
        }


# ── OLS Regression (with optional Rust acceleration) ───────────────────────


def _ols_numpy(X: np.ndarray, y: np.ndarray) -> dict:
    """Ordinary Least Squares via numpy.

    Returns: coefs, alpha, r_squared, residuals, n, std_errors
    """
    n, k = X.shape

    # Add constant for alpha
    X_with_const = np.column_stack([np.ones(n), X])

    # (X'X)^{-1} X'y
    xtx = X_with_const.T @ X_with_const
    try:
        xtx_inv = np.linalg.inv(xtx)
    except np.linalg.LinAlgError:
        xtx_inv = np.linalg.pinv(xtx)
    coefs = xtx_inv @ (X_with_const.T @ y)

    alpha = coefs[0]
    factor_coefs = coefs[1:]

    residuals = y - X_with_const @ coefs
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # Standard errors
    mse = ss_res / (n - k - 1) if n > k + 1 else 0.0
    std_errors = np.sqrt(np.diag(xtx_inv) * mse) if mse > 0 else np.zeros(k + 1)

    # T-statistics
    t_stats = coefs / std_errors if std_errors[0] > 0 else np.zeros_like(coefs)

    return {
        "alpha": float(alpha),
        "coefficients": {f"factor_{i}": float(factor_coefs[i]) for i in range(k)},
        "r_squared": float(r_squared),
        "adjusted_r_squared": float(1 - (1 - r_squared) * (n - 1) / max(1, n - k - 1)),
        "n_observations": n,
        "std_errors": [float(s) for s in std_errors],
        "t_statistics": [float(t) for t in t_stats],
        "residual_std": float(np.sqrt(mse)) if mse > 0 else 0.0,
    }


async def run_factor_regression(
    ticker: str,
    model: int = 3,
    include_momentum: bool = False,
    period: str = "2y",
) -> dict:
    """Run Fama-French factor regression for a ticker.

    1. Fetch ticker's daily returns
    2. Fetch factor data from Ken French
    3. Align time periods
    4. Run OLS: R_i - R_f = α + β₁·F₁ + β₂·F₂ + ... + ε
    5. Return results
    """
    # 1. Get ticker returns
    records = await get_history(ticker, period)
    if not records or len(records) < 30:
        return {"error": f"Insufficient price data for {ticker}"}

    closes = [r["close"] for r in records if r.get("close")]
    dates_str = []
    for r in records:
        d = r.get("date", "")
        if d:
            dates_str.append(d[:10].replace("-", ""))

    if len(closes) < 30:
        return {"error": f"Insufficient closing price data for {ticker}"}

    prices = np.array(closes, dtype=np.float64)
    returns = np.diff(np.log(prices))  # log returns

    # 2. Fetch factors
    factor_data = await fetch_factors(model=model, include_momentum=include_momentum)
    ff_dates = factor_data["dates"]
    ff_factors = factor_data["factors"]
    rf = factor_data["rf"]

    # 3. Align — match dates between stock returns and factor data
    # Stock dates are most recent, FF dates go further back
    # We need the overlapping period
    stock_date_strs = dates_str[1:]  # after diff, we have n-1 dates
    if len(stock_date_strs) != len(returns):
        stock_date_strs = stock_date_strs[:len(returns)]

    # Build aligned arrays
    date_to_ret = dict(zip(stock_date_strs, returns))
    date_to_rf = dict(zip(ff_dates, rf))

    # Get factor names
    factor_names = list(ff_factors.keys())
    factor_arrays: list[np.ndarray] = [ff_factors[name] for name in factor_names]
    date_to_factors: dict[str, np.ndarray] = {}
    for i, d in enumerate(ff_dates):
        date_to_factors[d] = np.array([ff_factors[name][i] for name in factor_names])

    # Align
    aligned_rets: list[float] = []
    aligned_factors: list[np.ndarray] = []
    aligned_rf: list[float] = []

    common_dates = sorted(set(date_to_ret.keys()) & set(date_to_factors.keys()))
    for d in common_dates:
        aligned_rets.append(date_to_ret[d])
        aligned_factors.append(date_to_factors[d])
        aligned_rf.append(date_to_rf.get(d, 0.0))

    if len(aligned_rets) < 20:
        return {"error": "Insufficient overlapping data between ticker and factors"}

    y = np.array(aligned_rets, dtype=np.float64) - np.array(aligned_rf, dtype=np.float64)
    X = np.array(aligned_factors, dtype=np.float64)

    # 4. Run OLS
    n, k = X.shape
    # 4. Run OLS (Rust returns list coefs + list std_errors including alpha)
    if _HAS_RUST:
        try:
            raw = dict(_rust_ols(X, y))
            result = {
                "alpha": raw["alpha"],
                "coefficients": {f"factor_{i}": float(raw["coefficients"][i]) for i in range(k)},
                "r_squared": raw["r_squared"],
                "adjusted_r_squared": raw["adjusted_r_squared"],
                "n_observations": raw["n_observations"],
                "std_errors": raw["std_errors"],      # includes alpha at index 0
                "t_statistics": raw["t_statistics"],    # includes alpha at index 0
                "residual_std": raw["residual_std"],
            }
        except Exception as e:
            logger.debug(f"Rust OLS failed, falling back to numpy: {e}")
            result = _ols_numpy(X, y)
    else:
        result = _ols_numpy(X, y)

    # 5. Build output
    # Rust: std_errors[0] is alpha's SE; numpy: std_errors[0] is also alpha's SE
    # Cast to dict-style for consistency
    coefs_dict = result["coefficients"] if isinstance(result["coefficients"], dict) else {}
    factor_results = {}
    for i, name in enumerate(factor_names):
        coef_key = f"factor_{i}"
        factor_results[name] = {
            "coefficient": round(coefs_dict.get(coef_key, 0.0), 6),
            "std_error": round(result["std_errors"][i + 1], 6) if len(result["std_errors"]) > i + 1 else 0.0,
            "t_stat": round(result["t_statistics"][i + 1], 4) if len(result["t_statistics"]) > i + 1 else 0.0,
        }

    # Annualized alpha
    alpha_ann = result["alpha"] * 252

    return {
        "ticker": ticker,
        "model": factor_data["model"],
        "period": period,
        "n_observations": result["n_observations"],
        "date_range": {
            "start": common_dates[0] if common_dates else "",
            "end": common_dates[-1] if common_dates else "",
        },
        "alpha": {
            "daily": round(result["alpha"], 6),
            "annualized": round(alpha_ann, 6),
            "std_error": round(result["std_errors"][0], 6) if result["std_errors"] else 0.0,
            "t_stat": round(result["t_statistics"][0], 4) if result["t_statistics"] else 0.0,
        },
        "factor_loadings": factor_results,
        "r_squared": round(result["r_squared"], 4),
        "adjusted_r_squared": round(result["adjusted_r_squared"], 4),
        "residual_std": round(result["residual_std"], 6),
        "as_of": datetime.now(timezone.utc).isoformat(),
    }
