import logging

logger = logging.getLogger(__name__)

FLOOR_ALERTS = {}
COLLECTIONS = {
    "bored-ape-yacht-club": {"floor_eth": 28.0, "change_24h": -2.5, "volume_7d_eth": 12500, "sales_24h": 42},
    "cryptopunks": {"floor_eth": 55.0, "change_24h": 1.2, "volume_7d_eth": 8200, "sales_24h": 18},
    "azuki": {"floor_eth": 5.5, "change_24h": -1.8, "volume_7d_eth": 4100, "sales_24h": 85},
    "pudgy-penguins": {"floor_eth": 8.5, "change_24h": 3.4, "volume_7d_eth": 6500, "sales_24h": 120},
    "milady": {"floor_eth": 3.2, "change_24h": 5.6, "volume_7d_eth": 2800, "sales_24h": 65},
}


async def get_floor(collection: str) -> dict:
    c = COLLECTIONS.get(collection)
    if not c:
        return {"error": "Collection not found"}
    return {"collection": collection, **c}


async def monitor_all() -> list[dict]:
    return [{"collection": k, **v} for k, v in COLLECTIONS.items()]


async def set_alert(collection: str, threshold_eth: float, direction: str = "below") -> dict:
    alert_id = f"alert_{collection}_{len(FLOOR_ALERTS)}"
    FLOOR_ALERTS[alert_id] = {"collection": collection, "threshold": threshold_eth, "direction": direction}
    return {"alert_id": alert_id, "collection": collection, "threshold_eth": threshold_eth, "direction": direction}


async def list_alerts() -> list[dict]:
    return [{"id": k, **v} for k, v in FLOOR_ALERTS.items()]


async def estimate_value(collection: str, token_id: int, attributes: list[str] = None) -> dict:
    c = COLLECTIONS.get(collection)
    if not c:
        return {"error": "Collection not found"}
    base_floor = c["floor_eth"]
    attr_bonus = len(attributes or []) * 0.15
    trait_mult = 1.0 + min(attr_bonus, 2.0)
    estimated = round(base_floor * trait_mult, 2)
    return {
        "collection": collection,
        "token_id": token_id,
        "floor_price": base_floor,
        "attributes": attributes or [],
        "attribute_bonus_pct": round((trait_mult - 1) * 100, 1),
        "estimated_value_eth": estimated,
        "estimated_value_usd": round(estimated * 3100, 2),
        "confidence": "high" if trait_mult < 1.5 else "medium",
    }
