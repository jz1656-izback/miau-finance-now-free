import os
import json
import base64
import logging
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from app.config import settings

logger = logging.getLogger(__name__)

KEY_STORE_PATH = os.getenv("BROKER_KEY_STORE", "/tmp/broker_keys.enc")
_MASTER_KEY: Optional[bytes] = None


def _get_master_key() -> bytes:
    global _MASTER_KEY
    if _MASTER_KEY is not None:
        return _MASTER_KEY
    raw = os.getenv("BROKER_MASTER_KEY")
    if raw:
        try:
            padded = raw.strip()
            padding = 4 - len(padded) % 4
            if padding != 4:
                padded += "=" * padding
            _MASTER_KEY = base64.urlsafe_b64decode(padded)
            return _MASTER_KEY
        except Exception as e:
            logger.error("Invalid BROKER_MASTER_KEY format, falling back to derived key: %s", e)
    salt_raw = os.getenv("BROKER_KEY_SALT")
    if not salt_raw:
        salt_raw = base64.urlsafe_b64encode(os.urandom(16)).decode()
        if settings.environment == "production":
            logger.warning("BROKER_KEY_SALT not set in production — using random salt per process")
    salt = salt_raw.encode()
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
    password = os.getenv("BROKER_KEY_PASSWORD", "CHANGE_ME_IN_PRODUCTION").encode()
    _MASTER_KEY = base64.urlsafe_b64encode(kdf.derive(password))
    logger.warning("Using derived master key — set BROKER_MASTER_KEY env var in production")
    return _MASTER_KEY


class KeyChain:
    def __init__(self):
        self._fernet = Fernet(_get_master_key())
        self._store: dict[str, bytes] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(KEY_STORE_PATH):
            try:
                with open(KEY_STORE_PATH, "rb") as f:
                    encrypted = f.read()
                decrypted = self._fernet.decrypt(encrypted)
                self._store = json.loads(decrypted)
            except Exception as e:
                logger.error(f"Failed to load key store: {e}")
                self._store = {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(KEY_STORE_PATH), exist_ok=True)
        encrypted = self._fernet.encrypt(json.dumps(self._store).encode())
        with open(KEY_STORE_PATH, "wb") as f:
            f.write(encrypted)

    def set_key(self, broker: str, api_key: str, api_secret: str) -> None:
        self._store[f"{broker}_key"] = api_key.encode()
        self._store[f"{broker}_secret"] = api_secret.encode()
        self._save()
        logger.info(f"Stored API key for broker '{broker}'")

    def get_key(self, broker: str) -> Optional[dict]:
        key = self._store.get(f"{broker}_key")
        secret = self._store.get(f"{broker}_secret")
        if key and secret:
            return {"api_key": key.decode(), "api_secret": secret.decode()}
        logger.warning(f"No API key found for broker '{broker}'")
        return None

    def rotate_key(self, broker: str, new_api_key: str, new_api_secret: str) -> None:
        old = self.get_key(broker)
        self.set_key(broker, new_api_key, new_api_secret)
        if old:
            logger.info(f"Rotated API key for broker '{broker}' (previous key archived)")

    def delete_key(self, broker: str) -> None:
        self._store.pop(f"{broker}_key", None)
        self._store.pop(f"{broker}_secret", None)
        self._save()
        logger.info(f"Deleted API key for broker '{broker}'")

    def list_brokers(self) -> list[str]:
        brokers = set()
        for k in self._store:
            if k.endswith("_key"):
                brokers.add(k[:-4])
        return sorted(brokers)
