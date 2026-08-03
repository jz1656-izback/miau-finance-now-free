import logging

logger = logging.getLogger(__name__)

BRIDGES = [
    {"name": "LayerZero", "type": "omnichain", "chains": ["Ethereum", "Arbitrum", "Optimism", "Polygon", "Base", "BNB", "Avalanche"], "tvl": "$3.2B", "fee_avg": "$0.50"},
    {"name": "Wormhole", "type": "cross-chain", "chains": ["Ethereum", "Solana", "Polygon", "BNB", "Avalanche", "Arbitrum", "Optimism"], "tvl": "$1.8B", "fee_avg": "$0.30"},
    {"name": "Stargate", "type": "liquidity", "chains": ["Ethereum", "Arbitrum", "Optimism", "Polygon", "BNB", "Avalanche"], "tvl": "$800M", "fee_avg": "$0.40"},
    {"name": "Across", "type": "intent-based", "chains": ["Ethereum", "Arbitrum", "Optimism", "Base"], "tvl": "$250M", "fee_avg": "$0.20"},
    {"name": "Hop", "type": "liquidity", "chains": ["Ethereum", "Arbitrum", "Optimism", "Polygon", "BNB"], "tvl": "$150M", "fee_avg": "$0.35"},
]

ASSET_BRIDGES = {
    "USDC": [b["name"] for b in BRIDGES],
    "USDT": [b["name"] for b in BRIDGES if b["name"] != "Across"],
    "WETH": [b["name"] for b in BRIDGES if b["name"] in ("LayerZero", "Wormhole", "Stargate")],
    "WBTC": ["LayerZero", "Wormhole"],
    "DAI": ["LayerZero", "Wormhole", "Stargate"],
    "SOL": ["Wormhole"],
}


async def list_bridges() -> list[dict]:
    return [{"name": b["name"], "type": b["type"], "chains": b["chains"],
             "tvl": b["tvl"], "fee_avg": b["fee_avg"]} for b in BRIDGES]


async def get_bridge(name: str) -> dict:
    for b in BRIDGES:
        if b["name"].lower() == name.lower():
            return b
    return {"error": f"Bridge {name} not found"}


async def supported_assets(bridge: str = None) -> dict:
    if bridge:
        return {a: b_list for a, b_list in ASSET_BRIDGES.items() if bridge in b_list}
    return {
        "assets": list(ASSET_BRIDGES.keys()),
        "bridges": {a: b_list for a, b_list in ASSET_BRIDGES.items()},
    }


async def simulate_bridge(asset: str, amount: float, from_chain: str, to_chain: str, bridge: str = "LayerZero") -> dict:
    fee = 0.50 if bridge == "LayerZero" else 0.30
    estimated_time = "5-20 min" if bridge != "Wormhole" else "1-5 min"
    return {
        "asset": asset,
        "amount": amount,
        "from_chain": from_chain,
        "to_chain": to_chain,
        "bridge": bridge,
        "fee_usd": fee,
        "estimated_time": estimated_time,
        "estimated_received": round(amount - fee / (amount if amount > 0 else 1), 4),
    }
