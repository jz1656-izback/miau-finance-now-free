import logging

logger = logging.getLogger(__name__)

try:
    import oqs
    try:
        _ = oqs.get_enabled_signature_mechanisms()
        _oqs_available = True
    except Exception:
        _oqs_available = False
except Exception:
    _oqs_available = False

FALCON_SECURITY_LEVELS = {
    512: "Falcon-512",   # NIST Level 1 — compact (≈ 1KB signatures)
    1024: "Falcon-1024",  # NIST Level 5 — compact but larger (≈ 2KB signatures)
}

DEFAULT_FALCON_LEVEL = 512


class FalconSigner:
    def __init__(self, security_level: int = DEFAULT_FALCON_LEVEL):
        self.security_level = security_level
        self._sig_name = FALCON_SECURITY_LEVELS.get(security_level)
        if not self._sig_name:
            raise ValueError(f"Invalid FALCON security level: {security_level}. Choose from: {list(FALCON_SECURITY_LEVELS.keys())}")

    def generate_keypair(self) -> tuple[bytes, bytes]:
        if _oqs_available:
            sig = oqs.Signature(self._sig_name)
            public_key = sig.generate_keypair()
            secret_key = sig.export_secret_key()
            sig.free()
            return public_key, secret_key
        else:
            logger.warning("liboqs not available — using classical fallback (Ed25519)")
            from cryptography.hazmat.primitives.asymmetric import ed25519
            from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
            private_key = ed25519.Ed25519PrivateKey.generate()
            pub_bytes = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            priv_bytes = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
            return pub_bytes, priv_bytes

    def sign(self, message: bytes, secret_key: bytes) -> bytes:
        if _oqs_available:
            sig = oqs.Signature(self._sig_name)
            sig.set_secret_key(secret_key)
            signature = sig.sign(message)
            sig.free()
            return signature
        else:
            logger.warning("liboqs not available — using classical fallback (Ed25519)")
            from cryptography.hazmat.primitives.asymmetric import ed25519
            private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key)
            return private_key.sign(message)

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        if _oqs_available:
            sig = oqs.Signature(self._sig_name)
            sig.set_public_key(public_key)
            try:
                result = sig.verify(message, signature)
                sig.free()
                return result
            except Exception:
                sig.free()
                return False
        else:
            logger.warning("liboqs not available — using classical fallback (Ed25519)")
            from cryptography.hazmat.primitives.asymmetric import ed25519
            from cryptography.exceptions import InvalidSignature
            try:
                public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
                public_key_obj.verify(signature, message)
                return True
            except InvalidSignature:
                return False
