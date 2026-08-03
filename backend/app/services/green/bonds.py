"""Green bond tracker — yield vs traditional bonds comparison."""
import logging
from dataclasses import dataclass, asdict
from typing import Optional

logger = logging.getLogger(__name__)

GREEN_BOND_DATA = [
    {"isin": "XS1234567890", "name": "EU Green Bond 2026", "issuer": "European Union", "currency": "EUR", "coupon": 2.5, "maturity": "2026-12-15", "rating": "AAA", "use_of_proceeds": "renewable_energy"},
    {"isin": "XS2345678901", "name": "World Bank Green Bond 2028", "issuer": "World Bank", "currency": "USD", "coupon": 3.0, "maturity": "2028-06-30", "rating": "AAA", "use_of_proceeds": "climate_adaptation"},
    {"isin": "XS3456789012", "name": "Apple Green Bond 2029", "issuer": "Apple Inc.", "currency": "USD", "coupon": 2.8, "maturity": "2029-09-15", "rating": "AA+", "use_of_proceeds": "clean_energy"},
    {"isin": "XS4567890123", "name": "Enel Green Bond 2027", "issuer": "Enel SpA", "currency": "EUR", "coupon": 3.5, "maturity": "2027-03-20", "rating": "BBB+", "use_of_proceeds": "renewable_energy"},
    {"isin": "XS5678901234", "name": "Iberdrola Green Bond 2030", "issuer": "Iberdrola SA", "currency": "EUR", "coupon": 3.2, "maturity": "2030-11-01", "rating": "A-", "use_of_proceeds": "wind_energy"},
    {"isin": "XS6789012345", "name": "Toyota Green Bond 2028", "issuer": "Toyota Motor Corp", "currency": "JPY", "coupon": 1.8, "maturity": "2028-04-30", "rating": "AA", "use_of_proceeds": "hybrid_vehicles"},
    {"isin": "XS7890123456", "name": "BNP Paribas Green Bond 2027", "issuer": "BNP Paribas", "currency": "EUR", "coupon": 2.0, "maturity": "2027-08-15", "rating": "A+", "use_of_proceeds": "green_buildings"},
    {"isin": "XS8901234567", "name": "China Green Bond 2029", "issuer": "China Development Bank", "currency": "CNY", "coupon": 3.8, "maturity": "2029-01-20", "rating": "A", "use_of_proceeds": "renewable_energy"},
]

BENCHMARK_YIELDS = {
    "USD": 4.5, "EUR": 3.2, "GBP": 4.0, "JPY": 0.8, "CNY": 2.8,
}


def list_bonds(currency: Optional[str] = None) -> list[dict]:
    bonds = list(GREEN_BOND_DATA)
    if currency:
        bonds = [b for b in bonds if b["currency"] == currency.upper()]
    return bonds


def yield_comparison(bond: dict) -> dict:
    bench = BENCHMARK_YIELDS.get(bond["currency"], 3.0)
    spread = bond["coupon"] - bench
    return {
        "isin": bond["isin"],
        "name": bond["name"],
        "green_yield": bond["coupon"],
        "benchmark_yield": bench,
        "yield_spread": round(spread, 2),
        "currency": bond["currency"],
        "rating": bond["rating"],
    }
