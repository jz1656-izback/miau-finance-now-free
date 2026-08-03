# 🔑 Miau Finance — Authentication Guide

All Miau apps share a single authentication system powered by **Pawdenity**,
the cat identity provider. One account, one login, infinite tools.

## How to Login

### Quickest Way
1. Open **http://localhost:5190** (Pawdenity)
2. Enter credentials or register a new account
3. After login, you are redirected back — token works everywhere

### Superadmin (Development)
```
Username: pawdmin
Password: miau2026
Role:     admin
```
This works even without a database running.

### Per-App Login

| App | How to Login |
|-----|-------------|
| **Pawdenity** (5190) | Login/register form on the page |
| **Ecosystem Site** (5175) | Click "🔑 Login" in header → modal → or 🐾 Pawdenity link |
| **Service Desk** (5180) | Click "🔑 Login" in header → modal → or 🐾 Pawdenity link |
| **Landing Page** (8080) | Click "🔑 Login" in footer → prompt |
| **Marketing Dashboard** (5176) | LoginForm on page → or 🐾 Pawdenity link |
| **Admin Panel** (8000/static/admin.html) | Click "🐾 Login via Pawdenity" → or paste token |
| **Terminal UI** (5173) | Type `login pawdmin miau2026` in terminal |
| **Education Platform** (5174) | Click "Sign In" → AuthModal → or "Continue as Student" |

## How Registration Works

1. On any app with registration (Pawdenity, Service Desk, Education, Ecosystem), click "Register"
2. Enter email, username, password
3. Account is created via `POST /api/v1/auth/register`
4. You are automatically logged in

Or register via the API directly:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"cat@miau.com","username":"catlover","password":"miau2026"}'
```

## Token Details

- **Type:** JWT (HS256)
- **Storage key:** `miau_token` in localStorage
- **Auth header:** `Authorization: Bearer <token>`
- **Expiry:** 60 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Refresh:** `POST /api/v1/auth/token/refresh`

## Cross-App Token Sync

When you log in on any app:
1. Token is stored in that app's `localStorage`
2. App calls `POST /api/v1/auth/broadcast-token` to relay the token
3. All other apps poll `GET /api/v1/auth/broadcast-token` on load
4. If a recent token (<30s old) is found, they pick it up automatically

## API Reference

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| `POST` | `/api/v1/auth/token` | No | Login — returns `{access_token, token_type}` |
| `POST` | `/api/v1/auth/register` | No | Create account |
| `POST` | `/api/v1/auth/token/refresh` | No | Refresh expired token |
| `POST` | `/api/v1/auth/broadcast-token` | No | Relay token for SSO |
| `GET` | `/api/v1/auth/broadcast-token` | No | Poll for relayed token |
| `POST` | `/api/v1/auth/education-student` | API key | Guest student access |

## Security Notes

- Tokens are stored in `localStorage` (accessible to JS — for production, use HttpOnly cookies)
- Rate limiting: 5 failed login attempts per IP per 60 seconds
- Passwords are bcrypt-hashed in the database
- Post-quantum JWT (Dilithium/Falcon) is implemented but not wired yet
- Demo credentials (`pawdmin`) are hardcoded for development only
