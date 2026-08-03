# 🔒 Miau Finance Security Architecture

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "A cat always knows what's behind the door.
               So should you."
```

This document describes the security architecture of Miau Finance — how we protect your financial data from unauthorized access, attacks, and hairballs.

---

## 📋 Security Overview

| Layer | Technology | Protection |
|-------|-----------|------------|
| **Transport** | HTTPS (production) | TLS 1.3 encryption in transit |
| **Authentication** | JWT (HS256) | Bearer token auth for all endpoints |
| **Authorization** | Middleware-based | Protected routes under `/api/v1/` |
| **Rate Limiting** | Redis-backed sliding window | 100 req/min/IP, 1000 req/hr/user |
| **CORS** | Origin whitelist | Only approved origins can access API |
| **Headers** | CSP, HSTS, X-Frame-Options | Prevents XSS, clickjacking, MITM |
| **Input Validation** | Pydantic + sanitize | SQL/XSS injection prevention |
| **Secrets** | Environment variables | Never in source code or version control |

---

## 🔐 Authentication Flow

```
POST /api/v1/auth/token
  {
    "username": "admin",
    "password": "admin"
  }
        │
        ▼
  ┌──────────────────┐
  │ Verify credentials │ (passlib bcrypt hash check)
  └──────────────────┘
        │
        ▼
  ┌──────────────────┐
  │ Generate JWT      │ (python-jose, HS256)
  │ - sub: username   │
  │ - exp: 24h        │
  └──────────────────┘
        │
        ▼
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
```

### Protected Endpoint Flow

```
GET /api/v1/market/price/AAPL
  Authorization: Bearer eyJhbGci...
        │
        ▼
  ┌──────────────────┐
  │ JWT Middleware    │ → decode token
  │ get_current_user  │ → verify signature
  │                   │ → check expiration
  └──────────────────┘
        │
        ▼
  ┌──────────────────┐
  │ ✓ Validated       │ → extract username from `sub`
  └──────────────────┘
        │
        ▼
     Handler
```

### Token Configuration

| Setting | Value | Location |
|---------|-------|----------|
| Algorithm | HS256 | `backend/app/middleware/auth.py` |
| Secret key | `JWT_SECRET` env var | `backend/.env` |
| Expiration | 24 hours | `backend/app/middleware/auth.py` |
| Token type | Bearer | Standard |

```python
# backend/app/middleware/auth.py
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(401, "Invalid token")
        return username
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
```

**Never commit `JWT_SECRET` to version control.** Use environment variables.

---

## 🚦 Rate Limiting

### Architecture

```
Request
    │
    ▼
┌───────────────────────┐
│ RateLimitMiddleware    │
│                       │
│ Per-IP window:        │  Redis key: rate_limit:ip:<ip>
│ → 100 req / 1 minute  │  → INCR + EXPIRE
│                       │
│ Per-user window:      │  Redis key: rate_limit:user:<username>
│ → 1000 req / 1 hour   │  → INCR + EXPIRE
│                       │
│ If exceeded:          │  → HTTP 429 Too Many Requests
│ → X-RateLimit-*       │  → Headers with limit/remaining/reset
└───────────────────────┘
    │
    ▼
  (continue to auth)
```

### Response Headers

| Header | Example | Meaning |
|--------|---------|---------|
| `X-RateLimit-Limit` | `100` | Max requests per window |
| `X-RateLimit-Remaining` | `73` | Requests left in window |
| `X-RateLimit-Reset` | `1716000000` | Unix timestamp when limit resets |

### 429 Response

```json
{
  "detail": "Rate limit exceeded. Try again in 34 seconds."
}
```

### Redis Fallback

If Redis is unavailable, rate limiting falls back to an in-memory counter. This provides basic protection without blocking all requests.

---

## 🛡️ CORS Configuration

```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",       # Dev frontend
        "http://localhost:3000",       # Grafana
        "https://miau.finance",        # Production
        "https://app.miau.finance",    # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"],
    max_age=600,
)
```

**Restriction:** In production, replace `localhost` origins with the actual domain. Never use `allow_origins=["*"]` with `allow_credentials=True`.

---

## 🛡️ Security Headers

```python
# backend/app/middleware/security_headers.py
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        if not settings.debug:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' ws://localhost:* ws://miau.finance:*; "
                "font-src 'self' data:; "
                "frame-ancestors 'none'; "
                "base-uri 'self'; "
                "form-action 'self'"
            )

        return response
```

| Header | Value | Protection |
|--------|-------|------------|
| `X-Content-Type-Options` | `nosniff` | Prevents MIME-type sniffing |
| `X-Frame-Options` | `DENY` | Prevents clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Enables browser XSS filter |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limits referrer leakage |
| `Strict-Transport-Security` | `max-age=31536000` | Enforces HTTPS |
| `Content-Security-Policy` | See above | Prevents XSS, data injection |

---

## 🧹 Input Validation & Sanitization

### Pydantic Validation (Backend)

All endpoint inputs go through Pydantic models for type checking:

```python
from pydantic import BaseModel, Field, validator

class PortfolioCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = Field(None, max_length=1024)
    holdings: list[Holding] = Field(..., min_items=1)

    @validator('name')
    def name_must_be_clean(cls, v):
        if v.startswith('__') or v.startswith('..'):
            raise ValueError('Name contains suspicious characters')
        return v.strip()
```

### Terminal Input Sanitization

```python
# backend/app/middleware/sanitize.py
import re

