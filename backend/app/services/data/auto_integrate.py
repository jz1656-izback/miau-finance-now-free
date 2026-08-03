"""Auto-API integration engine — probes new data sources and tries to map them to known models.

Given a URL (and optional API key), this engine:
1. Probes common endpoint patterns
2. Detects the data format and structure
3. Maps fields to Miau Finance data models
4. Runs basic analysis on the data
5. Reports what was discovered
"""
import httpx
import json
from typing import Any, Optional
from datetime import datetime


# Common endpoint patterns to probe
PROBE_PATHS = [
    "/api/v1/quote/{ticker}", "/api/v1/ticker/{ticker}",
    "/api/v1/live/{ticker}", "/api/v1/stock/{ticker}",
    "/latest?base=USD", "/api/v1/latest",
    "/api/v1/prices", "/api/v1/market",
    "/api/v1/overview", "/api/v1/summary",
    "/health", "/api/v1/health", "/status",
    "/api/v1/coins", "/api/v1/crypto",
    "/api/v1/rates", "/api/v1/fx",
    "/v1/quote/{ticker}", "/v1/{ticker}",
]

# Known field mappings for auto-detection
FIELD_MAPPINGS: dict[str, str] = {
    "close": "price", "closing_price": "price", "last": "price",
    "regularMarketPrice": "price", "currentPrice": "price",
    "bid": "price", "ask": "price", "lastPrice": "price",
    "symbol": "ticker", "ticker": "ticker", "instrument": "ticker",
    "open": "open", "opening_price": "open",
    "high": "high", "day_high": "high", "dayHigh": "high",
    "low": "low", "day_low": "low", "dayLow": "low",
    "volume": "volume", "vol": "volume",
    "previous_close": "previous_close", "prev_close": "previous_close",
    "change": "change", "change_amount": "change",
    "percent_change": "change_pct", "changePercent": "change_pct",
    "change_pct": "change_pct",
    "timestamp": "timestamp", "date": "timestamp", "datetime": "timestamp",
    "time": "timestamp", "created_at": "timestamp",
}


def _detect_fields(data: dict) -> dict[str, str]:
    """Try to map fields from a data response to known Miau models."""
    mapped = {}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in FIELD_MAPPINGS:
            mapped[key] = FIELD_MAPPINGS[key_lower]
        elif isinstance(value, (int, float)):
            # Try fuzzy detection
            for raw, standard in FIELD_MAPPINGS.items():
                if raw in key_lower or key_lower in raw:
                    mapped[key] = standard
                    break
    return mapped


def _detect_data_type(mapped: dict) -> str:
    """Detect what type of data this looks like."""
    if "price" in mapped.values() and "ticker" in mapped.values():
        return "Quote"
    if "open" in mapped.values() and "close" in mapped.values() and "high" in mapped.values():
        return "OHLCV"
    return "Unknown"


def _basic_analysis(values: list[float]) -> dict:
    """Run simple analysis on numeric data."""
    if not values or len(values) < 2:
        return {}
    import statistics, math
    mean = statistics.mean(values)
    median = statistics.median(values)
    min_v = min(values)
    max_v = max(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0
    trend = "up" if values[-1] > values[0] else "down"
    change = values[-1] - values[0]
    change_pct = (change / values[0] * 100) if values[0] != 0 else 0
    return {
        "mean": round(mean, 4),
        "median": round(median, 4),
        "min": round(min_v, 4),
        "max": round(max_v, 4),
        "std_dev": round(stdev, 4),
        "trend": trend,
        "change": round(change, 4),
        "change_pct": round(change_pct, 2),
        "data_points": len(values),
    }


def _simple_forecast(values: list[float], steps: int = 10) -> list[float]:
    """Simple linear forecast."""
    if len(values) < 2:
        return []
    import numpy as np
    x = np.arange(len(values))
    slope, intercept = np.polyfit(x, values, 1)
    pred_x = np.arange(len(values), len(values) + steps)
    return [float(slope * px + intercept) for px in pred_x]


async def auto_integrate(url: str, api_key: Optional[str] = None, ticker: str = "AAPL") -> dict:
    """Probe a URL, detect its API structure, and analyze the data.

    Args:
        url: Base URL of the API (e.g. https://api.example.com)
        api_key: Optional API key
        ticker: Ticker symbol to use for probe requests

    Returns:
        dict with probe results, detected models, and analysis
    """
    results = {
        "url": url,
        "probed_endpoints": [],
        "successful_endpoints": [],
        "detected_models": [],
        "analysis": {},
        "recommendation": "",
        "error": None,
    }

    probe_ticker = ticker.upper()
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["X-API-Key"] = api_key

    async with httpx.AsyncClient(timeout=8, headers=headers) as client:
        for path_template in PROBE_PATHS:
            path = path_template.replace("{ticker}", probe_ticker)
            full_url = url.rstrip("/") + path
            results["probed_endpoints"].append(path)
            try:
                r = await client.get(full_url)
                if r.status_code < 500:
                    data = r.json()
                    results["successful_endpoints"].append(path)
                    if isinstance(data, dict):
                        mapped = _detect_fields(data)
                        data_type = _detect_data_type(mapped)
                        model_info = {
                            "endpoint": path,
                            "status": r.status_code,
                            "detected_type": data_type,
                            "field_mappings": mapped,
                        }
                        results["detected_models"].append(model_info)

                        # If we found price-like data, add analysis
                        price_keys = [k for k, v in mapped.items() if v in ("price", "close")]
                        if price_keys and data.get(price_keys[0]):
                            price = data[price_keys[0]]
                            if isinstance(price, (int, float)):
                                results["analysis"]["current_price"] = float(price)
                                results["analysis"]["detected_ticker"] = data.get("symbol", data.get("ticker", probe_ticker))

                        # If we got a list or timeseries, analyze it
                        for key, val in data.items():
                            if isinstance(val, list) and len(val) > 1:
                                numeric = [v if isinstance(v, (int, float)) else v.get("close") or v.get("price") or v.get("value") for v in val[:100]]
                                numeric_f = [float(x) for x in numeric if isinstance(x, (int, float))]
                                if len(numeric_f) >= 3:
                                    analysis = _basic_analysis(numeric_f)
                                    analysis["forecast"] = _simple_forecast(numeric_f, 10)
                                    results["analysis"]["series_analysis"] = analysis
                    elif isinstance(data, list) and len(data) > 0:
                        if isinstance(data[0], dict):
                            mapped = _detect_fields(data[0])
                            results["detected_models"].append({
                                "endpoint": path,
                                "status": r.status_code,
                                "detected_type": "List<" + _detect_data_type(mapped) + ">",
                                "field_mappings": mapped,
                                "items": len(data),
                            })
            except (httpx.TimeoutException, httpx.RequestError, json.JSONDecodeError, Exception):
                continue

    # Generate recommendation
    if results["detected_models"]:
        results["recommendation"] = f"Found {len(results['detected_models'])} usable endpoints. Best match: {results['detected_models'][0]['detected_type']} at {results['detected_models'][0]['endpoint']}"
        if results["analysis"]:
            results["recommendation"] += ". Analysis available."
    else:
        results["recommendation"] = "No compatible endpoints detected. The API structure may be incompatible with Miau Finance models."
        results["error"] = "No endpoints matched known patterns"

    results["endpoints_tested"] = len(results["probed_endpoints"])
    results["endpoints_found"] = len(results["successful_endpoints"])
    return results
