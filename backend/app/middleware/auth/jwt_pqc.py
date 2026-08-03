import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.middleware.crypto.dilithium import DilithiumSigner, dilithium_sign_jwt, dilithium_verify_jwt
from app.middleware.crypto.falcon import FalconSigner
from app.middleware.crypto.hybrid import hybrid_sign, hybrid_verify

logger = logging.getLogger(__name__)

PQC_JWT_ALGORITHMS = {
    "ML-DSA-65": {"signer": "dilithium", "level": 3, "description": "CRYSTALS-Dilithium (NIST Level 3)"},
    "Falcon-512": {"signer": "falcon", "level": 512, "description": "FALCON (NIST Level 1, compact)"},
    "Hybrid-Dilithium-Ed25519": {"signer": "hybrid", "level": 3, "description": "Hybrid Dilithium3 + Ed25519"},
}

DEFAULT_PQC_JWT_ALG = "ML-DSA-65"
PQC_JWT_EXPIRY_MINUTES = 60


def create_pqc_jwt(payload: dict, secret_key_hex: str, algorithm: str = DEFAULT_PQC_JWT_ALG) -> str:
    alg_info = PQC_JWT_ALGORITHMS.get(algorithm)
    if not alg_info:
        raise ValueError(f"Unknown PQC JWT algorithm: {algorithm}. Choose from: {list(PQC_JWT_ALGORITHMS.keys())}")

    now = datetime.now(timezone.utc)
    token_payload = {
        **payload,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=PQC_JWT_EXPIRY_MINUTES)).timestamp()),
        "alg": algorithm,
    }

    message = json.dumps(token_payload, sort_keys=True).encode()

    signer_type = alg_info["signer"]
    if signer_type == "dilithium":
        signer = DilithiumSigner(alg_info["level"])
        priv = bytes.fromhex(secret_key_hex)
        signature = signer.sign(message, priv)
    elif signer_type == "falcon":
        signer = FalconSigner(alg_info["level"])
        priv = bytes.fromhex(secret_key_hex)
        signature = signer.sign(message, priv)
    elif signer_type == "hybrid":
        import binascii
        signature = bytes.fromhex(hybrid_sign(message, secret_key_hex))
    else:
        raise ValueError(f"Unsupported signer type: {signer_type}")

    import base64
    return base64.urlsafe_b64encode(json.dumps({
        "payload": token_payload,
        "signature": base64.urlsafe_b64encode(signature).decode(),
        "algorithm": algorithm,
    }).encode()).decode()


def verify_pqc_jwt(token: str, public_key_hex: str) -> Optional[dict]:
    import base64
    try:
        decoded = json.loads(base64.urlsafe_b64decode(token))
    except Exception as e:
        logger.warning("PQC JWT decode failed: %s", e)
        return None

    payload = decoded.get("payload", {})
    signature_b64 = decoded.get("signature", "")
    algorithm = decoded.get("algorithm", DEFAULT_PQC_JWT_ALG)

    alg_info = PQC_JWT_ALGORITHMS.get(algorithm)
    if not alg_info:
        logger.warning("Unknown PQC JWT algorithm: %s", algorithm)
        return None

    exp = payload.get("exp", 0)
    if datetime.now(timezone.utc).timestamp() > exp:
        logger.warning("PQC JWT expired")
        return None

    message = json.dumps(payload, sort_keys=True).encode()
    signature = base64.urlsafe_b64decode(signature_b64)
    pub = bytes.fromhex(public_key_hex)

    signer_type = alg_info["signer"]
    if signer_type == "dilithium":
        signer = DilithiumSigner(alg_info["level"])
        valid = signer.verify(message, signature, pub)
    elif signer_type == "falcon":
        signer = FalconSigner(alg_info["level"])
        valid = signer.verify(message, signature, pub)
    elif signer_type == "hybrid":
        valid = hybrid_verify(message, signature.hex(), public_key_hex)
    else:
        return None

    if not valid:
        logger.warning("PQC JWT signature verification failed")
        return None

    return payload
