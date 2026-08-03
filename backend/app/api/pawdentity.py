"""Pawdentity — unified identity / single sign-on for the Miau ecosystem.

One login, one HttpOnly cookie (`pawd_session`) shared across all apps
(terminal, frontend, education, ecosystem) via same-origin `/api` proxying.
API clients/SDKs can still use the Bearer token returned by `/login`.
"""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config import settings
from app.database import async_session
from app.middleware.auth.base import authenticate_db_user, create_access_token, verify_token

router = APIRouter(prefix="/api/v1/pawdentity", tags=["Pawdentity"])

COOKIE_NAME = "pawd_session"

# Simple in-memory rate limit (5 attempts / 60s per IP)
_login_attempts: dict[str, list[float]] = defaultdict(list)
LOGIN_RATE_LIMIT = 5
LOGIN_WINDOW = 60


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    authenticated: bool
    username: Optional[str] = None
    role: Optional[str] = None
    expires_in: Optional[int] = None
    access_token: Optional[str] = None
    detail: Optional[str] = None


class SessionInfo(BaseModel):
    authenticated: bool
    username: Optional[str] = None
    role: Optional[str] = None


class LogoutResponse(BaseModel):
    authenticated: bool = False


class ServiceInfo(BaseModel):
    service: str
    version: str
    issuer: str
    apps: list[str]


def _rate_limited(ip: str) -> bool:
    now = time.monotonic()
    _login_attempts[ip] = [t for t in _login_attempts[ip] if now - t < LOGIN_WINDOW]
    if len(_login_attempts[ip]) >= LOGIN_RATE_LIMIT:
        return True
    return False


def _record_attempt(ip: str) -> None:
    _login_attempts[ip].append(time.monotonic())


@router.post("/login", response_model=LoginResponse)
async def pawdentity_login(body: LoginRequest, request: Request) -> JSONResponse:
    client_ip = request.client.host if request.client else "unknown"
    if _rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"authenticated": False, "detail": "Too many login attempts. Try again in 60 seconds."},
        )

    db_user = None
    try:
        async with async_session() as db:
            db_user = await authenticate_db_user(body.username, body.password, db)
    except Exception:
        db_user = None

    if not db_user:
        _record_attempt(client_ip)
        return JSONResponse(
            status_code=401,
            content={"authenticated": False, "detail": "Incorrect username or password"},
        )

    role = db_user.get("role", "user")
    username = db_user.get("username", body.username)
    token = create_access_token(
        data={"sub": username, "role": role, "user_id": str(db_user.get("id", ""))}
    )
    max_age = settings.access_token_expire_minutes * 60
    response = JSONResponse(
        content={
            "authenticated": True,
            "username": username,
            "role": role,
            "expires_in": max_age,
            "access_token": token,
        }
    )
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/session", response_model=SessionInfo)
async def pawdentity_session(request: Request) -> SessionInfo:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        payload = verify_token(token)
        if payload:
            return SessionInfo(
                authenticated=True,
                username=payload.get("sub"),
                role=payload.get("role"),
            )
    return SessionInfo(authenticated=False)


@router.post("/logout", response_model=LogoutResponse)
async def pawdentity_logout() -> JSONResponse:
    response = JSONResponse(content={"authenticated": False})
    response.delete_cookie(COOKIE_NAME, path="/")
    return response


@router.get("/", response_model=ServiceInfo)
async def pawdentity_info() -> ServiceInfo:
    return ServiceInfo(
        service="pawdentity",
        version="1.0",
        issuer="miau-finance",
        apps=["terminal", "frontend", "education", "ecosystem"],
    )
