import logging
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

try:
    from eth_account.messages import encode_defunct
    from eth_account import Account as EthAccount

    _eth_available = True
except ImportError:
    _eth_available = False
    logger.warning("eth-account not installed — SIWE auth unavailable. Install with: pip install eth-account")

SIWE_NONCE_BYTES = 16
SIWE_NONCE_EXPIRY_MINUTES = 10
SIWE_SESSION_EXPIRE_MINUTES = 60
SIWE_VERSION = "1"
SIWE_CHAIN_ID = 1
SIWE_DOMAIN = "miau.finance"
SIWE_URI = "https://miau.finance"

router = APIRouter(prefix="/auth/web3", tags=["Web3 Auth"])

_nonce_store: dict[str, datetime] = {}


def _prune_expired_nonces():
    now = datetime.now(timezone.utc)
    expired = [k for k, v in _nonce_store.items() if v < now]
    for k in expired:
        del _nonce_store[k]


def generate_nonce() -> str:
    _prune_expired_nonces()
    nonce = secrets.token_urlsafe(SIWE_NONCE_BYTES)
    _nonce_store[nonce] = datetime.now(timezone.utc) + timedelta(minutes=SIWE_NONCE_EXPIRY_MINUTES)
    return nonce


def verify_nonce(nonce: str) -> bool:
    _prune_expired_nonces()
    if nonce not in _nonce_store:
        return False
    del _nonce_store[nonce]
    return True


def create_siwe_message(
    address: str,
    nonce: str,
    domain: str = SIWE_DOMAIN,
    uri: str = SIWE_URI,
    chain_id: int = SIWE_CHAIN_ID,
    issued_at: Optional[str] = None,
    statement: Optional[str] = None,
) -> str:
    now = issued_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    lines = [
        f"{domain} wants you to sign in with your Ethereum account:",
        address,
        "",
    ]
    if statement:
        lines.append(statement)
        lines.append("")
    lines.extend([
        f"URI: {uri}",
        "Version: 1",
        f"Chain ID: {chain_id}",
        f"Nonce: {nonce}",
        f"Issued At: {now}",
    ])
    return "\n".join(lines)


def verify_siwe_signature(message: str, signature: str) -> Optional[str]:
    if not _eth_available:
        logger.error("eth-account not installed — cannot verify SIWE signature")
        return None
    try:
        message_object = encode_defunct(text=message)
        recovered = EthAccount.recover_message(message_object, signature=signature)
        return recovered
    except Exception as e:
        logger.warning("SIWE signature verification failed: %s", e)
        return None


def format_eth_address(address: str) -> str:
    if not _eth_available:
        return address
    try:
        return EthAccount.to_checksum_address(address)
    except Exception:
        return address


class NonceResponse(BaseModel):
    nonce: str


class SiweRequest(BaseModel):
    message: str
    signature: str
    address: str


class SiweResponse(BaseModel):
    access_token: str
    address: str
    token_type: str = "bearer"


@router.get("/nonce", response_model=NonceResponse)
async def get_nonce():
    nonce = generate_nonce()
    return NonceResponse(nonce=nonce)


def create_siwe_jwt(address: str) -> str:
    from app.middleware.auth import create_access_token
    from datetime import timedelta

    return create_access_token(
        data={
            "sub": address,
            "role": "user",
            "auth_type": "web3",
            "address": address,
        },
        expires_delta=timedelta(minutes=SIWE_SESSION_EXPIRE_MINUTES),
    )


@router.post("/login", response_model=SiweResponse)
async def siwe_login(body: SiweRequest):
    if not _eth_available:
        raise HTTPException(503, "Web3 authentication is not available — eth-account library required")

    message = body.message
    signature = body.signature
    provided_address = body.address

    recovered = verify_siwe_signature(message, signature)
    if not recovered:
        raise HTTPException(401, "Signature verification failed")

    checksummed = format_eth_address(provided_address)
    recovered_checksummed = format_eth_address(recovered)
    if checksummed.lower() != recovered_checksummed.lower():
        raise HTTPException(401, "Address mismatch: recovered address does not match provided address")

    nonce = None
    for line in message.split("\n"):
        if line.startswith("Nonce: "):
            nonce = line[7:]
            break

    if nonce and not verify_nonce(nonce):
        raise HTTPException(401, "Nonce expired or invalid — please request a new nonce")

    token = create_siwe_jwt(checksummed)
    return SiweResponse(access_token=token, address=checksummed)
