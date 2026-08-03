"""🐾 PAWDENTITY NOTE: This is the legacy OAuth2/OIDC SSO bridge for
enterprise providers (Azure AD, Okta, Google). For first-party Miau Finance
apps, use /api/v1/pawdentity/* (cookie-based SSO) instead. This module
will be extracted into a plugin in a future release.
"""
import json
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from urllib.parse import urlencode

import httpx

logger = logging.getLogger(__name__)


class SSOProvider(str, Enum):
    google = "google"
    github = "github"
    microsoft = "microsoft"


SSO_SCOPES: dict[SSOProvider, list[str]] = {
    SSOProvider.google: ["openid", "email", "profile"],
    SSOProvider.github: ["read:user", "user:email"],
    SSOProvider.microsoft: ["openid", "email", "profile", "User.Read"],
}

SSO_ENDPOINTS: dict[SSOProvider, dict[str, str]] = {
    SSOProvider.google: {
        "authorize": "https://accounts.google.com/o/oauth2/v2/auth",
        "token": "https://oauth2.googleapis.com/token",
        "userinfo": "https://openidconnect.googleapis.com/v1/userinfo",
    },
    SSOProvider.github: {
        "authorize": "https://github.com/login/oauth/authorize",
        "token": "https://github.com/login/oauth/access_token",
        "userinfo": "https://api.github.com/user",
    },
    SSOProvider.microsoft: {
        "authorize": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo": "https://graph.microsoft.com/v1.0/me",
    },
}


@dataclass
class SSOProviderConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: list[str] = field(default_factory=list)
    authorize_url: str = ""
    token_url: str = ""
    userinfo_url: str = ""

    def __post_init__(self):
        if not self.scopes:
            self.scopes = ["openid", "email", "profile"]


@dataclass
class SSOTokenResponse:
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    raw: dict = field(default_factory=dict)


@dataclass
class SSOUserInfo:
    sub: str
    email: str
    name: str
    provider: SSOProvider
    avatar_url: Optional[str] = None
    raw: dict = field(default_factory=dict)


def _env_key(provider: SSOProvider, key: str) -> str:
    prefix = provider.value.upper()
    return f"SSO_{prefix}_{key}"


def load_provider_config(provider: SSOProvider, redirect_uri: Optional[str] = None) -> Optional[SSOProviderConfig]:
    client_id = os.getenv(_env_key(provider, "CLIENT_ID"), "")
    client_secret = os.getenv(_env_key(provider, "CLIENT_SECRET"), "")
    if not client_id or not client_secret:
        return None

    endpoints = SSO_ENDPOINTS.get(provider, {})
    return SSOProviderConfig(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri or os.getenv(_env_key(provider, "REDIRECT_URI"), ""),
        scopes=os.getenv(_env_key(provider, "SCOPES"), ",".join(SSO_SCOPES.get(provider, []))).split(","),
        authorize_url=endpoints.get("authorize", ""),
        token_url=endpoints.get("token", ""),
        userinfo_url=endpoints.get("userinfo", ""),
    )


def load_all_providers(redirect_uri_template: Optional[str] = None) -> dict[SSOProvider, SSOProviderConfig]:
    providers: dict[SSOProvider, SSOProviderConfig] = {}
    for provider in SSOProvider:
        uri = None
        if redirect_uri_template:
            uri = redirect_uri_template.format(provider=provider.value)
        config = load_provider_config(provider, redirect_uri=uri)
        if config:
            providers[provider] = config
    return providers


def get_authorization_url(provider: SSOProvider, config: SSOProviderConfig, state: str) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": " ".join(config.scopes),
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    return f"{config.authorize_url}?{urlencode(params)}"


async def exchange_code(provider: SSOProvider, config: SSOProviderConfig, code: str) -> SSOTokenResponse:
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
        "grant_type": "authorization_code",
    }
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(config.token_url, data=data, headers=headers, timeout=30)
        resp.raise_for_status()
        body = resp.json()

    return SSOTokenResponse(
        access_token=body.get("access_token", ""),
        token_type=body.get("token_type", "bearer"),
        expires_in=body.get("expires_in", 3600),
        refresh_token=body.get("refresh_token"),
        id_token=body.get("id_token"),
        raw=body,
    )


async def get_user_info(provider: SSOProvider, access_token: str) -> Optional[SSOUserInfo]:
    endpoints = SSO_ENDPOINTS.get(provider)
    if not endpoints:
        return None
    userinfo_url = endpoints["userinfo"]

    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    if provider == SSOProvider.github:
        headers["User-Agent"] = "MiauFinance/1.0"
        headers["X-GitHub-Api-Version"] = "2022-11-28"

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(userinfo_url, headers=headers, timeout=30)
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            logger.warning("SSO userinfo failed for %s: %s", provider.value, e)
            return None

    return _parse_user_info(provider, body)


def _parse_user_info(provider: SSOProvider, body: dict) -> Optional[SSOUserInfo]:
    try:
        if provider == SSOProvider.google:
            return SSOUserInfo(
                sub=body.get("sub", ""),
                email=body.get("email", ""),
                name=body.get("name", ""),
                provider=provider,
                avatar_url=body.get("picture"),
                raw=body,
            )
        elif provider == SSOProvider.github:
            return SSOUserInfo(
                sub=str(body.get("id", "")),
                email=body.get("email", "") or "",
                name=body.get("name") or body.get("login", ""),
                provider=provider,
                avatar_url=body.get("avatar_url"),
                raw=body,
            )
        elif provider == SSOProvider.microsoft:
            return SSOUserInfo(
                sub=body.get("id", "") or body.get("sub", ""),
                email=body.get("mail") or body.get("userPrincipalName", ""),
                name=body.get("displayName", ""),
                provider=provider,
                raw=body,
            )
    except Exception as e:
        logger.warning("Failed to parse SSO user info for %s: %s", provider.value, e)
    return None


async def refresh_access_token(provider: SSOProvider, config: SSOProviderConfig, refresh_token: str) -> Optional[SSOTokenResponse]:
    data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(config.token_url, data=data, headers=headers, timeout=30)
            resp.raise_for_status()
            body = resp.json()
        except Exception as e:
            logger.warning("SSO token refresh failed for %s: %s", provider.value, e)
            return None

    return SSOTokenResponse(
        access_token=body.get("access_token", ""),
        token_type=body.get("token_type", "bearer"),
        expires_in=body.get("expires_in", 3600),
        refresh_token=body.get("refresh_token", refresh_token),
        id_token=body.get("id_token"),
        raw=body,
    )
