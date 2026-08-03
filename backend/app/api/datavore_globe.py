"""datavore_globe.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
@router.get("/globe/batch")
async def globe_batch(
    layers: str = Query("aircraft,maritime", min_length=1, max_length=200, description="Comma-separated layer names"),
):
    requested = [l.strip().lower() for l in layers.split(",") if l.strip()]
    results: dict = {}
    for layer in requested:
        try:
            if layer == "aircraft":
                p = _get_provider("opensky")
                results[layer] = await p.fetch_globe_aircraft() if p else {"error": "provider not available"}
            elif layer == "maritime":
                p = _get_provider("maritime")
                results[layer] = await p.fetch_globe_maritime() if p else {"error": "provider not available"}
            elif layer == "satellites":
                p = _get_provider("celestrak")
                results[layer] = await p.fetch_globe_satellites() if p else {"error": "provider not available"}
            elif layer == "mining":
                p = _get_provider("mining")
                results[layer] = p.fetch_mines() if p else {"error": "provider not available"}
            elif layer == "military_bases":
                p = _get_provider("geopolitical")
                results[layer] = p.fetch_military_bases() if p else {"error": "not available"}
            elif layer == "nuclear":
                p = _get_provider("geopolitical")
                results[layer] = p.fetch_nuclear_facilities() if p else {"error": "not available"}
            elif layer == "defense_spending":
                p = _get_provider("geopolitical")
                results[layer] = p.fetch_defense_spending() if p else {"error": "not available"}
            elif layer == "oil_fields":
                p = _get_provider("energy")
                results[layer] = p.fetch_oil_fields() if p else {"error": "not available"}
            elif layer == "renewable":
                p = _get_provider("energy")
                results[layer] = p.fetch_renewable() if p else {"error": "not available"}
            elif layer == "ufo":
                p = _get_provider("alien")
                results[layer] = p.fetch_ufo_sightings() if p else {"error": "not available"}
            elif layer == "ancient_sites":
                p = _get_provider("alien")
                results[layer] = p.fetch_ancient_sites() if p else {"error": "not available"}
            elif layer == "conflicts":
                p = _get_provider("conflict")
                results[layer] = p.fetch_conflict_zones() if p else {"error": "not available"}
            elif layer == "cargo":
                p = _get_provider("cargo")
                if p:
                    results[layer] = {"hubs": p.fetch_cargo_hubs(), "routes": p.fetch_cargo_routes()}
                else:
                    results[layer] = {"error": "not available"}
            elif layer == "supply_chain":
                p_corp = _get_provider("corporate")
                p_cargo = _get_provider("cargo")
                results[layer] = {
                    "companies": p_corp.fetch() if p_corp else [],
                    "supplier_hubs": p_cargo.fetch_cargo_hubs() if p_cargo else [],
                }
            else:
                results[layer] = {"error": f"Unknown layer: {layer}"}
        except Exception as e:
            results[layer] = {"error": str(e)}
    return {"layers": results, "count": len(results)}
