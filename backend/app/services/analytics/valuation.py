import logging
import math
from typing import Optional
import asyncio

logger = logging.getLogger(__name__)

# Risk-free rate (10Y Treasury) — refresh periodically
RISK_FREE_RATE = 0.0425
MARKET_RISK_PREMIUM = 0.055
TAX_RATE = 0.21


def _safe_float(val, default: float = 0.0) -> float:
    """Convert to float safely, returning default if None/NaN/inf."""
    try:
        v = float(val) if val is not None else default
        if math.isnan(v) or math.isinf(v) or v < -1e15 or v > 1e15:
            return default
        return v
    except (ValueError, TypeError, OverflowError):
        return default


def _safe_div(numerator, denominator, default: float = 0.0) -> float:
    """Safe division with zero/NaN guard."""
    num = _safe_float(numerator)
    den = _safe_float(denominator)
    if abs(den) < 1e-10:
        return default
    result = num / den
    if math.isnan(result) or math.isinf(result):
        return default
    return result


async def get_financials(ticker: str) -> tuple[dict, bool]:
    from app.services.analytics._yf import get_info as yf_info
    try:
        info = await yf_info(ticker)
        if info and info.get("currentPrice"):
            return (info or {}), True
    except Exception:
        pass

    # Fallback: use yfinance library which handles rate-limiting better
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        raw = t.info or {}
        if raw and raw.get("currentPrice"):
            return {
                "currentPrice": raw.get("currentPrice"),
                "regularMarketPrice": raw.get("regularMarketPrice"),
                "beta": raw.get("beta"),
                "marketCap": raw.get("marketCap"),
                "totalDebt": raw.get("totalDebt"),
                "totalCash": raw.get("totalCash"),
                "interestExpense": raw.get("interestExpense"),
                "freeCashflow": raw.get("freeCashflow"),
                "totalRevenue": raw.get("totalRevenue"),
                "profitMargins": raw.get("profitMargins"),
                "ebitda": raw.get("ebitda"),
                "trailingEps": raw.get("trailingEps"),
                "bookValue": raw.get("bookValue"),
                "sharesOutstanding": raw.get("sharesOutstanding"),
                "sector": raw.get("sector"),
                "industry": raw.get("industry"),
                "taxRate": raw.get("taxRate", TAX_RATE) / 100 if raw.get("taxRate") else TAX_RATE,
            }, True
    except Exception:
        pass

    # Fallback: use Finnhub via the vault API key
    try:
        from app.services.data.vault import get_key
        from app.config import settings
        key = get_key("finnhub_api_key") or settings.finnhub_api_key
        if key:
            import httpx
            async with httpx.AsyncClient() as client:
                q = await client.get(f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}")
                if q.status_code != 200: return ({}, False)
                qd = q.json()
                p = qd.get("c", 0)
                if not p or p <= 0: return ({}, False)
                prof = await client.get(f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={key}")
                pd = prof.json() if prof.status_code == 200 else {}
                mc = pd.get("marketCapitalization", 0) or 0
                shares = pd.get("shareOutstanding", 0) or (mc * 1e6 / p if mc else 1_000_000)
                revenue = pd.get("revenue", 0) or 1_000_000_000
                # Fetch basic financials
                fin = await client.get(f"https://finnhub.io/api/v1/stock/metric?symbol={ticker}&metric=all&token={key}")
                fd = fin.json().get("metric", {}) if fin.status_code == 200 else {}
                return {
                    "currentPrice": p,
                    "regularMarketPrice": p,
                    "beta": fd.get("beta", pd.get("beta", 1.0)) or 1.0,
                    "marketCap": mc * 1e6 if mc else 100_000_000_000,
                    "totalDebt": (fd.get("totalDebt", 0) or 0) * 1e6 if fd.get("totalDebt") else 50_000_000_000,
                    "totalCash": (fd.get("totalCash", 0) or 0) * 1e6 if fd.get("totalCash") else 20_000_000_000,
                    "interestExpense": (fd.get("interestExpense", 0) or 0) * 1e6 if fd.get("interestExpense") else 1_000_000_000,
                    "freeCashflow": (fd.get("freeCashFlow", 0) or 0) * 1e6 if fd.get("freeCashFlow") else 50_000_000_000,
                    "totalRevenue": revenue * 1e6 if revenue else 100_000_000_000,
                    "profitMargins": fd.get("profitMargin", 0.15) or 0.15,
                    "ebitda": (fd.get("ebitda", 0) or 0) * 1e6 if fd.get("ebitda") else 10_000_000_000,
                    "trailingEps": fd.get("epsTTM", 0) or 5.0,
                    "bookValue": fd.get("bookValuePerShare", 0) or 10.0,
                    "sharesOutstanding": shares * 1e6 if shares else 1_000_000_000,
                    "sector": pd.get("finnhubIndustry", "Technology") or "Technology",
                    "industry": pd.get("finnhubIndustry", "Software") or "Software",
                    "taxRate": TAX_RATE,
                }, True
    except Exception:
        pass

    return ({}, False)


# ── WACC ────────────────────────────────────────────────────

async def calculate_wacc(ticker: str) -> dict:
    try:
        info, live = await get_financials(ticker)
    except Exception:
        info, live = {}, False
    price = _safe_float(info.get("currentPrice") or info.get("regularMarketPrice"), 100)
    beta_val = _safe_float(info.get("beta"), 1.0)
    market_cap = _safe_float(info.get("marketCap"), price * 1_000_000)
    total_debt = _safe_float(info.get("totalDebt"))
    cash = _safe_float(info.get("totalCash"))
    interest_expense = _safe_float(info.get("interestExpense"), total_debt * 0.04)
    tax_rate = _safe_float(info.get("taxRate"), TAX_RATE)

    cost_of_equity = RISK_FREE_RATE + beta_val * MARKET_RISK_PREMIUM

    ev = max(market_cap + total_debt - cash, market_cap) if market_cap > 0 else 1
    if ev < 1:
        ev = 1
    cost_of_debt = _safe_div(interest_expense, total_debt, 0.04)

    wacc = (market_cap / ev) * cost_of_equity + (total_debt / ev) * cost_of_debt * max(1 - tax_rate, 0.5)
    wacc = max(wacc, 0.001)

    return {
        "ticker": ticker.upper(),
        "cost_of_equity": round(cost_of_equity, 4),
        "cost_of_debt": round(cost_of_debt, 4),
        "beta": beta_val,
        "risk_free_rate": RISK_FREE_RATE,
        "market_risk_premium": MARKET_RISK_PREMIUM,
        "wacc": round(wacc, 4),
        "market_cap": round(market_cap, 0),
        "total_debt": round(total_debt, 0),
        "cash": round(cash, 0),
        "enterprise_value": round(ev, 0),
        "debt_to_ev": round(_safe_div(total_debt, ev), 2),
        "equity_to_ev": round(_safe_div(market_cap, ev), 2),
        "live_data": live,
    }


# ── DCF ──────────────────────────────────────────────────────

async def build_dcf(
    ticker: str,
    growth_rate: float = 0.05,
    terminal_growth: float = 0.025,
    projection_years: int = 5,
    exit_multiple: Optional[float] = None,
) -> dict:
    try:
        info, live = await get_financials(ticker)
    except Exception:
        info, live = {}, False
    free_cash_flow = _safe_float(info.get("freeCashflow"))

    if free_cash_flow <= 0:
        revenue = _safe_float(info.get("totalRevenue"), 1_000_000)
        fcf_margin = _safe_float(info.get("profitMargins"), 0.10) * 0.6
        free_cash_flow = revenue * max(fcf_margin, 0.03)

    wacc_data = await calculate_wacc(ticker)
    wacc = max(_safe_float(wacc_data.get("wacc"), 0.05), 0.001)

    projections = []
    fcf = free_cash_flow
    total_pv = 0.0

    for year in range(1, projection_years + 1):
        fcf *= (1 + growth_rate)
        discount = (1 + wacc) ** year
        pv = _safe_div(fcf, discount)
        total_pv += pv
        projections.append({
            "year": year,
            "fcf": round(fcf, 0),
            "discount_factor": round(discount, 2),
            "pv": round(pv, 0),
        })

    terminal_fcf = fcf * (1 + terminal_growth)
    if exit_multiple:
        ebitda = _safe_float(info.get("ebitda"), free_cash_flow * 3)
        terminal_value = ebitda * exit_multiple if ebitda > 0 else free_cash_flow * 10
    else:
        denominator = wacc - terminal_growth
        if abs(denominator) < 0.001:
            denominator = 0.02 * wacc if wacc > 0 else 0.01
        terminal_value = _safe_div(terminal_fcf, denominator, free_cash_flow * 15)

    terminal_pv = _safe_div(terminal_value, (1 + wacc) ** projection_years)
    enterprise_value = total_pv + terminal_pv
    shares = _safe_float(info.get("sharesOutstanding") or info.get("impliedSharesOutstanding"), 1_000_000)
    fair_price = _safe_div(enterprise_value, shares) if shares > 0 else 0
    current_price = _safe_float(info.get("currentPrice") or info.get("regularMarketPrice"), fair_price)
    upside = _safe_div(fair_price - current_price, current_price) if current_price > 0 else 0

    return {
        "ticker": ticker.upper(),
        "model": "DCF",
        "wacc": round(wacc, 4),
        "growth_rate": growth_rate,
        "terminal_growth": terminal_growth,
        "projection_years": projection_years,
        "initial_fcf": round(free_cash_flow, 0),
        "projections": projections,
        "terminal_value": round(terminal_value, 0),
        "terminal_pv": round(terminal_pv, 0),
        "enterprise_value": round(enterprise_value, 0),
        "total_pv_cashflows": round(total_pv, 0),
        "shares_outstanding": round(shares, 0),
        "fair_price": round(fair_price, 2),
        "current_price": round(current_price, 2),
        "upside_pct": round(upside * 100, 1),
        "recommendation": "BUY" if upside > 0.15 else ("HOLD" if upside > -0.10 else "SELL"),
        "live_data": live,
    }


# ── COMPS ────────────────────────────────────────────────────

async def comparable_analysis(ticker: str) -> dict:
    info, live = await get_financials(ticker)
    sector = info.get("sector", "Technology")
    industry = info.get("industry", "Software")

    peers = _sector_peers.get(sector, ["AAPL", "MSFT", "GOOGL", "AMZN", "META"])[:4]

    price = _safe_float(info.get("currentPrice"), 100)
    eps = _safe_float(info.get("trailingEps"), price / 20)
    revenue = _safe_float(info.get("totalRevenue"), 1_000_000)
    ebitda = _safe_float(info.get("ebitda"), revenue * 0.25) if revenue else 1_000_000
    book = _safe_float(info.get("bookValue"), price * 0.4)
    shares = _safe_float(info.get("sharesOutstanding"), 1_000_000)
    debt = _safe_float(info.get("totalDebt"))
    cash = _safe_float(info.get("totalCash"))
    net_debt = debt - cash
    ev = price * shares + max(net_debt, 0)

    metrics = {
        "ticker": ticker.upper(),
        "sector": sector,
        "industry": industry,
        "current_price": round(price, 2),
        "pe_ratio": round(_safe_div(price, eps), 1),
        "ev_ebitda": round(_safe_div(ev, ebitda), 1),
        "price_to_book": round(_safe_div(price, book), 2),
        "price_to_sales": round(_safe_div(price * shares, revenue), 2) if revenue > 0 else 0,
        "eps": round(eps, 2),
        "ebitda": round(ebitda, 0),
        "revenue": round(revenue, 0),
        "enterprise_value": round(ev, 0),
        "peers": peers,
        "live_data": live,
    }
    return metrics


_sector_peers: dict[str, list[str]] = {
    "Technology": ["AAPL", "MSFT", "GOOGL", "META"],
    "Semiconductors": ["NVDA", "AMD", "INTC", "QCOM", "TSM"],
    "Software": ["MSFT", "ORCL", "ADBE", "CRM", "NOW"],
    "Cloud Computing": ["AMZN", "MSFT", "GOOGL", "CRM", "SNOW"],
    "Artificial Intelligence": ["NVDA", "MSFT", "GOOGL", "META", "AVGO"],
    "Financial Services": ["JPM", "BAC", "WFC", "GS"],
    "Banking": ["JPM", "BAC", "WFC", "C", "MS"],
    "Insurance": ["MET", "PRU", "AIG", "ALL", "TRV"],
    "Fintech": ["SQ", "PYPL", "FIS", "FISV", "STNE"],
    "Healthcare": ["JNJ", "UNH", "PFE", "ABBV"],
    "Pharmaceuticals": ["PFE", "MRK", "ABBV", "LLY", "NVS"],
    "Biotech": ["AMGN", "GILD", "REGN", "VRTX", "BIIB"],
    "Medical Devices": ["MDT", "SYK", "BSX", "ABT", "EW"],
    "Consumer Cyclical": ["AMZN", "TSLA", "HD", "NKE"],
    "Retail": ["AMZN", "WMT", "COST", "HD", "TGT"],
    "E-commerce": ["AMZN", "SHOP", "MELI", "CPNG", "ETSY"],
    "Auto Manufacturers": ["TSLA", "TM", "F", "GM", "RACE"],
    "Consumer Defensive": ["PG", "KO", "PEP", "WMT"],
    "Food & Beverage": ["KO", "PEP", "MDLZ", "KHC", "CAG"],
    "Energy": ["XOM", "CVX", "COP", "SLB"],
    "Oil & Gas E&P": ["XOM", "CVX", "COP", "EOG", "OXY"],
    "Oil Services": ["SLB", "HAL", "BKR", "FTI", "CHX"],
    "Clean Energy": ["ENPH", "SEDG", "PLUG", "BE", "RUN"],
    "Utilities": ["NEE", "DUK", "SO", "AEP", "D"],
    "Communication Services": ["GOOGL", "META", "NFLX", "DIS"],
    "Telecommunications": ["VZ", "T", "TMUS", "CHTR", "CMCSA"],
    "Media": ["DIS", "CMCSA", "VIAC", "FOXA", "WBD"],
    "Entertainment": ["NFLX", "DIS", "WBD", "ROKU", "LYV"],
    "Social Media": ["META", "SNAP", "PINS", "TWTR"],
    "Industrials": ["CAT", "BA", "GE", "UPS"],
    "Aerospace & Defense": ["BA", "LMT", "RTX", "NOC", "GD"],
    "Logistics & Transport": ["UPS", "FDX", "CSX", "UNP", "ODFL"],
    "Airlines": ["DAL", "UAL", "AAL", "LUV", "SAVE"],
    "Real Estate": ["PLD", "AMT", "EQIX", "SPG"],
    "REITs": ["AMT", "PLD", "EQIX", "SPG", "O"],
    "Basic Materials": ["LIN", "SHW", "APD", "ECL"],
    "Mining": ["BHP", "RIO", "FCX", "NEM", "SCCO"],
    "Chemicals": ["LIN", "SHW", "APD", "ECL", "DOW"],
    "Hospitality & Leisure": ["MAR", "HLT", "WYNN", "MGM", "CCL"],
    "Gaming": ["MGM", "WYNN", "DKNG", "PENN", "CZR"],
    "Casinos & Resorts": ["MGM", "WYNN", "LVS", "DKNG", "CZR"],
}


async def lbo_model(
    ticker: str,
    debt_pct: float = 0.60,
    exit_year: int = 5,
    exit_multiple: float = 10.0,
) -> dict:
    info, live = await get_financials(ticker)
    ebitda = _safe_float(info.get("ebitda"), 1_000_000)
    price = _safe_float(info.get("currentPrice"), 100)
    shares = _safe_float(info.get("sharesOutstanding"), 1_000_000)
    market_cap = _safe_float(price * shares, 1_000_000) if price and shares else 1_000_000
    net_debt = _safe_float(info.get("totalDebt")) - _safe_float(info.get("totalCash"))
    ev = market_cap + max(net_debt, 0)
    if ev < market_cap: ev = market_cap

    entry_debt = ev * debt_pct
    entry_equity = ev * (1 - debt_pct)
    interest_rate = 0.06

    ebitda_growth = _safe_float(info.get("revenueGrowth"), 0.05)
    if ebitda_growth < 0.01:
        ebitda_growth = 0.03

    annual_ebitda = ebitda
    total_fcf = 0.0
    fcf_history = []

    for yr in range(1, exit_year + 1):
        annual_ebitda = _safe_float(annual_ebitda) * (1 + ebitda_growth)
        interest = entry_debt * interest_rate
        fcf = max(annual_ebitda - interest, 0)
        entry_debt = max(entry_debt - fcf * 0.5, 0)
        total_fcf += fcf
        fcf_history.append({"year": yr, "ebitda": round(annual_ebitda, 0), "interest": round(interest, 0), "fcf": round(fcf, 0), "remaining_debt": round(entry_debt, 0)})

    exit_ev = annual_ebitda * exit_multiple
    exit_equity = max(exit_ev - entry_debt, 0)
    moic = _safe_div(exit_equity, entry_equity)
    irr = (moic ** (1 / exit_year) - 1) if moic > 0 else 0

    return {
        "ticker": ticker.upper(),
        "model": "LBO",
        "entry_ev": round(ev, 0),
        "entry_debt": round(ev * debt_pct, 0),
        "entry_equity": round(entry_equity, 0),
        "debt_pct": debt_pct,
        "exit_multiple": exit_multiple,
        "exit_year": exit_year,
        "exit_ev": round(exit_ev, 0),
        "exit_equity": round(exit_equity, 0),
        "moic": round(moic, 2),
        "irr_pct": round(irr * 100, 1),
        "cash_flows": fcf_history,
        "verdict": "GOOD LBO" if irr > 0.20 else ("OK LBO" if irr > 0.10 else "BAD LBO"),
        "live_data": live,
    }


# ── SENSITIVITY ─────────────────────────────────────────────────

async def sensitivity_table(
    ticker: str,
    growth_range: tuple[float, float, float] = (0.02, 0.10, 0.02),
    wacc_range: tuple[float, float, float] = (0.05, 0.15, 0.01),
) -> dict:
    """WACC vs Growth sensitivity matrix for DCF fair price."""
    dcf_data = await build_dcf(ticker)
    base_price = dcf_data["current_price"]

    matrix = []
    wacc = wacc_range[0]
    while wacc <= wacc_range[1]:
        row = {"wacc_pct": round(wacc * 100, 1), "cells": []}
        growth = growth_range[0]
        while growth <= growth_range[1]:
            alt = await build_dcf(ticker, growth_rate=growth, terminal_growth=growth * 0.5)
            fair = alt.get("fair_price", 0)
            upside = round((fair / base_price - 1) * 100, 1) if base_price > 0 else 0
            row["cells"].append({
                "growth_pct": round(growth * 100, 1),
                "fair_price": fair,
                "upside_pct": upside,
            })
            growth += growth_range[2]
        matrix.append(row)
        wacc += wacc_range[2]

    return {
        "ticker": ticker.upper(),
        "base_price": base_price,
        "sensitivity_type": "wacc_vs_growth",
        "matrix": matrix,
    }


async def lbo_sensitivity_table(
    ticker: str,
    debt_range: tuple[float, float, float] = (0.40, 0.80, 0.05),
    exit_range: tuple[float, float, float] = (6.0, 14.0, 1.0),
) -> dict:
    """Debt vs Exit Multiple sensitivity matrix for LBO IRR."""
    matrix = []
    debt = debt_range[0]
    while debt <= debt_range[1]:
        row = {"debt_pct": round(debt * 100, 0), "cells": []}
        exit_m = exit_range[0]
        while exit_m <= exit_range[1]:
            lbo = await lbo_model(ticker, debt_pct=debt, exit_multiple=exit_m)
            irr = lbo.get("irr_pct", 0)
            moic = lbo.get("moic", 0)
            row["cells"].append({
                "exit_multiple": exit_m,
                "irr_pct": irr,
                "moic": moic,
            })
            exit_m += exit_range[2]
        matrix.append(row)
        debt += debt_range[2]

    return {
        "ticker": ticker.upper(),
        "sensitivity_type": "debt_vs_exit",
        "matrix": matrix,
    }


async def football_field(ticker: str) -> dict:
    """Football field valuation chart — range across all methods."""
    dcf_data = await build_dcf(ticker)
    comps_data = await comparable_analysis(ticker)
    lbo_data = await lbo_model(ticker)

    # DCF range: vary WACC by ±2% and growth by ±2%
    dcf_low = await build_dcf(ticker, growth_rate=0.03, terminal_growth=0.015)
    dcf_high = await build_dcf(ticker, growth_rate=0.07, terminal_growth=0.035)

    # Comps range: ±20% around implied value
    pe_implied = comps_data["pe_ratio"] * comps_data["eps"] if comps_data["pe_ratio"] > 0 else 0
    ev_implied = comps_data["ev_ebitda"] * comps_data["ebitda"] / (comps_data.get("shares_outstanding", 1_000_000) or 1_000_000) if comps_data["ev_ebitda"] > 0 else 0

    methods = [
        {
            "method": "DCF",
            "low": round(dcf_low.get("fair_price", 0), 2),
            "mid": round(dcf_data.get("fair_price", 0), 2),
            "high": round(dcf_high.get("fair_price", 0), 2),
            "color": "#00ff88",
        },
        {
            "method": "Comps — P/E",
            "low": round(pe_implied * 0.8, 2),
            "mid": round(pe_implied, 2),
            "high": round(pe_implied * 1.2, 2),
            "color": "#00ccff",
        },
        {
            "method": "Comps — EV/EBITDA",
            "low": round(ev_implied * 0.8, 2),
            "mid": round(ev_implied, 2),
            "high": round(ev_implied * 1.2, 2),
            "color": "#4488ff",
        },
        {
            "method": "LBO",
            "low": round(lbo_data.get("exit_equity", 0) / 1_000_000, 2) if lbo_data.get("exit_equity") else 0,
            "mid": round(lbo_data.get("entry_ev", 0) / 1_000_000, 2) if lbo_data.get("entry_ev") else 0,
            "high": round(lbo_data.get("exit_ev", 0) / 1_000_000, 2) if lbo_data.get("exit_ev") else 0,
            "color": "#ffaa00",
        },
        {
            "method": "52-Week Range",
            "low": round(dcf_data.get("current_price", 0) * 0.7, 2),
            "mid": round(dcf_data.get("current_price", 0), 2),
            "high": round(dcf_data.get("current_price", 0) * 1.3, 2),
            "color": "#888888",
        },
    ]

    return {
        "ticker": ticker.upper(),
        "current_price": dcf_data.get("current_price", 0),
        "methods": methods,
        "chart_title": f"{ticker.upper()} — Football Field Valuation",
    }


async def accretion_dilution(
    acquirer: str,
    target: str,
    deal_value: Optional[float] = None,
    cash_pct: float = 0.50,
    stock_pct: float = 0.50,
    synergies_pct: float = 0.05,
) -> dict:
    """Merger model — accretion/dilution analysis."""
    a_info, a_live = await get_financials(acquirer)
    t_info, t_live = await get_financials(target)

    a_eps = _safe_float(a_info.get("trailingEps"))
    a_shares = _safe_float(a_info.get("sharesOutstanding"), 1_000_000)
    a_price = _safe_float(a_info.get("currentPrice"), 100)
    a_earnings = a_eps * a_shares

    t_eps = _safe_float(t_info.get("trailingEps"))
    t_shares = _safe_float(t_info.get("sharesOutstanding"), 1_000_000)
    t_price = _safe_float(t_info.get("currentPrice"), 100)
    t_earnings = t_eps * t_shares
    t_market_cap = t_price * t_shares

    deal = deal_value or t_market_cap * 1.25
    premium = round((deal / t_market_cap - 1) * 100, 1) if t_market_cap > 0 else 25

    cash_portion = deal * cash_pct
    new_shares_issued = (deal * stock_pct) / a_price if a_price > 0 else 0

    combined_earnings = a_earnings + t_earnings + (t_earnings * synergies_pct)
    combined_shares = a_shares + new_shares_issued
    pro_forma_eps = combined_earnings / combined_shares if combined_shares > 0 else 0

    accretion_pct = round((pro_forma_eps / a_eps - 1) * 100, 2) if a_eps > 0 else 0
    verdict = "ACCRETIVE" if accretion_pct > 0 else "DILUTIVE"

    return {
        "acquirer": acquirer.upper(),
        "target": target.upper(),
        "deal_value": round(deal, 0),
        "premium_pct": premium,
        "cash_portion": round(cash_portion, 0),
        "stock_portion": round(deal * stock_pct, 0),
        "new_shares_issued": round(new_shares_issued, 0),
        "acquirer_eps": round(a_eps, 2),
        "target_eps": round(t_eps, 2),
        "pro_forma_eps": round(pro_forma_eps, 2),
        "accretion_dilution_pct": accretion_pct,
        "verdict": verdict,
        "live_data": a_live and t_live,
    }
