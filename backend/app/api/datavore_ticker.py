"""datavore_ticker.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
@router.get("/earnings/{ticker}")
async def earnings(ticker: str, user: dict = Depends(get_current_user)):
    provider = registry.get("finnhub")
    if provider:
        try: return await provider.fetch_earnings(ticker)
        except Exception: pass
    return {"ticker": ticker, "quarters": [], "note": "Finnhub not configured"}


@router.get("/recommendations/{ticker}")
async def recommendations(ticker: str, user: dict = Depends(get_current_user)):
    provider = registry.get("finnhub")
    if provider:
        try: return await provider.fetch_recommendations(ticker)
        except Exception: pass
    return {"ticker": ticker, "analysts": [], "note": "Finnhub not configured"}


@router.get("/ownership/{ticker}")
async def ownership(ticker: str, user: dict = Depends(get_current_user)):
    provider = registry.get("finnhub")
    if provider:
        try: return await provider.fetch_ownership(ticker)
        except Exception: pass
    return {"ticker": ticker, "ownership": [], "note": "Finnhub not configured"}


@router.get("/sec/{ticker}")
async def sec_filings(ticker: str, user: dict = Depends(get_current_user)):
    provider = registry.get("finnhub")
    if provider:
        try: return await provider.fetch_sec_filings(ticker)
        except Exception: pass
    return {"ticker": ticker, "filings": [], "note": "Finnhub not configured"}


@router.get("/risk-factors/{ticker}")
async def risk_factors(ticker: str, user: dict = Depends(get_current_user)):
    provider = _get_provider("securitiesdb")
    return await provider.fetch_risk_factors(ticker)


@router.get("/earnings-score/{ticker}")
async def earnings_score(ticker: str, user: dict = Depends(get_current_user)):
    provider = _get_provider("securitiesdb")
    return await provider.fetch_earnings_transparency(ticker)


@router.get("/fama-french/{ticker}")
async def fama_french(ticker: str, user: dict = Depends(get_current_user)):
    provider = _get_provider("securitiesdb")
    return await provider.fetch_fama_french(ticker)


@router.get("/passive-float/{ticker}")
async def passive_float(ticker: str, user: dict = Depends(get_current_user)):
    provider = _get_provider("securitiesdb")
    return await provider.fetch_passive_float(ticker)


@router.get("/globe/layers")
async def globe_layers():
    return {
        "layers": [
            {"id": "aircraft", "name": "Live Aircraft", "icon": "✈️", "provider": "opensky", "count": 500},
            {"id": "maritime", "name": "Ships & Ports", "icon": "🚢", "provider": "maritime", "count": 40},
            {"id": "companies", "name": "Companies", "icon": "🏢", "provider": "local", "count": 8000},
            {"id": "cats", "name": "Cat Hubs", "icon": "🐱", "provider": "local", "count": 10},
        ]
    }


@router.get("/globe/layer/{layer_id}")
async def globe_layer_data(layer_id: str):
    if layer_id == "aircraft":
        provider = _get_provider("opensky")
        if not provider:
            return {"aircraft": []}
        try:
            aircraft = await provider.fetch_globe_aircraft()
            return {"aircraft": aircraft}
        except Exception as e:
            return {"aircraft": [], "error": str(e)}
    if layer_id == "maritime":
        provider = _get_provider("maritime")
        if not provider:
            return {"ships": [], "ports": [], "lanes": []}
        try:
             return await provider.fetch_globe_maritime()
        except Exception as e:
            return {"ships": [], "ports": [], "lanes": [], "error": str(e)}
    if layer_id == "satellites":
        try:
            provider = _get_provider("celestrak")
            if provider:
                return await provider.fetch_globe_satellites()
        except Exception as e:
            return {"satellites": [], "error": str(e)}
    if layer_id == "mining":
        try:
            provider = _get_provider("mining")
            if provider:
                mines = provider.fetch_mines()
                return {"mines": mines}
        except Exception as e:
            return {"mines": [], "error": str(e)}
    if layer_id == "iss":
        try:
            provider = _get_provider("iss")
            if provider:
                return await provider.fetch_iss_location()
        except Exception as e:
            return {"iss": None, "error": str(e)}
    if layer_id == "weather":
        provider = _get_provider("weather")
        if provider:
            return await provider.fetch_global_weather()
        return {"weather": []}
    if layer_id == "companies":
        try:
            ...
        except Exception:
            return {"companies": []}
    return {"error": f"Unknown layer: {layer_id}"}


