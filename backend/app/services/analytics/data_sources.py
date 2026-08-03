import statistics

import httpx
import json
from datetime import datetime, timedelta
from typing import Any, Optional

from app.cache_utils import cached


@cached(ttl=60, prefix="crypto_price")
async def coingecko_coin_price(coin_id: str = "bitcoin", vs_currency: str = "usd") -> dict:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={vs_currency}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
    try:
        async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json().get(coin_id, {})
                return {
                    "coin": coin_id,
                    "price": data.get(vs_currency),
                    "change_24h_pct": data.get(f"{vs_currency}_24h_change"),
                    "market_cap": data.get(f"{vs_currency}_market_cap"),
                    "volume_24h": data.get(f"{vs_currency}_24h_vol"),
                    "currency": vs_currency.upper(),
                    "source": "CoinGecko",
                }
            return {"coin": coin_id, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"coin": coin_id, "error": str(e)}


@cached(ttl=300, prefix="crypto_market")
async def coingecko_market(currency: str = "usd") -> dict:
    url = f"https://api.coingecko.com/api/v3/global"
    try:
        async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json().get("data", {})
                btc_dominance = round(data.get("market_cap_percentage", {}).get("btc", 0), 2)
                total_mcap = round(data.get("total_market_cap", {}).get(currency, 0) / 1e12, 2)
                total_vol = round(data.get("total_volume", {}).get(currency, 0) / 1e12, 2)
                return {
                    "total_market_cap_trillions": total_mcap,
                    "total_volume_24h_trillions": total_vol,
                    "btc_dominance_pct": btc_dominance,
                    "active_cryptos": data.get("active_cryptocurrencies", 0),
                    "markets": data.get("markets", 0),
                    "source": "CoinGecko",
                    "as_of": datetime.now().isoformat(),
                }
            return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@cached(ttl=300, prefix="crypto_top")
async def coingecko_top_coins(limit: int = 20, currency: str = "usd") -> list:
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false&price_change_percentage=24h"
    try:
        async with httpx.AsyncClient(timeout=20, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                coins = r.json()
                return [
                    {
                        "rank": c.get("market_cap_rank"),
                        "name": c.get("name"),
                        "symbol": c.get("symbol", "").upper(),
                        "price": round(c.get("current_price", 0), 6),
                        "market_cap": c.get("market_cap", 0),
                        "volume_24h": c.get("total_volume", 0),
                        "change_24h_pct": round(c.get("price_change_percentage_24h", 0), 2),
                        "high_24h": c.get("high_24h"),
                        "low_24h": c.get("low_24h"),
                        "circulating_supply": c.get("circulating_supply"),
                    }
                    for c in coins
                ]
            return [{"error": f"HTTP {r.status_code}"}]
    except Exception as e:
        return [{"error": str(e)}]


@cached(ttl=3600, prefix="crypto_hist")
async def coingecko_historical(coin_id: str = "bitcoin", days: int = 30, currency: str = "usd") -> dict:
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={days}"
    try:
        async with httpx.AsyncClient(timeout=20, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json()
                prices = []
                for ts, price in data.get("prices", []):
                    prices.append({
                        "date": datetime.fromtimestamp(ts / 1000).isoformat(),
                        "price": round(price, 6),
                    })
                return {
                    "coin": coin_id,
                    "currency": currency.upper(),
                    "days": days,
                    "prices": prices,
                    "source": "CoinGecko",
                }
            return {"coin": coin_id, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"coin": coin_id, "error": str(e)}


@cached(ttl=600, prefix="fx")
async def exchange_rate(base: str = "USD", targets: Optional[list[str]] = None) -> dict:
    if targets is None:
        targets = ["EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY", "INR", "BRL", "MXN"]
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json()
                rates = data.get("rates", {})
                result = {"base": base, "date": data.get("date"), "rates": {}}
                for t in targets:
                    if t in rates:
                        result["rates"][t] = rates[t]
                return result
            return {"base": base, "error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"base": base, "error": str(e)}


@cached(ttl=3600, prefix="fear_greed")
async def bitcoin_fear_greed_index() -> dict:
    url = "https://api.alternative.me/fng/?limit=1"
    try:
        async with httpx.AsyncClient(timeout=15, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json().get("data", [{}])[0]
                return {
                    "value": int(data.get("value", 50)),
                    "classification": data.get("value_classification", "Neutral"),
                    "timestamp": datetime.fromtimestamp(int(data.get("timestamp", 0))).isoformat(),
                    "source": "Alternative.me",
                }
            return {"error": f"HTTP {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@cached(ttl=300, prefix="indicators")
async def us_indicators() -> dict:
    results = {}
    async with httpx.AsyncClient(timeout=20, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
        # S&P 500
        try:
            r = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC", timeout=10)
            if r.status_code == 200:
                data = r.json()
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                q = meta.get("regularMarketPrice", 0)
                prev = meta.get("previousClose", 0)
                results["sp500"] = {
                    "value": round(q, 2),
                    "change": round(q - prev, 2),
                    "change_pct": round((q - prev) / prev * 100, 2),
                }
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError, ValueError):
            results["sp500"] = {"error": "Could not fetch"}

        # VIX
        try:
            r = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX", timeout=10)
            if r.status_code == 200:
                data = r.json()
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                results["vix"] = {"value": round(meta.get("regularMarketPrice", 0), 2)}
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError, ValueError):
            results["vix"] = {"error": "Could not fetch"}

        # 10Y Treasury Yield
        try:
            r = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ETNX", timeout=10)
            if r.status_code == 200:
                data = r.json()
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                results["treasury_10y"] = {"value": round(meta.get("regularMarketPrice", 0), 2)}
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError, ValueError):
            results["treasury_10y"] = {"error": "Could not fetch"}

        # DXY (Dollar Index)
        try:
            r = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/DX-Y.NYB", timeout=10)
            if r.status_code == 200:
                data = r.json()
                meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                results["dxy"] = {"value": round(meta.get("regularMarketPrice", 0), 2)}
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError, ValueError):
            results["dxy"] = {"error": "Could not fetch"}

    return results


@cached(ttl=300, prefix="sectors")
async def sector_performance() -> list:
    sectors = {"XLF": "Financials", "XLK": "Technology", "XLE": "Energy",
               "XLV": "Healthcare", "XLI": "Industrials", "XLP": "Consumer Staples",
               "XLY": "Consumer Discretionary", "XLB": "Materials", "XLU": "Utilities",
               "XLRE": "Real Estate"}
    results = []
    for ticker, name in sectors.items():
        try:
            async with httpx.AsyncClient(timeout=10, transport=httpx.AsyncHTTPTransport(local_address="0.0.0.0")) as client:
                r = await client.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}", timeout=10)
                if r.status_code == 200:
                    data = r.json()
                    meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
                    q = meta.get("regularMarketPrice", 0)
                    prev = meta.get("previousClose", 0)
                    if q and prev:
                        results.append({
                            "ticker": ticker,
                            "name": name,
                            "price": round(q, 2),
                            "change_pct": round((q - prev) / prev * 100, 2),
                        })
        except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError, ValueError):
            pass
    return sorted(results, key=lambda x: abs(x.get("change_pct", 0)), reverse=True)


