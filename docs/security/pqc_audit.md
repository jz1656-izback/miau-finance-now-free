# Post-Quantum Cryptography (PQC) Audit — Miau Finance

**Date:** 2026-05-19
**Auditor:** security-dev
**Scope:** All cryptographic subsystems — identify Shor-vulnerable algorithms, plan NIST PQC migration

---

## 1. Executive Summary

Quantum computers capable of breaking RSA-2048 and ECDSA-256 are projected within 5-10 years (Mosca's Inequality). Miau Finance must migrate to NIST-standardized PQC algorithms before quantum threat becomes operational.

**Current status:** All classical (vulnerable). **Target:** Hybrid classical + PQC by end of Phase 26.

---

## 2. Algorithm Inventory

| # | Component | Algorithm | Key Size | NIST Category | Quantum Risk | Migration Target |
|---|-----------|-----------|----------|---------------|--------------|------------------|
| 1 | JWT signing | HS256 (HMAC-SHA256) | 256b | Symmetric | Low (Grover only) | HS256 → HS512 |
| 2 | JWT signing | RS256 (RSA-2048) | 2048b | Asymmetric | **CRITICAL** | → CRYSTALS-Dilithium |
| 3 | JWT signing | ES256 (ECDSA P-256) | 256b | Asymmetric | **CRITICAL** | → CRYSTALS-Dilithium |
| 4 | TLS 1.3 | X25519 key exchange | 256b | Asymmetric | **HIGH** | → CRYSTALS-Kyber + X25519 hybrid |
| 5 | TLS 1.3 | P-256/P-384 ECDHE | 256-384b | Asymmetric | **HIGH** | → CRYSTALS-Kyber |
| 6 | Fernet encryption | AES-256-GCM | 256b | Symmetric | Low (double key) | → AES-256 (sufficient) |
| 7 | API key hashing | SHA-256 | 256b | Symmetric | Low | → SHA-256 (sufficient) |
| 8 | Password hashing | bcrypt | 184b | Symmetric | Low | → bcrypt (sufficient) |
| 9 | Broker auth | RSA-OAEP (TLS) | 2048b | Asymmetric | **CRITICAL** | → CRYSTALS-Kyber |
| 10 | SIWE auth | ECDSA (secp256k1) | 256b | Asymmetric | **CRITICAL** | → CRYSTALS-Dilithium |

---

## 3. Risk Assessment

| Risk Level | Count | Components | Timeline |
|------------|-------|-----------|----------|
| **CRITICAL** | 4 | JWT (RS256/ES256), Broker auth TLS, SIWE ECDSA | Migrate within 12 months |
| **HIGH** | 2 | TLS key exchange (X25519, ECDHE) | Migrate within 18 months |
| **LOW** | 4 | HS256, AES-256, SHA-256, bcrypt | Monitor (symmetric less affected) |

---

## 4. NIST PQC Standard Selection

| NIST Standard | Type | Function | Miau Finance Use |
|--------------|------|----------|-----------------|
| **CRYSTALS-Kyber** | KEM (Key Encapsulation) | Secure key exchange | TLS 1.3 hybrid, broker auth encryption |
| **CRYSTALS-Dilithium** | Digital Signature | Message signing | JWT signing, SIWE auth, code signing |
| **FALCON** | Digital Signature | Compact signing | Resource-constrained environments, Rust engine |
| **SPHINCS+** | Digital Signature | Stateless hash-based | Long-term archival, code signing backup |

---

## 5. Migration Plan

### Phase 1 (Immediate — This sprint)
| Task | File | Owner |
|------|------|-------|
| CRYSTALS-Kyber KEM middleware | `backend/app/middleware/crypto/kyber.py` | security-dev |
| CRYSTALS-Dilithium signatures | `backend/app/middleware/crypto/dilithium.py` | security-dev |
| FALCON signature scheme | `backend/app/middleware/crypto/falcon.py` | security-dev |

### Phase 2 (Next sprint)
| Task | File | Owner |
|------|------|-------|
| Hybrid crypto (classical + PQC) | `backend/app/middleware/crypto/hybrid.py` | security-dev |
| PQC JWT signing adapter | `backend/app/middleware/auth/jwt_pqc.py` | security-dev |
| PQC TLS 1.3 integration | `backend/app/middleware/crypto/tls_pqc.py` | security-dev |

### Phase 3 (Follow-up)
| Task | File | Owner |
|------|------|-------|
| PQC key management | `backend/app/middleware/crypto/key_mgmt.py` | security-dev |
| Rust PQC implementation | `backend/rust_analytics/src/pqc.rs` | rust-dev |
| PQC API endpoints | `backend/app/api/security/pqc.py` | security-dev |

---

## 6. Dependencies

Install liboqs for production PQC:
```bash
pip install liboqs-python  # CRYSTALS-Kyber, CRYSTALS-Dilithium, FALCON, SPHINCS+
```

For development without liboqs, the middleware falls back to classical cryptography (`cryptography` library) with a warning log.
