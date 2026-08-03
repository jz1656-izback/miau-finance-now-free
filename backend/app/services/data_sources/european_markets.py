import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

EXCHANGES = {
    "LSE": {"name": "London Stock Exchange", "suffix": ".L", "country": "United Kingdom", "tz": "Europe/London"},
    "EURONEXT": {"name": "Euronext", "suffix": ".PA", "country": "France", "tz": "Europe/Paris"},
    "XETRA": {"name": "Xetra (Deutsche Börse)", "suffix": ".DE", "country": "Germany", "tz": "Europe/Berlin"},
    "SIX": {"name": "SIX Swiss Exchange", "suffix": ".SW", "country": "Switzerland", "tz": "Europe/Zurich"},
    "BME": {"name": "BME (Bolsa de Madrid)", "suffix": ".MC", "country": "Spain", "tz": "Europe/Madrid"},
    "BIT": {"name": "Borsa Italiana", "suffix": ".MI", "country": "Italy", "tz": "Europe/Rome"},
    "OMX_ST": {"name": "Nasdaq Stockholm", "suffix": ".ST", "country": "Sweden", "tz": "Europe/Stockholm"},
    "OMX_CO": {"name": "Nasdaq Copenhagen", "suffix": ".CO", "country": "Denmark", "tz": "Europe/Copenhagen"},
    "OMX_HE": {"name": "Nasdaq Helsinki", "suffix": ".HE", "country": "Finland", "tz": "Europe/Helsinki"},
    "OSE": {"name": "Oslo Børs", "suffix": ".OL", "country": "Norway", "tz": "Europe/Oslo"},
    "EURONEXT_AMS": {"name": "Euronext Amsterdam", "suffix": ".AS", "country": "Netherlands", "tz": "Europe/Amsterdam"},
    "EURONEXT_BR": {"name": "Euronext Brussels", "suffix": ".BR", "country": "Belgium", "tz": "Europe/Brussels"},
    "WSE": {"name": "Warsaw Stock Exchange", "suffix": ".WA", "country": "Poland", "tz": "Europe/Warsaw"},
    "VIE": {"name": "Wiener Börse", "suffix": ".VI", "country": "Austria", "tz": "Europe/Vienna"},
}

BENCHMARKS = {
    "LSE": "^FTSE",
    "EURONEXT": "^FCHI",
    "XETRA": "^GDAXI",
    "SIX": "^SSMI",
    "BME": "^IBEX",
    "BIT": "^FTMIB",
    "OMX_ST": "^OMX",
    "OMX_CO": "^OMXC25",
    "OMX_HE": "^OMXH25",
    "OSE": "^OSEAX",
    "EURONEXT_AMS": "^AEX",
    "EURONEXT_BR": "^BFX",
    "WSE": "^WIG20",
    "VIE": "^ATX",
}

MARKER_TICKERS = {
    "LSE": ["HSBA.L", "AZN.L", "SHEL.L"],
    "EURONEXT": ["MC.PA", "OR.PA", "AI.PA"],
    "XETRA": ["SAP.DE", "DTE.DE", "ALV.DE"],
    "SIX": ["NESN.SW", "ROG.SW", "NOVN.SW"],
    "BME": ["SAN.MC", "BBVA.MC", "TEF.MC"],
    "BIT": ["ENEL.MI", "UCG.MI", "ISP.MI"],
    "OMX_ST": ["SEB-A.ST", "ERIC-B.ST", "VOLV-B.ST"],
    "OMX_CO": ["NOVO-B.CO", "MAERSK-A.CO", "DSV.CO"],
    "OMX_HE": ["NOKIA.HE", "SAMPO.HE", "STERV.HE"],
    "OSE": ["EQNR.OL", "DNB.OL", "NHY.OL"],
    "EURONEXT_AMS": ["ASML.AS", "ADYEN.AS", "INGA.AS"],
    "EURONEXT_BR": ["ABI.BR", "UCB.BR", "KBC.BR"],
    "WSE": ["PZU.WA", "PKO.WA", "PEO.WA"],
    "VIE": ["EBS.VI", "RBI.VI", "VOE.VI"],
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
        logger.warning("Failed to fetch European benchmarks: %s", e)

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
        "LSE": "GBP", "EURONEXT": "EUR", "XETRA": "EUR", "SIX": "CHF",
        "BME": "EUR", "BIT": "EUR", "OMX_ST": "SEK", "OMX_CO": "DKK",
        "OMX_HE": "EUR", "OSE": "NOK", "EURONEXT_AMS": "EUR",
        "EURONEXT_BR": "EUR", "WSE": "PLN", "VIE": "EUR",
    }
    return currencies.get(code, "EUR")