def detect_outliers(
    data: list[float],
    method: str = "zscore",
    threshold: float = 3.0,
) -> dict[str, Any]:
    """Detect outliers in a list of numeric values.

    Supports two methods:
      - 'zscore': flags values where |z-score| > threshold
      - 'iqr':    flags values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]

    Args:
        data: List of numeric values.
        method: 'zscore' or 'iqr'. Default 'zscore'.
        threshold: Z-score threshold (ignored for IQR). Default 3.0.

    Returns:
        Dict with:
          - 'outlier_indices': list of int indices
          - 'outlier_values': list of float values
          - 'method': method used
          - 'threshold': threshold used
          - 'total': total data points
          - 'outlier_count': number of outliers found
    """
    if not data:
        return {
            "outlier_indices": [],
            "outlier_values": [],
            "method": method,
            "threshold": threshold,
            "total": 0,
            "outlier_count": 0,
        }

    if method == "zscore":
        mean = statistics.mean(data)
        stdev = statistics.stdev(data) if len(data) > 1 else 0.0
        if stdev == 0:
            return {
                "outlier_indices": [],
                "outlier_values": [],
                "method": method,
                "threshold": threshold,
                "total": len(data),
                "outlier_count": 0,
            }
        indices = [i for i, v in enumerate(data) if abs((v - mean) / stdev) > threshold]
        values = [data[i] for i in indices]

    elif method == "iqr":
        sorted_data = sorted(data)
        n = len(sorted_data)
        q1 = sorted_data[n // 4]
        q3 = sorted_data[(3 * n) // 4]
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        indices = [i for i, v in enumerate(data) if v < lower or v > upper]
        values = [data[i] for i in indices]

    else:
        raise ValueError(f"Unknown method '{method}'. Use 'zscore' or 'iqr'.")

    return {
        "outlier_indices": indices,
        "outlier_values": [round(v, 6) for v in values],
        "method": method,
        "threshold": threshold,
        "total": len(data),
        "outlier_count": len(indices),
    }
