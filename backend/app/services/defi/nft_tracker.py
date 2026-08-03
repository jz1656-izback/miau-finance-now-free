import logging

logger = logging.getLogger(__name__)

PORTFOLIO = {
    "0xabc...def": [
        {"collection": "Bored Ape Yacht Club", "token_id": 1234, "contract": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "chain": "ethereum", "acquired_price_eth": 42.5, "current_floor": 28.0, "rarity_rank": 750, "rarity_pct": 15.0},
        {"collection": "CryptoPunks", "token_id": 5678, "contract": "0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB", "chain": "ethereum", "acquired_price_eth": 65.0, "current_floor": 55.0, "rarity_rank": 120, "rarity_pct": 2.5},
        {"collection": "Azuki", "token_id": 9012, "contract": "0xED5AF388653567Af2F388E6224dC7C4b3241C544", "chain": "ethereum", "acquired_price_eth": 8.2, "current_floor": 5.5, "rarity_rank": 3400, "rarity_pct": 35.0},
    ]
}


async def get_portfolio(wallet_address: str) -> list[dict]:
    nfts = PORTFOLIO.get(wallet_address.lower(), [])
    total_cost = sum(n["acquired_price_eth"] for n in nfts)
    total_value = sum(n["current_floor"] for n in nfts)
    return {
        "wallet": wallet_address,
        "nft_count": len(nfts),
        "total_cost_eth": round(total_cost, 2),
        "total_value_eth": round(total_value, 2),
        "pnl_eth": round(total_value - total_cost, 2),
        "pnl_pct": round((total_value / total_cost - 1) * 100, 1) if total_cost else 0,
        "nfts": nfts,
    }


NFT_COLLECTIONS = {
    "bored-ape-yacht-club": {"name": "Bored Ape Yacht Club", "floor_eth": 28.0, "floor_change_24h": -2.5, "volume_7d": "12,500 ETH", "items": 10000, "owners": 5800},
    "cryptopunks": {"name": "CryptoPunks", "floor_eth": 55.0, "floor_change_24h": 1.2, "volume_7d": "8,200 ETH", "items": 10000, "owners": 3600},
    "azuki": {"name": "Azuki", "floor_eth": 5.5, "floor_change_24h": -1.8, "volume_7d": "4,100 ETH", "items": 10000, "owners": 4800},
    "milady": {"name": "Milady Maker", "floor_eth": 3.2, "floor_change_24h": 5.6, "volume_7d": "2,800 ETH", "items": 10000, "owners": 4200},
    "pudgy-penguins": {"name": "Pudgy Penguins", "floor_eth": 8.5, "floor_change_24h": 3.4, "volume_7d": "6,500 ETH", "items": 8888, "owners": 4100},
}


async def get_floor_price(collection_slug: str) -> dict:
    col = NFT_COLLECTIONS.get(collection_slug)
    if not col:
        return {"error": f"Collection '{collection_slug}' not found"}
    return col


async def list_collections() -> list[dict]:
    return [{"slug": k, **v} for k, v in NFT_COLLECTIONS.items()]


async def get_rarity(collection_slug: str, token_id: int) -> dict:
    col = NFT_COLLECTIONS.get(collection_slug)
    if not col:
        return {"error": "Collection not found"}
    rarity_pct = (token_id % 100) / 100
    rank = int(col["items"] * rarity_pct)
    return {
        "collection": col["name"],
        "token_id": token_id,
        "items": col["items"],
        "rarity_rank": max(rank, 1),
        "rarity_pct": round(rarity_pct * 100, 1),
        "tier": "legendary" if rarity_pct < 0.01 else ("rare" if rarity_pct < 0.1 else "common"),
    }
