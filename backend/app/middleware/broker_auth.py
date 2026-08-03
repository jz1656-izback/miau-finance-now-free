import base64
import hashlib
import hmac
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlencode

import httpx
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

logger = logging.getLogger(__name__)

SUPPORTED_REGIONS = {"us", "eu", "asia", "latam", "mea"}
BROKER_OAUTH_ENDPOINTS: dict[str, dict[str, str]] = {
    "ibkr": {
        "authorize": "https://apps.ibkr.com/oauth/authorize",
        "token": "https://api.ibkr.com/v1/api/oauth/access_token",
    },
    "saxo": {
        "authorize": "https://www.saxotrader.com/oauth2/authorize",
        "token": "https://www.saxotrader.com/oauth2/token",
    },
    "degiro": {
        "authorize": "https://trader.degiro.com/oauth2/authorize",
        "token": "https://trader.degiro.com/oauth2/token",
    },
    "rakuten": {
        "authorize": "https://api.rakuten-sec.co.jp/oauth/authorize",
        "token": "https://api.rakuten-sec.co.jp/oauth/token",
    },
    "zerodha": {
        "authorize": "https://api.kite.trade/connect/login",
        "token": "https://api.kite.trade/session/token",
    },
}


@dataclass
class BrokerOAuthConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: list[str] = field(default_factory=list)
    authorize_url: str = ""
    token_url: str = ""
    region: str = "us"


@dataclass
class BrokerTokenResponse:
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    refresh_token: Optional[str] = None
    raw: dict = field(default_factory=dict)


def _env_key(broker: str, key: str) -> str:
    return f"BROKER_{broker.upper()}_{key}"


def load_broker_oauth_config(broker: str, region: str = "us") -> Optional[BrokerOAuthConfig]:
    client_id = os.getenv(_env_key(broker, "CLIENT_ID"), "")
    client_secret = os.getenv(_env_key(broker, "CLIENT_SECRET"), "")
    if not client_id or not client_secret:
        logger.debug("Broker OAuth not configured for %s (missing CLIENT_ID/CLIENT_SECRET)", broker)
        return None

    endpoints = BROKER_OAUTH_ENDPOINTS.get(broker, {})
    return BrokerOAuthConfig(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=os.getenv(_env_key(broker, "REDIRECT_URI"), ""),
        scopes=os.getenv(_env_key(broker, "SCOPES"), "trading,account").split(","),
        authorize_url=endpoints.get("authorize", ""),
        token_url=endpoints.get("token", ""),
        region=region,
    )


def get_broker_authorization_url(config: BrokerOAuthConfig, state: str) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": " ".join(config.scopes),
        "state": state,
    }
    return f"{config.authorize_url}?{urlencode(params)}"


async def exchange_broker_code(config: BrokerOAuthConfig, code: str) -> Optional[BrokerTokenResponse]:
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
        "grant_type": "authorization_code",
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(config.token_url, data=data, headers=headers, timeout=30)
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            logger.warning("Broker OAuth token exchange failed for %s: %s", config.client_id[:8], e)
            return None

    return BrokerTokenResponse(
        access_token=body.get("access_token", ""),
        token_type=body.get("token_type", "bearer"),
        expires_in=body.get("expires_in", 86400),
        refresh_token=body.get("refresh_token"),
        raw=body,
    )


async def refresh_broker_token(config: BrokerOAuthConfig, refresh_token: str) -> Optional[BrokerTokenResponse]:
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(config.token_url, data=data, headers=headers, timeout=30)
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            logger.warning("Broker token refresh failed for %s: %s", config.client_id[:8], e)
            return None

    return BrokerTokenResponse(
        access_token=body.get("access_token", ""),
        token_type=body.get("token_type", "bearer"),
        expires_in=body.get("expires_in", 86400),
        refresh_token=body.get("refresh_token", refresh_token),
        raw=body,
    )


def _get_master_key() -> bytes:
    raw = os.getenv("BROKER_ENCRYPTION_KEY", "")
    if not raw:
        raise RuntimeError("BROKER_ENCRYPTION_KEY environment variable is not set")
    if len(raw) < 32:
        raise RuntimeError("BROKER_ENCRYPTION_KEY must be at least 32 characters")
    return hashlib.sha256(raw.encode()).digest()


def derive_region_key(region: str) -> bytes:
    master = _get_master_key()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=region.encode(),
        info=b"broker-credential-encryption",
    )
    return hkdf.derive(master)


def encrypt_broker_credentials(credentials: dict, region: str = "us") -> str:
    key = derive_region_key(region)
    fernet = Fernet(base64.urlsafe_b64encode(key))
    payload = json.dumps(credentials, sort_keys=True).encode()
    return fernet.encrypt(payload).decode()


def decrypt_broker_credentials(encrypted: str, region: str = "us") -> Optional[dict]:
    try:
        key = derive_region_key(region)
        fernet = Fernet(base64.urlsafe_b64encode(key))
        decrypted = fernet.decrypt(encrypted.encode())
        return json.loads(decrypted)
    except Exception as e:
        logger.warning("Failed to decrypt broker credentials for region %s: %s", region, e)
        return None
