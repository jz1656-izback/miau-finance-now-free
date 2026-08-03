import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

EXCHANGES = {
    "TSE": {"name": "Tokyo Stock Exchange", "suffix": ".T", "country": "Japan", "tz": "Asia/Tokyo"},
    "HKEX": {"name": "Hong Kong Exchange", "suffix": ".HK", "country": "Hong Kong", "tz": "Asia/Hong_Kong"},
    "SSE": {"name": "Shanghai Stock Exchange", "suffix": ".SS", "country": "China", "tz": "Asia/Shanghai"},
    "NSE": {"name": "National Stock Exchange of India", "suffix": ".NS", "country": "India", "tz": "Asia/Kolkata"},
    "ASX": {"name": "Australian Securities Exchange", "suffix": ".AX", "country": "Australia", "tz": "Australia/Sydney"},
    "KRX": {"name": "Korea Exchange", "suffix": ".KS", "country": "South Korea", "tz": "Asia/Seoul"},
    "SGX": {"name": "Singapore Exchange", "suffix": ".SI", "country": "Singapore", "tz": "Asia/Singapore"},
    "TWSE": {"name": "Taiwan Stock Exchange", "suffix": ".TW", "country": "Taiwan", "tz": "Asia/Taipei"},
    "SET": {"name": "Stock Exchange of Thailand", "suffix": ".BK", "country": "Thailand", "tz": "Asia/Bangkok"},
    "IDX": {"name": "Indonesia Stock Exchange", "suffix": ".JK", "country": "Indonesia", "tz": "Asia/Jakarta"},
    "PSE": {"name": "Philippine Stock Exchange", "suffix": ".PS", "country": "Philippines", "tz": "Asia/Manila"},
}

BENCHMARKS = {
    "TSE": "^N225",
    "HKEX": "^HSI",
    "SSE": "000001.SS",
    "NSE": "^NSEI",
    "ASX": "^AXJO",
    "KRX": "^KS11",
    "SGX": "^STI",
    "TWSE": "^TWII",
    "SET": "^SET.BK",
    "IDX": "^JKSE",
    "PSE": "^PSI",
}

MARKER_TICKERS = {
    "TSE": ["7203.T", "9984.T", "6758.T"],
    "HKEX": ["0700.HK", "9988.HK", "0005.HK"],
    "SSE": ["600519.SS", "601398.SS", "601939.SS"],
    "NSE": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"],
    "ASX": ["BHP.AX", "CBA.AX", "CSL.AX"],
    "KRX": ["005930.KS", "000660.KS", "207940.KS"],
    "SGX": ["D05.SI", "C31.SI", "Z74.SI"],
    "TWSE": ["2330.TW", "2317.TW", "2454.TW"],
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
        logger.warning("Failed to fetch Asian benchmarks: %s", e)

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
        "TSE": "JPY", "HKEX": "HKD", "SSE": "CNY", "NSE": "INR",
        "ASX": "AUD", "KRX": "KRW", "SGX": "SGD", "TWSE": "TWD",
        "SET": "THB", "IDX": "IDR", "PSE": "PHP",
    }
    return currencies.get(code, "USD")
