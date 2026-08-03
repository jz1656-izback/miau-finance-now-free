"""Global mining & resources data provider for MiauGlobe."""
import logging
from typing import Any
from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

MAJOR_MINES = [
    {"name": "Grasberg", "lat": -4.05, "lng": 137.11, "commodity": "Gold/Copper", "country": "Indonesia", "owner": "Freeport-McMoRan", "production": "1.5M oz Au"},
    {"name": "Escondida", "lat": -24.27, "lng": -69.06, "commodity": "Copper", "country": "Chile", "owner": "BHP", "production": "1.0M tonnes Cu"},
    {"name": "Muruntau", "lat": 41.53, "lng": 65.15, "commodity": "Gold", "country": "Uzbekistan", "owner": "Navoi Mining", "production": "3.0M oz Au"},
    {"name": "Olympic Dam", "lat": -30.44, "lng": 136.89, "commodity": "Uranium/Copper", "country": "Australia", "owner": "BHP", "production": "200K tonnes Cu"},
    {"name": "Cerro Verde", "lat": -16.54, "lng": -71.57, "commodity": "Copper", "country": "Peru", "owner": "Freeport-McMoRan", "production": "500K tonnes Cu"},
    {"name": "Chuquicamata", "lat": -22.29, "lng": -68.90, "commodity": "Copper", "country": "Chile", "owner": "Codelco", "production": "700K tonnes Cu"},
    {"name": "Collahuasi", "lat": -20.98, "lng": -68.65, "commodity": "Copper", "country": "Chile", "owner": "Glencore", "production": "600K tonnes Cu"},
    {"name": "Tenke Fungurume", "lat": -10.64, "lng": 26.22, "commodity": "Cobalt/Copper", "country": "DRC", "owner": "CMOC", "production": "200K tonnes Cu"},
    {"name": "KGHM Polska Miedź", "lat": 51.40, "lng": 16.20, "commodity": "Copper/Silver", "country": "Poland", "owner": "KGHM", "production": "500K tonnes Cu"},
    {"name": "Norilsk", "lat": 69.33, "lng": 88.10, "commodity": "Nickel/Palladium", "country": "Russia", "owner": "Nornickel", "production": "200K tonnes Ni"},
    {"name": "Mponeng", "lat": -26.44, "lng": 27.43, "commodity": "Gold", "country": "South Africa", "owner": "AngloGold Ashanti", "production": "500K oz Au"},
    {"name": "Kumtor", "lat": 41.87, "lng": 78.18, "commodity": "Gold", "country": "Kyrgyzstan", "owner": "Centerra", "production": "600K oz Au"},
    {"name": "Super Pit", "lat": -30.77, "lng": 121.48, "commodity": "Gold", "country": "Australia", "owner": "Northern Star", "production": "700K oz Au"},
    {"name": "Yanacocha", "lat": -6.99, "lng": -78.51, "commodity": "Gold", "country": "Peru", "owner": "Newmont", "production": "500K oz Au"},
    {"name": "Pueblo Viejo", "lat": 18.83, "lng": -70.20, "commodity": "Gold", "country": "Dominican Republic", "owner": "Barrick", "production": "800K oz Au"},
    {"name": "Cortez", "lat": 40.17, "lng": -116.60, "commodity": "Gold", "country": "USA", "owner": "Barrick", "production": "1.0M oz Au"},
    {"name": "Goldstrike", "lat": 40.96, "lng": -116.33, "commodity": "Gold", "country": "USA", "owner": "Barrick", "production": "1.0M oz Au"},
    {"name": "Lihir", "lat": -3.12, "lng": 152.63, "commodity": "Gold", "country": "PNG", "owner": "Newmont", "production": "800K oz Au"},
    {"name": "Oyu Tolgoi", "lat": 43.01, "lng": 106.84, "commodity": "Copper/Gold", "country": "Mongolia", "owner": "Rio Tinto", "production": "500K tonnes Cu"},
    {"name": "Morenci", "lat": 33.09, "lng": -109.36, "commodity": "Copper", "country": "USA", "owner": "Freeport-McMoRan", "production": "900K tonnes Cu"},
    {"name": "Bingham Canyon", "lat": 40.52, "lng": -112.15, "commodity": "Copper", "country": "USA", "owner": "Rio Tinto", "production": "200K tonnes Cu"},
    {"name": "Antamina", "lat": -9.54, "lng": -77.04, "commodity": "Copper/Zinc", "country": "Peru", "owner": "Glencore", "production": "400K tonnes Cu"},
    {"name": "Los Pelambres", "lat": -31.70, "lng": -70.60, "commodity": "Copper", "country": "Chile", "owner": "Antofagasta", "production": "350K tonnes Cu"},
    {"name": "Kansanshi", "lat": -12.10, "lng": 26.40, "commodity": "Copper", "country": "Zambia", "owner": "First Quantum", "production": "300K tonnes Cu"},
    {"name": "Sentinel", "lat": -12.62, "lng": 27.83, "commodity": "Copper", "country": "Zambia", "owner": "First Quantum", "production": "250K tonnes Cu"},
    {"name": "Karara", "lat": -29.25, "lng": 116.60, "commodity": "Iron Ore", "country": "Australia", "owner": "Gindalbie", "production": "10M tonnes Fe"},
    {"name": "Sino Iron", "lat": -20.70, "lng": 119.20, "commodity": "Iron Ore", "country": "Australia", "owner": "CITIC", "production": "20M tonnes Fe"},
    {"name": "Pilbara", "lat": -22.50, "lng": 118.50, "commodity": "Iron Ore", "country": "Australia", "owner": "Rio Tinto/BHP", "production": "280M tonnes Fe"},
    {"name": "Carajás", "lat": -6.06, "lng": -50.18, "commodity": "Iron Ore", "country": "Brazil", "owner": "Vale", "production": "180M tonnes Fe"},
    {"name": "Serra Sul", "lat": -6.40, "lng": -50.30, "commodity": "Iron Ore", "country": "Brazil", "owner": "Vale", "production": "90M tonnes Fe"},
]

