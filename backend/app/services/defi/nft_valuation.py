"""NFT valuation model — floor price, trait-based pricing, collection analytics."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

FLOOR_PRICES: dict[str, dict] = {
    "bayc": {"name": "Bored Ape Yacht Club", "floor_eth": 32.5, "floor_usd": 97500, "volume_7d_eth": 12500, "items": 10000, "owners": 6200},
    "cryptopunks": {"name": "CryptoPunks", "floor_eth": 4500, "floor_usd": 13500000, "volume_7d_eth": 8900, "items": 10000, "owners": 3600},
    "azuki": {"name": "Azuki", "floor_eth": 6.2, "floor_usd": 18600, "volume_7d_eth": 4500, "items": 10000, "owners": 4800},
    "doodles": {"name": "Doodles", "floor_eth": 3.8, "floor_usd": 11400, "volume_7d_eth": 2100, "items": 10000, "owners": 5200},
    "clonex": {"name": "Clone X", "floor_eth": 2.1, "floor_usd": 6300, "volume_7d_eth": 1800, "items": 20000, "owners": 7100},
    "moonbirds": {"name": "Moonbirds", "floor_eth": 8.5, "floor_usd": 25500, "volume_7d_eth": 3200, "items": 10000, "owners": 4100},
}

TRAIT_PREMIUMS: dict[str, dict[str, float]] = {
    "bayc": {"Gold Fur": 2.5, "Laser Eyes": 3.0, "Crown": 5.0, "Robot": 4.0},
    "cryptopunks": {"Alien": 10.0, "Ape": 3.0, "Zombie": 2.5, "Blue Bandana": 1.5},
}


def get_floor(collection_id: str) -> Optional[dict]:
    data = FLOOR_PRICES.get(collection_id.lower())
    if not data:
        return None
    return data


def estimate_nft_value(collection_id: str, traits: Optional[list[str]] = None, rarity_multiplier: float = 1.0) -> dict:
    floor_data = get_floor(collection_id)
    if not floor_data:
        return {"error": f"Unknown collection: {collection_id}"}

    base_price = floor_data["floor_eth"]
    trait_premium = 1.0
    if traits and collection_id.lower() in TRAIT_PREMIUMS:
        premiums = TRAIT_PREMIUMS[collection_id.lower()]
        for trait in traits:
            trait_premium *= premiums.get(trait, 1.0)

    estimated = base_price * trait_premium * rarity_multiplier
    return {
        "collection": floor_data["name"],
        "base_floor_eth": base_price,
        "trait_premium": round(trait_premium, 2),
        "rarity_multiplier": rarity_multiplier,
        "estimated_value_eth": round(estimated, 2),
        "estimated_value_usd": round(estimated * 3000, 2),
    }


def list_collections() -> list[dict]:
    return [
        {"id": k, "name": v["name"], "floor_eth": v["floor_eth"], "floor_usd": v["floor_usd"], "items": v["items"]}
        for k, v in FLOOR_PRICES.items()
    ]
