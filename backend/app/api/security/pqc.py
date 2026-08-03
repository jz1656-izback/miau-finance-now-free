import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.middleware.crypto.kyber import KyberKEM, kyber_encrypt, kyber_decrypt
from app.middleware.crypto.dilithium import DilithiumSigner
from app.middleware.crypto.falcon import FalconSigner
from app.middleware.crypto.hybrid import hybrid_generate_keypair, hybrid_encapsulate, hybrid_decapsulate, hybrid_sign, hybrid_verify
from app.middleware.crypto.key_mgmt import pqc_key_manager
from app.middleware.auth.jwt_pqc import create_pqc_jwt, verify_pqc_jwt, PQC_JWT_ALGORITHMS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/security/pqc", tags=["Post-Quantum Security"])


class KeypairRequest(BaseModel):
    algorithm: str = "dilithium"
    level: int = 3
    name: str = "default"


class KeypairResponse(BaseModel):
    name: str
    algorithm: str
    public_key: str
    secret_key: str


class EncryptRequest(BaseModel):
    plaintext: str
    public_key_hex: str
    level: int = 768


class EncryptResponse(BaseModel):
    ciphertext: str


class DecryptRequest(BaseModel):
    ciphertext: str
    secret_key_hex: str
    level: int = 768


class DecryptResponse(BaseModel):
    plaintext: str


class SignRequest(BaseModel):
    message: str
    secret_key_hex: str
    algorithm: str = "dilithium"
    level: int = 3


class SignResponse(BaseModel):
    signature: str
    algorithm: str


class VerifyRequest(BaseModel):
    message: str
    signature: str
    public_key_hex: str
    algorithm: str = "dilithium"
    level: int = 3


class VerifyResponse(BaseModel):
    valid: bool


class JwtCreateRequest(BaseModel):
    payload: dict
    secret_key_hex: str
    algorithm: str = "ML-DSA-65"


class JwtVerifyRequest(BaseModel):
    token: str
    public_key_hex: str


class StatusResponse(BaseModel):
    algorithms: dict
    key_count: int
    liboqs_available: bool


@router.get("/status", response_model=StatusResponse)
async def pqc_status():
    from app.middleware.crypto.kyber import _oqs_available as kyber_avail

    return StatusResponse(
        algorithms=PQC_JWT_ALGORITHMS,
        key_count=len(pqc_key_manager.list_keys()),
        liboqs_available=kyber_avail,
    )


@router.post("/keypair", response_model=KeypairResponse)
async def generate_keypair(req: KeypairRequest):
    if req.algorithm == "dilithium":
        entry = pqc_key_manager.generate_signing_keypair(req.name, "dilithium", req.level)
    elif req.algorithm == "falcon":
        entry = pqc_key_manager.generate_signing_keypair(req.name, "falcon", req.level)
    elif req.algorithm == "kyber":
        entry = pqc_key_manager.generate_encryption_keypair(req.name, req.level)
    elif req.algorithm == "hybrid":
        keys = hybrid_generate_keypair()
        return KeypairResponse(name=req.name, algorithm="hybrid", public_key=keys["encryption"]["pqc_public"], secret_key=keys["encryption"]["pqc_secret"])
    else:
        raise HTTPException(400, f"Unknown algorithm: {req.algorithm}. Choose: dilithium, falcon, kyber, hybrid")

    return KeypairResponse(name=entry["name"], algorithm=entry["algorithm"], public_key=entry["public_key"], secret_key=entry["secret_key"])


@router.post("/encrypt", response_model=EncryptResponse)
async def pqc_encrypt(req: EncryptRequest):
    try:
        pub = bytes.fromhex(req.public_key_hex)
        ct = kyber_encrypt(req.plaintext.encode(), pub)
        return EncryptResponse(ciphertext=ct.hex())
    except Exception as e:
        raise HTTPException(400, f"Encryption failed: {e}")


@router.post("/decrypt", response_model=DecryptResponse)
async def pqc_decrypt(req: DecryptRequest):
    try:
        priv = bytes.fromhex(req.secret_key_hex)
        ct = bytes.fromhex(req.ciphertext)
        pt = kyber_decrypt(ct, priv)
        return DecryptResponse(plaintext=pt.decode())
    except Exception as e:
        raise HTTPException(400, f"Decryption failed: {e}")


@router.post("/sign", response_model=SignResponse)
async def pqc_sign(req: SignRequest):
    try:
        priv = bytes.fromhex(req.secret_key_hex)
        msg = req.message.encode()
        if req.algorithm == "dilithium":
            signer = DilithiumSigner(req.level)
            sig = signer.sign(msg, priv)
        elif req.algorithm == "falcon":
            signer = FalconSigner(req.level)
            sig = signer.sign(msg, priv)
        else:
            raise HTTPException(400, f"Unknown algorithm: {req.algorithm}")
        return SignResponse(signature=sig.hex(), algorithm=f"{req.algorithm}-{req.level}")
    except Exception as e:
        raise HTTPException(400, f"Signing failed: {e}")


@router.post("/verify", response_model=VerifyResponse)
async def pqc_verify(req: VerifyRequest):
    try:
        pub = bytes.fromhex(req.public_key_hex)
        sig = bytes.fromhex(req.signature)
        msg = req.message.encode()
        if req.algorithm == "dilithium":
            signer = DilithiumSigner(req.level)
            valid = signer.verify(msg, sig, pub)
        elif req.algorithm == "falcon":
            signer = FalconSigner(req.level)
            valid = signer.verify(msg, sig, pub)
        else:
            raise HTTPException(400, f"Unknown algorithm: {req.algorithm}")
        return VerifyResponse(valid=valid)
    except Exception as e:
        logger.warning("PQC verify failed: %s", e)
        return VerifyResponse(valid=False)


@router.post("/jwt/create")
async def pqc_jwt_create(req: JwtCreateRequest):
    try:
        token = create_pqc_jwt(req.payload, req.secret_key_hex, req.algorithm)
        return {"token": token, "algorithm": req.algorithm}
    except Exception as e:
        raise HTTPException(400, f"JWT creation failed: {e}")


@router.post("/jwt/verify")
async def pqc_jwt_verify(req: JwtVerifyRequest):
    payload = verify_pqc_jwt(req.token, req.public_key_hex)
    if payload is None:
        raise HTTPException(401, "Invalid or expired PQC JWT")
    return {"valid": True, "payload": payload}
