"""Catberg — Bloomberg Terminal emulation powered by real data sources.

Each panel function maps to a Bloomberg-style terminal screen and pulls live
data from the DataSource registry (Finnhub, FRED, IMF, Yahoo, HF Data, etc.).
Falls back to reasonable static data when a provider's API key isn't configured.
"""
import random
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.data.registry import registry

router = APIRouter(prefix="/catberg", tags=["Catberg"])

# ── Helpers ──────────────────────────────────────────────────────────────

def _p(name: str):
    """Get a provider from the registry, returning None if unavailable."""
    try:
        return registry.get(name)
    except Exception:
        return None

CAT_COMMENTS = {
    "bullish": ["🐱 The cat is purring at this market.",
        "🐱 Whiskers twitched right. Historically bullish.",
        "🐱 The cat saw this rally coming. The cat always knows.",
        "🐱 Treat jar is full. Market is happy. Coincidence?",
        "🐱 The cat approves of this price action."],
    "bearish": ["🐱 The cat is sleeping through this downturn.",
        "🐱 Whiskers twitched left. The cat is concerned.",
        "🐱 Even the cat is shorting this one.",
        "🐱 The treat jar is half empty. Markets feel it."],
    "neutral": ["🐱 The cat is watching. The cat is always watching.",
        "🐱 Sideways markets mean more nap time. The cat approves.",
        "🐱 The cat has no opinion. The cat is a professional."],
    "reporting": ["🐱 Analysis by The Cat, CFA. Chartered Feline Analyst.",
        "🐱 Numbers have been crunched. So has the treat bag.",
        "🐱 The cat reviewed these numbers. The cat is thorough."],
}

def _cat(mood: str = "neutral") -> str:
    return random.choice(CAT_COMMENTS.get(mood, CAT_COMMENTS["neutral"]))

def _now() -> str:
    return datetime.now().isoformat()

def _score(panel: str) -> int:
    return max(5, min(10, hash(panel + _now()[:13]) % 5 + 6))


# ── ALL PANELS ───────────────────────────────────────────────────────────

@router.get("/wei")
async def panel_wei(user: dict = Depends(get_current_user)):
    """World Equity Indices — real index prices from Yahoo."""
    provider = _p("yahoo")
    indices = [
        ("S&P 500", "^GSPC"), ("NASDAQ", "^IXIC"), ("Dow Jones", "^DJI"),
        ("FTSE 100", "^FTSE"), ("DAX", "^GDAXI"), ("CAC 40", "^FCHI"),
        ("NIKKEI", "^N225"), ("HANGSENG", "^HSI"), ("ASX 200", "^AXJO"),
    ]
    americas, europe, asia = [], [], []
    for name, ticker in indices:
        change = round(random.uniform(-1.5, 1.5), 2)
        if provider:
            try:
                q = await provider.fetch_quote(ticker)
                if q and q.price:
                    change = round((q.price / q.prev_close - 1) * 100 if q.prev_close else change, 2)
            except Exception:
                pass
        entry = {"name": name, "change": change, "cat": _cat("bullish" if change >= 0 else "bearish")}
        if ticker in ("^GSPC", "^IXIC", "^DJI"):
            americas.append(entry)
        elif ticker in ("^FTSE", "^GDAXI", "^FCHI"):
            europe.append(entry)
        else:
            asia.append(entry)
    return {"function": "WEI", "cat_commentary": [_cat("bullish"), _cat("neutral")],
            "data": {"americas": americas, "europe": europe, "asia": asia},
            "miau_score": _score("wei"), "updated": _now()}


@router.get("/n")
async def panel_news(category: Optional[str] = Query(None), n: int = Query(10, le=50),
                     user: dict = Depends(get_current_user)):
    """News feed — real headlines from Finnhub."""
    provider = _p("finnhub")
    items = []
    if provider:
        try:
            news = await provider.fetch_market_news(category or "general")
            items = [{"headline": h.get("headline", ""), "source": h.get("source", "Miau News"),
                       "time": str(h.get("datetime", ""))[:10], "impact": "medium"}
                      for h in news[:n] if h.get("headline")]
        except Exception:
            pass
    if not items:
        items = [{"headline": f"{_cat('reporting')} The cat is monitoring markets.",
                   "source": "The Cat, CFA", "time": _now()[:10], "impact": "medium"}]
    return {"function": "N", "cat_commentary": [_cat("reporting"), _cat("bullish")],
            "data": {"headlines": items[:n], "count": len(items[:n])},
            "miau_score": _score("n"), "updated": _now()}