MAJOR_OIL_FIELDS = [
    {"name": "Ghawar", "lat": 24.80, "lng": 49.30, "commodity": "Oil", "country": "Saudi Arabia", "owner": "Saudi Aramco", "production": "3.8M bbl/d"},
    {"name": "Burgan", "lat": 29.05, "lng": 47.78, "commodity": "Oil", "country": "Kuwait", "owner": "KOC", "production": "1.6M bbl/d"},
    {"name": "Ahvaz", "lat": 31.32, "lng": 48.65, "commodity": "Oil", "country": "Iran", "owner": "NIOC", "production": "900K bbl/d"},
    {"name": "Cantarell", "lat": 19.30, "lng": -92.70, "commodity": "Oil", "country": "Mexico", "owner": "Pemex", "production": "400K bbl/d"},
    {"name": "Samotlor", "lat": 60.98, "lng": 76.82, "commodity": "Oil", "country": "Russia", "owner": "Rosneft", "production": "500K bbl/d"},
    {"name": "Prudhoe Bay", "lat": 70.30, "lng": -148.60, "commodity": "Oil", "country": "USA", "owner": "ConocoPhillips", "production": "300K bbl/d"},
    {"name": "Rumaila", "lat": 30.28, "lng": 47.30, "commodity": "Oil", "country": "Iraq", "owner": "Basra Oil", "production": "1.5M bbl/d"},
    {"name": "Zakum", "lat": 24.80, "lng": 53.00, "commodity": "Oil", "country": "UAE", "owner": "ADNOC", "production": "700K bbl/d"},
    {"name": "Safaniya", "lat": 27.80, "lng": 49.30, "commodity": "Oil", "country": "Saudi Arabia", "owner": "Saudi Aramco", "production": "1.2M bbl/d"},
    {"name": "Shaybah", "lat": 22.50, "lng": 54.00, "commodity": "Oil", "country": "Saudi Arabia", "owner": "Saudi Aramco", "production": "1.0M bbl/d"},
]

MAJOR_RENEWABLE = [
    {"name": "Three Gorges Dam", "lat": 30.82, "lng": 111.00, "commodity": "Hydro", "country": "China", "owner": "CTG", "production": "22.5 GW"},
    {"name": "Gansu Wind Farm", "lat": 40.20, "lng": 96.50, "commodity": "Wind", "country": "China", "owner": "State Grid", "production": "20 GW"},
    {"name": "Itaipu Dam", "lat": -25.40, "lng": -54.58, "commodity": "Hydro", "country": "Brazil/Paraguay", "owner": "Itaipu Binacional", "production": "14 GW"},
    {"name": "Belo Monte", "lat": -3.10, "lng": -51.80, "commodity": "Hydro", "country": "Brazil", "owner": "Norte Energia", "production": "11 GW"},
    {"name": "Jiuquan Wind", "lat": 39.70, "lng": 98.50, "commodity": "Wind", "country": "China", "owner": "CPID", "production": "10 GW"},
    {"name": "Bhadla Solar", "lat": 27.30, "lng": 71.80, "commodity": "Solar", "country": "India", "owner": "SECI", "production": "2.2 GW"},
    {"name": "Pavagada Solar", "lat": 14.20, "lng": 77.30, "commodity": "Solar", "country": "India", "owner": "KREDL", "production": "2.0 GW"},
    {"name": "Tengger Desert Solar", "lat": 37.50, "lng": 105.00, "commodity": "Solar", "country": "China", "owner": "Zhongwei", "production": "1.5 GW"},
    {"name": "Hornsea Wind", "lat": 53.80, "lng": 1.50, "commodity": "Wind", "country": "UK", "owner": "Ørsted", "production": "3.6 GW"},
    {"name": "Grand Coulee Dam", "lat": 47.95, "lng": -118.97, "commodity": "Hydro", "country": "USA", "owner": "USBR", "production": "6.8 GW"},
]


class MiningProvider(DataSource):
    def __init__(self):
        super().__init__()

    async def _test_connection(self) -> bool:
        return len(MAJOR_MINES) > 0

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — mining data source does not provide quotes"}

    async def health(self) -> bool:
        return True

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 1000

    @property
    def base_url(self) -> str:
        return ""

    @property
    def name(self) -> str:
        return "mining"

    @property
    def capabilities(self) -> list[str]:
        return ["mining"]

    async def fetch(self, query: str = "") -> list[dict[str, Any]]:
        return self.fetch_mines()

    def fetch_mines(self) -> list[dict[str, Any]]:
        return [
            {**m, "type": "mine", "size": 0.3}
            for m in MAJOR_MINES + MAJOR_OIL_FIELDS + MAJOR_RENEWABLE
        ]
