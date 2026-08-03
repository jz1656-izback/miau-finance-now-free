"""Cargo route provider — major air freight routes with hub locations."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

CARGO_HUBS: list[dict[str, Any]] = [
    {"name":"FedEx Memphis","lat":35.042,"lng":-89.977,"carrier":"FedEx","throughput_year":5000000,"type":"hub"},
    {"name":"FedEx Anchorage","lat":61.174,"lng":-149.996,"carrier":"FedEx","throughput_year":2500000,"type":"hub"},
    {"name":"UPS Louisville","lat":38.174,"lng":-85.736,"carrier":"UPS","throughput_year":6000000,"type":"hub"},
    {"name":"UPS Cologne","lat":50.900,"lng":7.140,"carrier":"UPS","throughput_year":2000000,"type":"hub"},
    {"name":"DHL Leipzig","lat":51.424,"lng":12.236,"carrier":"DHL","throughput_year":4000000,"type":"hub"},
    {"name":"DHL Cincinnati","lat":39.049,"lng":-84.668,"carrier":"DHL","throughput_year":3000000,"type":"hub"},
    {"name":"DHL Hong Kong","lat":22.308,"lng":113.915,"carrier":"DHL","throughput_year":3500000,"type":"hub"},
    {"name":"FedEx Dubai","lat":25.253,"lng":55.366,"carrier":"FedEx","throughput_year":1800000,"type":"hub"},
    {"name":"FedEx Guangzhou","lat":23.392,"lng":113.299,"carrier":"FedEx","throughput_year":2200000,"type":"hub"},
    {"name":"UPS Shanghai","lat":31.144,"lng":121.808,"carrier":"UPS","throughput_year":1500000,"type":"hub"},
]

CARGO_ROUTES: list[dict[str, Any]] = [
    {"from":"FedEx Memphis","to":"FedEx Anchorage","carrier":"FedEx","daily_flights":12,"distance_km":5180},
    {"from":"FedEx Memphis","to":"FedEx Dubai","carrier":"FedEx","daily_flights":4,"distance_km":11360},
    {"from":"FedEx Memphis","to":"FedEx Guangzhou","carrier":"FedEx","daily_flights":3,"distance_km":12500},
    {"from":"FedEx Anchorage","to":"FedEx Guangzhou","carrier":"FedEx","daily_flights":8,"distance_km":6000},
    {"from":"FedEx Anchorage","to":"FedEx Dubai","carrier":"FedEx","daily_flights":5,"distance_km":8970},
    {"from":"UPS Louisville","to":"UPS Cologne","carrier":"UPS","daily_flights":10,"distance_km":7050},
    {"from":"UPS Louisville","to":"UPS Shanghai","carrier":"UPS","daily_flights":6,"distance_km":12000},
    {"from":"UPS Cologne","to":"UPS Shanghai","carrier":"UPS","daily_flights":5,"distance_km":8200},
    {"from":"UPS Louisville","to":"UPS Cologne","carrier":"UPS","daily_flights":12,"distance_km":7050},
    {"from":"DHL Leipzig","to":"DHL Cincinnati","carrier":"DHL","daily_flights":8,"distance_km":7070},
    {"from":"DHL Leipzig","to":"DHL Hong Kong","carrier":"DHL","daily_flights":7,"distance_km":8600},
    {"from":"DHL Cincinnati","to":"DHL Hong Kong","carrier":"DHL","daily_flights":5,"distance_km":12800},
    {"from":"DHL Leipzig","to":"DHL Hong Kong","carrier":"DHL","daily_flights":7,"distance_km":8600},
    {"from":"DHL Cincinnati","to":"DHL Hong Kong","carrier":"DHL","daily_flights":5,"distance_km":12800},
    {"from":"FedEx Dubai","to":"FedEx Guangzhou","carrier":"FedEx","daily_flights":9,"distance_km":6100},
    {"from":"DHL Hong Kong","to":"DHL Cincinnati","carrier":"DHL","daily_flights":5,"distance_km":12800},
    {"from":"UPS Shanghai","to":"UPS Cologne","carrier":"UPS","daily_flights":6,"distance_km":8200},
    {"from":"FedEx Guangzhou","to":"FedEx Memphis","carrier":"FedEx","daily_flights":3,"distance_km":12500},
]


class CargoDataSource(DataSource):
    @property
    def name(self) -> str: return "cargo"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["cargo"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"hubs": CARGO_HUBS, "routes": CARGO_ROUTES}

    def fetch_cargo_hubs(self) -> list[dict[str, Any]]:
        return CARGO_HUBS

    def fetch_cargo_routes(self) -> list[dict[str, Any]]:
        return CARGO_ROUTES


data_source = CargoDataSource()