def sanitize_terminal_input(text: str) -> str:
    """Sanitize user input from the terminal."""
    # Strip ANSI escape sequences
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    # Strip control characters except newline
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    # Trim and limit length
    text = text.strip()[:4096]
    return text

def sanitize_html(text: str) -> str:
    """Escape HTML entities to prevent XSS."""
    return (
        text.replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;')
    )
```

### SQL Injection Prevention

We use parameterized queries via SQLAlchemy — never string interpolation:

```python
# ✅ SAFE: Parameterized
await db.execute(
    select(Instrument).where(Instrument.ticker == ticker)
)

# ❌ DANGER: String interpolation — NEVER do this
await db.execute(f"SELECT * FROM instruments WHERE ticker = '{ticker}'")
```

---

## 🔑 Secrets Management

| Secret | Location | How to Set |
|--------|----------|------------|
| `JWT_SECRET` | `backend/.env` | Generate with `openssl rand -hex 32` |
| `POSTGRES_PASSWORD` | `.env` (root) | Set in `.env.example` |
| `REDIS_PASSWORD` | `.env` (root) | Set in `.env.example` |
| `FRED_API_KEY` | `backend/.env` | Free key from FRED website |
| `MINIO_ROOT_PASSWORD` | `.env` (root) | Set in `.env.example` |
| `SUPERSET_SECRET_KEY` | `.env` (root) | Set in `.env.example` |

**Rules:**
- `.env` is in `.gitignore` — never committed
- `.env.example` provides template with dummy values
- In production, use Kubernetes Secrets or Docker Swarm secrets
- Rotate keys regularly

---

## 🚨 Threat Model

| Threat | Mitigation |
|--------|-----------|
| **Brute force login** | Rate limiting (100 req/min/IP) |
| **Token theft** | JWT 24h expiration, HTTPS-only in production |
| **XSS via terminal** | HTML entity escaping in output |
| **SQL injection** | Parameterized queries (SQLAlchemy ORM) |
| **DDoS** | Rate limiting + nginx/traefik frontend |
| **Data exfiltration** | CORS origin whitelist |
| **Clickjacking** | X-Frame-Options: DENY |
| **MITM** | HSTS enforcement in production |
| **Secret exposure** | .gitignore + env vars only |
| **API key leakage** | Keys in env vars, never in code |

---

## ✅ Security Checklist

- [x] JWT authentication on all `/api/v1/` endpoints
- [x] Rate limiting (100/min IP, 1000/hr user)
- [x] CORS restricted to approved origins
- [x] Security headers (CSP, HSTS, X-Frame-Options, etc.)
- [x] Pydantic input validation on all endpoints
- [x] HTML/terminal input sanitization
- [x] Parameterized queries (SQL injection prevention)
- [x] `.env` in `.gitignore`
- [x] `.env.example` template with no real secrets
- [x] Password hashing with bcrypt
- [x] Graceful Redis fallback for rate limiting
- [ ] HTTPS enforcement in production (nginx/traefik)
- [ ] Dependency vulnerability scanning (e.g. Snyk, Dependabot)
- [ ] Regular security audit schedule

---

## 📞 Reporting Vulnerabilities

If you discover a security vulnerability, **do not open a public issue.** Email the maintainers directly. We will respond within 48 hours and keep you updated throughout the fix process.

---

## 🔐 Phase 26: Post-Quantum Cryptography (PQC)

### Overview

Miau Finance Phase 26 adds post-quantum cryptographic primitives to protect against attacks from quantum computers using Shor's and Grover's algorithms.

### Implemented Primitives

| Algorithm | Type | NIST Standard | Status |
|-----------|------|---------------|--------|
| **CRYSTALS-Kyber** | Key Encapsulation Mechanism (KEM) | Selected for ML-KEM | ✅ Implemented |
| **CRYSTALS-Dilithium** | Digital Signature | Selected for ML-DSA | ✅ Implemented |
| **FALCON** | Digital Signature | Selected for FN-DSA | ✅ Implemented |
| **Hybrid (X25519+Kyber)** | Hybrid KEM | ECDH + PQC combined | ✅ Implemented |

### Where PQC Is Used

| Component | Traditional | PQC Replacement |
|-----------|-------------|-----------------|
| JWT Signing | RS256 / ES256 | Dilithium + FALCON |
| TLS 1.3 | X25519 key exchange | X25519 + Kyber hybrid |
| API Authentication | ECDSA signatures | FALCON signatures |
| Data Encryption | AES-256-GCM | AES-256-GCM + Kyber-encapsulated keys |
| Key Exchange | ECDH | Kyber KEM |

### PQC Key Management

- **Kyber keys**: 1.184 bytes (public), 2.400 bytes (private) for ML-KEM-768
- **Dilithium keys**: 1.312 bytes (public), 2.520 bytes (private) for ML-DSA-65
- **FALCON keys**: 897 bytes (public), 1.281 bytes (private) for FN-DSA-512
- Keys are stored encrypted at rest using the existing keychain service
- All PQC operations are implemented in pure Rust via `pqcrypto-rs` and exposed to Python via PyO3

### Migration Path

See the [PQC Migration Guide](security/pqc_migration.md) for step-by-step upgrade instructions.

---

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "Security is not a feature.
               It's the cat door lock.
               Without it, anything gets in."
```

---
_[Back to README](../README.md) | [Developer Guide](./DEVELOPER.md) | [Architecture](./ARCHITECTURE.md)_
