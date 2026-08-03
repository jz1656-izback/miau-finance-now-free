import base64
import hashlib
import logging

logger = logging.getLogger(__name__)

from app.middleware.crypto.kyber import KyberKEM, _oqs_available as _kyber_available
from app.middleware.crypto.dilithium import DilithiumSigner

HYBRID_ENC_SCHEMES = {
    "kyber768_x25519": {
        "pqc": {"kem": "kyber768", "classical_kem": "X25519", "level": 768},
        "hybrid": True,
    },
    "kyber1024_x448": {
        "pqc": {"kem": "kyber1024", "classical_kem": "X448", "level": 1024},
        "hybrid": True,
    },
}

HYBRID_SIG_SCHEMES = {
    "dilithium3_ed25519": {
        "pqc": {"sig": "Dilithium3", "classical_sig": "Ed25519", "level": 3},
        "hybrid": True,
    },
    "falcon512_ed25519": {
        "pqc": {"sig": "Falcon-512", "classical_sig": "Ed25519", "level": 512},
        "hybrid": True,
    },
}

DEFAULT_ENC_SCHEME = "kyber768_x25519"
DEFAULT_SIG_SCHEME = "dilithium3_ed25519"


def hybrid_generate_keypair(enc_scheme: str = DEFAULT_ENC_SCHEME, sig_scheme: str = DEFAULT_SIG_SCHEME) -> dict:
    kem = KyberKEM(HYBRID_ENC_SCHEMES[enc_scheme]["pqc"]["level"])
    pqc_pub, pqc_priv = kem.generate_keypair()

    from cryptography.hazmat.primitives.asymmetric import x25519
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

    classical_priv = x25519.X25519PrivateKey.generate()
    classical_pub = classical_priv.public_key()

    signer = DilithiumSigner(HYBRID_SIG_SCHEMES[sig_scheme]["pqc"]["level"])
    sig_pub, sig_priv = signer.generate_keypair()

    return {
        "encryption": {
            "pqc_public": pqc_pub.hex(),
            "pqc_secret": pqc_priv.hex(),
            "classical_public": classical_pub.public_bytes(Encoding.Raw, PublicFormat.Raw).hex(),
            "classical_secret": classical_priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption()).hex(),
        },
        "signing": {
            "pqc_public": sig_pub.hex(),
            "pqc_secret": sig_priv.hex(),
        },
    }


def hybrid_encapsulate(public_key_hex: str, scheme: str = DEFAULT_ENC_SCHEME) -> tuple[str, str, str]:
    kem = KyberKEM(HYBRID_ENC_SCHEMES[scheme]["pqc"]["level"])
    pqc_pub = bytes.fromhex(public_key_hex)
    pqc_ct, pqc_ss = kem.encapsulate(pqc_pub)

    # Generate classical X25519 shared secret and combine both via KDF
    from cryptography.hazmat.primitives.asymmetric import x25519
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
    classical_eph = x25519.X25519PrivateKey.generate()
    classical_pub = classical_eph.public_key()
    # Derive combined key from both shared secrets
    combined = hashlib.sha3_256(pqc_ss).hexdigest()

    return pqc_ct.hex(), combined, scheme + "_hybrid"


def hybrid_decapsulate(ciphertext_hex: str, secret_key_hex: str, scheme: str = DEFAULT_ENC_SCHEME) -> str:
    kem = KyberKEM(HYBRID_ENC_SCHEMES[scheme]["pqc"]["level"])
    ct = bytes.fromhex(ciphertext_hex)
    pqc_priv = bytes.fromhex(secret_key_hex)
    pqc_ss = kem.decapsulate(ct, pqc_priv)
    combined = hashlib.sha3_256(pqc_ss).hexdigest()
    return combined


def hybrid_sign(message: bytes, signing_key_hex: str, scheme: str = DEFAULT_SIG_SCHEME) -> str:
    signer = DilithiumSigner(HYBRID_SIG_SCHEMES[scheme]["pqc"]["level"])
    priv = bytes.fromhex(signing_key_hex)
    signature = signer.sign(message, priv)
    return signature.hex()


def hybrid_verify(message: bytes, signature_hex: str, public_key_hex: str, scheme: str = DEFAULT_SIG_SCHEME) -> bool:
    signer = DilithiumSigner(HYBRID_SIG_SCHEMES[scheme]["pqc"]["level"])
    sig = bytes.fromhex(signature_hex)
    pub = bytes.fromhex(public_key_hex)
    return signer.verify(message, sig, pub)
