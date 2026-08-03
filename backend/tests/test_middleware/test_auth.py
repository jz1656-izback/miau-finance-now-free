import pytest
import time
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from jose import jwt
from fastapi import HTTPException
from app.config import settings


_JWT_AUD = "miau-finance-api"


class TestCreateAccessToken:
    def test_creates_valid_jwt(self):
        from app.middleware.auth import create_access_token

        token = create_access_token(data={"sub": "testuser", "role": "user"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm], audience=_JWT_AUD)
        assert payload["sub"] == "testuser"
        assert payload["role"] == "user"
        assert "exp" in payload
        assert "iat" in payload
        assert payload["iss"] == "miau-finance"
        assert payload["aud"] == _JWT_AUD

    def test_uses_custom_expiry(self):
        from app.middleware.auth import create_access_token

        token = create_access_token(data={"sub": "test"}, expires_delta=timedelta(seconds=5))
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm], audience=_JWT_AUD)
        exp = payload["exp"]
        expected = (datetime.now(timezone.utc) + timedelta(seconds=5)).timestamp()
        assert abs(exp - expected) < 2

    def test_includes_custom_claims(self):
        from app.middleware.auth import create_access_token

        token = create_access_token(data={"sub": "user1", "user_id": "abc123", "role": "admin"})
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm], audience=_JWT_AUD)
        assert payload["user_id"] == "abc123"
        assert payload["role"] == "admin"


class TestVerifyToken:
    def test_returns_payload_for_valid_token(self):
        from app.middleware.auth import create_access_token, verify_token

        token = create_access_token(data={"sub": "testuser"})
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"

    def test_returns_none_for_expired_token(self):
        from app.middleware.auth import create_access_token, verify_token

        token = create_access_token(data={"sub": "test"}, expires_delta=timedelta(seconds=-1))
        payload = verify_token(token)
        assert payload is None

    def test_returns_none_for_malformed_token(self):
        from app.middleware.auth import verify_token

        payload = verify_token("not.a.token")
        assert payload is None

    def test_returns_none_for_tampered_token(self):
        from app.middleware.auth import create_access_token, verify_token

        token = create_access_token(data={"sub": "test"})
        tampered = token[:-5] + "XXXXX"
        payload = verify_token(tampered)
        assert payload is None


class TestGetCurrentUser:
    @pytest.fixture
    def mock_request(self):
        req = MagicMock()
        req.cookies = {}
        return req

    @pytest.mark.anyio
    async def test_valid_token_returns_payload(self, mock_request):
        from app.middleware.auth import create_access_token, get_current_user

        token = create_access_token(data={"sub": "validuser", "role": "user"})
        mock_creds = MagicMock()
        mock_creds.credentials = token
        user = await get_current_user(request=mock_request, credentials=mock_creds)
        assert user["sub"] == "validuser"
        assert user["role"] == "user"

    @pytest.mark.anyio
    async def test_missing_credentials_raises_401(self, mock_request):
        from app.middleware.auth import get_current_user

        with pytest.raises(HTTPException) as exc:
            await get_current_user(request=mock_request, credentials=None)
        assert exc.value.status_code == 401
        assert "Not authenticated" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_invalid_token_raises_401(self, mock_request):
        from app.middleware.auth import get_current_user

        mock_creds = MagicMock()
        mock_creds.credentials = "invalid.token.here"
        with pytest.raises(HTTPException) as exc:
            await get_current_user(request=mock_request, credentials=mock_creds)
        assert exc.value.status_code == 401
        assert "Invalid or expired token" in str(exc.value.detail)


class TestOptionalUser:
    @pytest.fixture
    def mock_request(self):
        req = MagicMock()
        req.cookies = {}
        return req

    @pytest.mark.anyio
    async def test_without_credentials_returns_none(self, mock_request):
        from app.middleware.auth import optional_user

        result = await optional_user(request=mock_request, credentials=None)
        assert result is None

    @pytest.mark.anyio
    async def test_with_valid_credentials_returns_payload(self, mock_request):
        from app.middleware.auth import create_access_token, optional_user

        token = create_access_token(data={"sub": "test"})
        mock_creds = MagicMock()
        mock_creds.credentials = token
        result = await optional_user(request=mock_request, credentials=mock_creds)
        assert result is not None
        assert result["sub"] == "test"


