# Miau Finance — PQC Migration Guide

**Phase:** 26 (v1.9.0)  
**Last Updated:** May 2026

---

## Overview

This guide explains how to migrate Miau Finance deployments from traditional cryptography to post-quantum cryptography (PQC). Migration is optional until quantum computers threaten current crypto, but early adoption is recommended for long-lived systems.

---

## Migration Steps

### Step 1: Audit Current Crypto Usage

```bash
# Run the PQC audit script
python scripts/audit_pqc.py
```

This identifies all cryptographic operations and flags which need PQC upgrades.

### Step 2: Generate PQC Keys

```bash
# Generate Kyber KEM keys
python -m app.middleware.crypto.key_mgmt --generate kyber

# Generate Dilithium signing keys
python -m app.middleware.crypto.key_mgmt --generate dilithium

# Generate FALCON signing keys
python -m app.middleware.crypto.key_mgmt --generate falcon
```

Keys are stored in the existing encrypted keychain (`backend/app/services/defi/keychain.py`).

### Step 3: Enable Hybrid Mode

Set the PQC mode in `.env`:

```bash
# Start with hybrid mode (traditional + PQC)
PQC_MODE=hybrid
```

Hybrid mode uses both traditional (X25519/ECDSA) and PQC (Kyber/Dilithium) simultaneously. This ensures backward compatibility while phasing in PQC.

### Step 4: Migrate JWT Signing

```bash
# Generate a PQC JWT signing key
python -m app.middleware.crypto.key_mgmt --generate dilithium --purpose jwt

# Update JWT configuration
JWT_PQC_ENABLED=true
JWT_SIGNING_ALGORITHM=ML-DSA-65
```

The middleware at `backend/app/middleware/auth/jwt_pqc.py` handles transparent verification of both traditional and PQC-signed tokens during migration.

### Step 5: Enable TLS 1.3 PQC

```bash
# In docker-compose.override.yml
services:
  backend:
    environment:
      - TLS_PQC_ENABLED=true
      - TLS_PQC_MODE=hybrid
```

The hybrid TLS mode negotiates X25519+Kyber as the key exchange when the client supports it.

### Step 6: Full PQC Mode

After all clients and services have been upgraded:

```bash
# Switch to full PQC mode
PQC_MODE=full
JWT_PQC_ENABLED=true
TLS_PQC_ENABLED=true
```

---

## Verification

```bash
# Check PQC status
python -m app.middleware.crypto.status

# Run PQC test suite
pytest tests/test_api/test_pqc.py -v

# Verify JWT with PQC
python -c "
from app.middleware.auth.jwt_pqc import sign_pqc, verify_pqc
token = sign_pqc({'sub': 'admin'})
assert verify_pqc(token)
print('PQC JWT OK')
"
```

---

## Rollback

```bash
# Revert to traditional crypto
PQC_MODE=disabled
docker compose up -d backend
```

Keys generated during PQC mode remain in the keychain and can be re-enabled later.

---

## Key Sizes Comparison

| Algorithm | Public Key | Private Key | Signature/Ciphertext |
|-----------|-----------|-------------|---------------------|
| RSA-3072 | 544 B | 1.2 KB | 384 B |
| ECDSA P-256 | 64 B | 32 B | 64-72 B |
| Kyber-768 | 1,184 B | 2,400 B | 1,088 B (ciphertext) |
| Dilithium-65 | 1,312 B | 2,520 B | 2,420 B |
| FALCON-512 | 897 B | 1,281 B | 666 B |

---

## Reference

- [NIST PQC Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [CRYSTALS-Kyber Specification](https://pq-crystals.org/kyber/)
- [CRYSTALS-Dilithium Specification](https://pq-crystals.org/dilithium/)
- [FALCON Specification](https://falcon-sign.info/)
