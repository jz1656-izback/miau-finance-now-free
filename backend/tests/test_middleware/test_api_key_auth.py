import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.middleware.api_key_auth import generate_api_key, hash_api_key, hash_api_key, authenticate_api_key


class TestGenerateApiKey:
    def test_key_format(self):
        raw, prefix, key_hash = generate_api_key()
        assert raw.startswith("miau_")
        assert len(raw) > 40
        assert len(prefix) == 8
        assert len(key_hash) == 64  # SHA-256 hex

    def test_key_uniqueness(self):
        keys = {generate_api_key()[0] for _ in range(10)}
        assert len(keys) == 10

    def test_hash_consistency(self):
        raw, _, _ = generate_api_key()
        h1 = hash_api_key(raw)
        h2 = hash_api_key(raw)
        assert h1 == h2


class TestHashApiKey:
    def test_different_keys_produce_different_hashes(self):
        h1 = hash_api_key("miau_test_key_alpha_0123456789")
        h2 = hash_api_key("miau_test_key_beta_0123456789")
        assert h1 != h2

    def test_same_key_produces_same_hash(self):
        raw = "miau_consistent_test_key_0123456"
        assert hash_api_key(raw) == hash_api_key(raw)