class TestValidateUser:
    def test_valid_credentials(self):
        from app.middleware.auth import validate_user

        assert validate_user(settings.demo_username, settings.demo_password) is True

    def test_invalid_username(self):
        from app.middleware.auth import validate_user

        assert validate_user("wronguser", settings.demo_password) is False

    def test_invalid_password(self):
        from app.middleware.auth import validate_user

        assert validate_user(settings.demo_username, "wrongpass") is False

    def test_empty_credentials(self):
        from app.middleware.auth import validate_user

        assert validate_user("", "") is False


class TestLoginEndpoint:
    """Tests for login_for_access_token (no demo fallback — V7-001/C1 removed it)."""

    @pytest.fixture
    def mock_request(self):
        """Minimal request with a client IP for rate limiting."""
        req = MagicMock()
        req.client.host = "127.0.0.1"
        return req

    @staticmethod
    def _patch_auth():
        """Patch authenticate_db_user at the defining module (base.py)."""
        import app.middleware.auth.base as auth_base_mod
        return patch.object(auth_base_mod, 'authenticate_db_user')

    @pytest.mark.anyio
    async def test_login_with_valid_credentials_returns_token(self, mock_request):
        from app.middleware.auth import login_for_access_token, TokenRequest

        with self._patch_auth() as mock_auth:
            mock_auth.return_value = {"id": "1", "role": "user", "username": settings.demo_username}
            form = TokenRequest(username=settings.demo_username, password=settings.demo_password)
            resp = await login_for_access_token(form_data=form, request=mock_request)
            assert resp.access_token is not None
            assert resp.token_type == "bearer"

            payload = jwt.decode(resp.access_token, settings.secret_key, algorithms=[settings.jwt_algorithm], audience="miau-finance-api")
            assert payload["sub"] == settings.demo_username
            assert payload["role"] == "user"

    @pytest.mark.anyio
    async def test_login_with_invalid_credentials_raises_401(self, mock_request):
        from app.middleware.auth import login_for_access_token, TokenRequest

        with self._patch_auth() as mock_auth:
            mock_auth.return_value = None
            form = TokenRequest(username="wrong", password="wrong")
            with pytest.raises(HTTPException) as exc:
                await login_for_access_token(form_data=form, request=mock_request)
            assert exc.value.status_code == 401
            assert "Incorrect username or password" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_login_handles_db_failure_gracefully(self, mock_request):
        """🔒 SECURITY (V7-001/C1): DB failure MUST NOT fall back to any user.
        Returns 401 — no demo bypass, no silent pass-through."""
        from app.middleware.auth import login_for_access_token, TokenRequest

        with self._patch_auth() as mock_auth:
            mock_auth.side_effect = Exception("DB down")
            form = TokenRequest(username=settings.demo_username, password=settings.demo_password)
            with pytest.raises(HTTPException) as exc:
                await login_for_access_token(form_data=form, request=mock_request)
            assert exc.value.status_code == 401
            assert "Incorrect username or password" in str(exc.value.detail)

    @pytest.mark.anyio
    async def test_login_uses_db_role_when_available(self, mock_request):
        from app.middleware.auth import login_for_access_token, TokenRequest

        with self._patch_auth() as mock_auth:
            mock_auth.return_value = {"id": "42", "role": "admin", "username": settings.demo_username}
            form = TokenRequest(username=settings.demo_username, password=settings.demo_password)
            resp = await login_for_access_token(form_data=form, request=mock_request)
        payload = jwt.decode(resp.access_token, settings.secret_key, algorithms=[settings.jwt_algorithm], audience="miau-finance-api")
        assert payload["role"] == "admin"
        assert payload["user_id"] == "42"
