"""External API key management endpoints.

Manages API keys for third-party data providers (Finnhub, Twelve Data, BLS, etc.).
Keys are encrypted at rest using the API key vault (AES-256-GCM via Fernet).
"""
import logging
import os
import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict
from app.config import settings
from app.middleware.auth import get_current_user
from app.services.data.vault import get_key, set_key, delete_key

logger = logging.getLogger(__name__)

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
API_KEYS_PATH = os.path.join(DATA_DIR, "external_api_keys.json")
VAULT_PATH = os.path.join(DATA_DIR, "key_vault.enc")

EXTERNAL_KEY_FIELDS = [
    "finnhub_api_key", "twelvedata_api_key", "bls_api_key",
    "etherscan_api_key", "eia_api_key", "imf_api_key",
]


def _load_keys() -> Dict[str, str]:
    """Load external API keys with decryption from vault."""
    keys: Dict[str, str] = {}
    
    # Try encrypted vault first
    try:
        if os.path.exists(VAULT_PATH):
            with open(VAULT_PATH) as f:
                vault_data = json.load(f)
            for field in EXTERNAL_KEY_FIELDS:
                if field in vault_data:
                    decrypted = decrypt_value(vault_data[field])
                    if decrypted:
                        keys[field] = decrypted
                        os.environ[field.upper()] = decrypted
                        if hasattr(settings, field):
                            setattr(settings, field, decrypted)
                        return keys
    except Exception:
        pass
    
    # Fallback: plain JSON + env vars
    for field in EXTERNAL_KEY_FIELDS:
        val = getattr(settings, field, None) or os.environ.get(field.upper(), "")
        keys[field] = val or ""
    try:
        if os.path.exists(API_KEYS_PATH):
            with open(API_KEYS_PATH) as f:
                file_keys = json.load(f)
                for k, v in file_keys.items():
                    if v:
                        keys[k] = v
    except Exception:
        pass
    return keys


def _save_keys(keys: Dict[str, str]) -> None:
    """Persist keys encrypted to vault, also update runtime."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Save encrypted
    vault_data = {}
    for k, v in keys.items():
        if v:
            vault_data[k] = encrypt_value(v)
    try:
        with open(VAULT_PATH, "w") as f:
            json.dump(vault_data, f)
        logger.info("Keys saved to encrypted vault (%d keys)", len(vault_data))
    except Exception as e:
        logger.error("Failed to save encrypted vault: %s", e)
    
    # Update runtime
    for k, v in keys.items():
        os.environ[k.upper()] = v
        if hasattr(settings, k):
            setattr(settings, k, v)


def _mask_key(key: str) -> str:
    if not key or len(key) <= 4:
        return key
    return key[:4] + "*" * (len(key) - 4)


class ExternalApiKeysUpdate(BaseModel):
    keys: Dict[str, str]


@router.get("/api-keys")
async def get_all_api_keys(user: dict = Depends(get_current_user)):
    """Return all supported API keys with masked values."""
    logger.debug("get_all_api_keys by %s", user.get("sub", "unknown"))
    keys = []
    for key_name, meta in SUPPORTED_KEYS.items():
        val = get_key(key_name)
        masked = _mask_key(val) if val else ""
        keys.append({
            "key": key_name,
            "label": meta["label"],
            "provider": meta["provider"],
            "configured": bool(val),
            "masked_value": masked,
        })
    return {"keys": keys}


@router.post("/api-keys")
async def save_api_keys(
    body: ExternalApiKeysUpdate,
    user: dict = Depends(get_current_user),
):
    """Save API keys to the encrypted vault."""
    logger.info("save_api_keys by %s keys=%s", user.get("sub", "unknown"), list(body.keys.keys()))
    saved = []
    for k, v in body.keys.items():
        if v:
            set_key(k, v)
            saved.append(k)
    return {"status": "saved", "keys": saved}


@router.delete("/api-keys/{key_name}")
async def remove_api_key(
    key_name: str,
    user: dict = Depends(get_current_user),
):
    """Delete an API key from the vault."""
    logger.info("remove_api_key by %s key=%s", user.get("sub", "unknown"), key_name)
    delete_key(key_name)
    return {"status": "deleted", "key": key_name}


@router.get("/api-keys/providers")
async def list_key_providers(user: dict = Depends(get_current_user)):
    """List all supported key providers with their doc URLs."""
    return {"providers": SUPPORTED_KEYS}
