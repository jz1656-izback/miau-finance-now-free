"""Multi-chain balance aggregation across EVM and Solana wallets."""

from __future__ import annotations

import logging
from typing import Any

from app.services.defi.evm_wallet import get_balance as get_evm_balance
from app.services.defi.evm_wallet import get_token_balances as get_evm_tokens
from app.services.defi.solana_wallet import get_balance as get_sol_balance

logger = logging.getLogger(__name__)

EVM_CHAINS = ["ethereum", "polygon", "arbitrum", "optimism"]


async def aggregate_balances(addresses: dict[str, list[str]]) -> dict[str, Any]:
    results: dict[str, Any] = {"wallets": [], "total_usd": 0.0}

    for chain, addrs in addresses.items():
        if chain == "solana":
            for addr in addrs:
                bal = await get_sol_balance(addr)
                results["wallets"].append(bal)
        elif chain in EVM_CHAINS:
            for addr in addrs:
                bal = await get_evm_balance(addr, chain)
                results["wallets"].append(bal)

    total_native = sum(w.get("balance", 0) for w in results["wallets"])
    results["total_native"] = round(total_native, 6)
    results["wallet_count"] = len(results["wallets"])
    results["chain_count"] = len([c for c in addresses if addresses[c]])
    return results


async def aggregate_all(addresses: dict[str, list[str]]) -> dict[str, Any]:
    return await aggregate_balances(addresses)
