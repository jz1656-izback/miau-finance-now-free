"""datavore_map.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
# ── Map Data — Batch company data, commodities, bonds, DeFi ────

@router.get("/map/companies")
async def map_companies(
    continent: str = Query(None, description="Filter by continent code"),
    industry: str = Query(None, description="Filter by industry"),
    country: str = Query(None, description="Filter by country code"),
    min_mcap: float = Query(0, alias="minMcap", description="Min market cap in billions"),
    max_mcap: float = Query(999999, alias="maxMcap", description="Max market cap in billions"),
    search: str = Query(None, description="Search ticker or name"),
    limit: int = Query(100, description="Max results"),
    user: dict = Depends(get_current_user),
):
    logger.debug("map_companies: continent=%s industry=%s country=%s min_mcap=%s max_mcap=%s search=%s limit=%d", continent, industry, country, min_mcap, max_mcap, search, limit)
    companies = get_companies_by_continent(continent)
    if industry:
        companies = [c for c in companies if c["i"] and industry.lower() in c["i"].lower()]
    if country:
        companies = [c for c in companies if c["co"] and c["co"].upper() == country.upper()]
    if min_mcap > 0:
        companies = [c for c in companies if (c["mc"] or 0) >= min_mcap]
    if max_mcap < 999999:
        companies = [c for c in companies if (c["mc"] or 0) <= max_mcap]
    if search:
        s = search.lower()
        companies = [c for c in companies if s in (c["t"] or "").lower() or s in (c["n"] or "").lower()]
    companies = companies[:limit]
    return {
        "total": len(companies),
        "companies": [
            {"ticker": c["t"], "name": c["n"], "industry": c["i"], "country": c["co"], "marketCap": c["mc"]}
            for c in companies
        ],
    }


@router.get("/map/continents")
async def map_continents(user: dict = Depends(get_current_user)):
    logger.debug("map_continents called")
    return {
        "continents": {
            k: {"center_lat": v["lat"], "center_lng": v["lng"], "count": len(get_companies_by_continent(k))}
            for k, v in CONTINENT_CENTROIDS.items()
        },
        "total": get_company_count(),
    }


@router.get("/map/batch-prices")
async def map_batch_prices(
    tickers: str = Query(..., description="Comma-separated tickers"),
    user: dict = Depends(get_current_user),
):
    logger.debug("map_batch_prices: tickers=%s", tickers)
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    yahoo = registry.get("yahoo")
    if not yahoo:
        raise HTTPException(503, "Yahoo Finance provider unavailable")
    import asyncio
    prices = {}
    # Batch in groups of 10 to avoid rate limiting
    for i in range(0, len(ticker_list), 10):
        batch = ticker_list[i:i+10]
        results = await asyncio.gather(
            *[yahoo.fetch_quote(t) for t in batch],
            return_exceptions=True,
        )
        for t, r in zip(batch, results):
            if isinstance(r, Exception):
                prices[t] = {"error": str(r)}
            else:
                prices[t] = r.model_dump() if hasattr(r, 'model_dump') else r
    return {"prices": prices, "count": len(prices)}


@router.get("/map/commodities")
async def map_commodities(user: dict = Depends(get_current_user)):
    """Return commodities with hardcoded positions + live prices from Yahoo."""
    COMMODITY_MAP = {
        "CL=F": {"name": "Crude Oil (WTI)", "icon": "🛢️", "unit": "USD/bbl", "lat": 31.9, "lng": -102.9},
        "BZ=F": {"name": "Brent Crude", "icon": "🛢️", "unit": "USD/bbl", "lat": 58.0, "lng": 2.0},
        "GC=F": {"name": "Gold", "icon": "🥇", "unit": "USD/oz", "lat": -26.2, "lng": 28.0},
        "SI=F": {"name": "Silver", "icon": "🥈", "unit": "USD/oz", "lat": 23.0, "lng": -102.0},
        "HG=F": {"name": "Copper", "icon": "🪙", "unit": "USD/lb", "lat": -22.0, "lng": -68.0},
        "NG=F": {"name": "Natural Gas", "icon": "🔥", "unit": "USD/MMBtu", "lat": 42.0, "lng": -80.0},
        "ZW=F": {"name": "Wheat", "icon": "🌾", "unit": "USD/bu", "lat": 46.0, "lng": -100.0},
        "KC=F": {"name": "Coffee", "icon": "☕", "unit": "USD/lb", "lat": -15.0, "lng": -47.0},
    }
    yahoo = registry.get("yahoo")
    results = []
    if yahoo:
        import asyncio
        quotes = await asyncio.gather(
            *[yahoo.fetch_quote(s) for s in COMMODITY_MAP.keys()],
            return_exceptions=True,
        )
        for (symbol, meta), quote in zip(COMMODITY_MAP.items(), quotes):
            price = quote.price if isinstance(quote, object) and hasattr(quote, 'price') else 0
            change = quote.change_pct if isinstance(quote, object) and hasattr(quote, 'change_pct') else 0
            results.append({**meta, "symbol": symbol, "price": price, "change_pct": change})
    else:
        for symbol, meta in COMMODITY_MAP.items():
            results.append({**meta, "symbol": symbol, "price": 0, "change_pct": 0})
    return {"commodities": results}


@router.get("/map/bonds")
async def map_bonds(user: dict = Depends(get_current_user)):
    """Return bond yields with positions + live data."""
    BOND_MAP = {
        "^TNX": {"country": "US", "name": "US Treasury 10Y", "lat": 38.9, "lng": -77.0},
        "T10YIE": {"country": "GB", "name": "UK Gilt 10Y", "lat": 51.5, "lng": -0.1},
        "DE10Y": {"country": "DE", "name": "German Bund 10Y", "lat": 52.5, "lng": 13.4},
        "JP10Y": {"country": "JP", "name": "Japan JGB 10Y", "lat": 35.7, "lng": 139.7},
        "IN10Y": {"country": "IN", "name": "India 10Y", "lat": 28.6, "lng": 77.2},
        "BR10Y": {"country": "BR", "name": "Brazil 10Y", "lat": -15.8, "lng": -47.9},
        "CN10Y": {"country": "CN", "name": "China 10Y", "lat": 35.0, "lng": 105.0},
        "AU10Y": {"country": "AU", "name": "Australia 10Y", "lat": -25.0, "lng": 133.0},
        "CH10Y": {"country": "CH", "name": "Switzerland 10Y", "lat": 46.8, "lng": 8.2},
        "CA10Y": {"country": "CA", "name": "Canada 10Y", "lat": 43.6, "lng": -79.4},
    }
    yahoo = registry.get("yahoo")
    results = []
    if yahoo:
        import asyncio
        quotes = await asyncio.gather(
            *[yahoo.fetch_quote(s) for s in BOND_MAP.keys()],
            return_exceptions=True,
        )
        for (symbol, meta), quote in zip(BOND_MAP.items(), quotes):
            yield_val = quote.price if isinstance(quote, object) and hasattr(quote, 'price') else meta.get("_yield", 0)
            results.append({**meta, "symbol": symbol, "yield": yield_val})
    else:
        for symbol, meta in BOND_MAP.items():
            results.append({**meta, "symbol": symbol, "yield": 0})
    return {"bonds": results}


@router.get("/map/defi-protocols")
async def map_defi_protocols(
    limit: int = Query(50, description="Max protocols"),
    user: dict = Depends(get_current_user),
):
    """Return DeFi protocols with approximate geographic positions based on chain."""
    CHAIN_COORDS = {
        "Ethereum": (45.0, 10.0),
        "Solana": (37.8, -122.4),
        "BSC": (22.3, 114.1),
        "Polygon": (41.9, 12.5),
        "Arbitrum": (48.8, 2.3),
        "Optimism": (52.5, 13.4),
        "Avalanche": (39.7, -104.9),
        "Base": (37.8, -122.4),
        "Sui": (-33.9, 151.2),
        "Aptos": (37.6, 127.0),
        "Near": (55.7, 37.6),
        "Fantom": (45.4, 12.3),
        "Tron": (39.9, 116.4),
        "Cardano": (52.2, 21.0),
        "Polkadot": (59.9, 10.8),
    }
    defillama = registry.get("defillama")
    if not defillama:
        return {"protocols": [], "count": 0}
    protocols = await defillama.fetch_protocols()
    results = []
    for p in protocols[:limit]:
        chain = p.chain or "Ethereum"
        coords = None
        for c_name, c_pos in CHAIN_COORDS.items():
            if c_name.lower() in chain.lower() or chain.lower() in c_name.lower():
                coords = c_pos
                break
        if not coords:
            coords = (20.0, 0.0)
        results.append({
            "name": p.name,
            "chain": chain,
            "tvl": p.tvl,
            "category": p.category or "DeFi",
            "change_24h": p.change_24h,
            "lat": coords[0],
            "lng": coords[1],
        })
    return {"protocols": results, "count": len(results)}


