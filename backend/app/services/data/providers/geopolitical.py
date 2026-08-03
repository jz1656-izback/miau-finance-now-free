"""Geopolitical data provider — military bases, nuclear facilities, defense spending."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

MILITARY_BASES: list[dict[str, Any]] = [
    {"name":"Pentagon","country":"USA","lat":38.871,"lng":-77.056,"branch":"Joint","personnel":23000},
    {"name":"Fort Liberty","country":"USA","lat":35.138,"lng":-78.999,"branch":"Army","personnel":52000},
    {"name":"Fort Cavazos","country":"USA","lat":31.139,"lng":-97.762,"branch":"Army","personnel":45000},
    {"name":"Fort Campbell","country":"USA","lat":36.652,"lng":-87.459,"branch":"Army","personnel":30000},
    {"name":"Camp Humphreys","country":"South Korea","lat":36.963,"lng":127.018,"branch":"Army","personnel":28500},
    {"name":"Naval Base Norfolk","country":"USA","lat":36.947,"lng":-76.317,"branch":"Navy","personnel":60000},
    {"name":"Naval Base San Diego","country":"USA","lat":32.682,"lng":-117.119,"branch":"Navy","personnel":35000},
    {"name":"NAS Pensacola","country":"USA","lat":30.355,"lng":-87.317,"branch":"Navy","personnel":16000},
    {"name":"Andersen AFB","country":"Guam","lat":13.584,"lng":144.928,"branch":"Air Force","personnel":9000},
    {"name":"RAF Lakenheath","country":"UK","lat":52.409,"lng":0.561,"branch":"Air Force","personnel":8000},
    {"name":"Ramstein AB","country":"Germany","lat":49.437,"lng":7.600,"branch":"Air Force","personnel":16000},
    {"name":"Camp Lemonnier","country":"Djibouti","lat":11.545,"lng":43.145,"branch":"Navy","personnel":4000},
    {"name":"MCAS Iwakuni","country":"Japan","lat":34.147,"lng":132.223,"branch":"Marines","personnel":7000},
    {"name":"Camp Foster","country":"Japan","lat":26.296,"lng":127.795,"branch":"Marines","personnel":10000},
    {"name":"Osan AB","country":"South Korea","lat":37.091,"lng":127.029,"branch":"Air Force","personnel":8000},
    {"name":"Kunsan AB","country":"South Korea","lat":35.903,"lng":126.615,"branch":"Air Force","personnel":6000},
    {"name":"Diego Garcia","country":"British IOT","lat":-7.313,"lng":72.411,"branch":"Navy","personnel":3000},
    {"name":"Naval Station Guantanamo","country":"Cuba","lat":19.900,"lng":-75.153,"branch":"Navy","personnel":5000},
    {"name":"Thule AB","country":"Greenland","lat":76.531,"lng":-68.703,"branch":"Air Force","personnel":600},
    {"name":"Bagram Airfield","country":"Afghanistan","lat":34.944,"lng":69.260,"branch":"Joint","personnel":8000},
    {"name":"Al Udeid AB","country":"Qatar","lat":25.117,"lng":51.315,"branch":"Air Force","personnel":10000},
    {"name":"Camp Arifjan","country":"Kuwait","lat":28.883,"lng":48.154,"branch":"Army","personnel":13000},
    {"name":"Naval Support Activity Bahrain","country":"Bahrain","lat":26.203,"lng":50.611,"branch":"Navy","personnel":7000},
    {"name":"NSF Diego Garcia","country":"British IOT","lat":-7.300,"lng":72.400,"branch":"Joint","personnel":2500},
    {"name":"Pine Gap","country":"Australia","lat":-23.799,"lng":133.737,"branch":"Joint","personnel":800},
    {"name":"Ascension Island","country":"St Helena","lat":-7.947,"lng":-14.378,"branch":"Air Force","personnel":600},
    {"name":"MacDill AFB","country":"USA","lat":27.849,"lng":-82.521,"branch":"Air Force","personnel":14000},
    {"name":"Fort Drum","country":"USA","lat":44.030,"lng":-75.761,"branch":"Army","personnel":17000},
    {"name":"Fort Carson","country":"USA","lat":38.745,"lng":-104.783,"branch":"Army","personnel":25000},
    {"name":"Fort Riley","country":"USA","lat":39.095,"lng":-96.761,"branch":"Army","personnel":15000},
    {"name":"Fort Sill","country":"USA","lat":34.669,"lng":-98.413,"branch":"Army","personnel":20000},
    {"name":"Redstone Arsenal","country":"USA","lat":34.685,"lng":-86.653,"branch":"Army","personnel":14000},
    {"name":"Fort Lewis","country":"USA","lat":47.114,"lng":-122.563,"branch":"Army","personnel":27000},
    {"name":"Camp Lejeune","country":"USA","lat":34.651,"lng":-77.372,"branch":"Marines","personnel":35000},
    {"name":"Twentynine Palms","country":"USA","lat":34.261,"lng":-116.100,"branch":"Marines","personnel":16000},
    {"name":"Langley AFB","country":"USA","lat":37.083,"lng":-76.360,"branch":"Air Force","personnel":10000},
    {"name":"RAF Mildenhall","country":"UK","lat":52.361,"lng":0.486,"branch":"Air Force","personnel":4000},
    {"name":"Spangdahlem AB","country":"Germany","lat":49.972,"lng":6.690,"branch":"Air Force","personnel":5000},
    {"name":"Aviano AB","country":"Italy","lat":46.034,"lng":12.592,"branch":"Air Force","personnel":4000},
    {"name":"CNOOC Tianjin","country":"China","lat":39.100,"lng":117.716,"branch":"Navy","personnel":40000},
    {"name":"Zhoushan Naval Base","country":"China","lat":29.985,"lng":122.201,"branch":"Navy","personnel":25000},
    {"name":"Yulin Naval Base","country":"China","lat":18.208,"lng":109.692,"branch":"Navy","personnel":30000},
    {"name":"Sanya Naval Base","country":"China","lat":18.238,"lng":109.520,"branch":"Navy","personnel":15000},
    {"name":"Qingdao Naval Base","country":"China","lat":36.067,"lng":120.383,"branch":"Navy","personnel":20000},
    {"name":"Severomorsk","country":"Russia","lat":69.063,"lng":33.420,"branch":"Navy","personnel":25000},
    {"name":"Kaliningrad","country":"Russia","lat":54.700,"lng":20.500,"branch":"Joint","personnel":25000},
    {"name":"Petropavlovsk","country":"Russia","lat":53.016,"lng":158.650,"branch":"Navy","personnel":20000},
    {"name":"Sevastopol","country":"Russia/UA","lat":44.600,"lng":33.525,"branch":"Navy","personnel":15000},
    {"name":"Murmansk","country":"Russia","lat":68.970,"lng":33.075,"branch":"Navy","personnel":30000},
    {"name":"Vladivostok","country":"Russia","lat":43.100,"lng":131.880,"branch":"Navy","personnel":25000},
    {"name":"INS Kadamba","country":"India","lat":14.754,"lng":74.124,"branch":"Navy","personnel":15000},
    {"name":"INS Vikramaditya","country":"India","lat":14.500,"lng":74.000,"branch":"Navy","personnel":2000},
    {"name":"Karwar Naval Base","country":"India","lat":14.754,"lng":74.124,"branch":"Navy","personnel":10000},
    {"name":"Toulon","country":"France","lat":43.127,"lng":5.923,"branch":"Navy","personnel":20000},
    {"name":"Brest","country":"France","lat":48.390,"lng":-4.486,"branch":"Navy","personnel":15000},
    {"name":"HMNB Portsmouth","country":"UK","lat":50.800,"lng":-1.110,"branch":"Navy","personnel":17000},
    {"name":"HMNB Clyde","country":"UK","lat":56.000,"lng":-4.800,"branch":"Navy","personnel":8000},
    {"name":"Carrier Strike Group One","country":"USA","lat":32.710,"lng":-117.180,"branch":"Navy","personnel":5000},
    {"name":"Camp Bondsteel","country":"Kosovo","lat":42.373,"lng":21.244,"branch":"Army","personnel":5000},
    {"name":"Campi Bisenzio","country":"Italy","lat":43.827,"lng":11.133,"branch":"Joint","personnel":3000},
]

NUCLEAR_FACILITIES: list[dict[str, Any]] = [
    {"name":"Kozloduy","country":"Bulgaria","lat":43.750,"lng":23.750,"type":"Power Plant","capacity":2000},
    {"name":"Temelín","country":"Czech Rep.","lat":49.183,"lng":14.383,"type":"Power Plant","capacity":2100},
    {"name":"Dukovany","country":"Czech Rep.","lat":49.083,"lng":16.150,"type":"Power Plant","capacity":2000},
    {"name":"Loviisa","country":"Finland","lat":60.383,"lng":26.333,"type":"Power Plant","capacity":1000},
    {"name":"Olkiluoto","country":"Finland","lat":61.233,"lng":21.433,"type":"Power Plant","capacity":1700},
    {"name":"Flamanville","country":"France","lat":49.533,"lng":-1.883,"type":"Power Plant","capacity":1650},
    {"name":"Gravelines","country":"France","lat":50.983,"lng":2.133,"type":"Power Plant","capacity":5700},
    {"name":"Paluel","country":"France","lat":49.850,"lng":0.633,"type":"Power Plant","capacity":5500},
    {"name":"Tricastin","country":"France","lat":44.333,"lng":4.733,"type":"Power Plant","capacity":3700},
    {"name":"Cattenom","country":"France","lat":49.416,"lng":6.216,"type":"Power Plant","capacity":5500},
    {"name":"Civaux","country":"France","lat":46.450,"lng":0.650,"type":"Power Plant","capacity":3100},
    {"name":"Grohnde","country":"Germany","lat":51.933,"lng":9.433,"type":"Power Plant","capacity":1400},
    {"name":"Isar","country":"Germany","lat":48.600,"lng":12.283,"type":"Power Plant","capacity":1500},
    {"name":"Neckarwestheim","country":"Germany","lat":49.050,"lng":9.183,"type":"Power Plant","capacity":1400},
    {"name":"Paks","country":"Hungary","lat":46.567,"lng":18.850,"type":"Power Plant","capacity":2000},
    {"name":"Krško","country":"Slovenia","lat":45.933,"lng":15.517,"type":"Power Plant","capacity":700},
    {"name":"Almaraz","country":"Spain","lat":39.750,"lng":-5.683,"type":"Power Plant","capacity":2000},
    {"name":"Forsmark","country":"Sweden","lat":60.400,"lng":18.183,"type":"Power Plant","capacity":3300},
    {"name":"Oskarshamn","country":"Sweden","lat":57.417,"lng":16.667,"type":"Power Plant","capacity":1400},
    {"name":"Ringhals","country":"Sweden","lat":57.250,"lng":12.100,"type":"Power Plant","capacity":3700},
    {"name":"Beznau","country":"Switzerland","lat":47.550,"lng":8.233,"type":"Power Plant","capacity":730},
    {"name":"Gösgen","country":"Switzerland","lat":47.366,"lng":7.967,"type":"Power Plant","capacity":1010},
    {"name":"Borssele","country":"Netherlands","lat":51.433,"lng":3.717,"type":"Power Plant","capacity":480},
    {"name":"Belene","country":"Bulgaria","lat":43.630,"lng":25.200,"type":"Under Construction","capacity":2000},
    {"name":"Cernavodă","country":"Romania","lat":44.317,"lng":28.033,"type":"Power Plant","capacity":1400},
    {"name":"Mochovce","country":"Slovakia","lat":48.433,"lng":18.450,"type":"Power Plant","capacity":940},
    {"name":"Bohunice","country":"Slovakia","lat":48.483,"lng":17.683,"type":"Power Plant","capacity":940},
    {"name":"Khmelnytskyi","country":"Ukraine","lat":50.300,"lng":26.650,"type":"Power Plant","capacity":2000},
    {"name":"Rivne","country":"Ukraine","lat":51.326,"lng":25.892,"type":"Power Plant","capacity":2800},
    {"name":"South Ukraine","country":"Ukraine","lat":47.816,"lng":31.217,"type":"Power Plant","capacity":3000},
    {"name":"Zaporizhzhia","country":"Ukraine","lat":47.512,"lng":34.586,"type":"Power Plant","capacity":6000},
    {"name":"Akkuyu","country":"Turkey","lat":36.133,"lng":33.533,"type":"Under Construction","capacity":4800},
    {"name":"Bushehr","country":"Iran","lat":28.833,"lng":50.883,"type":"Power Plant","capacity":1000},
    {"name":"Barakah","country":"UAE","lat":24.133,"lng":52.667,"type":"Power Plant","capacity":5600},
    {"name":"El Dabaa","country":"Egypt","lat":31.000,"lng":28.500,"type":"Under Construction","capacity":4800},
    {"name":"Ostrovets","country":"Belarus","lat":54.850,"lbl":26.467,"type":"Power Plant","capacity":2400},
]

DEFENSE_SPENDING: dict[str, dict[str, Any]] = {
    "USA":{"amount_b":916,"pct_gdp":3.5,"rank":1},
    "China":{"amount_b":292,"pct_gdp":1.6,"rank":2},
    "Russia":{"amount_b":86,"pct_gdp":4.1,"rank":3},
    "India":{"amount_b":81,"pct_gdp":2.1,"rank":4},
    "Saudi Arabia":{"amount_b":76,"pct_gdp":7.5,"rank":5},
    "UK":{"amount_b":69,"pct_gdp":2.2,"rank":6},
    "Germany":{"amount_b":56,"pct_gdp":1.3,"rank":7},
    "France":{"amount_b":50,"pct_gdp":1.9,"rank":8},
    "Japan":{"amount_b":48,"pct_gdp":1.0,"rank":9},
    "South Korea":{"amount_b":45,"pct_gdp":2.8,"rank":10},
}


class GeopoliticalDataSource(DataSource):
    @property
    def name(self) -> str: return "geopolitical"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["military_bases", "nuclear", "defense_spending"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — geopolitical data source"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"military_bases": MILITARY_BASES}

    def fetch_military_bases(self) -> list[dict[str, Any]]:
        return MILITARY_BASES

    def fetch_nuclear_facilities(self) -> list[dict[str, Any]]:
        return NUCLEAR_FACILITIES

    def fetch_defense_spending(self) -> dict:
        return DEFENSE_SPENDING


data_source = GeopoliticalDataSource()
