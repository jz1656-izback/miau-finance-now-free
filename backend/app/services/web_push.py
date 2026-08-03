import json
import logging
import base64
import time
from typing import Optional

import httpx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from app.config import settings

logger = logging.getLogger(__name__)


def _urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _urlsafe_b64decode(data: str) -> bytes:
    padded = data + "=" * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(padded)


def generate_vapid_keys() -> tuple[str, str]:
    from cryptography.hazmat.primitives.serialization import PrivateFormat, NoEncryption
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    priv_numbers = private_key.private_numbers()
    priv_bytes = priv_numbers.private_value.to_bytes(32, 'big')
    return _urlsafe_b64encode(pub_bytes), _urlsafe_b64encode(priv_bytes)


def _create_vapid_jwt(endpoint: str, private_key_b64: str) -> tuple[str, str]:
    """Create VAPID JWT and public key for push authentication."""
    import jwt as pyjwt
    private_bytes = _urlsafe_b64decode(private_key_b64)
    private_key = ec.derive_private_key(
        int.from_bytes(private_bytes, 'big'),
        ec.SECP256R1(),
    )
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    pub_b64 = _urlsafe_b64encode(pub_bytes)

    now = int(time.time())
    vapid_claims = {
        "aud": f"{endpoint.split('/')[0]}//{endpoint.split('/')[2]}",
        "exp": now + 86400,
        "sub": settings.vapid_claim_email or "mailto:admin@miau.finance",
    }
    from cryptography.hazmat.primitives.serialization import PrivateFormat, NoEncryption
    pk_bytes = private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption())
    token = pyjwt.encode(vapid_claims, pk_bytes, algorithm="ES256")
    return token, pub_b64


async def send_web_push(
    subscription: dict,
    title: str,
    body: str,
    icon: str = "/favicon.ico",
    url: Optional[str] = None,
) -> bool:
    endpoint = subscription.get("endpoint")
    p256dh = subscription.get("p256dh_key") or subscription.get("keys", {}).get("p256dh", "")
    auth = subscription.get("auth_key") or subscription.get("keys", {}).get("auth", "")

    if not endpoint:
        logger.warning("No endpoint in push subscription")
        return False

    vapid_private = settings.vapid_private_key
    if not vapid_private:
        logger.warning("VAPID_PRIVATE_KEY not configured — push notification skipped")
        return False

    payload = json.dumps({"title": title, "body": body, "icon": icon, "url": url or ""})

    try:
        vapid_token, vapid_pub = _create_vapid_jwt(endpoint, vapid_private)
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                endpoint,
                content=payload,
                headers={
                    "Content-Type": "application/json",
                    "TTL": "86400",
                    "Authorization": f"vapid t={vapid_token}, k={vapid_pub}",
                },
            )
            if resp.status_code < 300 or resp.status_code == 410:
                return True
            logger.warning(f"Web push returned {resp.status_code}: {resp.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"Web push failed: {e}")
        return False


async def send_whatsapp(recipient: str, message: str) -> bool:
    api_key = settings.whatsapp_api_key
    phone_id = settings.whatsapp_phone_number_id
    if not api_key or not phone_id:
        logger.debug("WhatsApp not configured")
        return False

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"https://graph.facebook.com/v18.0/{phone_id}/messages",
                json={
                    "messaging_product": "whatsapp",
                    "to": recipient,
                    "type": "text",
                    "text": {"body": message},
                },
                headers={"Authorization": f"Bearer {api_key}"},
            )
            return resp.status_code < 300
    except Exception as e:
        logger.error(f"WhatsApp send failed: {e}")
        return False


async def send_telegram(chat_id: str, message: str) -> bool:
    token = settings.telegram_bot_token
    if not token:
        logger.debug("Telegram bot not configured")
        return False

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
            )
            return resp.status_code < 300
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")
        return False
