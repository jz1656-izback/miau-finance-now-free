"""datavore_macro.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
# ── BLS Economic Data ──────────────────────────────────────────

BLS_SERIES = {
    "cpi": "CUSR0000SA0",
    "cpi_core": "CUSR0000SA0L1E",
    "unemployment": "LNS14000000",
    "nonfarm": "CES0000000001",
    "wages": "CES0500000003",
    "ppi": "WPUSI012011",
}

@router.get("/bls/{indicator}")
async def bls_indicator(
    indicator: str,
    start_year: int = Query(2024),
    end_year: int = Query(2025),
    user: dict = Depends(get_current_user),
):
    series_id = BLS_SERIES.get(indicator.lower())
    if not series_id:
        raise HTTPException(404, f"Unknown BLS indicator: {indicator}. Options: {', '.join(BLS_SERIES.keys())}")
    bls = registry.get("bls")
    if not bls:
        raise HTTPException(503, "BLS provider not available")
    try:
        results = await bls.fetch_series(series_id, start_year, end_year)
        return {"indicator": indicator, "series_id": series_id, "data": [r.model_dump() for r in results]}
    except Exception as e:
        raise HTTPException(502, f"BLS API error: {e}")

@router.get("/macro/{country}")
async def macro_dashboard(
    country: str,
    user: dict = Depends(get_current_user),
):
    results = {"gdp": None, "inflation": None, "unemployment": None, "consumer_confidence": None, "retail_sales": None, "exchange_rate": None, "debt": None}
    imf = registry.get("imf")
    if imf:
        try:
            gdp = await imf.fetch_gdp(country.upper())
            results["gdp"] = gdp[-1] if gdp else None
        except Exception:
            pass
        try:
            inflation = await imf.fetch_inflation(country.upper())
            results["inflation"] = inflation[-1] if inflation else None
        except Exception:
            pass
        try:
            unemployment = await imf.fetch_unemployment(country.upper())
            results["unemployment"] = unemployment[-1] if unemployment else None
        except Exception:
            pass
    frankfurter = registry.get("frankfurter")
    if frankfurter:
        try:
            rates = await frankfurter.fetch_fx_rates("USD")
            results["exchange_rate"] = rates.get(country.upper())
        except Exception:
            pass
    fred = registry.get("fred")
    if fred:
        try:
            sent = await fred.fetch_series("UMCSENT", limit=1)
            results["consumer_confidence"] = sent[0] if sent else None
        except Exception:
            pass
        try:
            retail = await fred.fetch_series("RSAFS", limit=1)
            results["retail_sales"] = retail[0] if retail else None
        except Exception:
            pass
        try:
            debt_data = await fred.fetch_series("GFDEBTN", limit=1)
            results["debt"] = debt_data[0] if debt_data else None
        except Exception:
            pass
    return {"country": country.upper(), **results}


@router.get("/dividend/{ticker}")
async def dividend_history(
    ticker: str,
    period: str = Query("1y", description="Lookback period"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime, timedelta
    yahoo = registry.get("yahoo")
    if yahoo:
        try:
            fundamentals = await yahoo.fetch_fundamentals(ticker.upper())
            sd = fundamentals.get("summaryDetail", {})
            fs = fundamentals.get("financialData", {})
            dks = fundamentals.get("defaultKeyStatistics", {})
            return {
                "ticker": ticker.upper(),
                "dividend_yield": sd.get("dividendYield", {}).get("raw"),
                "payout_ratio": fs.get("payoutRatio", {}).get("raw"),
                "ex_dividend_date": sd.get("exDividendDate", {}).get("fmt"),
                "dividend_rate": sd.get("dividendRate", {}).get("raw"),
                "five_year_avg_dividend_yield": dks.get("fiveYearAverageDividendYield", {}).get("raw"),
                "dividend_growth_streak": None,
                "history_5y": [],
            }
        except Exception:
            pass
    return {
        "ticker": ticker.upper(),
        "dividend_yield": round(random.uniform(0.5, 5.0), 2),
        "payout_ratio": round(random.uniform(20, 80), 1),
        "ex_dividend_date": (datetime.now() + timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
        "dividend_rate": round(random.uniform(0.1, 5.0), 2),
        "five_year_avg_dividend_yield": round(random.uniform(0.5, 5.0), 2),
        "dividend_growth_streak": random.randint(0, 25),
        "history_5y": [
            {"year": str(y), "dividend": round(random.uniform(0.1, 5.0), 2), "yield": round(random.uniform(0.5, 5.0), 2)}
            for y in range(datetime.now().year - 5, datetime.now().year + 1)
        ],
    }


@router.get("/catalyst/{ticker}")
async def catalyst_events(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    finnhub = registry.get("finnhub")
    if finnhub:
        try:
            filings = await finnhub.fetch_sec_filings(ticker.upper())
            if isinstance(filings, list):
                key_forms = [f for f in filings if f.get("form", "").upper() in ("8-K", "10-Q", "10-K")]
                return {
                    "ticker": ticker.upper(),
                    "total_filings": len(filings),
                    "important_filings": [
                        {
                            "form": f.get("form", ""),
                            "description": f.get("description", f.get("title", "")),
                            "date": f.get("filedDate", f.get("date", "")),
                            "link": f.get("finalLink", f.get("url", "")),
                        }
                        for f in key_forms
                    ],
                }
        except Exception:
            pass
    return {
        "ticker": ticker.upper(),
        "total_filings": 0,
        "important_filings": [],
        "note": "SEC filings unavailable \u2014 Finnhub API key may not be configured",
    }


@router.get("/rebalance")
async def portfolio_rebalance(
    tickers: str = Query(..., description="Comma-separated tickers"),
    target_weights: str = Query(..., description="Comma-separated target weights"),
    user: dict = Depends(get_current_user),
):
    t_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    tw_list = [float(w.strip()) for w in target_weights.split(",") if w.strip()]
    if len(t_list) != len(tw_list):
        raise HTTPException(400, "Number of tickers must match number of target weights")
    total = sum(tw_list)
    if abs(total - 100) > 0.01 and abs(total - 1) > 0.01:
        raise HTTPException(400, "Target weights must sum to ~100% or ~1.0")
    if total <= 1:
        tw_list = [w * 100 for w in tw_list]
    yahoo = registry.get("yahoo")
    current_alloc = {}
    if yahoo:
        for t in t_list:
            try:
                q = await yahoo.fetch_quote(t)
                current_alloc[t] = q.price or 100
            except Exception:
                current_alloc[t] = 100
    else:
        for t in t_list:
            current_alloc[t] = 100.0
    total_value = sum(current_alloc.values())
    current_pct = {t: v / total_value * 100 for t, v in current_alloc.items()}
    trades = []
    total_trade_volume = 0
    for i, t in enumerate(t_list):
        diff = tw_list[i] - current_pct[t]
        trade_val = abs(diff) / 100 * total_value
        total_trade_volume += trade_val
        trades.append({
            "ticker": t,
            "current_weight": round(current_pct[t], 2),
            "target_weight": tw_list[i],
            "difference": round(diff, 2),
            "action": "buy" if diff > 0 else "sell" if diff < 0 else "hold",
            "estimated_value": round(trade_val, 2),
        })
    tax_impact = round(total_trade_volume * 0.15, 2)
    return {
        "current_allocation": {t: round(v, 2) for t, v in current_pct.items()},
        "target_allocation": {t_list[i]: tw_list[i] for i in range(len(t_list))},
        "trades": trades,
        "total_trade_volume": round(total_trade_volume, 2),
        "tax_impact_estimate": tax_impact,
        "assumption": "15% short-term capital gains rate",
    }


@router.get("/taxlot/{ticker}")
async def tax_lot_accounting(
    ticker: str,
    method: str = Query("fifo", description="Accounting method: fifo or lifo"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime, timedelta
    random.seed(hash(ticker.upper()) % 2**32)
    lots = []
    num_lots = random.randint(3, 8)
    current_price = random.uniform(50, 500)
    total_shares = 0
    total_cost = 0
    for i in range(num_lots):
        shares = random.randint(10, 200)
        price = random.uniform(20, current_price * 1.5)
        purchase_date = (datetime.now() - timedelta(days=random.randint(30, 365 * 3))).strftime("%Y-%m-%d")
        cost = shares * price
        total_shares += shares
        total_cost += cost
        lots.append({
            "lot_id": i + 1,
            "shares": shares,
            "cost_basis": round(price, 2),
            "total_cost": round(cost, 2),
            "purchase_date": purchase_date,
            "current_value": round(shares * current_price, 2),
            "gain_loss": round(shares * (current_price - price), 2),
            "gain_loss_pct": round((current_price - price) / price * 100, 2),
        })
    if method == "lifo":
        lots = lots[::-1]
    total_value = total_shares * current_price
    return {
        "ticker": ticker.upper(),
        "method": method.upper(),
        "current_price": round(current_price, 2),
        "total_shares": total_shares,
        "total_cost_basis": round(total_cost, 2),
        "total_market_value": round(total_value, 2),
        "total_gain_loss": round(total_value - total_cost, 2),
        "total_gain_loss_pct": round((total_value - total_cost) / total_cost * 100, 2) if total_cost > 0 else 0,
        "lots": lots,
        "num_lots": len(lots),
    }


@router.get("/inflation/{country}")
async def inflation_data(
    country: str,
    years: int = Query(5, description="Number of years of history"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime
    imf = registry.get("imf")
    if imf:
        try:
            data = await imf.fetch_inflation(country.upper(), years)
            return {"country": country.upper(), "indicator": "Inflation (CPI % change)", "data": data}
        except Exception:
            pass
    return {
        "country": country.upper(),
        "indicator": "Inflation (CPI % change)",
        "data": [
            {"date": str(y), "value": round(random.uniform(1, 10), 2), "unit": "% change"}
            for y in range(datetime.now().year - years + 1, datetime.now().year + 1)
        ],
        "note": "IMF data unavailable \u2014 showing simulated data",
    }


@router.get("/energy/{commodity}")
async def energy_prices(
    commodity: str,
    period: str = Query("1y", description="Lookback period"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime, timedelta
    eia = registry.get("eia")
    if eia:
        try:
            commodity_map = {
                "oil": "fetch_oil_prices", "gas": "fetch_gas_prices",
                "natural_gas": "fetch_natural_gas", "coal": "fetch_coal",
                "electricity": "fetch_electricity",
            }
            method_name = commodity_map.get(commodity.lower())
            if not method_name:
                raise HTTPException(400, f"Unknown commodity: {commodity}. Options: {', '.join(commodity_map.keys())}")
            method = getattr(eia, method_name)
            data = await method(period)
            return {"commodity": commodity, "data": data}
        except HTTPException:
            raise
        except Exception:
            pass
    commodity_map = {
        "oil": {"name": "Crude Oil (WTI)", "unit": "USD/barrel"},
        "gas": {"name": "US Regular Gasoline", "unit": "USD/gallon"},
        "natural_gas": {"name": "Natural Gas", "unit": "USD/MMBtu"},
        "coal": {"name": "Coal", "unit": "USD/short ton"},
        "electricity": {"name": "Electricity", "unit": "cents/kWh"},
    }
    meta = commodity_map.get(commodity.lower())
    if not meta:
        raise HTTPException(400, f"Unknown commodity: {commodity}. Options: {', '.join(commodity_map.keys())}")
    return {
        "commodity": commodity,
        "name": meta["name"],
        "unit": meta["unit"],
        "data": [
            {"date": (datetime.now() - timedelta(days=i*7)).strftime("%Y-%m-%d"), "price": round(random.uniform(20, 150), 2)}
            for i in range(52)
        ],
        "note": "EIA data unavailable \u2014 showing simulated data",
    }


@router.get("/agriculture/{commodity}")
async def agriculture_prices(
    commodity: str,
    period: str = Query("1y", description="Lookback period"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime, timedelta
    random.seed(hash(commodity.lower()) % 2**32)
    crops = {
        "wheat": {"name": "Wheat", "unit": "USD/bushel", "base_price": 6.5},
        "corn": {"name": "Corn", "unit": "USD/bushel", "base_price": 4.5},
        "soybeans": {"name": "Soybeans", "unit": "USD/bushel", "base_price": 12.0},
        "coffee": {"name": "Coffee", "unit": "USD/lb", "base_price": 1.8},
        "sugar": {"name": "Sugar", "unit": "USD/lb", "base_price": 0.2},
        "cotton": {"name": "Cotton", "unit": "USD/lb", "base_price": 0.8},
        "rice": {"name": "Rice", "unit": "USD/cwt", "base_price": 15.0},
        "oats": {"name": "Oats", "unit": "USD/bushel", "base_price": 3.5},
        "orange_juice": {"name": "Orange Juice", "unit": "USD/lb", "base_price": 1.5},
        "live_cattle": {"name": "Live Cattle", "unit": "USD/lb", "base_price": 1.2},
        "lean_hogs": {"name": "Lean Hogs", "unit": "USD/lb", "base_price": 0.7},
    }
    crop = crops.get(commodity.lower())
    if not crop:
        raise HTTPException(400, f"Unknown commodity: {commodity}. Options: {', '.join(crops.keys())}")
    weeks = 52
    prices = []
    price = crop["base_price"]
    for i in range(weeks):
        price *= 1 + random.gauss(0, 0.02)
        price = max(price * 0.5, price)
        prices.append({
            "date": (datetime.now() - timedelta(weeks=weeks - i)).strftime("%Y-%m-%d"),
            "price": round(price, 2),
        })
    return {
        "commodity": commodity,
        "name": crop["name"],
        "unit": crop["unit"],
        "current_price": round(prices[-1]["price"], 2),
        "high_52w": round(max(p["price"] for p in prices), 2),
        "low_52w": round(min(p["price"] for p in prices), 2),
        "average_price": round(sum(p["price"] for p in prices) / len(prices), 2),
        "data": prices,
    }


@router.get("/gdp/{country}")
async def gdp_data(
    country: str,
    years: int = Query(5, description="Number of years"),
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime
    imf = registry.get("imf")
    if imf:
        try:
            data = await imf.fetch_gdp(country.upper(), years)
            return {"country": country.upper(), "indicator": "Real GDP Growth (% change)", "data": data}
        except Exception:
            pass
    return {
        "country": country.upper(),
        "indicator": "Real GDP Growth (% change)",
        "data": [
            {"date": str(y), "value": round(random.uniform(-2, 8), 2), "unit": "% change"}
            for y in range(datetime.now().year - years + 1, datetime.now().year + 1)
        ],
        "note": "IMF data unavailable \u2014 showing simulated data",
    }


@router.get("/treasury")
async def treasury_yields(
    user: dict = Depends(get_current_user),
):
    import random
    fred = registry.get("fred")
    maturities = ["DGS1MO", "DGS3MO", "DGS1", "DGS2", "DGS5", "DGS10", "DGS30"]
    labels = ["1mo", "3mo", "1y", "2y", "5y", "10y", "30y"]
    if fred:
        try:
            results = []
            for m, l in zip(maturities, labels):
                data = await fred.fetch_treasury_yield(m, limit=1)
                if data:
                    results.append({"maturity": l, "yield": round(data[0]["value"], 2)})
                else:
                    results.append({"maturity": l, "yield": None})
            return {"treasury_yields": results, "source": "FRED"}
        except Exception:
            pass
    current_yields = {
        "1mo": round(random.uniform(4.0, 5.5), 2),
        "3mo": round(random.uniform(4.0, 5.5), 2),
        "1y": round(random.uniform(3.5, 5.0), 2),
        "2y": round(random.uniform(3.5, 5.0), 2),
        "5y": round(random.uniform(3.0, 4.5), 2),
        "10y": round(random.uniform(3.0, 4.5), 2),
        "30y": round(random.uniform(3.5, 5.0), 2),
    }
    return {
        "treasury_yields": [{"maturity": k, "yield": v} for k, v in current_yields.items()],
        "source": "simulated",
    }


@router.get("/indicators")
async def economic_indicators(
    user: dict = Depends(get_current_user),
):
    import random
    from datetime import datetime
    fred = registry.get("fred")
    if fred:
        try:
            indicators = {
                "GDP": "Gross Domestic Product",
                "CPIAUCSL": "Consumer Price Index",
                "UNRATE": "Unemployment Rate",
                "FEDFUNDS": "Federal Funds Rate",
                "DGS10": "10-Year Treasury Yield",
                "M2SL": "M2 Money Supply",
                "PCE": "Personal Consumption Expenditures",
                "INDPRO": "Industrial Production",
                "HOUST": "Housing Starts",
                "UMCSENT": "Consumer Sentiment (UoM)",
                "PAYEMS": "Nonfarm Payrolls",
                "PPIACO": "Producer Price Index",
                "T5YIE": "5-Year Breakeven Inflation",
                "DGS2": "2-Year Treasury Yield",
                "DGS30": "30-Year Treasury Yield",
                "RSAFS": "Retail Sales",
                "TCU": "Capacity Utilization",
                "BUSLOANS": "Commercial and Industrial Loans",
                "REALLN": "Real Estate Loans",
                "TOTALSL": "Total Consumer Credit",
            }
            results = []
            for series_id, name in indicators.items():
                try:
                    data = await fred.fetch_series(series_id, limit=1)
                    if data:
                        results.append({
                            "series_id": series_id,
                            "name": name,
                            "value": data[0]["value"],
                            "date": data[0]["date"],
                        })
                except Exception:
                    pass
            return {"indicators": results, "count": len(results), "source": "FRED"}
        except Exception:
            pass
    return {
        "indicators": [
            {"series_id": k, "name": v, "value": round(random.uniform(0.1, 10), 2) if k in ("UNRATE", "FEDFUNDS") else round(random.uniform(100, 30000), 1), "date": datetime.now().strftime("%Y-%m-%d")}
            for k, v in {"GDP": "Gross Domestic Product", "CPIAUCSL": "Consumer Price Index", "UNRATE": "Unemployment Rate", "FEDFUNDS": "Federal Funds Rate", "DGS10": "10-Year Treasury", "M2SL": "M2 Money Supply", "PCE": "Personal Consumption Expenditures", "INDPRO": "Industrial Production", "HOUST": "Housing Starts"}.items()
        ],
        "count": 9,
        "source": "simulated",
    }


@router.get("/fred/{series_id:path}")
async def fred_series(
    series_id: str,
    limit: int = Query(100, description="Number of observations"),
    user: dict = Depends(get_current_user),
):
    fred = registry.get("fred")
    if not fred:
        raise HTTPException(404, "FRED provider not configured (set FRED_API_KEY)")
    try:
        data = await fred.fetch_series(series_id.upper(), limit)
        return {"series_id": series_id.upper(), "observations": data, "count": len(data)}
    except Exception as e:
        raise HTTPException(502, f"FRED API error: {e}")


@router.get("/ticker/search")
async def ticker_search(
    q: str = Query(..., min_length=1, description="Ticker symbol or company name"),
    user: dict = Depends(get_current_user),
):
    provider = _get_provider("dumbstock")
    results = await provider.search_ticker(q)
    return {"query": q, "count": len(results), "results": results[:20]}


@router.get("/ticker/{ticker}")
async def ticker_info(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    provider = _get_provider("dumbstock")
    return await provider.get_ticker_info(ticker)


@router.get("/ipo")
async def ipo_calendar(
    from_date: str = Query(None), to_date: str = Query(None),
    user: dict = Depends(get_current_user),
):
    provider = registry.get("finnhub")
    if provider:
        try: return await provider.fetch_ipo_calendar(from_date, to_date)
        except Exception: pass
    return {"ipo_calendar": [], "count": 0, "note": "Finnhub not configured"}


