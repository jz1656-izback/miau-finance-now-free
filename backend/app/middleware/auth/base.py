from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import defaultdict
from uuid import uuid4
from jose import JWTError, jwt
import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db, async_session

security = HTTPBearer(auto_error=False)

class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    iat: Optional[datetime] = None
    role: Optional[str] = None
    user_id: Optional[str] = None


JWT_ISSUER = "miau-finance"
JWT_AUDIENCE = "miau-finance-api"


def _jwt_secret() -> str:
    """Return the JWT signing secret, failing closed if unset.

    🔒 SECURITY (V7-007): Fail closed — never sign/verify with an empty or
    missing secret key.
    """
    if not settings.secret_key:
        raise RuntimeError("JWT secret_key is not configured — refusing to sign/verify tokens")
    return settings.secret_key


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
    })
    return jwt.encode(to_encode, _jwt_secret(), algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=[settings.jwt_algorithm],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
        )
        return payload
    except JWTError:
        return None


async def get_current_user(request: Request, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> dict:
    # Pawdentity SSO: accept a Bearer header (API/SDK clients) OR the
    # pawd_session HttpOnly cookie (all browser apps share ONE login).
    if credentials is not None:
        payload = verify_token(credentials.credentials)
        if payload is not None:
            return payload
        # Bearer header present but stale/invalid → fall back to the SSO
        # cookie before failing, then keep the original 401 semantics.
        cookie_token = request.cookies.get("pawd_session")
        cookie_payload = verify_token(cookie_token) if cookie_token else None
        if cookie_payload is not None:
            return cookie_payload
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # No Bearer header → try the pawd_session cookie (SSO).
    cookie_token = request.cookies.get("pawd_session")
    payload = verify_token(cookie_token) if cookie_token else None
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


async def optional_user(request: Request, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[dict]:
    payload: Optional[dict] = None
    if credentials is not None:
        payload = verify_token(credentials.credentials)
    if payload is None:
        # Pawdentity SSO fallback: accept the pawd_session cookie.
        cookie_token = request.cookies.get("pawd_session")
        if cookie_token:
            payload = verify_token(cookie_token)
    return payload


def validate_user(username: str, password: str) -> bool:
    """Validate against configured demo credentials only.

    🔒 SECURITY (V7-001/C1): Hardcoded superadmin backdoor (pawdmin/miau2026)
    removed. All authentication now goes through the DB user path.
    """
    import hmac
    user_ok = hmac.compare_digest(username, settings.demo_username or "")
    pass_ok = hmac.compare_digest(password, settings.demo_password or "")
    return user_ok and pass_ok


async def authenticate_db_user(username: str, password: str, db: AsyncSession) -> Optional[dict]:
    result = await db.execute(
        text("SELECT id, username, email, password_hash, role FROM users WHERE username = :username OR email = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        return dict(row)
    return None


router = APIRouter(tags=["Authentication"])

import time as _time
from collections import defaultdict
_login_attempts: dict[str, list[float]] = defaultdict(list)
LOGIN_RATE_LIMIT = 5
LOGIN_WINDOW = 60

def _check_login_rate(ip: str) -> bool:
    now = _time.time()
    _login_attempts[ip] = [t for t in _login_attempts[ip] if now - t < LOGIN_WINDOW]
    if len(_login_attempts[ip]) >= LOGIN_RATE_LIMIT:
        return False
    return True

def _record_login_attempt(ip: str) -> None:
    _login_attempts[ip].append(_time.time())


@router.post("/register", status_code=201)
async def register_user(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        text("SELECT id FROM users WHERE username = :username OR email = :email"),
        {"username": body.username, "email": body.email},
    )
    if existing.mappings().first():
        raise HTTPException(status_code=409, detail="Username or email already taken")

    user_id = uuid4()
    password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    await db.execute(
        text("""
            INSERT INTO users (id, username, email, password_hash, role)
            VALUES (:id, :username, :email, :password_hash, 'user')
        """),
        {"id": user_id, "username": body.username, "email": body.email, "password_hash": password_hash},
    )
    await db.commit()
    return {"message": "User created successfully"}


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: TokenRequest, request: Request):
    # 🐾 PAWDENTITY NOTE: This endpoint is the legacy JWT path (SDK/clients).
    # Browser-based apps should use POST /api/v1/pawdentity/login instead which
    # sets the shared HttpOnly `pawd_session` cookie for single sign-on across
    # ALL Miau Finance apps (terminal, frontend, education, ecosystem).
    # Rate limit: 5 failed attempts per IP per minute
    client_ip = request.client.host if request.client else "unknown"
    if not _check_login_rate(client_ip):
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again in 60 seconds.")

    # 🔒 SECURITY (V7-001/C1): Hardcoded pawdmin superadmin fast path removed.
    # All authentication goes through the DB user path only.
    try:
        async with async_session() as db:
            db_user = await authenticate_db_user(form_data.username, form_data.password, db)
    except Exception:
        db_user = None

    if db_user:
        role = db_user.get("role", "user")
        user_id = str(db_user.get("id", ""))
        username = db_user.get("username", form_data.username)
    else:
        _record_login_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={
            "sub": username,
            "role": role,
            "user_id": user_id,
        },
    )
    return TokenResponse(access_token=access_token)


class RefreshRequest(BaseModel):
    access_token: str
    username: str
    password: str


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh_access_token(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    payload = verify_token(body.access_token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    db_user = await authenticate_db_user(body.username, body.password, db)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Re-authentication failed", headers={"WWW-Authenticate": "Bearer"})
    new_token = create_access_token(
        data={
            "sub": payload.get("sub", ""),
            "role": payload.get("role", "user"),
            "user_id": payload.get("user_id", ""),
        },
    )
    return TokenResponse(access_token=new_token)


@router.post("/education-student", response_model=TokenResponse)
async def create_education_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if not credentials or credentials.credentials != settings.education_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Valid education API key required")
    access_token = create_access_token(
        data={
            "sub": "edu_student",
            "role": "student",
            "user_id": "",
            "auth_type": "education",
            "scopes": ["market:read", "risk:read", "esg:read", "forex:read", "portfolio:read"],
        },
        expires_delta=timedelta(hours=2),
    )
    return TokenResponse(access_token=access_token)
