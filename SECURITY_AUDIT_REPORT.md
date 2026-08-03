# 🔐 Miau Finance — Security Audit Report

**Project:** `/home/jevgeniz/Projekte/miau-finance` (branch `cat`, 918 commits, 1,660 tracked files)
**Audit date:** 2026-08-03
**Scope:** Full-stack — FastAPI backend, React 18 frontend, Docker Compose, K8s manifests, git history
**Method:** Direct code verification (every finding verified against source + tool output). No findings asserted from memory.

---

## Executive Summary

| Severity | Count | Summary |
|:--------:|:-----:|:--------|
| 🔴 CRITICAL | 4 | Hardcoded superadmin backdoor; unauthenticated token relay; duplicate unauthenticated router; Stripe webhook signature bypass |
| 🟠 HIGH | 7 | Secrets committed to git; exec() sandbox bypass; no K8s security context; exposed infra ports; vulnerable npm deps; JWT in localStorage |
| 🟡 MEDIUM | 6 | python-jose vulnerable range; rate-limit bypass; no network policies; weak password policy; missing issuer/audience on JWT |
| 🟢 LOW / INFO | 5 | Debug logging in prod bundle; metrics exposure; missing .gitignore hardening |

**Bottom line:** This project **must not go to production in its current state**. The hardcoded `pawdmin/miau2026` superadmin gives anyone with repo access full admin control, and the unauthenticated token relay + Stripe webhook bypass allow privilege escalation and payment fraud. Several items are 1-line fixes.

---

## 🔴 CRITICAL FINDINGS

### C1. Hardcoded superadmin backdoor — `pawdmin` / `miau2026`
- **File:** `backend/app/middleware/auth/base.py:79-86, 148-152`; `backend/app/middleware/tier.py:135-138`
- **Evidence (verified):**
  ```python
  # base.py:82
  if hmac.compare_digest(username, "pawdmin") and hmac.compare_digest(password, "miau2026"):
      return True
  # base.py:150 — grants admin role, bypasses DB entirely
  role = "admin" if form_data.username == "pawdmin" else "user"
  ```
- **Aggravating:** Credentials are **published in the repo**: `README.md:854-867`, `apps/auth/index.html:78`, `apps/README.md:34`, `apps/marketing-dashboard/src/App.tsx:150` ("Demo: pawdmin / miau2026").
- **Impact:** Anyone who can read this repo (or README) can log in as **admin**, call `POST /api/v1/auth/token`, and receive a JWT with `role=admin` — bypassing the database, password hashing, and rate-limit slow path. Full account takeover + admin API access.
- **Fix:** Remove the hardcoded branch. Use only DB-backed auth. If a superadmin bootstrap is needed, create one via a secure seed script with env-provided credentials, and rotate immediately.

### C2. Unauthenticated JWT token relay (token theft / poisoning)
- **File:** `backend/app/api/service_desk.py:26-37`
- **Evidence (verified):**
  ```python
  @router.post("/api/v1/auth/broadcast-token")
  async def broadcast_token(body: TokenRelayBody):      # NO auth dependency
      _token_relay["token"] = body.token                # anyone can SET a token
      ...
  @router.get("/api/v1/auth/broadcast-token")
  async def get_broadcast_token():                      # NO auth dependency
      return _token_relay                               # anyone can READ last JWT
  ```
- **Impact:** An attacker can **read** a real user's JWT from the in-memory relay (account takeover), or **poison** it to hijack SSO flows across the apps.
- **Fix:** Remove the relay entirely (use httpOnly cookies or a proper broker), or at minimum require authentication + short TTL + one-time consumption.

### C3. Service Desk router registered TWICE — once with NO authentication
- **File:** `backend/app/main.py:364-367`
- **Evidence (verified):**
  ```python
  app.include_router(service_desk_api.router, dependencies=[])            # UNAUTHENTICATED
  service_desk_auth = [Depends(get_current_user)]
  app.include_router(service_desk_api.router, dependencies=service_desk_auth)  # duplicate
  ```
- **Impact:** FastAPI registers **both** copies → all `/api/v1/service-desk/*` endpoints (ticket listing, creation, update, delete, poke) are reachable **without authentication**, including reads of all users' tickets and a `broadcast-token` relay.
- **Fix:** Remove the unauthenticated `include_router` line (the first one). Register once, with auth.

