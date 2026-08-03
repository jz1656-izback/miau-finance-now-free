# 🐾 Pawdenity — Cat Identity Provider

Central authentication hub for the Miau Finance ecosystem.
One account, one login, infinite tools.

## How it works

1. User visits `http://localhost:5190` (or clicks "🐾 Pawdenity" from any app)
2. Enters username + password (or registers a new account)
3. On success, JWT token is stored in `localStorage` as `miau_token`
4. Token is broadcast to all apps via `POST /api/v1/auth/broadcast-token`
5. User is redirected back to the originating app
6. All apps read `miau_token` from localStorage and attach it as `Authorization: Bearer`

## Superadmin Account

```
Username: pawdmin
Password: miau2026
Role:     admin
```

This account bypasses the database and is hardcoded in the auth middleware for development/demo use.
It works even if the database is not running.

## Login Endpoints (Backend)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/v1/auth/token` | Login — returns `{access_token, token_type}` |
| `POST` | `/api/v1/auth/register` | Register — creates user in DB |
| `POST` | `/api/v1/auth/token/refresh` | Refresh expired token |
| `POST` | `/api/v1/auth/broadcast-token` | Relay token to other apps |
| `GET` | `/api/v1/auth/broadcast-token` | Poll for relayed token |

## Cross-Origin Token Relay

When you log in on any app, it calls `POST /api/v1/auth/broadcast-token` with the token.
All other apps check this endpoint on load (and every 30s) and pick up the token automatically.

## Apps that use Pawdenity

| App | Port | Login UI |
|-----|------|----------|
| Pawdenity (this page) | 5190 | Full login/register card |
| Service Desk | 5180 | Modal with Pawdenity link |
| Ecosystem Site | 5175 | Modal with Pawdenity link |
| Landing Page | 8080 | Prompt with Pawdenity link |
| Marketing Dashboard | 5176 | LoginForm with Pawdenity link |
| Admin Panel | 8000 | Token paste + Pawdenity button |
| Terminal UI | 5173 | `login` command |
| Education Platform | 5174 | AuthModal |
| Log Viewer | 8000/logs-viewer | Pawdenity link in header |
