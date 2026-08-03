"""Tests for WebSocket price endpoint."""
import pytest
from app.middleware.auth import create_access_token, verify_token


def test_token_creation():
    """Verify JWT tokens can be created and verified."""
    token = create_access_token(data={"sub": "test_user", "role": "user"})
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test_user"
    assert payload["role"] == "user"


def test_token_rejection():
    """Verify invalid tokens are rejected."""
    payload = verify_token("invalid_token")
    assert payload is None


def test_ticker_validation():
    """Verify ticker validation in WebSocket module."""
    from app.api.ws import validate_ticker

    assert validate_ticker("AAPL") is True
    assert validate_ticker("MSFT") is True
    assert validate_ticker("GOOGL") is True
    assert validate_ticker("a") is True
    assert validate_ticker("ABCDE") is True
    assert validate_ticker("") is False
    assert validate_ticker("AAPLXX") is False  # 6 chars
    assert validate_ticker("AAP!") is False  # special char
    assert validate_ticker(None) is False
    assert validate_ticker(123) is False
