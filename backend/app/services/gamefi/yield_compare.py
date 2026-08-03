import logging
logger = logging.getLogger(__name__)

YIELDS = [
    {"strategy": "Axie Infinity Breeding", "game": "Axie Infinity", "apy": 35.0, "risk": "high", "min_investment_usd": 500, "liquidity": "medium", "active_players": 280000},
    {"strategy": "Sandbox Land Rental", "game": "The Sandbox", "apy": 18.5, "risk": "medium", "min_investment_usd": 5000, "liquidity": "low", "active_players": 95000},
    {"strategy": "Decentraland Land Rental", "game": "Decentraland", "apy": 15.2, "risk": "medium", "min_investment_usd": 8000, "liquidity": "low", "active_players": 45000},
    {"strategy": "YGG Scholarship Pool", "game": "Yield Guild Games", "apy": 42.0, "risk": "high", "min_investment_usd": 1000, "liquidity": "high", "active_players": 12500},
    {"strategy": "Splinterlands Card Rental", "game": "Splinterlands", "apy": 22.0, "risk": "medium", "min_investment_usd": 200, "liquidity": "medium", "active_players": 420000},
    {"strategy": "Gods Unchained Card Rental", "game": "Gods Unchained", "apy": 28.5, "risk": "medium", "min_investment_usd": 300, "liquidity": "medium", "active_players": 65000},
]

async def list_all() -> list[dict]:
    return sorted(YIELDS, key=lambda x: x["apy"], reverse=True)

async def by_game(game: str) -> list[dict]:
    return [y for y in YIELDS if game.lower() in y["game"].lower()]

async def by_risk(max_risk: str = "high") -> list[dict]:
    risk_order = {"low": 0, "medium": 1, "high": 2}
    max_order = risk_order.get(max_risk, 2)
    return sorted([y for y in YIELDS if risk_order.get(y["risk"], 99) <= max_order], key=lambda x: x["apy"], reverse=True)

async def best_apy(min_investment: float = 0) -> dict:
    candidates = [y for y in YIELDS if y["min_investment_usd"] <= min_investment or min_investment == 0]
    return max(candidates, key=lambda x: x["apy"]) if candidates else {"error": "No strategies found"}
