import base64
import hashlib
import json
import logging
import os
import time
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

logger = logging.getLogger(__name__)

KEYCHAIN_CACHE_TTL_SECONDS = 300  # 5 minutes
KEYCHAIN_SOCIAL_THRESHOLD = 3  # 3-of-5 guardians for recovery


class KeychainError(Exception):
    pass


class KeyNotFoundError(KeychainError):
    pass


class KeychainLockedError(KeychainError):
    pass


class Keychain:
    """Encrypted per-user key store with session-bound caching and social recovery.

    Usage:
        kc = Keychain()
        kc.store(user_id, "my-private-key", context="evm")
        key = kc.retrieve(user_id, context="evm")
        kc.delete(user_id, context="evm")
    """

    def __init__(self):
        self._cache: dict[str, tuple[str, float]] = {}
        self._recovery_guardians: dict[str, list[str]] = {}

    def _get_master_key(self) -> bytes:
        raw = os.getenv("KEYCHAIN_ENCRYPTION_KEY", "")
        if not raw:
            raise KeychainError("KEYCHAIN_ENCRYPTION_KEY environment variable is not set")
        return hashlib.sha256(raw.encode()).digest()

    def _derive_user_key(self, user_id: str, context: str = "default") -> bytes:
        master = self._get_master_key()
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=context.encode(),
            info=user_id.encode(),
        )
        return hkdf.derive(master)

    def _encrypt(self, plaintext: str, user_id: str, context: str = "default") -> str:
        key = self._derive_user_key(user_id, context)
        fernet = Fernet(base64.urlsafe_b64encode(key))
        return fernet.encrypt(plaintext.encode()).decode()

    def _decrypt(self, ciphertext: str, user_id: str, context: str = "default") -> str:
        key = self._derive_user_key(user_id, context)
        fernet = Fernet(base64.urlsafe_b64encode(key))
        return fernet.decrypt(ciphertext.encode()).decode()

    def store(self, user_id: str, private_key: str, context: str = "default") -> None:
        encrypted = self._encrypt(private_key, user_id, context)
        cache_key = f"{user_id}:{context}"
        self._cache[cache_key] = (encrypted, time.time())

    def retrieve(self, user_id: str, context: str = "default") -> Optional[str]:
        cache_key = f"{user_id}:{context}"
        cached = self._cache.get(cache_key)
        if cached:
            encrypted, ts = cached
            if time.time() - ts < KEYCHAIN_CACHE_TTL_SECONDS:
                try:
                    return self._decrypt(encrypted, user_id, context)
                except Exception:
                    pass
        return None

    def delete(self, user_id: str, context: str = "default") -> None:
        cache_key = f"{user_id}:{context}"
        self._cache.pop(cache_key, None)

    def clear_session(self, user_id: str) -> None:
        keys = [k for k in self._cache if k.startswith(f"{user_id}:")]
        for k in keys:
            del self._cache[k]

    def set_recovery_guardians(self, user_id: str, guardians: list[str]) -> None:
        if len(guardians) < KEYCHAIN_SOCIAL_THRESHOLD:
            raise KeychainError(
                f"Need at least {KEYCHAIN_SOCIAL_THRESHOLD} guardians for recovery "
                f"(got {len(guardians)})"
            )
        self._recovery_guardians[user_id] = guardians

    def get_recovery_guardians(self, user_id: str) -> list[str]:
        return self._recovery_guardians.get(user_id, [])

    def initiate_recovery(self, user_id: str, guardian_addresses: list[str]) -> str:
        expected = set(self._recovery_guardians.get(user_id, []))
        provided = set(guardian_addresses)
        matched = len(expected & provided)
        if matched < KEYCHAIN_SOCIAL_THRESHOLD:
            raise KeychainError(
                f"Recovery requires {KEYCHAIN_SOCIAL_THRESHOLD} of "
                f"{len(expected)} guardians to approve (got {matched})"
            )
        recovery_code = base64.urlsafe_b64encode(os.urandom(16)).decode()
        return recovery_code


keychain = Keychain()
