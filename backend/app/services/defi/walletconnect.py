"""WalletConnect v2 SDK integration.

Session management, URI generation, chain switching, and wallet connectivity
via the WalletConnect v2 protocol.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

SUPPORTED_CHAINS: dict[str, dict[str, Any]] = {
    "ethereum": {"chain_id": 1, "rpc": "https://mainnet.infura.io/v3/", "explorer": "https://etherscan.io", "currency": "ETH"},
    "ethereum_sepolia": {"chain_id": 11155111, "rpc": "https://sepolia.infura.io/v3/", "explorer": "https://sepolia.etherscan.io", "currency": "ETH"},
    "polygon": {"chain_id": 137, "rpc": "https://polygon-rpc.com", "explorer": "https://polygonscan.com", "currency": "MATIC"},
    "arbitrum": {"chain_id": 42161, "rpc": "https://arb1.arbitrum.io/rpc", "explorer": "https://arbiscan.io", "currency": "ETH"},
    "optimism": {"chain_id": 10, "rpc": "https://mainnet.optimism.io", "explorer": "https://optimistic.etherscan.io", "currency": "ETH"},
    "solana": {"chain_id": -1, "rpc": "https://api.mainnet-beta.solana.com", "explorer": "https://explorer.solana.com", "currency": "SOL"},
}

WC_URI_PREFIX = "wc:"


def generate_uri() -> str:
    """Generate a WalletConnect v2 URI for QR code display."""
    return WC_URI_PREFIX + uuid.uuid4().hex + "@2?relay-protocol=irn&symKey=" + uuid.uuid4().hex[:64]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class WalletSession:
    """Represents an active WalletConnect session with a chain."""

    def __init__(self, topic: str, address: str, chain: str, metadata: Optional[dict] = None):
        self.topic = topic
        self.address = address
        self.chain = chain
        self.metadata = metadata or {}
        self.created_at = _now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "address": self.address,
            "chain": self.chain,
            "chain_id": SUPPORTED_CHAINS.get(self.chain, {}).get("chain_id"),
            "explorer": SUPPORTED_CHAINS.get(self.chain, {}).get("explorer"),
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


_sessions: dict[str, WalletSession] = {}


async def create_session(address: str, chain: str = "ethereum", metadata: Optional[dict] = None) -> dict[str, Any]:
    topic = uuid.uuid4().hex
    if chain not in SUPPORTED_CHAINS:
        raise ValueError(f"Unsupported chain: {chain}. Supported: {list(SUPPORTED_CHAINS.keys())}")
    session = WalletSession(topic=topic, address=address, chain=chain, metadata=metadata)
    _sessions[topic] = session
    logger.info("Wallet session created: %s (%s)", topic[:8], chain)
    return session.to_dict()


async def list_sessions() -> list[dict[str, Any]]:
    return [s.to_dict() for s in _sessions.values()]


async def get_session(topic: str) -> Optional[dict[str, Any]]:
    session = _sessions.get(topic)
    return session.to_dict() if session else None


async def disconnect(topic: str) -> bool:
    if topic in _sessions:
        del _sessions[topic]
        logger.info("Wallet session disconnected: %s", topic[:8])
        return True
    return False


async def switch_chain(topic: str, chain: str) -> Optional[dict[str, Any]]:
    if chain not in SUPPORTED_CHAINS:
        raise ValueError(f"Unsupported chain: {chain}")
    session = _sessions.get(topic)
    if not session:
        return None
    session.chain = chain
    logger.info("Session %s switched to %s", topic[:8], chain)
    return session.to_dict()
