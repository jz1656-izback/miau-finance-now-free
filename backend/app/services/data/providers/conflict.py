"""Geopolitical conflict provider — active conflict zones worldwide."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

CONFLICT_ZONES: list[dict[str, Any]] = [
    {"name":"Ukraine War","region":"Eastern Europe","lat":48.500,"lng":31.500,"type":"Conventional War","intensity":"High","start_year":2022,"parties":["Ukraine","Russia"]},
    {"name":"Gaza Strip","region":"Middle East","lat":31.500,"lng":34.500,"type":"Conventional War","intensity":"High","start_year":2023,"parties":["Israel","Hamas"]},
    {"name":"Syrian Civil War","region":"Middle East","lat":35.000,"lng":38.500,"type":"Civil War","intensity":"High","start_year":2011,"parties":["Syria","Rebels","Kurds","Turkey"]},
    {"name":"Yemen Civil War","region":"Middle East","lat":15.500,"lng":47.500,"type":"Civil War","intensity":"High","start_year":2014,"parties":["Yemen","Houthis","Saudi Coalition"]},
    {"name":"Myanmar Civil War","region":"Southeast Asia","lat":22.000,"lng":96.000,"type":"Civil War","intensity":"High","start_year":2021,"parties":["Junta","Rebel Alliances"]},
    {"name":"Sudan Civil War","region":"Africa","lat":15.500,"lng":30.000,"type":"Civil War","intensity":"High","start_year":2023,"parties":["SAF","RSF"]},
    {"name":"DRC Conflict","region":"Africa","lat":-2.500,"lng":25.000,"type":"Insurgency","intensity":"High","start_year":1996,"parties":["DRC","M23","Militias"]},
    {"name":"Somalia Conflict","region":"Africa","lat":5.000,"lng":46.000,"type":"Insurgency","intensity":"Medium","start_year":1991,"parties":["Somalia","Al-Shabaab"]},
    {"name":"Sahel Insurgency","region":"Africa","lat":15.000,"lng":0.000,"type":"Insurgency","intensity":"High","start_year":2012,"parties":["Mali","Burkina Faso","Niger","Jihadists"]},
    {"name":"Nagorno-Karabakh","region":"Caucasus","lat":39.800,"lng":46.700,"type":"Border Conflict","intensity":"Medium","start_year":2020,"parties":["Armenia","Azerbaijan"]},
    {"name":"Afghanistan","region":"Central Asia","lat":34.000,"lng":66.000,"type":"Insurgency","intensity":"Medium","start_year":2021,"parties":["Taliban","ISIS-K"]},
    {"name":"Ethiopia-Tigray","region":"Africa","lat":14.000,"lng":39.000,"type":"Border Conflict","intensity":"Medium","start_year":2020,"parties":["Ethiopia","Tigray"]},
    {"name":"Kashmir","region":"South Asia","lat":34.500,"lng":76.000,"type":"Border Conflict","intensity":"Medium","start_year":1947,"parties":["India","Pakistan"]},
    {"name":"Haiti Gang War","region":"Caribbean","lat":18.500,"lng":-72.500,"type":"Gang Violence","intensity":"High","start_year":2021,"parties":["Haiti","Gangs"]},
    {"name":"Colombia Conflict","region":"South America","lat":4.000,"lng":-74.000,"type":"Insurgency","intensity":"Medium","start_year":1964,"parties":["Colombia","ELN","FARC Dissidents"]},
    {"name":"Balochistan","region":"South Asia","lat":28.000,"lng":64.000,"type":"Insurgency","intensity":"Medium","start_year":2000,"parties":["Pakistan","Baloch Separatists"]},
    {"name":"Kurdish-Turkish","region":"Middle East","lat":38.000,"lng":39.000,"type":"Insurgency","intensity":"Medium","start_year":1984,"parties":["Turkey","PKK"]},
    {"name":"Libya Crisis","region":"Africa","lat":26.500,"lng":17.500,"type":"Civil War","intensity":"Low","start_year":2011,"parties":["Libya","Militias"]},
    {"name":"Central African Rep.","region":"Africa","lat":7.000,"lng":21.000,"type":"Civil War","intensity":"Medium","start_year":2012,"parties":["CAR","Rebels"]},
    {"name":"Mozambique Insurgency","region":"Africa","lat":-13.000,"lng":40.000,"type":"Insurgency","intensity":"Medium","start_year":2017,"parties":["Mozambique","ISIS-Mozambique"]},
    {"name":"Donbas","region":"Eastern Europe","lat":48.000,"lng":37.800,"type":"Conventional War","intensity":"High","start_year":2014,"parties":["Ukraine","Russia","Separatists"]},
    {"name":"West Bank","region":"Middle East","lat":31.900,"lng":35.200,"type":"Occupation","intensity":"Medium","start_year":1967,"parties":["Israel","Palestinian Authority"]},
    {"name":"Amazon Deforestation Conflict","region":"South America","lat":-5.000,"lng":-55.000,"type":"Resource Conflict","intensity":"Low","start_year":2019,"parties":["Brazil","Loggers","Indigenous"]},
    {"name":"South China Sea","region":"Southeast Asia","lat":12.000,"lng":114.000,"type":"Maritime Dispute","intensity":"Low","start_year":2012,"parties":["China","Philippines","Vietnam"]},
    {"name":"Rohingya Crisis","region":"Southeast Asia","lat":21.000,"lng":92.500,"type":"Ethnic Conflict","intensity":"Low","start_year":2017,"parties":["Myanmar","Rohingya"]},
]


class ConflictDataSource(DataSource):
    @property
    def name(self) -> str: return "conflict"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["conflict_zones"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — conflict data source"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"conflicts": CONFLICT_ZONES}

    def fetch_conflict_zones(self) -> list[dict[str, Any]]:
        return CONFLICT_ZONES


data_source = ConflictDataSource()