### C4. Stripe webhook signature verification bypass
- **File:** `backend/app/api/billing.py:580-612`
- **Evidence (verified):**
  ```python
  except Exception:
      if not STRIPE_WEBHOOK_SECRET:
          logger.warning("No webhook secret configured, skipping verification")
          event = json.loads(payload)      # ⚠️ unsigned payload accepted!
  ```
  And later, a forged `checkout.session.completed` with `metadata.user_id` + `tier` directly **writes a paid subscription row** (`INSERT INTO subscriptions ... 'active'`) via `text()`.
- **Impact:** Any unauthenticated caller can forge webhook events → **grant themselves paid Pro/Enterprise tiers** → bypass paywalls / unlock paid features.
- **Fix:** If `STRIPE_WEBHOOK_SECRET` is not set, **fail closed** (reject webhooks, log error). Never parse the payload as trusted when signature verification was skipped.

---

## 🟠 HIGH FINDINGS

### H1. Secrets committed to git
- **File:** `config/.env.go-live` — **tracked** in git (commit `fb332b3`, "move config files to config/") and **NOT ignored** (`git check-ignore` → not ignored).
- **Contents (verified, redacted):** Stripe key **placeholders** in live format (`sk_live_YOUR_STRIPE_SECRET_KEY`, `pk_live_YOUR_STRIPE_PUBLISHABLE_KEY`, `whsec_YOUR_WEBHOOK_SECRET`), **real payout email** (`HOOMAN_PAYPAL=ziebartjevgeni@gmail.com`), payout tag, ops budget, and `CRYPTO_MERCHANT_EVM_PRIVATE_KEY=` field.
- **Impact:** Template is dangerous-by-design ("rename to .env"), and the live-format placeholders + personal payout email are public. Any future commit filling real keys will leak them permanently. The root `.env` (real passwords) is correctly untracked — but `config/.env.go-live` defeats that protection.
- **Fix:** `git rm --cached config/.env.go-live`, delete it, add `config/.env.*` to `.gitignore`, purge from history if ever a real key was committed (`git filter-repo`).

### H2. k8s secret manifest committed + invalid YAML
- **File:** `k8s/secret.yaml` (tracked)
- **Evidence (verified):** Values are base64 `Q0hBTkdFX01F` = `CHANGE_ME` (placeholders — no real secrets leaked, but pattern is wrong). More importantly, the file **fails to parse**:
  ```
  YAML ERROR: while parsing a block mapping ... line 25, column 4
  ```
  The line `   STRIPE_SECRET_KEY: ...` has a stray leading space (line 25) → whole manifest is invalid.
- **Impact:** If applied, the deployment breaks or secrets silently missing. Committing secret manifests normalizes leaking real secrets later.
- **Fix:** Fix indentation, move to sealed-secrets/external-secrets, never commit secret manifests.

### H3. AI-generated strategy code executed via `exec()` with bypassable validation
- **File:** `backend/app/services/strategies/ai_generated.py:30-44, 95-109`
- **Evidence (verified):** `_validate_strategy_code` blocks only **attribute** calls (`node.func.attr in ("open","exec","eval","__import__","compile")`). **Bare calls pass** — I verified:
  ```python
  code = 'result = exec("print(1)")'          # ast.Call with Name func, NOT Attribute
  blocked? -> False                            # ✅ bypass confirmed
  ```
  Then `exec(self._strategy_code, module.__dict__)` runs it. Description text from the API flows into the LLM prompt that produces this code → **prompt-injection → arbitrary code execution** on the backend host.
- **Fix:** Don't `exec` LLM output, ever. Run strategies in a real subprocess sandbox (or WASM). If exec must stay: block `ast.Name` calls too, reject `__subclasses__`, `__bases__`, `getattr`, etc. Best: treat LLM output as untrusted and refuse codegen.

### H4. Plugin sandbox is an `exec()` jail — escape risk
- **File:** `backend/app/middleware/plugin_sandbox.py:131-196`
- **Evidence (verified):** `exec(compiled, global_ns, local_ns)` with a custom `__import__` guard and memory/time limits, but full `exec` semantics remain; standard Python sandbox escapes (e.g., `().__class__.__bases__[0].__subclasses__()`) are not blocked by the AST/module checks.
- **Impact:** A malicious plugin (or one smuggled past the loader) can likely escape to the host.
- **Fix:** Run plugins in an isolated subprocess with OS-level sandboxing (gVisor/firecracker, Docker, or restricted worker) — never `exec` in-process.

### H5. Infrastructure exposure & default credentials (Docker Compose)
- **File:** `docker-compose.yml`, `infra/docker/docker-compose.prod.yml`
- **Evidence (verified):** All ports bound to `0.0.0.0`:
  - `redis: 6379:6379` with fallback password `${REDIS_PASSWORD:-miau_redis}`
  - `postgres: 5434:5432`
  - `minio: 9000:9000, 9001:9001`
  - `grafana: 3000:3000` with **`GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}`** (default `admin`!)
  - `superset: 8088`, `airflow: 8080`, `cube: 4000`, `prometheus: 9090`