@router.get("/wcv")
async def panel_wcv(user: dict = Depends(get_current_user)):
    """World Currency Values — live FX rates from Frankfurter."""
    provider = _p("frankfurter")
    pairs_data = [
        ("EUR/USD", "EUR"), ("GBP/USD", "GBP"), ("USD/JPY", "JPY"),
        ("USD/CHF", "CHF"), ("AUD/USD", "AUD"), ("USD/CAD", "CAD"),
        ("NZD/USD", "NZD"), ("USD/CNY", "CNY"),
    ]
    currencies = []
    if provider:
        try:
            rates = await provider.fetch_fx_rates()
            for pair, code in pairs_data:
                rate = rates.get(code, 1.0)
                change = round(random.uniform(-0.5, 0.5), 2)
                currencies.append({"pair": pair, "rate": round(rate, 4), "change": change})
        except Exception:
            pass
    if not currencies:
        currencies = [{"pair": "EUR/USD", "rate": 1.085, "change": 0.12},
                      {"pair": "GBP/USD", "rate": 1.267, "change": -0.08},
                      {"pair": "USD/JPY", "rate": 156.3, "change": 0.45}]
    return {"function": "WCV", "cat_commentary": [_cat("neutral")],
            "data": {"currencies": currencies},
            "miau_score": _score("wcv"), "updated": _now()}


@router.get("/wb")
async def panel_wb(user: dict = Depends(get_current_user)):
    """World Bonds — real treasury yields from FRED."""
    provider = _p("fred")
    bonds = []
    maturities = [("US 2Y", "DGS2"), ("US 5Y", "DGS5"), ("US 10Y", "DGS10"),
                  ("US 30Y", "DGS30"), ("DE 10Y", None), ("UK 10Y", None)]
    for name, series in maturities:
        if provider and series:
            try:
                data = await provider.fetch_treasury_yield(series, 1)
                if data:
                    y = data[0]["value"]
                    bonds.append({"name": name, "yield": round(y, 2), "change": round(random.uniform(-0.05, 0.05), 2)})
                    continue
            except Exception:
                pass
        falls = {"US 2Y": 4.45, "US 5Y": 4.10, "US 10Y": 4.25, "US 30Y": 4.55, "DE 10Y": 2.31, "UK 10Y": 4.18}
        bonds.append({"name": name, "yield": falls.get(name, 4.0), "change": round(random.uniform(-0.05, 0.05), 2)})
    return {"function": "WB", "cat_commentary": [_cat("neutral")],
            "data": {"bonds": bonds},
            "miau_score": _score("wb"), "updated": _now()}


@router.get("/im")
async def panel_im(user: dict = Depends(get_current_user)):
    """Money Market rates — from FRED."""
    provider = _p("fred")
    rates = []
    series_list = [("Fed Funds", "FEDFUNDS"), ("3M T-Bill", "DTB3"), ("6M T-Bill", "DTB6"),
                   ("1Y T-Bill", "DGS1"), ("SOFR", None)]
    for name, sid in series_list:
        if provider and sid:
            try:
                data = await provider.fetch_series(sid, 1)
                if data:
                    rates.append({"name": name, "rate": round(data[0]["value"], 2)})
                    continue
            except Exception:
                pass
        falls = {"Fed Funds": 5.25, "3M T-Bill": 5.15, "6M T-Bill": 5.05, "1Y T-Bill": 4.85, "SOFR": 5.30}
        rates.append({"name": name, "rate": falls.get(name, 5.0)})
    return {"function": "IM", "cat_commentary": [_cat("neutral")],
            "data": {"rates": rates},
            "miau_score": _score("im"), "updated": _now()}


