"""Gas estimator and optimizer for Ethereum and EVM chains."""

from __future__ import annotations

import logging
from typing import Any

from web3 import Web3

logger = logging.getLogger(__name__)

RPC_URLS = {
    "ethereum": "https://cloudflare-eth.com",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
}


async def estimate_gas(chain: str = "ethereum") -> dict[str, Any]:
    url = RPC_URLS.get(chain, RPC_URLS["ethereum"])
    w3 = Web3(Web3.HTTPProvider(url))
    fee_history = w3.eth.fee_history(10, "latest", [25, 50, 75])
    base_fee = w3.eth.get_block("latest").get("baseFeePerGas", 0)
    priority_fees = [f["priorityFeePerGas"][0] for f in fee_history.get("reward", []) if f.get("priorityFeePerGas")]
    avg_priority = sum(priority_fees) // len(priority_fees) if priority_fees else 1_000_000_000
    return {
        "chain": chain,
        "base_fee_gwei": round(w3.from_wei(base_fee, "gwei"), 2),
        "priority_fee_gwei": round(w3.from_wei(avg_priority, "gwei"), 2),
        "max_fee_gwei": round(w3.from_wei(base_fee + avg_priority, "gwei"), 2),
        "gas_price_gwei": round(w3.from_wei(w3.eth.gas_price, "gwei"), 2),
    }


GAS_SPEED_LABELS = {
    "slow": {"multiplier": 0.9, "label": "Slow (~30min)"},
    "standard": {"multiplier": 1.0, "label": "Standard (~5min)"},
    "fast": {"multiplier": 1.2, "label": "Fast (~30s)"},
    "instant": {"multiplier": 1.5, "label": "Instant (~15s)"},
}
