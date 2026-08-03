import base64
import logging
import os

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

KYBER_SECURITY_LEVELS = {
    512: "kyber512",  # NIST Level 1 (AES-128 equivalent)
    768: "kyber768",  # NIST Level 3 (AES-192 equivalent)
    1024: "kyber1024",  # NIST Level 5 (AES-256 equivalent)
}

DEFAULT_KYBER_LEVEL = 768


class KyberKEM:
    def __init__(self, security_level: int = DEFAULT_KYBER_LEVEL):
        self.security_level = security_level
        self._kem_name = KYBER_SECURITY_LEVELS.get(security_level)
        if not self._kem_name:
            raise ValueError(f"Invalid Kyber security level: {security_level}. Choose from: {list(KYBER_SECURITY_LEVELS.keys())}")

    def generate_keypair(self) -> tuple[bytes, bytes]:
        if _oqs_available:
            kem = oqs.KeyEncapsulation(self._kem_name)
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()
            kem.free()
            return public_key, secret_key
        else:
            logger.warning("liboqs not available — using classical fallback (X25519)")
            from cryptography.hazmat.primitives.asymmetric import x25519
            from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

            private_key = x25519.X25519PrivateKey.generate()
            public_key = private_key.public_key()
            pub_bytes = public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
            priv_bytes = private_key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
            return pub_bytes, priv_bytes

    def encapsulate(self, public_key: bytes) -> tuple[bytes, bytes]:
        if _oqs_available:
            kem = oqs.KeyEncapsulation(self._kem_name)
            ciphertext, shared_secret = kem.encap_secret(public_key)
            kem.free()
            return ciphertext, shared_secret
        else:
            logger.warning("liboqs not available — using classical fallback (X25519)")
            from cryptography.hazmat.primitives.asymmetric import x25519
            from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

            private_key = x25519.X25519PrivateKey.generate()
            pub_obj = x25519.X25519PublicKey.from_public_bytes(public_key)
            shared = private_key.exchange(pub_obj)
            ct = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            return ct, shared

    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        if _oqs_available:
            kem = oqs.KeyEncapsulation(self._kem_name)
            kem.set_secret_key(secret_key)
            shared_secret = kem.decap_secret(ciphertext)
            kem.free()
            return shared_secret
        else:
            logger.warning("liboqs not available — using classical fallback (X25519)")
            from cryptography.hazmat.primitives.asymmetric import x25519
            from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

            private_key = x25519.X25519PrivateKey.from_private_bytes(secret_key)
            pub = x25519.X25519PublicKey.from_public_bytes(ciphertext)
            return private_key.exchange(pub)


def kyber_encrypt(plaintext: bytes, public_key: bytes) -> bytes:
    kem = KyberKEM()
    ciphertext, shared_secret = kem.encapsulate(public_key)
    from cryptography.fernet import Fernet
    import base64, hashlib
    key = base64.urlsafe_b64encode(hashlib.sha256(shared_secret).digest())
    f = Fernet(key)
    encrypted = f.encrypt(plaintext)
    return ciphertext + encrypted


def kyber_decrypt(ciphertext_payload: bytes, secret_key: bytes) -> bytes:
    kem = KyberKEM()
    ct_len = 32  # X25519 pub key length in fallback mode
    if _oqs_available:
        ct_len = 1080  # Kyber-768 ciphertext
    ciphertext = ciphertext_payload[:ct_len]
    encrypted_data = ciphertext_payload[ct_len:]
    shared_secret = kem.decapsulate(ciphertext, secret_key)
    from cryptography.fernet import Fernet
    import base64, hashlib
    key = base64.urlsafe_b64encode(hashlib.sha256(shared_secret).digest())
    f = Fernet(key)
    return f.decrypt(encrypted_data)
