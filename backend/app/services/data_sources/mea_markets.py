import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

EXCHANGES = {
    "DFM": {"name": "Dubai Financial Market", "suffix": ".DU", "country": "UAE", "tz": "Asia/Dubai"},
    "ADX": {"name": "Abu Dhabi Securities Exchange", "suffix": ".AU", "country": "UAE", "tz": "Asia/Dubai"},
    "TADAWUL": {"name": "Saudi Stock Exchange (Tadawul)", "suffix": ".SR", "country": "Saudi Arabia", "tz": "Asia/Riyadh"},
    "QE": {"name": "Qatar Stock Exchange", "suffix": ".QA", "country": "Qatar", "tz": "Asia/Qatar"},
    "JSE": {"name": "Johannesburg Stock Exchange", "suffix": ".JO", "country": "South Africa", "tz": "Africa/Johannesburg"},
    "NSE_NG": {"name": "Nigerian Exchange Group", "suffix": ".NG", "country": "Nigeria", "tz": "Africa/Lagos"},
    "EGX": {"name": "Egyptian Exchange", "suffix": ".CA", "country": "Egypt", "tz": "Africa/Cairo"},
    "KSE": {"name": "Kenya Securities Exchange", "suffix": ".NR", "country": "Kenya", "tz": "Africa/Nairobi"},
    "ISE": {"name": "Tel Aviv Stock Exchange", "suffix": ".TA", "country": "Israel", "tz": "Asia/Jerusalem"},
}

BENCHMARKS = {
    "DFM": "^DFMGI",
    "ADX": "^FTFADX",
    "TADAWUL": "^TASI",
    "QE": "^QSI",
    "JSE": "^J203",
    "NSE_NG": "^NGSEIND",
    "EGX": "^EGX30",
    "KSE": "^NSEASI",
    "ISE": "^TA125",
}

MARKER_TICKERS = {
    "DFM": ["EMAAR.DU", "DEWA.DU", "DUBAI.DU"],
    "ADX": ["FAB.AU", "ADNOC.AU", "ADIB.AU"],
    "TADAWUL": ["2222.SR", "1120.SR", "1010.SR"],
    "QE": ["QNBK.QA", "QIIK.QA", "IQCD.QA"],
    "JSE": ["NPN.JO", "AGL.JO", "FSR.JO"],
    "NSE_NG": ["MTNN.NG", "DANGCEM.NG", "ZENITH.NG"],
    "EGX": ["COMI.CA", "HRHO.CA", "EMFD.CA"],
    "KSE": ["SCOM.NR", "KCB.NR", "EABL.NR"],
    "ISE": ["AZN.TA", "TEVA.TA", "NICE.TA"],
}

_cache: dict[str, dict] = {}
_last_fetch: Optional[datetime] = None


async def get_benchmarks() -> list[dict]:
    global _cache, _last_fetch
    now = datetime.now()
    if _last_fetch and (now - _last_fetch).seconds < 300:
        return list(_cache.values())

    results = []
    try:
        import yfinance as yf
        codes = list(BENCHMARKS.values())
        data = yf.download(codes, period="5d", progress=False)
        if data is not None and not data.empty:
            close = data["Close"] if "Close" in data else data
            for code, yahoo_ticker in BENCHMARKS.items():
                exch = EXCHANGES[code]
                price = None
                change_pct = None
                if yahoo_ticker in close.columns:
                    vals = close[yahoo_ticker].dropna()
                    if len(vals) >= 1:
                        price = float(vals.iloc[-1])
                    if len(vals) >= 2:
                        prev = float(vals.iloc[-2])
                        change_pct = round((price / prev - 1) * 100, 2) if prev else None
                results.append({
                    "code": code,
                    "name": exch["name"],
                    "country": exch["country"],
                    "benchmark": yahoo_ticker,
                    "price": price,
                    "change_pct": change_pct,
                    "currency": _get_currency(code),
                })
    except Exception as e:
        logger.warning("Failed to fetch MEA benchmarks: %s", e)

    if results:
        _cache = {r["code"]: r for r in results}
        _last_fetch = now
    return results or list(_cache.values())


async def get_market_data() -> list[dict]:
    results = []
    for code, exchange in EXCHANGES.items():
        tickers = MARKER_TICKERS.get(code, [])
        stocks = []
        for ticker in tickers:
            try:
                import yfinance as yf
                t = yf.Ticker(ticker)
                hist = t.history(period="5d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])
                    prev = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else price
                    change = round((price / prev - 1) * 100, 2) if prev else 0
                    stocks.append({
                        "symbol": ticker,
                        "price": price,
                        "change_pct": change,
                    })
            except Exception as e:
                logger.debug("Failed to fetch %s: %s", ticker, e)
        results.append({
            "code": code,
            "name": exchange["name"],
            "country": exchange["country"],
            "stocks": stocks,
        })
    return results


async def get_index_history(code: str, period: str = "1mo") -> list[dict]:
    yahoo_ticker = BENCHMARKS.get(code)
    if not yahoo_ticker:
        return []
    try:
        import yfinance as yf
        t = yf.Ticker(yahoo_ticker)
        hist = t.history(period=period)
        if hist.empty:
            return []
        return [
            {
                "date": str(d.date()),
                "close": float(row["Close"]),
                "volume": int(row["Volume"]),
            }
            for d, row in hist.iterrows()
        ]
    except Exception as e:
        logger.warning("Failed to fetch index history for %s: %s", code, e)
        return []


def _get_currency(code: str) -> str:
    currencies = {
        "DFM": "AED", "ADX": "AED", "TADAWUL": "SAR", "QE": "QAR",
        "JSE": "ZAR", "NSE_NG": "NGN", "EGX": "EGP", "KSE": "KES",
        "ISE": "ILS",
    }
    return currencies.get(code, "USD")