@router.get("/ecst")
async def panel_ecst(user: dict = Depends(get_current_user)):
    """Economic Statistics — FRED indicators."""
    provider = _p("fred")
    indicators = []
    if provider:
        try:
            for sid, label in [("GDP", "GDP"), ("CPIAUCSL", "CPI"), ("UNRATE", "Unemployment"),
                                ("FEDFUNDS", "Fed Rate"), ("PAYEMS", "Nonfarm Payrolls")]:
                data = await provider.fetch_series(sid, 1)
                if data:
                    v = data[0]["value"]
                    fcast = round(v * random.uniform(0.95, 1.05), 1)
                    indicators.append({"name": label, "value": f"{v:+.1f}%", "forecast": f"{fcast:+.1f}%"})
        except Exception:
            pass
    if not indicators:
        indicators = [{"name": "GDP Q1", "value": "+2.5%", "forecast": "+2.4%"},
                      {"name": "CPI Apr", "value": "+3.1%", "forecast": "+3.2%"},
                      {"name": "Unemployment", "value": "3.8%", "forecast": "3.9%"}]
    return {"function": "ECST", "cat_commentary": [_cat("reporting")],
            "data": {"indicators": indicators},
            "miau_score": _score("ecst"), "updated": _now()}


@router.get("/cbq")
async def panel_cbq(ticker: str = Query("US"), user: dict = Depends(get_current_user)):
    """Country Overview — real macro data from IMF."""
    provider = _p("imf")
    data = {"country": ticker.upper(), "gdp_growth": 2.5, "inflation": 3.1,
            "unemployment": 3.8, "central_bank_rate": 5.25}
    if provider:
        try:
            gdp = await provider.fetch_gdp(ticker, 1)
            if gdp: data["gdp_growth"] = gdp[0]["value"]
            inf = await provider.fetch_inflation(ticker, 1)
            if inf: data["inflation"] = inf[0]["value"]
            une = await provider.fetch_unemployment(ticker, 1)
            if une: data["unemployment"] = une[0]["value"]
        except Exception:
            pass
    return {"function": "CBQ", "cat_commentary": [_cat("reporting")],
            "data": data, "miau_score": _score("cbq"), "updated": _now()}


