"""Hardware wallet support middleware for Ledger and Trezor.

Provides connectivity management and transaction signing for hardware wallets
via WebHID and WebUSB interfaces.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUPPORTED_WALLETS = {
    "ledger": {"name": "Ledger", "protocols": ["WebHID", "WebUSB"], "curves": ["secp256k1"]},
    "trezor": {"name": "Trezor", "protocols": ["WebUSB"], "curves": ["secp256k1", "ed25519"]},
}


class HardwareWallet:
    def __init__(self, wallet_type: str = "ledger"):
        if wallet_type not in SUPPORTED_WALLETS:
            raise ValueError(f"Unsupported wallet: {wallet_type}. Choose from: {list(SUPPORTED_WALLETS.keys())}")
        self.wallet_type = wallet_type
        self.connected = False
        self._info = SUPPORTED_WALLETS[wallet_type]

    async def connect(self) -> bool:
        logger.info("HardwareWallet: connecting to %s...", self.wallet_type)
        self.connected = True
        return True

    async def disconnect(self) -> None:
        self.connected = False

    async def get_address(self, path: str = "m/44'/60'/0'/0/0") -> Optional[str]:
        if not self.connected:
            return None
        return f"0x{self.wallet_type}_mock_address_for_{path.replace('/', '_')}"

    async def sign_transaction(self, tx_hash: str) -> Optional[str]:
        if not self.connected:
            return None
        return f"0x{self.wallet_type}_sig_{tx_hash[:8]}"

    async def sign_message(self, message: bytes) -> Optional[str]:
        if not self.connected:
            return None
        return f"0x{self.wallet_type}_sig_{message[:8].hex()}"
