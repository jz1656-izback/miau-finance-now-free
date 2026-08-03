# 🐱 MIAU FINANCE — Security Guide

## JWT · RBAC · PQC · TLS · CSRF · SIWE · Audit

### Security Layers
- **Auth**: JWT (HS256) tokens
- **RBAC**: 3 roles (readonly, user, admin)
- **Encryption**: Fernet AES-256-GCM for API keys
- **PQC**: CRYSTALS-Kyber + Dilithium ready
- **Web3**: SIWE (Sign-In With Ethereum)
- **CSRF**: Double-submit cookie pattern
- **CSP/HSTS**: XSS + HTTPS enforcement
- **Rate Limit**: 30/min free, 300/min Pro, 10K/min Enterprise
- **Audit**: All mutations logged

### Best Practices
- Never commit `.env` to git
- Rotate secrets regularly
- API keys encrypted at rest
- All passwords hashed with bcrypt
- TLS everywhere in production

### Tier Enforcement
```python
@router.get("/ai/summary/{ticker}")
async def ai_summary(
    _=Depends(require_tier("pro", "enterprise")),
    ...
)
```

### Security Audit
0 critical, 0 high severity findings. Full report at `docs/SECURITY_AUDIT.md`.
