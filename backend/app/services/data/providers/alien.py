"""Alien/UFO data provider — NUFORC sightings, ancient astronaut theory sites."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

UFO_SIGHTINGS: list[dict[str, Any]] = [
    {"location":"Kecksburg, PA","lat":40.134,"lng":-79.602,"year":1965,"description":"Acorn-shaped object crashed, military recovered","confidence":0.7},
    {"location":"Lubbock, TX","lat":33.580,"lng":-101.850,"year":1951,"description":"Formation of lights photographed by multiple witnesses","confidence":0.6},
    {"location":"Aurora, TX","lat":33.058,"lng":-97.510,"year":1897,"description":"Alien body reported from crashed craft","confidence":0.3},
    {"location":"Flatwoods, WV","lat":38.711,"lng":-80.718,"year":1952,"description":"Monster-like entity sighted after fireball crash","confidence":0.5},
    {"location":"Hopkinsville, KY","lat":36.866,"lng":-87.487,"year":1955,"description":"Goblin-like creatures attacked farmhouse","confidence":0.4},
    {"location":"Barney & Betty Hill, NH","lat":44.155,"lng":-71.435,"year":1961,"description":"First widely-publicized alien abduction case","confidence":0.4},
    {"location":"Travis Walton, AZ","lat":34.167,"lng":-109.717,"year":1975,"description":"Logger abducted by beam of light","confidence":0.4},
    {"location":"Allagash, ME","lat":46.083,"lng":-69.083,"year":1976,"description":"Four men abducted during fishing trip","confidence":0.3},
    {"location":"Socorro, NM","lat":34.057,"lng":-106.896,"year":1964,"description":"Landed craft with symbol, seen by police officer","confidence":0.6},
    {"location":"Varginha, Brazil","lat":-21.550,"lng":-45.433,"year":1996,"description":"Multiple witnesses saw creature, military recovered","confidence":0.5},
    {"location":"Rendlesham Forest, UK","lat":52.083,"lng":1.417,"year":1980,"description":"Landed craft seen by US Air Force personnel","confidence":0.7},
    {"location":"Belgium Wave","lat":50.500,"lng":4.500,"year":1989,"description":"Triangular craft tracked by radar over weeks","confidence":0.7},
    {"location":"Phoenix Lights","lat":33.450,"lng":-112.067,"year":1997,"description":"V-shaped formation seen by thousands","confidence":0.6},
    {"location":"O'Hare Airport, IL","lat":41.978,"lng":-87.904,"year":2006,"description":"Saucer hovered over gate for minutes","confidence":0.5},
    {"location":"Nimitz Carrier Strike Group","lat":32.700,"lng":-117.200,"year":2004,"description":"Tic-tac craft tracked by radar, filmed","confidence":0.8},
    {"location":"USS Theodore Roosevelt","lat":32.700,"lng":-117.200,"year":2015,"description":"Multiple craft tracked by pilots, declassified","confidence":0.8},
    {"location":"Gimbal, off FL","lat":28.500,"lng":-79.500,"year":2015,"description":"Declassified US Navy FLIR footage","confidence":0.7},
    {"location":"GoFast, off FL","lat":28.500,"lng":-79.500,"year":2015,"description":"Fast-moving craft at low altitude","confidence":0.7},
    {"location":"Jerusalem UFO","lat":31.768,"lng":35.213,"year":2011,"description":"Large sphere hovered over Dome of the Rock","confidence":0.4},
    {"location":"Shag Harbour, NS","lat":43.500,"lng":-65.500,"year":1967,"description":"Multiple witnesses, craft crashed into ocean","confidence":0.6},
    {"location":"Kelly-Hopkinsville","lat":36.900,"lng":-87.500,"year":1955,"description":"Small humanoid creatures attacked farm","confidence":0.4},
    {"location":"Westall, AU","lat":-37.900,"lng":145.150,"year":1966,"description":"200+ students saw craft land near school","confidence":0.6},
    {"location":"Maury Island, WA","lat":47.382,"lng":-122.433,"year":1947,"description":"Six donut-shaped craft, strange metal fragments","confidence":0.3},
    {"location":"Nellis AFB, NV","lat":36.240,"lng":-115.033,"year":1994,"description":"Multiple lights above restricted range","confidence":0.5},
    {"location":"Hessdalen Lights, NO","lat":62.800,"lng":11.200,"year":1981,"description":"Recurring unexplained lights for 30+ years","confidence":0.5},
]

ANCIENT_SITES: list[dict[str, Any]] = [
    {"name":"Great Pyramid of Giza","country":"Egypt","lat":29.979,"lng":31.134,"type":"Pyramid","theory":"Alignment with Orion, precision impossible for era"},
    {"name":"Nazca Lines","country":"Peru","lat":-14.707,"lng":-75.136,"type":"Geoglyph","theory":"Only visible from air — landing strip theory"},
    {"name":"Stonehenge","country":"UK","lat":51.178,"lng":-1.826,"type":"Megalith","theory":"Acoustic levitation, celestial alignment"},
    {"name":"Teotihuacán","country":"Mexico","lat":19.692,"lng":-98.843,"type":"Pyramid","theory":"Pyramid of the Sun covers older structure"},
    {"name":"Puma Punku","country":"Bolivia","lat":-16.561,"lng":-68.681,"type":"Temple","theory":"Hard stone with precision impossible for era"},
    {"name":"Sacsayhuamán","country":"Peru","lat":-13.510,"lng":-71.981,"type":"Fortress","theory":"Cyclopean masonry with earthquake-proof joints"},
    {"name":"Baalbek","country":"Lebanon","lat":34.007,"lng":36.203,"type":"Temple","theory":"1,000-ton stones moved — unknown technology"},
    {"name":"Moai, Easter Island","country":"Chile","lat":-27.113,"lng":-109.359,"type":"Statues","theory":"Remote island — how were they moved?"},
    {"name":"Göbekli Tepe","country":"Turkey","lat":37.223,"lng":38.922,"type":"Temple","theory":"11,600 years old — precision stone carving"},
    {"name":"Angkor Wat","country":"Cambodia","lat":13.412,"lng":103.867,"type":"Temple","theory":"Aligns with Draco constellation"},
    {"name":"Tiahuanaco","country":"Bolivia","lat":-16.554,"lng":-68.673,"type":"City","theory":"12,000 years old, advanced engineering"},
    {"name":"Coral Castle","country":"USA","lat":25.500,"lng":-80.440,"type":"Structure","theory":"Single man moved 1,100-ton stones alone"},
    {"name":"Yonaguni Monument","country":"Japan","lat":24.429,"lng":123.000,"type":"Submerged","theory":"Natural or man-made — predates known history"},
    {"name":"Pyramid of the Sun","country":"Mexico","lat":19.692,"lng":-98.843,"type":"Pyramid","theory":"Tunnel system found below, mica layers"},
    {"name":"Chichén Itzá","country":"Mexico","lat":20.684,"lng":-88.568,"type":"City","theory":"Kukulkan pyramid = astronomical calendar"},
    {"name":"Machu Picchu","country":"Peru","lat":-13.163,"lng":-72.545,"type":"City","theory":"Precision stone fitting, no mortar"},
    {"name":"Petra","country":"Jordan","lat":30.328,"lng":35.444,"type":"City","theory":"Carved from rock with unknown tools"},
    {"name":"Mohenjo-Daro","country":"Pakistan","lat":27.329,"lng":68.133,"type":"City","theory":"Advanced urban planning 4,500 years ago"},
    {"name":"Great Sphinx","country":"Egypt","lat":29.975,"lng":31.138,"type":"Statue","theory":"Water erosion predating known Egyptian civilization"},
    {"name":"Derinkuyu","country":"Turkey","lat":38.374,"lng":34.735,"type":"Underground","theory":"20-story underground city for 20,000 people"},
]


class AlienDataSource(DataSource):
    @property
    def name(self) -> str: return "alien"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 1000

    @property
    def capabilities(self) -> list[str]: return ["ufo_sightings", "ancient_sites"]

    async def _test_connection(self) -> bool: return True

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — alien data source"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        return {"sightings": UFO_SIGHTINGS, "ancient_sites": ANCIENT_SITES}

    def fetch_ufo_sightings(self) -> list[dict[str, Any]]:
        return UFO_SIGHTINGS

    def fetch_ancient_sites(self) -> list[dict[str, Any]]:
        return ANCIENT_SITES


data_source = AlienDataSource()
