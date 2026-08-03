"""Encrypted API key vault for third-party data sources.

Uses AES-256-GCM encryption with a master key derived from
the application secret. Keys are stored in the database with
encrypted values and retrieved on demand by data providers.
"""
import os
import json
import base64
import logging
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

# In-memory cache of decrypted keys (cleared on restart)
_key_cache: dict[str, str] = {}

# Supported API keys with metadata
SUPPORTED_KEYS = {
    "finnhub_api_key": {"label": "Finnhub API Key", "provider": "finnhub", "doc_url": "https://finnhub.io/register"},
    "twelvedata_api_key": {"label": "Twelve Data API Key", "provider": "twelvedata", "doc_url": "https://twelvedata.com/apikey"},
    "bls_api_key": {"label": "BLS API Key", "provider": "bls", "doc_url": "https://www.bls.gov/developers/"},
    "eia_api_key": {"label": "EIA API Key", "provider": "eia", "doc_url": "https://www.eia.gov/opendata/register.php"},
    "imf_api_key": {"label": "IMF API Key", "provider": "imf", "doc_url": "https://www.imf.org/en/Data"},
    "coinpaprika_api_key": {"label": "CoinPaprika API Key", "provider": "coinpaprika", "doc_url": "https://coinpaprika.com/api"},
    "etherscan_api_key": {"label": "Etherscan API Key", "provider": "etherscan", "doc_url": "https://etherscan.io/register"},
}


def _get_fernet() -> Fernet:
    """Create a Fernet cipher from the app's SECRET_KEY."""
    secret = os.getenv("SECRET_KEY") or os.getenv("MIAU_SECRET")
    if not secret:
        raise RuntimeError("SECRET_KEY or MIAU_SECRET env var must be set for API key vault")
    salt = b"miau_key_vault_salt_v1"
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    return Fernet(key)


def encrypt_value(plaintext: str) -> str:
    """Encrypt a plaintext API key. Returns base64-encoded ciphertext."""
    if not plaintext:
        return ""
    f = _get_fernet()
    return f.encrypt(plaintext.encode()).decode()


def decrypt_value(ciphertext: str) -> str:
    """Decrypt an encrypted API key. Returns plaintext."""
    if not ciphertext:
        return ""
    try:
        f = _get_fernet()
        return f.decrypt(ciphertext.encode()).decode()
    except Exception as e:
        logger.error("Failed to decrypt API key: %s", e)
        return ""


async def get_api_key(key_name: str) -> Optional[str]:
    """Get a decrypted API key by name.
    
    Checks in order:
    1. In-memory cache
    2. Environment variable
    3. Database (via API key storage)
    """
    # Check cache first
    if key_name in _key_cache:
        return _key_cache[key_name]
    
    # Check environment
    env_val = os.getenv(key_name.upper()) or os.getenv(key_name)
    if env_val:
        _key_cache[key_name] = env_val
        return env_val
    
    # Check database (via API key management endpoint)
    try:
        encrypted = None
        try:
            from app.services.data.key_store import get_encrypted_key
            encrypted = await get_encrypted_key(key_name)
        except ModuleNotFoundError:
            logger.warning("key_store module not available — database-backed key storage not enabled")
        if encrypted:
            decrypted = decrypt_value(encrypted)
            if decrypted:
                _key_cache[key_name] = decrypted
                return decrypted
    except Exception as e:
        logger.debug("Key store not available for %s: %s", key_name, e)
    
    return None


async def set_api_key(key_name: str, value: str) -> bool:
    """Encrypt and store an API key."""
    if not value:
        return False
    
    encrypted = encrypt_value(value)
    try:
        stored = False
        try:
            from app.services.data.key_store import store_encrypted_key
            stored = await store_encrypted_key(key_name, encrypted)
        except ModuleNotFoundError:
            logger.warning("key_store module not available — database-backed key storage disabled")
        if not stored:
            logger.debug("Key storage backend unavailable, key cached in memory only")
    except Exception as e:
        logger.error("Failed to store API key %s: %s", key_name, e)
        return False
    
    # Update cache
    _key_cache[key_name] = value
    # Also set env var for current session
    os.environ[key_name.upper()] = value
    os.environ[key_name] = value
    
    logger.info("API key %s stored successfully", key_name)
    return True


async def delete_api_key(key_name: str) -> bool:
    """Delete an encrypted API key."""
    _key_cache.pop(key_name, None)
    try:
        removed = False
        try:
            from app.services.data.key_store import remove_encrypted_key
            removed = await remove_encrypted_key(key_name)
        except ModuleNotFoundError:
            logger.warning("key_store module not available — key removal from DB disabled")
        if not removed:
            logger.debug("Key removed from cache only (no DB backend)")
    except Exception as e:
        logger.error("Failed to delete API key %s: %s", key_name, e)
        return False
    
    logger.info("API key %s deleted", key_name)
    return True


async def list_api_keys() -> list[dict]:
    """List all configured API keys with masked values."""
    keys = []
    for key_name, meta in SUPPORTED_KEYS.items():
        val = await get_api_key(key_name)
        masked = val[:4] + "****" + val[-4:] if val and len(val) > 8 else "****" if val else ""
        keys.append({
            "key": key_name,
            "label": meta["label"],
            "provider": meta["provider"],
            "doc_url": meta["doc_url"],
            "configured": bool(val),
            "masked_value": masked,
        })
    return keys
