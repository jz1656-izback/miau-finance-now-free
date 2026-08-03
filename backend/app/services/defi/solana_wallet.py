"""Solana wallet support (Phantom, Solflare)."""

from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

SOLANA_RPC = "https://api.mainnet-beta.solana.com"


async def get_balance(address: str) -> dict[str, Any]:
    try:
        import requests
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance", "params": [address]}
        resp = requests.post(SOLANA_RPC, json=payload, timeout=10)
        data = resp.json()
        lamports = data.get("result", {}).get("value", 0)
        sol = lamports / 1e9
        return {"address": address, "chain": "solana", "balance": sol, "lamports": lamports}
    except Exception as e:
        logger.warning("Solana RPC error: %s", e)
        return {"address": address, "chain": "solana", "balance": 0, "error": str(e)}


async def get_token_balances(address: str) -> list[dict[str, Any]]:
    try:
        import requests
        payload = {"jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner", "params": [address, {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"}, {"encoding": "jsonParsed"}]}
        resp = requests.post(SOLANA_RPC, json=payload, timeout=10)
        data = resp.json()
        tokens = []
        for account in data.get("result", {}).get("value", []):
            info = account.get("account", {}).get("data", {}).get("parsed", {}).get("info", {})
            mint = info.get("mint", "")
            amount = int(info.get("tokenAmount", {}).get("amount", 0))
            decimals = int(info.get("tokenAmount", {}).get("decimals", 0))
            tokens.append({"mint": mint, "balance": amount / (10 ** decimals), "decimals": decimals})
        return tokens
    except Exception as e:
        logger.warning("Solana token RPC error: %s", e)
        return []


async def is_valid_address(address: str) -> bool:
    if len(address) < 32 or len(address) > 44:
        return False
    import base58
    try:
        base58.b58decode(address)
        return True
    except Exception:
        return False
