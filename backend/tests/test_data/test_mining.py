"""Tests for the Mining & Resources data provider."""
import pytest
from app.services.data.providers.mining import MiningProvider, MAJOR_MINES, MAJOR_OIL_FIELDS, MAJOR_RENEWABLE


@pytest.fixture
def provider():
    return MiningProvider()


@pytest.mark.asyncio
async def test_provider_name(provider):
    assert provider.name == "mining"
    assert provider.requires_key is False
    assert provider.rate_limit_per_minute == 1000


@pytest.mark.asyncio
async def test_health(provider):
    healthy = await provider.health()
    assert healthy is True


def test_fetch_mines_count(provider):
    mines = provider.fetch_mines()
    expected = len(MAJOR_MINES) + len(MAJOR_OIL_FIELDS) + len(MAJOR_RENEWABLE)
    assert len(mines) == expected
    assert len(mines) > 0


def test_fetch_mines_structure(provider):
    mines = provider.fetch_mines()
    for mine in mines:
        assert "name" in mine
        assert "lat" in mine
        assert "lng" in mine
        assert "commodity" in mine
        assert "country" in mine
        assert "owner" in mine
        assert "production" in mine
        assert "type" in mine
        assert mine["type"] == "mine"


def test_mine_coordinates_valid(provider):
    mines = provider.fetch_mines()
    for mine in mines:
        assert -90 <= mine["lat"] <= 90, f"{mine['name']} lat={mine['lat']}"
        assert -180 <= mine["lng"] <= 180, f"{mine['name']} lng={mine['lng']}"


def test_all_commodities_covered(provider):
    mines = provider.fetch_mines()
    commodities = {m["commodity"] for m in mines}
    assert "Gold" in commodities or "Gold/Copper" in commodities
    assert "Oil" in commodities
    assert "Copper" in commodities
    assert "Iron Ore" in commodities


def test_major_mines_have_owners(provider):
    for mine in MAJOR_MINES:
        assert mine["owner"], f"{mine['name']} missing owner"
        assert mine["production"], f"{mine['name']} missing production"


def test_oil_fields_have_countries(provider):
    for field in MAJOR_OIL_FIELDS:
        assert field["country"], f"{field['name']} missing country"


def test_renewable_have_capacity(provider):
    for plant in MAJOR_RENEWABLE:
        assert "GW" in plant["production"] or "MW" in plant["production"]
