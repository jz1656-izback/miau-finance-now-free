"""Tests for the globe layer API endpoints — runs against the live backend."""
import os
import pytest
import httpx

BASE = "http://localhost:8000/api/v1/datavore/globe/layer"
BATCH = "http://localhost:8000/api/v1/datavore/globe/batch"

# Credentials come from env — never hardcode (V7-001.5 / C1 backdoor removed)
AUTH_USER = os.getenv("MIAU_TEST_USER", "admin")
AUTH_PASS = os.getenv("MIAU_TEST_PASS", "")

# Get auth token once for all tests
AUTH_TOKEN = httpx.post(
    "http://localhost:8000/api/v1/auth/token",
    json={"username": AUTH_USER, "password": AUTH_PASS},
    timeout=5,
).json().get("access_token", "")
HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}

LAYERS_TO_TEST = [
    ("mining", "mines", [("name", str), ("lat", float), ("lng", float), ("commodity", str), ("country", str), ("owner", str)]),
    ("conflicts", "conflicts", [("name", str), ("lat", float), ("lng", float), ("type", str), ("region", str), ("intensity", str)]),
    ("ufo", "sightings", [("location", str), ("lat", float), ("lng", float)]),
    ("ancient_sites", "sites", [("name", str), ("lat", float), ("lng", float)]),
    ("oil_fields", "fields", [("name", str), ("lat", float), ("lng", float), ("type", str)]),
    ("renewable", "installations", [("name", str), ("lat", float), ("lng", float), ("type", str)]),
]


@pytest.mark.parametrize("layer_name,key,checks", LAYERS_TO_TEST)
def test_layer_data_structure(layer_name, key, checks):
    """Verify each layer endpoint returns data with correct field types."""
    r = httpx.get(f"{BASE}/{layer_name}", headers=HEADERS, timeout=10)
    assert r.status_code == 200, f"{layer_name} returned {r.status_code}"
    data = r.json()
    assert key in data, f"Missing key '{key}' in response"
    items = data[key]
    assert isinstance(items, list), f"{key} is not a list"
    assert len(items) > 0, f"{key} is empty"
    # Check first item's fields
    for field, expected_type in checks:
        assert field in items[0], f"Missing field '{field}'"
        assert isinstance(items[0][field], expected_type), \
            f"Field '{field}' is {type(items[0][field])}, expected {expected_type}"
    # Valid coordinates
    for item in items:
        assert -90 <= item["lat"] <= 90, f"{item.get('name','?')} lat={item['lat']}"
        assert -180 <= item["lng"] <= 180, f"{item.get('name','?')} lng={item['lng']}"


def test_batch_endpoint():
    r = httpx.get(f"{BATCH}?layers=mining,conflicts,ufo", headers=HEADERS, timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert "layers" in data
    for layer in ["mining", "conflicts"]:
        assert layer in data["layers"]


def test_unknown_layer():
    r = httpx.get(f"{BASE}/nonexistent_xyz", headers=HEADERS, timeout=10)
    data = r.json()
    assert "error" in data
    assert "not found" in data["error"].lower()


def test_layer_types_unique():
    """Check all layer names are unique."""
    names = [l[0] for l in LAYERS_TO_TEST]
    assert len(names) == len(set(names))