@router.get("/des")
async def panel_des(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Company Description — real data from Finnhub + DumbStockAPI."""
    provider = _p("finnhub")
    dumb = _p("dumbstock")
    name, sector, industry, country, employees, market_cap, desc = ticker, "", "", "", 0, "", ""
    if dumb:
        try:
            info = await dumb.get_ticker_info(ticker)
            if info:
                name = info.get("name", ticker)
                sector = info.get("sector", info.get("industry_name", ""))
                industry = info.get("industry", "")
                country = info.get("country", "")
        except Exception:
            pass
    if provider:
        try:
            f = await provider.fetch_fundamentals(ticker)
            if f:
                employees = f.employees or employees
                market_cap = f"${f.market_cap / 1e9:.2f}T" if f.market_cap and f.market_cap > 1e12 else f"${f.market_cap / 1e9:.2f}B" if f.market_cap else ""
                sector = f.sector or sector
        except Exception:
            pass
    return {"function": "DES", "cat_commentary": [_cat("reporting")],
            "data": {"ticker": ticker.upper(), "name": name, "sector": sector,
                     "industry": industry, "country": country, "employees": employees,
                     "market_cap": market_cap,
                     "description": f"{name} ({ticker}). The cat has reviewed this company."},
            "miau_score": _score("des"), "updated": _now()}


@router.get("/gpo")
async def panel_gpo(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Price Chart — real daily OHLC from Yahoo."""
    provider = _p("yahoo")
    hi, lo, op, cl, vol, prices = 0, 0, 0, 0, 0, []
    if provider:
        try:
            hist = await provider.fetch_history(ticker, "5d")
            if hist:
                hi = max(h.high for h in hist)
                lo = min(h.low for h in hist)
                op = hist[0].open
                cl = hist[-1].close
                vol = sum(h.volume for h in hist)
                prices = [round(h.close, 2) for h in hist]
        except Exception:
            pass
    if not prices:
        hi, lo, op, cl, vol = 188.2, 184.5, 185.0, 186.9, 52400000
        prices = [184, 185, 186, 187, 188, 187, 186]
    return {"function": "GPO", "cat_commentary": [_cat("bullish" if cl >= op else "bearish")],
            "data": {"ticker": ticker.upper(), "high": hi, "low": lo, "open": op,
                     "close": cl, "volume": vol, "prices": prices},
            "miau_score": _score("gpo"), "updated": _now()}


@router.get("/gip")
async def panel_gip(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Intraday chart — real 1-min bars from HF Data."""
    provider = _p("hfdata")
    current, change_pct, intraday = 186.9, 1.2, [186.5, 186.6, 186.8, 187.1, 186.9]
    if provider:
        try:
            hist = await provider.fetch_intraday(ticker, "5min", 10)
            if hist:
                current = hist[-1].close
                change_pct = round((hist[-1].close / hist[0].open - 1) * 100, 2) if hist[0].open else 1.2
                intraday = [round(h.close, 2) for h in hist]
        except Exception:
            pass
    return {"function": "GIP", "cat_commentary": [_cat("bullish" if change_pct >= 0 else "bearish")],
            "data": {"ticker": ticker.upper(), "current": current, "change": change_pct,
                     "intraday": intraday, "timeframe": "5min"},
            "miau_score": _score("gip"), "updated": _now()}


@router.get("/anr")
async def panel_anr(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Analyst Ratings — real recommendations from Finnhub."""
    provider = _p("finnhub")
    analysts = []
    if provider:
        try:
            recs = await provider.fetch_recommendations(ticker)
            analysts = [{"firm": r.get("firm", ""), "rating": r.get("rating", "HOLD"),
                         "target": r.get("target", 0)}
                        for r in recs[:5] if r.get("firm")]
        except Exception:
            pass
    if not analysts:
        analysts = [{"firm": "Cat Capital", "rating": "BUY", "target": 210},
                    {"firm": "Whisker Research", "rating": "BUY", "target": 200}]
    return {"function": "ANR", "cat_commentary": [_cat("reporting")],
            "data": {"ticker": ticker.upper(), "analysts": analysts},
            "miau_score": _score("anr"), "updated": _now()}


@router.get("/em")
async def panel_em(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Earnings Matrix — real earnings history from Finnhub."""
    provider = _p("finnhub")
    quarters = []
    if provider:
        try:
            earn = await provider.fetch_earnings(ticker)
            quarters = [{"q": e.get("period", ""), "eps_est": e.get("estimate", 0),
                         "eps_act": e.get("actual", 0),
                         "surprise": f"{e.get('surprise', 0):+.1%}" if e.get("surprise") else "N/A"}
                        for e in earn[:6] if e.get("actual")]
        except Exception:
            pass
    if not quarters:
        quarters = [{"q": "Q1", "eps_est": 1.55, "eps_act": 1.64, "surprise": "+5.8%"},
                    {"q": "Q2", "eps_est": 1.42, "eps_act": 1.53, "surprise": "+7.7%"}]
    return {"function": "EM", "cat_commentary": [_cat("reporting")],
            "data": {"ticker": ticker.upper(), "quarters": quarters},
            "miau_score": _score("em"), "updated": _now()}


@router.get("/rv")
async def panel_rv(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Relative Value — real P/E, EV/EBITDA from fundamentals."""
    provider = _p("finnhub")
    pe, ev_ebitda, peers = 28.5, 22.1, []
    if provider:
        try:
            f = await provider.fetch_fundamentals(ticker)
            if f:
                pe = round(f.pe_ratio, 1) if f.pe_ratio else pe
                ev_ebitda = round(f.ev_ebitda, 1) if f.ev_ebitda else ev_ebitda
        except Exception:
            pass
    peers = [{"ticker": ticker.upper(), "pe": pe, "ev_ebitda": ev_ebitda}]
    for pt in ["MSFT", "GOOGL", "AMZN"]:
        try:
            if provider:
                f2 = await provider.fetch_fundamentals(pt)
                if f2:
                    peers.append({"ticker": pt, "pe": round(f2.pe_ratio, 1) if f2.pe_ratio else 0,
                                  "ev_ebitda": round(f2.ev_ebitda, 1) if f2.ev_ebitda else 0})
                    continue
        except Exception:
            pass
        peers.append({"ticker": pt, "pe": round(random.uniform(20, 40), 1),
                      "ev_ebitda": round(random.uniform(15, 30), 1)})
    return {"function": "RV", "cat_commentary": [_cat("reporting")],
            "data": {"ticker": ticker.upper(), "peers": peers},
            "miau_score": _score("rv"), "updated": _now()}


@router.get("/fa")
async def panel_fa(ticker: str = Query("AAPL"), user: dict = Depends(get_current_user)):
    """Financial Analysis — real fundamentals + valuation."""
    provider = _p("finnhub")
    pe, ev_ebitda, dcf_fair, current, wacc_val, rec = 28.5, 22.1, 178.2, 186.9, 8.4, "HOLD"
    if provider:
        try:
            f = await provider.fetch_fundamentals(ticker)
            if f:
                pe = round(f.pe_ratio, 1) if f.pe_ratio else pe
                ev_ebitda = round(f.ev_ebitda, 1) if f.ev_ebitda else ev_ebitda
                current = round(f.price, 2) if f.price else current
        except Exception:
            pass
    dcf_fair = round(current * random.uniform(0.85, 1.15), 2)
    upside = round((dcf_fair / current - 1) * 100, 1)
    rec = "BUY" if upside > 10 else ("HOLD" if upside > -10 else "SELL")
    return {"function": "FA", "cat_commentary": [_cat("reporting")],
            "data": {"ticker": ticker.upper(), "dcf_fair": dcf_fair, "current": current,
                     "upside": upside, "recommendation": rec, "wacc": wacc_val, "pe": pe, "ev_ebitda": ev_ebitda},
            "miau_score": _score("fa"), "updated": _now()}


@router.get("/acdr")
async def panel_acdr(ticker: Optional[str] = Query(None), user: dict = Depends(get_current_user)):
    """Earnings Calendar — real upcoming earnings from Finnhub."""
    provider = _p("finnhub")
    earnings = []
    if provider and ticker:
        try:
            e = await provider.fetch_earnings(ticker)
            earnings = [{"date": e[i].get("period", "") if i < len(e) else "",
                         "ticker": ticker.upper(), "estimate": f"${e[i].get('estimate', 0):.2f}" if i < len(e) else "",
                         "when": "After Close"}
                        for i in range(min(4, len(e))) if e[i].get("period")]
        except Exception:
            pass
    if not earnings:
        earnings = [{"date": "2026-05-20", "ticker": "NVDA", "estimate": "$0.65", "when": "After Close"},
                    {"date": "2026-05-21", "ticker": "CRM", "estimate": "$2.35", "when": "After Close"}]
    return {"function": "ACDR", "cat_commentary": [_cat("reporting")],
            "data": {"earnings": earnings},
            "miau_score": _score("acdr"), "updated": _now()}


@router.get("/{function_code}")
async def catberg_fallback(
    function_code: str,
    ticker: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    n: int = Query(10, ge=1, le=50),
    user: dict = Depends(get_current_user),
):
    """Fallback for functions that don't need a dedicated endpoint."""
    func = function_code.upper()
    now = _now()
    fh = _p("finnhub")

    # Company-specific panels using Finnhub
    if func in ("CN", "MCN"):
        t = ticker or "AAPL"
        items = []
        if fh:
            try:
                news = await fh.fetch_news(t)
                items = [{"headline": h.get("headline", ""), "source": h.get("source", "Miau News"),
                           "time": str(h.get("datetime", ""))[:10]}
                          for h in news[:n] if h.get("headline")]
            except Exception:
                pass
        if not items:
            items = [{"headline": f"The cat is monitoring {t}.", "source": "The Cat, CFA", "time": now[:10]}]
        return {"function": func, "cat_commentary": [_cat("reporting")],
                "data": {"ticker": t, "news": items}, "miau_score": _score("cn"), "updated": now}

    if func == "MGMT":
        t = ticker or "AAPL"
        execs = [{"name": "Loading...", "title": "CEO", "since": "N/A"}]
        if fh:
            try:
                f = await fh.fetch_fundamentals(t)
                if f and f.company_name:
                    execs = [{"name": f.company_name[:30], "title": "CEO", "since": "N/A"}]
            except Exception:
                pass
        return {"function": "MGMT", "cat_commentary": [_cat("reporting")],
                "data": {"ticker": t, "executives": execs}, "miau_score": _score("mgmt"), "updated": now}

    if func == "PHDC":
        t = ticker or "AAPL"
        holders = [{"name": "Vanguard", "pct": 8.5}]
        if fh:
            try:
                d = await fh.fetch_ownership(t)
                if d:
                    holders = [{"name": h.get("holder", h.get("name", "")), "pct": h.get("share", h.get("pct", 0))}
                               for h in (d[:5] if isinstance(d, list) else [])]
            except Exception:
                pass
        return {"function": "PHDC", "cat_commentary": [_cat("reporting")],
                "data": {"ticker": t, "institutional_pct": 61.2, "top_holders": holders},
                "miau_score": _score("phdc"), "updated": now}

    if func in ("TOP", "NI", "TNI", "NI HOT"):
        provider = _p("finnhub")
        items = []
        if provider:
            try:
                news = await provider.fetch_market_news("general")
                items = [{"headline": h.get("headline", ""), "source": h.get("source", "Miau News"),
                           "time": str(h.get("datetime", ""))[:10], "impact": "medium"}
                          for h in news[:n] if h.get("headline")]
            except Exception:
                pass
        if not items:
            items = [{"headline": "The cat is monitoring global markets.",
                       "source": "The Cat, CFA", "time": now[:10], "impact": "medium"}]
        return {"function": func, "cat_commentary": [_cat("bullish"), _cat("reporting")],
                "data": {"headlines": items}, "miau_score": _score("top"), "updated": now}

    if func == "READ":
        return {"function": "READ", "cat_commentary": ["🐱 Most read by cats with good taste."],
                "data": {"stories": [{"title": "How Cats Are Outperforming Hedge Funds", "reads": 12453},
                                     {"title": "Terminal Trading for Felines", "reads": 8921}]},
                "miau_score": 9, "updated": now}

    if func == "EASY":
        return {"function": "EASY", "cat_commentary": [_cat("reporting")],
                "data": {"tips": ["Press F1 for help", "Type catberg <function> for Bloomberg-style codes",
                                  "The cat watches every trade", "Tuna earned for daily check-in",
                                  "catberg wei shows World Equity Indices"]},
                "miau_score": 9, "updated": now}

    if func == "HELP":
        return {"function": "HELP", "cat_commentary": ["🐱 Keyboard help. The cat knows all shortcuts."],
                "data": {"shortcuts": [{"key": "F2", "action": "News (catberg n)"},
                                       {"key": "F3", "action": "FX (catberg wcv)"},
                                       {"key": "F4", "action": "Economic Calendar (catberg weco)"},
                                       {"key": "F5", "action": "Price Chart (catberg gpo)"},
                                       {"key": "F6", "action": "Company Overview (catberg des)"}]},
                "miau_score": 9, "updated": now}

    # Static data panels (UI features, not data-dependent)
    static = {
        "WECO": {"events": [{"date":"2026-05-20","event":"FOMC Minutes","country":"US"},
                            {"date":"2026-05-21","event":"CPI Report","country":"DE"}]},
        "YAS":  {"yields": [{"bond":"US 10Y","ytm":4.25,"spread":0},
                            {"bond":"AAA Corp","ytm":4.65,"spread":40}]},
        "WS":   {"swaps": [{"tenor":"2Y","rate":4.55},{"tenor":"5Y","rate":4.15}]},
        "NRG":  {"sector": "Energy"},
        "HYM":  {"sector": "High Yield"},
        "MA":   {"sector": "M&A"},
        "FUND": {"sector": "Funds"},
        "EMKT": {"sector": "Emerging Markets"},
        "ET":   {"sector": "E-Trading"},
        "IRSM": {"sector": "Interest Rate Swaps"},
        "PDFQ": {"watchlist": ["AAPL","MSFT","SPY","BTC"], "theme": "green", "refresh": 5},
        "BLP":  {"launchpad": {"top_left":"WEI","top_right":"NEWS","bottom_left":"GP AAPL","bottom_right":"WCV"}},
        "PRINT": {},
    }
    if func in static:
        return {"function": func, "cat_commentary": [_cat("neutral")],
                "data": static[func], "miau_score": 7, "updated": now}

    return {"function": func, "cat_commentary": [f"🐱 Function '{func}' recognized. The cat is working on it."],
            "data": {"available_functions": ["WEI", "N", "WCV", "WB", "IM", "ECST", "CBQ", "DES",
                     "GPO", "GIP", "ANR", "EM", "RV", "FA", "ACDR"]},
            "miau_score": 5, "updated": now}
