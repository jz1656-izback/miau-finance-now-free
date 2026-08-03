import ssl
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def verify_tls(hostname: str, port: int = 443, cert_path: Optional[str] = None) -> bool:
    try:
        context = ssl.create_default_context()
        if cert_path:
            context.load_verify_locations(cert_path)
        with ssl.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if not cert:
                    logger.warning(f"No certificate presented by {hostname}")
                    return False
                logger.info(f"TLS verified for {hostname}: issuer={cert.get('issuer', [])}")
                return True
    except ssl.SSLError as e:
        logger.error(f"TLS verification failed for {hostname}: {e}")
        return False
    except Exception as e:
        logger.error(f"Connection failed to {hostname}: {e}")
        return False


def verify_tls_endpoint(endpoint_url: str, cert_path: Optional[str] = None) -> bool:
    from urllib.parse import urlparse
    parsed = urlparse(endpoint_url)
    hostname = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if parsed.scheme == "http":
        logger.warning(f"Non-TLS connection to {endpoint_url}")
        return False
    return verify_tls(hostname, port, cert_path)


def encrypt_sensitive(data: str, key: bytes) -> bytes:
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.encrypt(data.encode())


def decrypt_sensitive(token: bytes, key: bytes) -> str:
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.decrypt(token).decode()
