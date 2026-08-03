import logging
logger = logging.getLogger(__name__)

TOKENS = {
    "AXS": {"name": "Axie Infinity", "price": 8.45, "change_24h": 3.2, "market_cap": "$1.2B", "volume_24h": "$85M", "category": "fighting"},
    "SAND": {"name": "The Sandbox", "price": 0.52, "change_24h": -1.8, "market_cap": "$780M", "volume_24h": "$42M", "category": "building"},
    "MANA": {"name": "Decentraland", "price": 0.48, "change_24h": 2.5, "market_cap": "$620M", "volume_24h": "$38M", "category": "building"},
    "GALA": {"name": "Gala Games", "price": 0.035, "change_24h": 5.1, "market_cap": "$320M", "volume_24h": "$28M", "category": "ecosystem"},
    "IMX": {"name": "Immutable X", "price": 1.85, "change_24h": -2.3, "market_cap": "$2.4B", "volume_24h": "$95M", "category": "layer2"},
    "PRIME": {"name": "Echelon Prime", "price": 12.20, "change_24h": 8.5, "market_cap": "$450M", "volume_24h": "$22M", "category": "trading_card"},
    "ILV": {"name": "Illuvium", "price": 95.50, "change_24h": 1.2, "market_cap": "$180M", "volume_24h": "$8M", "category": "rpg"},
    "YGG": {"name": "Yield Guild Games", "price": 0.62, "change_24h": -0.5, "market_cap": "$120M", "volume_24h": "$5M", "category": "guild"},
}

async def list_tokens() -> list[dict]:
    return [{"symbol": k, **v} for k, v in TOKENS.items()]

async def get_token(symbol: str) -> dict:
    t = TOKENS.get(symbol.upper())
    if not t:
        return {"error": f"Token {symbol} not found"}
    return {"symbol": symbol.upper(), **t}

async def get_by_category(category: str) -> list[dict]:
    return [{"symbol": k, **v} for k, v in TOKENS.items() if v["category"] == category.lower()]
