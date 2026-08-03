import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

EXCHANGES = {
    "B3": {"name": "B3 (Brasil Bolsa Balcão)", "suffix": ".SA", "country": "Brazil", "tz": "America/Sao_Paulo"},
    "BMV": {"name": "Bolsa Mexicana de Valores", "suffix": ".MX", "country": "Mexico", "tz": "America/Mexico_City"},
    "BCS": {"name": "Bolsa de Comercio de Santiago", "suffix": ".SN", "country": "Chile", "tz": "America/Santiago"},
    "MERVAL": {"name": "Bolsa de Comercio de Buenos Aires", "suffix": ".BA", "country": "Argentina", "tz": "America/Argentina/Buenos_Aires"},
    "BVC": {"name": "Bolsa de Valores de Colombia", "suffix": ".CN", "country": "Colombia", "tz": "America/Bogota"},
    "BVL": {"name": "Bolsa de Valores de Lima", "suffix": ".LM", "country": "Peru", "tz": "America/Lima"},
}

BENCHMARKS = {
    "B3": "^BVSP",
    "BMV": "^MXX",
    "BCS": "^IPSA",
    "MERVAL": "^MERV",
    "BVC": "^COLCAP",
    "BVL": "^SPBLPGPT",
}

MARKER_TICKERS = {
    "B3": ["PETR4.SA", "VALE3.SA", "ITUB4.SA"],
    "BMV": ["AMXL.MX", "CEMEXCPO.MX", "FEMSAUBD.MX"],
    "BCS": ["COPEC.SN", "BSANTANDER.SN", "SONDA.SN"],
    "MERVAL": ["GGAL.BA", "YPFD.BA", "PAMP.BA"],
    "BVC": ["ECOPETROL.CN", "PFBCOLOM.CN", "NUTRESA.CN"],
    "BVL": ["BVN.LM", "CRETC1.LM", "ALICORC1.LM"],
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
        logger.warning("Failed to fetch LatAm benchmarks: %s", e)

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
        "B3": "BRL", "BMV": "MXN", "BCS": "CLP",
        "MERVAL": "ARS", "BVC": "COP", "BVL": "PEN",
    }
    return currencies.get(code, "USD")
