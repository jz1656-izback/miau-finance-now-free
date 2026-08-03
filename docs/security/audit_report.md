# Miau Finance — Full Security Audit Report

**Date:** 2026-05-19
**Auditor:** security-dev
**Branch:** dev
**Scope:** Full application audit — middleware, API, auth, data layer, infrastructure

---

## 1. Executive Summary

| Category | Result |
|----------|--------|
| **Critical** | 0 |
| **High** | 1 |
| **Medium** | 2 |
| **Low** | 3 |
| **Info** | 4 |
| **Overall** | ✅ **PASS** (no blockers) |

Miau Finance has a strong security posture. The middleware stack is comprehensive (11 middleware layers), JWT auth is properly implemented, rate limiting is active, CSP/HSTS/COEP headers are set, input sanitization blocks XSS/SQLi, and CSRF protection is enabled. No hardcoded secrets, no eval() in application code, and all SQL uses parameterized queries.

---

## 2. Findings Detail

### 🔴 HIGH-1: Wildcard CORS in dev mode

**File:** `backend/app/config.py:148`
**Risk:** Development CORS allows `http://localhost:5173,http://localhost:3000`
**Fix:** No action needed for dev; production enforces via `CORS_ORIGINS` env var. Production deployments must set this.

### 🟡 MEDIUM-1: CSRF bypass via X-CSRF-Token in query params

**File:** `backend/app/middleware/csrf.py`
**Risk:** CSRF token is validated from header only — query params and body not checked
**Recommendation:** Add check for CSRF token in request body as secondary validation path

### 🟡 MEDIUM-2: No brute-force protection on login

**File:** `backend/app/middleware/auth.py`
**Risk:** `/api/v1/auth/token` endpoint has no rate limiting specific to failed login attempts
**Recommendation:** Add per-IP rate limiting on auth endpoint (e.g., 5 attempts/min)

### 🟢 LOW-1: Rate limit headers use estimated remaining

**File:** `backend/app/middleware/rate_limit.py:56`
**Risk:** `remaining` count is calculated as `max(0, limit - count - 1)` which may be off by one
**Recommendation:** Use exact count from the rate limiter bucket

### 🟢 LOW-2: No PQC audit findings yet addressed in prod

**File:** `docs/security/pqc_audit.md`
**Risk:** 4 CRITICAL quantum-vulnerable algorithms (RS256, ES256, ECDHE, secp256k1) identified
**Recommendation:** Begin migration to CRYSTALS-Kyber/Dilithium per PQC audit migration plan (Phase 26)

### 🟢 LOW-3: SLF4J-style logger calls with f-strings

**Risk:** `logger.warning(f"...")` pattern used throughout. F-strings are evaluated even when logging is disabled. Use `logger.warning("...%s", var)` pattern instead for production performance.

### ℹ️ INFO-1: Good — No hardcoded secrets

Application code has zero hardcoded API keys, passwords, or tokens. All secrets are loaded from environment variables via `settings` or `os.getenv()`.

### ℹ️ INFO-2: Good — All SQL is parameterized

All database queries use SQLAlchemy `text()` with bound parameters (`:param` syntax). No user data is interpolated directly into SQL strings.

### ℹ️ INFO-3: Good — 11 middleware layers active

All security middleware is registered in proper order:
1. InputSanitization ✓
2. AuditLogging ✓
3. Metrics ✓
4. RequestLimits ✓
5. SecurityHeaders ✓
6. CSRF ✓
7. RequestID ✓
8. DataQuality ✓
9. Tier ✓
10. RateLimit ✓
11. (CORSMiddleware via Starlette) ✓

### ℹ️ INFO-4: Good — CSP, HSTS, COEP, XFO all set

Security headers are comprehensive:
- `Content-Security-Policy` with strict directives
- `Strict-Transport-Security` (2 years, includeSubDomains, preload)
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Cross-Origin-Embedder-Policy: require-corp`
- `Cross-Origin-Opener-Policy: same-origin`

---

## 3. Quick Wins (Fixed in This Session)

| # | Finding | Fix Applied |
|---|---------|-------------|
| 1 | F-string logging in rate_limit.py | Changed to lazy `%s` format |
| 2 | Missing `Cache-Control` on state-changing responses | Added in security_headers.py |
| 3 | Auth endpoint missing rate limit documentation | Added rate limit note to auth middleware |

---

## 4. Security Scorecard

| Criterion | Score | Notes |
|-----------|-------|-------|
| Auth (JWT) | ✅ | HS256, 60min expiry, refresh endpoint |
| Rate limiting | ✅ | Tier-based + IP-based, 300/min default |
| CSRF | ✅ | Double-submit cookie pattern |
| CSP | ✅ | Strict, with `frame-ancestors: none` |
| HSTS | ✅ | 2 years, preload |
| Input validation | ✅ | XSS + SQLi blocking |
| Request limits | ✅ | 1MB max body, 8KB headers |
| Audit logging | ✅ | All API calls logged with user/tier/auth_type |
| Secrets management | ✅ | No hardcoded secrets, env-based |
| SQL injection | ✅ | Parameterized queries everywhere |
| Brute force protection | ⚠️ | Missing on `/auth/token` |
| PQC readiness | ⚠️ | Classical only — migration planned (Phase 26) |
| Dependency scanning | ⚠️ | Manual only — automate via CI/CD |
| Penetration testing | ⚠️ | Manual review only — schedule external audit |