- **Impact:** Public exposure of databases/queues with known default credentials = easy compromise. Grafana default `admin/admin` is a classic target.
- **Fix:** Bind to `127.0.0.1` or an internal network; require strong passwords (no fallbacks); remove `:-admin` default.

### H6. Frontend dependency vulnerabilities (npm audit — 3 high)
- **Evidence (verified, `npm audit` run):** 0 critical, **3 high**, 3 moderate, 1 low, 7 total.
  - **vite 6.4.2 (high):** `server.fs.deny` bypass; launch-editor NTLMv2 hash disclosure
  - **postcss (high):** path traversal in previous source map auto-loading
  - **undici (high):** TLS validation bypass, HTTP header injection, WS DoS, queue poisoning
  - **dompurify (moderate ×N):** multiple sanitizer bypasses — significant because DOMPurify is the primary XSS defense
  - **react-router / react-router-dom (moderate):** open redirect → XSS
- **Fix:** `npm audit fix` / upgrade vite, postcss, undici, dompurify, react-router to patched versions.

### H7. JWT stored in `localStorage`
- **File:** `frontend/src/lib/auth.ts:1-23` — `miau_token` / `miau_refresh_token` in `localStorage` (used across many components, e.g. `ApiPlayground.tsx`, `Chart3D.tsx`).
- **Impact:** Any XSS (and H6's dompurify bypasses raise that risk) exfiltrates tokens. localStorage is also readable by any same-origin script.
- **Fix:** Use httpOnly + Secure + SameSite cookies for tokens, or at minimum `sessionStorage` + short-lived tokens + refresh rotation.

---

## 🟡 MEDIUM FINDINGS

### M1. python-jose dependency range permits known-vulnerable version
- **File:** `backend/requirements.txt`: `python-jose[cryptography]>=3.3.0`
- **Verified CVEs:** CVE-2024-33663 (algorithm confusion w/ OpenSSH ECDSA keys) and CVE-2024-33664 (JWT bomb DoS) affect **≤ 3.3.0**; fixed in 3.4.0. Installed venv has 3.5.0 (safe) but the **`>=3.3.0` constraint permits 3.3.0** — a fresh install could pull a vulnerable version.
- **Fix:** Pin `python-jose>=3.4.0` (or switch to `PyJWT`).

### M2. Rate limiting can be bypassed via spoofable client key
- **File:** `backend/app/middleware/rate_limit.py:182-187`
  ```python
  forwarded = request.headers.get("X-Forwarded-For")
  if forwarded:
      return forwarded.split(",")[0].strip()   # trusts client-supplied header
  ```
- **Impact:** Attacker sets `X-Forwarded-For` to rotate identity → unlimited requests (brute force, scraping, AI endpoint abuse). Login limiter also keys on `request.client.host` only — but XFF trust makes global limiter ineffective behind any proxy.
- **Fix:** Only trust XFF when the proxy is a known trusted peer (e.g., from env `TRUSTED_PROXIES`); otherwise use socket peer IP.

### M3. No Kubernetes security context / network policies
- **Evidence (verified):** `grep runAsNonRoot|readOnlyRootFilesystem|allowPrivilegeEscalation|privileged` across `k8s/*.yaml` → **zero matches**. No NetworkPolicy in `k8s/namespace.yaml` or elsewhere. `imagePullPolicy: Always` with `:latest` tags in `deployment.yaml`.
- **Impact:** Pods run as root-capable, no blast-radius control; `:latest` = non-reproducible, mutable image risk.
- **Fix:** Add `securityContext: {runAsNonRoot, runAsUser: 1000, allowPrivilegeEscalation: false, readOnlyRootFilesystem: true, capabilities: {drop: [ALL]}}`; add NetworkPolicies; pin images by digest.

### M4. Registration / auth hardening gaps
- **File:** `backend/app/middleware/auth/base.py:119-138`
  - No password strength policy (any string accepted).
  - No email verification; `409` on register discloses username/email existence (enumeration).
  - `register` has no rate limit (only login does).
- **Fix:** Enforce password policy (length/complexity), add rate limiting + captcha on register, generic 409 message.

### M5. JWT lacks issuer/audience; refresh flow is broken AND re-requests password
- **Files:** `backend/app/middleware/auth/base.py:41-53, 189-204`; `frontend/src/lib/auth.ts:60-96`
- **Verified mismatch:** Frontend calls `/api/v1/auth/refresh` with `{refresh_token}`, but backend `RefreshRequest` requires `{access_token, username, password}`. The refresh endpoint **re-authenticates with plaintext password** instead of using a refresh token, and the frontend's stored refresh token is never actually issued by the backend (`/token` returns only `access_token`).
- **Fix:** Implement proper refresh-token rotation (opaque, server-stored, revoked on use), and align frontend/backend payloads.

### M6. WebSocket lacks per-connection message limits / CSRF-style origin check
- **File:** `backend/app/api/ws.py:76-120` — token-in-first-message auth is good and tickers are validated (`validate_ticker`, `MAX_TICKERS`). But no origin check and no per-connection send rate limit (the push loop runs regardless of client consumption → resource exhaustion for server push).
- **Fix:** Validate `Origin` against allowed hosts; cap subscription count per connection; backpressure handling.

---

## 🟢 LOW / INFO

### L1. Debug logging in production bundle
- `frontend/index.html:21` — `window.__LOG_LEVEL__ = 'debug'` ships in the production build. Reduce noise / info leakage.

### L2. Prometheus `/metrics` is public (no auth)
- Verified: `/metrics` is in the rate-limiter and audit-logger skip lists; endpoint is served without auth. Standard for monitoring, but confirms internal names/metrics are exposed if deployed publicly.

### L3. `.gitignore` hardening
- `.gitignore` covers `.env` / `.env.*` at root but not `config/.env.*` (the exact file that is tracked). Add `**/.env*` and secret-file patterns (`.pem`, `*.key`, `*.p12`, `secrets.yaml`, `terraform.tfstate`).

### L4. Positive controls verified (no action needed)
- ✅ **SQL injection:** all `text(f"..."` usages interpolate only fixed/whitelisted fragments with bound parameters (verified across `users.py`, `teams.py`, `service_desk.py`, `audit.py`, `education.py`, `governance.py`) — no direct user input reaches raw SQL.
- ✅ **CSRF:** `CSRFMiddleware` double-submit token with `SameSite=Lax`, `httponly` cookie, constant-time compare; sensible exclusions for auth endpoints.
- ✅ **Security headers (nginx):** CSP `default-src 'self'`, HSTS preload, `X-Frame-Options DENY`, `X-Content-Type-Options nosniff`, `frame-ancestors 'none'`.
- ✅ **Input sanitization:** `sanitize.py` middleware + DOMPurify allowlist (`ALLOWED_TAGS: span,br,b,i,u,a`) in `Terminal.tsx`.
- ✅ **Dockerfiles:** run as non-root (`appuser`, `nginxuser`), multi-stage, source maps deleted in frontend prod build.
- ✅ **Backend deps:** `pip-audit -r requirements.txt` → **no known CVEs** in pinned/installed versions.
- ✅ **API docs:** `/docs`, `/redoc`, `/openapi.json` disabled when `environment=production` (`main.py:108-114`).
- ✅ **Audit logging** redacts sensitive fields (`password, secret, token, key, api_key, jwt`) and truncates Bearer tokens (`audit_logging.py:67-89`).
- ✅ **Stripe checkout** uses `stripe.checkout.Session` server-side; webhook only issue is C4.

---

## Priority Remediation Roadmap

| Priority | Action | Effort |
|:--------:|:-------|:------:|
| P0 | Remove `pawdmin/miau2026` backdoor (C1) | S |
| P0 | Remove unauthenticated service_desk router registration (C3) | S |
| P0 | Remove/secure broadcast-token relay (C2) | S |
| P0 | Fail-closed Stripe webhook when secret missing (C4) | S |
| P1 | Delete tracked `config/.env.go-live` + fix `.gitignore` (H1) | S |
| P1 | Fix `k8s/secret.yaml` + move to sealed-secrets (H2) | S |
| P1 | Kill `exec()` on LLM output; harden plugin sandbox (H3, H4) | M |
| P1 | `npm audit fix` + pin vite/undici/postcss/dompurify (H6) | S |
| P2 | Harden compose port bindings + Grafana default admin (H5) | S |
| P2 | Trusted-proxy XFF handling (M2), K8s security contexts (M3) | M |
| P2 | Password policy + registration rate limit (M4) | S |
| P2 | Proper refresh-token rotation (M5) | M |
| P3 | httpOnly cookie auth, WS origin/limits (H7, M6) | M |

---

*This audit was performed read-only against the working tree and git history. All findings were verified directly against source code and tool output (git log/grep, npm audit, pip-audit, Python AST validation, YAML parsing). No files were modified.*
