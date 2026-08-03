"""Satellite data provider — orbit positions, ISS tracker, Celestrak-style TLE data."""

import logging
import math
import time
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

# Major orbital satellites with Keplerian elements for position computation
SATELLITES: list[dict[str, Any]] = [
    {"name":"ISS","norad":25544,"apogee_km":420,"inclination":51.6,"period_min":92.68,"phase":0.0,"lon_asc":0.0,"country":"International","type":"Station","launch_year":1998},
    {"name":"HST","norad":20580,"apogee_km":540,"inclination":28.5,"period_min":95.4,"phase":1.2,"lon_asc":30.0,"country":"USA","type":"Telescope","launch_year":1990},
    {"name":"Tiangong","norad":54216,"apogee_km":390,"inclination":41.5,"period_min":92.2,"phase":3.4,"lon_asc":120.0,"country":"China","type":"Station","launch_year":2021},
    {"name":"Starlink-1001","norad":44235,"apogee_km":550,"inclination":53.0,"period_min":95.6,"phase":5.1,"lon_asc":10.0,"country":"USA","type":"Comms","launch_year":2019},
    {"name":"Iridium-1","norad":24793,"apogee_km":780,"inclination":86.4,"period_min":100.4,"phase":0.8,"lon_asc":60.0,"country":"USA","type":"Comms","launch_year":1997},
    {"name":"GPS-BIIR-2","norad":24876,"apogee_km":20200,"inclination":55.0,"period_min":718.0,"phase":2.3,"lon_asc":180.0,"country":"USA","type":"Navigation","launch_year":1997},
    {"name":"Glonass-735","norad":32393,"apogee_km":19130,"inclination":64.8,"period_min":675.0,"phase":4.1,"lon_asc":270.0,"country":"Russia","type":"Navigation","launch_year":2007},
    {"name":"BeiDou-3M1","norad":43001,"apogee_km":21528,"inclination":55.0,"period_min":775.0,"phase":1.5,"lon_asc":90.0,"country":"China","type":"Navigation","launch_year":2018},
    {"name":"Galileo-1","norad":29499,"apogee_km":23222,"inclination":56.0,"period_min":810.0,"phase":0.6,"lon_asc":150.0,"country":"EU","type":"Navigation","launch_year":2005},
    {"name":"GOES-16","norad":41866,"apogee_km":35786,"inclination":0.0,"period_min":1436.0,"phase":0.0,"lon_asc":-75.0,"country":"USA","type":"Weather","launch_year":2016},
    {"name":"Meteosat-11","norad":42900,"apogee_km":35786,"inclination":0.0,"period_min":1436.0,"phase":0.0,"lon_asc":0.0,"country":"EUMETSAT","type":"Weather","launch_year":2015},
    {"name":"Himawari-8","norad":41567,"apogee_km":35786,"inclination":0.0,"period_min":1436.0,"phase":0.0,"lon_asc":140.0,"country":"Japan","type":"Weather","launch_year":2014},
    {"name":"Landsat-8","norad":39084,"apogee_km":705,"inclination":98.2,"period_min":98.8,"phase":2.9,"lon_asc":190.0,"country":"USA","type":"Earth Observation","launch_year":2013},
    {"name":"Sentinel-2A","norad":40697,"apogee_km":786,"inclination":98.5,"period_min":100.3,"phase":5.7,"lon_asc":220.0,"country":"EU","type":"Earth Observation","launch_year":2015},
    {"name":"Cubesat-1","norad":42000,"apogee_km":400,"inclination":51.6,"period_min":92.5,"phase":6.0,"lon_asc":45.0,"country":"USA","type":"Cubesat","launch_year":2016},
    {"name":"KH-11","norad":26000,"apogee_km":270,"inclination":97.9,"period_min":90.5,"phase":1.8,"lon_asc":200.0,"country":"USA","type":"Reconnaissance","launch_year":2000},
    {"name":"Cosmos-2555","norad":53000,"apogee_km":350,"inclination":67.1,"period_min":91.5,"phase":3.2,"lon_asc":320.0,"country":"Russia","type":"Reconnaissance","launch_year":2022},
]


def compute_orbital_position_ms(epoch_ms: int, period_min: float, inclination_deg: float, phase_deg: float, lon_asc_deg: float) -> tuple[float, float]:
    """Compute lat/lng for a satellite at a given epoch using simplified Keplerian model."""
    t = (epoch_ms % (period_min * 60 * 1000)) / (period_min * 60 * 1000)
    inc = inclination_deg * math.pi / 180
    lat = math.asin(math.sin(inc) * math.sin(t * 2 * math.pi + phase_deg * math.pi / 180)) * 180 / math.pi
    d_lng = (t + phase_deg / 360) * 360 - 180 + lon_asc_deg
    lng = ((d_lng + 180) % 360) - 180
    return (round(lat, 2), round(lng, 2))


class SatelliteDataSource(DataSource):
    @property
    def name(self) -> str: return "celestrak"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["satellites", "iss"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — satellite data source"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"satellites": self.fetch_globe_satellites()}

    def fetch_globe_satellites(self) -> list[dict[str, Any]]:
        now = int(time.time() * 1000)
        results = []
        for s in SATELLITES:
            lat, lng = compute_orbital_position_ms(now, s["period_min"], s["inclination"], s["phase"], s["lon_asc"])
            results.append({
                "name": s["name"], "norad": s["norad"],
                "lat": lat, "lng": lng,
                "type": s["type"], "country": s["country"],
                "altitude_km": s["apogee_km"],
                "period_min": s["period_min"],
            })
        return results

    def fetch_iss_position(self) -> dict[str, Any]:
        now = int(time.time() * 1000)
        iss = next(s for s in SATELLITES if s["name"] == "ISS")
        lat, lng = compute_orbital_position_ms(now, iss["period_min"], iss["inclination"], iss["phase"], iss["lon_asc"])
        return {"name": "ISS", "norad": 25544, "lat": lat, "lng": lng, "altitude_km": 420, "crew": 7, "speed_km_s": 7.66}


data_source = SatelliteDataSource()
