"""Tests for international broker connectors."""
import pytest
from app.services.brokers.registry import list_brokers, get_broker


def test_intl_brokers_registered():
    brokers = {b.name: b for b in list_brokers()}
    for name in ["degiro", "rakuten", "zerodha", "saxo", "ibkr"]:
        assert name in brokers, f"{name} not registered"


def test_intl_broker_imports():
    from app.services.brokers.degiro import DegiroBroker
    from app.services.brokers.rakuten import RakutenBroker
    from app.services.brokers.zerodha import ZerodhaBroker
    assert DegiroBroker.display_name == "DEGIRO"
    assert RakutenBroker.display_name == "Rakuten Securities"
    assert ZerodhaBroker.display_name == "Zerodha Kite"
