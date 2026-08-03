import logging

logger = logging.getLogger(__name__)

LISTINGS = [
    {"id": "listing_1", "collection": "Bored Ape Yacht Club", "token_id": 1001, "price_eth": 32.5, "seller": "0x111...aaa", "marketplace": "OpenSea", "expires_in": "3d", "traits": ["gold_fur", "laser_eyes"]},
    {"id": "listing_2", "collection": "Bored Ape Yacht Club", "token_id": 1002, "price_eth": 29.0, "seller": "0x222...bbb", "marketplace": "Blur", "expires_in": "1d", "traits": ["blue_fur", "party_hat"]},
    {"id": "listing_3", "collection": "CryptoPunks", "token_id": 5000, "price_eth": 59.0, "seller": "0x333...ccc", "marketplace": "OpenSea", "expires_in": "7d", "traits": ["bandana", "smile"]},
    {"id": "listing_4", "collection": "Azuki", "token_id": 2001, "price_eth": 6.8, "seller": "0x444...ddd", "marketplace": "Blur", "expires_in": "2d", "traits": ["red_kimono", "straw_hat"]},
    {"id": "listing_5", "collection": "Pudgy Penguins", "token_id": 3001, "price_eth": 9.2, "seller": "0x555...eee", "marketplace": "OpenSea", "expires_in": "5d", "traits": ["crown", "sunglasses"]},
]

MARKETPLACES = [
    {"name": "OpenSea", "url": "https://opensea.io", "volume_30d": "$2.1B", "fee_pct": 2.5},
    {"name": "Blur", "url": "https://blur.io", "volume_30d": "$1.8B", "fee_pct": 0.5},
    {"name": "LooksRare", "url": "https://looksrare.org", "volume_30d": "$120M", "fee_pct": 2.0},
    {"name": "X2Y2", "url": "https://x2y2.io", "volume_30d": "$80M", "fee_pct": 0.5},
]


async def list_listings(collection: str = None, marketplace: str = None, sort: str = "price_asc") -> list[dict]:
    items = list(LISTINGS)
    if collection:
        items = [i for i in items if collection.lower() in i["collection"].lower()]
    if marketplace:
        items = [i for i in items if i["marketplace"].lower() == marketplace.lower()]
    items.sort(key=lambda x: x["price_eth"])
    return items


async def get_listing(listing_id: str) -> dict:
    for l in LISTINGS:
        if l["id"] == listing_id:
            return l
    return {"error": "Listing not found"}


async def simulate_purchase(listing_id: str) -> dict:
    for l in LISTINGS:
        if l["id"] == listing_id:
            fee = l["price_eth"] * 0.025
            total = l["price_eth"] + fee
            return {
                "listing_id": listing_id,
                "collection": l["collection"],
                "token_id": l["token_id"],
                "price_eth": l["price_eth"],
                "marketplace_fee_eth": round(fee, 4),
                "total_cost_eth": round(total, 4),
                "total_cost_usd": round(total * 3100, 2),
                "marketplace": l["marketplace"],
            }
    return {"error": "Listing not found"}


async def list_marketplaces() -> list[dict]:
    return MARKETPLACES
