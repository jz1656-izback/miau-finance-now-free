"""EVM wallet support (MetaMask, Rainbow, Coinbase Wallet)."""

from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

try:
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    _web3_available = True
except ImportError:
    Web3 = None
    geth_poa_middleware = None
    _web3_available = False
    logger.warning("web3 package not installed — EVM wallet features unavailable")

RPC_URLS: dict[str, str] = {
    "ethereum": "https://cloudflare-eth.com",
    "ethereum_sepolia": "https://rpc.sepolia.org",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
}


def _ensure_web3():
    if not _web3_available:
        raise RuntimeError("web3 package is required for EVM operations. Install with: pip install web3")


def _get_w3(chain: str) -> Any:
    _ensure_web3()
    url = RPC_URLS.get(chain, RPC_URLS["ethereum"])
    w3 = Web3(Web3.HTTPProvider(url))
    if chain in ("polygon",):
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


async def get_balance(address: str, chain: str = "ethereum") -> dict[str, Any]:
    _ensure_web3()
    w3 = _get_w3(chain)
    checksum = w3.to_checksum_address(address)
    wei_balance = w3.eth.get_balance(checksum)
    eth_balance = w3.from_wei(wei_balance, "ether")
    return {
        "address": address,
        "chain": chain,
        "balance": float(eth_balance),
        "balance_wei": str(wei_balance),
    }


async def get_token_balances(address: str, chain: str = "ethereum") -> list[dict[str, Any]]:
    _ensure_web3()
    w3 = _get_w3(chain)
    checksum = w3.to_checksum_address(address)
    native = w3.from_wei(w3.eth.get_balance(checksum), "ether")
    tokens = [{"symbol": "ETH", "name": "Ether", "balance": float(native), "decimals": 18}]
    return tokens


async def get_transaction_count(address: str, chain: str = "ethereum") -> int:
    _ensure_web3()
    w3 = _get_w3(chain)
    return w3.eth.get_transaction_count(w3.to_checksum_address(address))


async def is_valid_address(address: str) -> bool:
    _ensure_web3()
    try:
        return Web3.is_address(address)
    except Exception:
        return False
    try:
        return Web3.is_address(address)
    except Exception:
        return False
