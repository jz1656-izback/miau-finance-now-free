"""Encrypted API key vault — stores and manages third-party API keys."""
import json
import os
from typing import Optional
from cryptography.fernet import Fernet

VAULT_PATH = os.getenv("KEY_VAULT_PATH", "/app/data/key_vault.json")
_MASTER_KEY = os.getenv("KEY_VAULT_MASTER_KEY") or Fernet.generate_key().decode()


def _cipher() -> Fernet:
    return Fernet(_MASTER_KEY.encode() if isinstance(_MASTER_KEY, str) else _MASTER_KEY)


def _load() -> dict:
    if not os.path.exists(VAULT_PATH):
        return {}
    with open(VAULT_PATH) as f:
        return json.loads(_cipher().decrypt(f.read().encode()).decode())


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(VAULT_PATH) or ".", exist_ok=True)
    with open(VAULT_PATH, "w") as f:
        f.write(_cipher().encrypt(json.dumps(data).encode()).decode())


def get_key(provider: str) -> Optional[str]:
    vault = _load()
    return vault.get(provider)


def set_key(provider: str, key: str) -> None:
    vault = _load()
    vault[provider] = key
    _save(vault)


def delete_key(provider: str) -> None:
    vault = _load()
    vault.pop(provider, None)
    _save(vault)


def list_keys() -> list[dict]:
    vault = _load()
    return [{"provider": k, "configured": bool(v), "masked": v[:4] + "****" + v[-4:] if len(v) > 8 else "****"} for k, v in vault.items()]
