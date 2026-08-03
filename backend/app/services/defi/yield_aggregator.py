import logging
from typing import Optional

logger = logging.getLogger(__name__)

SOURCES = [
    {"protocol": "Aave",     "asset": "USDC", "apy": 4.8, "tvl": "$2.1B", "risk": "low", "type": "lending"},
    {"protocol": "Aave",     "asset": "WETH", "apy": 2.5, "tvl": "$1.2B", "risk": "low", "type": "lending"},
    {"protocol": "Aave",     "asset": "DAI",  "apy": 4.5, "tvl": "$900M", "risk": "low", "type": "lending"},
    {"protocol": "Curve",    "asset": "3Pool",  "apy": 3.2, "tvl": "$450M", "risk": "low", "type": "lp"},
    {"protocol": "Curve",    "asset": "stETH",  "apy": 2.8, "tvl": "$2.1B", "risk": "low", "type": "lp"},
    {"protocol": "Lido",     "asset": "stETH",  "apy": 3.25,"tvl": "$32.5B","risk": "low", "type": "staking"},
    {"protocol": "Yearn",    "asset": "yvUSDC", "apy": 5.8, "tvl": "$420M", "risk": "medium", "type": "vault"},
    {"protocol": "Yearn",    "asset": "yvDAI",  "apy": 5.5, "tvl": "$180M", "risk": "medium", "type": "vault"},
    {"protocol": "Maker",    "asset": "DAI",    "apy": 3.75,"tvl": "$5.2B", "risk": "low", "type": "dai_savings"},
    {"protocol": "Solana",   "asset": "SOL",    "apy": 6.8, "tvl": "$350M", "risk": "medium", "type": "staking"},
    {"protocol": "Jupiter",  "asset": "SOL-USDC","apy": 12.5,"tvl": "$180M","risk": "high", "type": "lp"},
    {"protocol": "Marinade", "asset": "mSOL",   "apy": 6.5, "tvl": "$520M", "risk": "medium", "type": "staking"},
    {"protocol": "Raydium",  "asset": "SOL-USDC","apy": 18.2,"tvl": "$95M", "risk": "high", "type": "lp"},
]


async def get_all_yields(min_apy: float = 0, max_risk: str = "high") -> list[dict]:
    results = []
    for s in SOURCES:
        if s["apy"] < min_apy:
            continue
        risk_order = {"low": 0, "medium": 1, "high": 2}
        if risk_order.get(s["risk"], 99) > risk_order.get(max_risk, 2):
            continue
        results.append(dict(s))
    results.sort(key=lambda x: x["apy"], reverse=True)
    return results


async def best_yield(asset: str = "USDC", min_tvl: str = "$100M") -> list[dict]:
    candidates = [s for s in SOURCES if s["asset"] == asset]
    candidates.sort(key=lambda x: x["apy"], reverse=True)
    return candidates[:5]


async def get_protocol_summary(protocol: str) -> dict:
    yields = [s for s in SOURCES if s["protocol"].lower() == protocol.lower()]
    if not yields:
        return {"protocol": protocol, "error": "Protocol not found"}
    best = max(y["apy"] for y in yields)
    total_tvl = sum(float(y["tvl"].replace("$", "").replace("B", "e9").replace("M", "e6")) for y in yields)
    return {
        "protocol": protocol,
        "products": yields,
        "best_apy": best,
        "total_tvl": total_tvl,
        "product_count": len(yields),
    }
