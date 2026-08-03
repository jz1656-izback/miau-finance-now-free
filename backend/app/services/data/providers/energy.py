"""Energy data provider — oil & gas fields, renewable energy installations."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

OIL_FIELDS: list[dict[str, Any]] = [
    {"name":"Ghawar","country":"Saudi Arabia","lat":25.400,"lng":49.600,"type":"Oil Field","daily_bbl":3800000},
    {"name":"Burgan","country":"Kuwait","lat":29.083,"lng":48.000,"type":"Oil Field","daily_bbl":1700000},
    {"name":"Ahvaz","country":"Iran","lat":31.317,"lng":48.667,"type":"Oil Field","daily_bbl":1500000},
    {"name":"Upper Zakum","country":"UAE","lat":24.750,"lng":53.500,"type":"Oil Field","daily_bbl":1100000},
    {"name":"Cantarell","country":"Mexico","lat":19.167,"lng":-91.000,"type":"Oil Field","daily_bbl":400000},
    {"name":"Kashagan","country":"Kazakhstan","lat":46.600,"lng":52.000,"type":"Oil Field","daily_bbl":400000},
    {"name":"Tengiz","country":"Kazakhstan","lat":46.200,"lng":53.500,"type":"Oil Field","daily_bbl":600000},
    {"name":"Safaniya","country":"Saudi Arabia","lat":27.500,"lng":49.500,"type":"Oil Field","daily_bbl":1200000},
    {"name":"Manifa","country":"Saudi Arabia","lat":27.700,"lng":50.000,"type":"Oil Field","daily_bbl":900000},
    {"name":"Zuluf","country":"Saudi Arabia","lat":27.500,"lng":49.800,"type":"Oil Field","daily_bbl":600000},
    {"name":"Shaybah","country":"Saudi Arabia","lat":22.000,"lng":54.000,"type":"Oil Field","daily_bbl":600000},
    {"name":"Rumaila","country":"Iraq","lat":30.333,"lng":47.667,"type":"Oil Field","daily_bbl":1400000},
    {"name":"West Qurna","country":"Iraq","lat":30.750,"lng":47.500,"type":"Oil Field","daily_bbl":600000},
    {"name":"Majnoon","country":"Iraq","lat":31.000,"lng":48.000,"type":"Oil Field","daily_bbl":400000},
    {"name":"Kirkuk","country":"Iraq","lat":35.467,"lng":44.333,"type":"Oil Field","daily_bbl":500000},
    {"name":"Daqing","country":"China","lat":46.600,"lng":125.000,"type":"Oil Field","daily_bbl":600000},
    {"name":"Samotlor","country":"Russia","lat":61.100,"lng":76.700,"type":"Oil Field","daily_bbl":500000},
    {"name":"Priobskoye","country":"Russia","lat":61.000,"lng":73.000,"type":"Oil Field","daily_bbl":700000},
    {"name":"Romashkino","country":"Russia","lat":54.800,"lng":52.500,"type":"Oil Field","daily_bbl":400000},
    {"name":"Sakhalin","country":"Russia","lat":52.000,"lng":143.000,"type":"Oil Field","daily_bbl":250000},
{"name":"Prudhoe Bay","country":"USA","lat":70.300,"lng":-148.500,"type":"Oil Field","daily_bbl":300000},
    {"name":"Permian Basin","country":"USA","lat":31.900,"lng":-102.900,"type":"Basin","daily_bbl":5600000},
    {"name":"Eagle Ford","country":"USA","lat":28.500,"lng":-98.500,"type":"Shale","daily_bbl":1200000},
    {"name":"Bakken","country":"USA","lat":47.500,"lng":-103.000,"type":"Shale","daily_bbl":1300000},
    {"name":"Marcellus","country":"USA","lat":40.000,"lng":-79.000,"type":"Shale Gas","daily_bbl_equiv":2000000},
    {"name":"Tupi","country":"Brazil","lat":-25.500,"lng":-42.500,"type":"Offshore","daily_bbl":1000000},
    {"name":"Búzios","country":"Brazil","lat":-26.000,"lng":-42.500,"type":"Offshore","daily_bbl":600000},
    {"name":"Mero","country":"Brazil","lat":-25.800,"lng":-43.000,"type":"Offshore","daily_bbl":400000},
    {"name":"Johan Sverdrup","country":"Norway","lat":59.000,"lng":2.500,"type":"Offshore","daily_bbl":750000},
    {"name":"Troll","country":"Norway","lat":60.600,"lng":3.700,"type":"Gas","daily_bbl_equiv":1200000},
    {"name":"Ormen Lange","country":"Norway","lat":63.000,"lng":5.000,"type":"Gas","daily_bbl_equiv":700000},
    {"name":"Groningen","country":"Netherlands","lat":53.000,"lng":6.800,"type":"Gas","daily_bbl_equiv":100000},
    {"name":"Hassi Messaoud","country":"Algeria","lat":31.700,"lng":6.000,"type":"Oil Field","daily_bbl":400000},
    {"name":"Zarzaitine","country":"Algeria","lat":28.000,"lng":9.000,"type":"Oil Field","daily_bbl":200000},
    {"name":"Egina","country":"Nigeria","lat":3.500,"lng":7.000,"type":"Offshore","daily_bbl":200000},
    {"name":"Bonga","country":"Nigeria","lat":4.000,"lng":5.000,"type":"Offshore","daily_bbl":200000},
    {"name":"Agbami","country":"Nigeria","lat":3.500,"lng":6.000,"type":"Offshore","daily_bbl":250000},
    {"name":"Azadegan","country":"Iran","lat":31.500,"lng":48.500,"type":"Oil Field","daily_bbl":400000},
    {"name":"Yadavaran","country":"Iran","lat":31.000,"lng":48.500,"type":"Oil Field","daily_bbl":200000},
    {"name":"South Pars","country":"Iran/Qatar","lat":26.500,"lng":52.000,"type":"Gas","daily_bbl_equiv":6000000},
    {"name":"North Field","country":"Qatar","lat":26.500,"lng":52.000,"type":"Gas","daily_bbl_equiv":5000000},
]

RENEWABLE: list[dict[str, Any]] = [
    {"name":"Three Gorges Dam","country":"China","lat":30.823,"lng":111.003,"type":"Hydro","capacity_mw":22500},
    {"name":"Itaipu Dam","country":"Brazil/Paraguay","lat":-25.408,"lng":-54.589,"type":"Hydro","capacity_mw":14000},
    {"name":"Guri Dam","country":"Venezuela","lat":7.783,"lng":-62.983,"type":"Hydro","capacity_mw":10235},
    {"name":"Tucuruí Dam","country":"Brazil","lat":-3.833,"lng":-49.650,"type":"Hydro","capacity_mw":8370},
    {"name":"Grand Coulee Dam","country":"USA","lat":47.956,"lng":-118.979,"type":"Hydro","capacity_mw":6809},
    {"name":"Xiluodu Dam","country":"China","lat":28.261,"lng":103.636,"type":"Hydro","capacity_mw":13860},
    {"name":"Baihetan Dam","country":"China","lat":27.250,"lng":102.867,"type":"Hydro","capacity_mw":16000},
    {"name":"Wudongde Dam","country":"China","lat":26.333,"lng":102.633,"type":"Hydro","capacity_mw":10240},
    {"name":"Gorges du Rhône","country":"France","lat":44.000,"lng":4.700,"type":"Hydro","capacity_mw":3000},
    {"name":"Jirau Dam","country":"Brazil","lat":-9.350,"lng":-64.717,"type":"Hydro","capacity_mw":3750},
    {"name":"Belo Monte Dam","country":"Brazil","lat":-3.117,"lng":-51.783,"type":"Hydro","capacity_mw":11233},
    {"name":"Tarbela Dam","country":"Pakistan","lat":34.083,"lng":72.683,"type":"Hydro","capacity_mw":4888},
    {"name":"Gansu Wind Farm","country":"China","lat":40.000,"lng":96.500,"type":"Wind","capacity_mw":7965},
    {"name":"Hornsea Wind","country":"UK","lat":53.800,"lng":1.500,"type":"Wind","capacity_mw":3600},
    {"name":"Dogger Bank Wind","country":"UK","lat":55.000,"lng":2.000,"type":"Wind","capacity_mw":3600},
    {"name":"Vestas HQ (Wind)","country":"Denmark","lat":56.150,"lng":8.150,"type":"Wind","capacity_mw":500},
    {"name":"Alta Wind Energy","country":"USA","lat":35.000,"lng":-118.300,"type":"Wind","capacity_mw":1550},
    {"name":"Shepherds Flat","country":"USA","lat":45.500,"lng":-120.000,"type":"Wind","capacity_mw":845},
    {"name":"London Array","country":"UK","lat":51.650,"lng":1.550,"type":"Wind","capacity_mw":630},
    {"name":"Jiuquan Wind","country":"China","lat":39.700,"lng":98.500,"type":"Wind","capacity_mw":10000},
    {"name":"Huanghe Hydropower","country":"China","lat":36.000,"lng":100.000,"type":"Wind","capacity_mw":2000},
    {"name":"Tengger Desert Solar","country":"China","lat":37.500,"lng":105.000,"type":"Solar","capacity_mw":1547},
    {"name":"Bhadla Solar","country":"India","lat":27.300,"lng":71.800,"type":"Solar","capacity_mw":2255},
    {"name":"Pavagada Solar","country":"India","lat":14.200,"lng":77.300,"type":"Solar","capacity_mw":2050},
    {"name":"Kurnool Solar","country":"India","lat":15.800,"lng":78.000,"type":"Solar","capacity_mw":1000},
    {"name":"Benban Solar","country":"Egypt","lat":24.500,"lng":32.900,"type":"Solar","capacity_mw":1650},
    {"name":"Noor Complex","country":"Morocco","lat":31.000,"lng":-4.000,"type":"Solar","capacity_mw":580},
    {"name":"Ivanpah Solar","country":"USA","lat":35.570,"lng":-115.470,"type":"Solar","capacity_mw":392},
    {"name":"Solar Star","country":"USA","lat":34.900,"lng":-118.400,"type":"Solar","capacity_mw":579},
    {"name":"Kamuthi Solar","country":"India","lat":9.500,"lng":78.500,"type":"Solar","capacity_mw":648},
    {"name":"Ica Solar","country":"Peru","lat":-14.000,"lng":-75.500,"type":"Solar","capacity_mw":440},
    {"name":"Flamanville","country":"France","lat":49.533,"lng":-1.883,"type":"Nuclear","capacity_mw":1650},
]


class EnergyDataSource(DataSource):
    @property
    def name(self) -> str: return "energy"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["oil_gas", "renewable"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — energy data source"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"oil_fields": OIL_FIELDS, "renewable": RENEWABLE}

    def fetch_oil_fields(self) -> list[dict[str, Any]]:
        return OIL_FIELDS

    def fetch_renewable(self) -> list[dict[str, Any]]:
        return RENEWABLE

    def fetch_geothermal(self) -> list[dict[str, Any]]:
        return [r for r in RENEWABLE if r["type"] == "Geothermal"]


data_source = EnergyDataSource()
