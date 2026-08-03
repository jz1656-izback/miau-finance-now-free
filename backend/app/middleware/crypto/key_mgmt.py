import logging
import os
from typing import Optional

from app.middleware.crypto.kyber import KyberKEM
from app.middleware.crypto.dilithium import DilithiumSigner
from app.middleware.crypto.falcon import FalconSigner

logger = logging.getLogger(__name__)


class PQCKeyManager:
    def __init__(self):
        self._keyring: dict[str, dict] = {}

    def generate_encryption_keypair(self, name: str, level: int = 768) -> dict:
        kem = KyberKEM(level)
        pub, priv = kem.generate_keypair()
        entry = {
            "name": name,
            "type": "kem",
            "algorithm": f"Kyber-{level}",
            "public_key": pub.hex(),
            "secret_key": priv.hex(),
            "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }
        self._keyring[name] = entry
        return entry

    def generate_signing_keypair(self, name: str, algorithm: str = "dilithium", level: int = 3) -> dict:
        if algorithm == "dilithium":
            signer = DilithiumSigner(level)
        elif algorithm == "falcon":
            signer = FalconSigner(level)
        else:
            raise ValueError(f"Unknown signing algorithm: {algorithm}")

        pub, priv = signer.generate_keypair()
        entry = {
            "name": name,
            "type": "signature",
            "algorithm": f"{algorithm.capitalize()}-{level}",
            "public_key": pub.hex(),
            "secret_key": priv.hex(),
            "created_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        }
        self._keyring[name] = entry
        return entry

    def get_key(self, name: str) -> Optional[dict]:
        return self._keyring.get(name)

    def list_keys(self) -> list[dict]:
        return [v for v in self._keyring.values()]

    def rotate_key(self, name: str, algorithm: Optional[str] = None, level: Optional[int] = None) -> Optional[dict]:
        existing = self._keyring.get(name)
        if not existing:
            logger.warning("Key '%s' not found for rotation", name)
            return None

        alg = algorithm or ("dilithium" if existing["type"] == "signature" else "kyber")
        lvl = level or (int(existing["algorithm"].split("-")[-1]) if "-" in existing["algorithm"] else 768)

        if existing["type"] == "kem":
            return self.generate_encryption_keypair(f"{name}_rotated", lvl)
        else:
            return self.generate_signing_keypair(f"{name}_rotated", alg, lvl)

    def export_public_key(self, name: str) -> Optional[str]:
        key = self._keyring.get(name)
        if not key:
            return None
        return key["public_key"]


pqc_key_manager = PQCKeyManager()
