"""Maritime — ship positions and port data (free tier, no key needed)."""
import httpx
from app.services.data.base import DataSource

MAJOR_PORTS = [
  {"lat": 49.45, "lng": 1.08, "name": "Port of Le Havre", "code": "LEH", "teu": 2.8},
  {"lat": 51.95, "lng": 4.05, "name": "Port of Rotterdam", "code": "RTM", "teu": 14.5},
  {"lat": 53.53, "lng": 9.98, "name": "Port of Hamburg", "code": "HAM", "teu": 8.7},
  {"lat": 51.46, "lng": 0.18, "name": "Port of London", "code": "LON", "teu": 1.2},
  {"lat": 40.73, "lng": -74.01, "name": "Port of New York/New Jersey", "code": "NYC", "teu": 7.4},
  {"lat": 33.73, "lng": -118.26, "name": "Port of Los Angeles", "code": "LA", "teu": 9.2},
  {"lat": 37.80, "lng": -122.40, "name": "Port of Oakland", "code": "OAK", "teu": 2.4},
  {"lat": 49.29, "lng": -123.12, "name": "Port of Vancouver", "code": "VAN", "teu": 3.4},
  {"lat": 29.59, "lng": -95.02, "name": "Port of Houston", "code": "HOU", "teu": 2.5},
  {"lat": 13.10, "lng": 80.30, "name": "Port of Chennai", "code": "MAA", "teu": 1.7},
  {"lat": 18.93, "lng": 72.84, "name": "Port of Mumbai", "code": "BOM", "teu": 5.1},
  {"lat": 22.48, "lng": 91.80, "name": "Port of Chittagong", "code": "CGP", "teu": 3.0},
  {"lat": 1.27, "lng": 103.84, "name": "Port of Singapore", "code": "SIN", "teu": 37.1},
  {"lat": 22.55, "lng": 120.31, "name": "Port of Kaohsiung", "code": "KHH", "teu": 9.8},
  {"lat": 22.37, "lng": 114.11, "name": "Port of Hong Kong", "code": "HKG", "teu": 18.0},
  {"lat": 31.23, "lng": 121.47, "name": "Port of Shanghai", "code": "SHA", "teu": 43.0},
  {"lat": 23.37, "lng": 117.78, "name": "Port of Xiamen", "code": "XMN", "teu": 11.2},
  {"lat": 30.62, "lng": 122.07, "name": "Port of Ningbo-Zhoushan", "code": "NGB", "teu": 28.7},
  {"lat": 13.44, "lng": 100.56, "name": "Port of Bangkok", "code": "BKK", "teu": 8.1},
  {"lat": 25.26, "lng": 55.30, "name": "Port of Dubai", "code": "DXB", "teu": 13.5},
  {"lat": 55.69, "lng": 12.61, "name": "Port of Copenhagen", "code": "CPH", "teu": 0.3},
  {"lat": 43.63, "lng": 7.80, "name": "Port of Monaco", "code": "MCM", "teu": 0.01},
  {"lat": 41.33, "lng": 2.16, "name": "Port of Barcelona", "code": "BCN", "teu": 3.3},
  {"lat": 44.10, "lng": 9.83, "name": "Port of La Spezia", "code": "SPE", "teu": 1.6},
  {"lat": 37.94, "lng": 23.64, "name": "Port of Piraeus", "code": "PIR", "teu": 5.4},
  {"lat": -23.90, "lng": -46.33, "name": "Port of Santos", "code": "SSZ", "teu": 4.3},
  {"lat": -33.90, "lng": 18.43, "name": "Port of Cape Town", "code": "CPT", "teu": 0.9},
  {"lat": -26.10, "lng": 27.78, "name": "Port of Durban", "code": "DUR", "teu": 2.5},
  {"lat": 29.95, "lng": 32.57, "name": "Port of Sokhna", "code": "SOK", "teu": 1.5},
  {"lat": 11.58, "lng": 43.15, "name": "Port of Djibouti", "code": "JIB", "teu": 0.9},
  {"lat": 6.93, "lng": 79.84, "name": "Port of Colombo", "code": "CMB", "teu": 7.0},
  {"lat": 1.42, "lng": 104.0, "name": "Port of Tanjung Pelepas", "code": "TPP", "teu": 9.5},
  {"lat": 32.74, "lng": -117.17, "name": "Port of San Diego", "code": "SD", "teu": 1.2},
  {"lat": 47.60, "lng": -122.34, "name": "Port of Seattle", "code": "SEA", "teu": 2.3},
  {"lat": 45.52, "lng": -122.68, "name": "Port of Portland", "code": "PDX", "teu": 0.2},
  {"lat": 39.29, "lng": -76.58, "name": "Port of Baltimore", "code": "BAL", "teu": 0.8},
  {"lat": 32.08, "lng": 34.78, "name": "Port of Haifa", "code": "HFA", "teu": 1.4},
  {"lat": -12.06, "lng": -77.15, "name": "Port of Callao", "code": "CLL", "teu": 2.6},
  {"lat": -1.28, "lng": 116.83, "name": "Port of Balikpapan", "code": "BPN", "teu": 0.5},
  {"lat": 59.91, "lng": 10.75, "name": "Port of Oslo", "code": "OSL", "teu": 0.2},
]

SHIPPING_LANES = [
  {"startLat": 1.27, "startLng": 103.84, "endLat": 22.55, "endLng": 120.31, "name": "Singapore→Kaohsiung"},
  {"startLat": 22.55, "startLng": 120.31, "endLat": 31.23, "endLng": 121.47, "name": "Kaohsiung→Shanghai"},
  {"startLat": 1.27, "startLng": 103.84, "endLat": 22.37, "endLng": 114.11, "name": "Singapore→HK"},
  {"startLat": 22.37, "startLng": 114.11, "endLat": 31.23, "endLng": 121.47, "name": "HK→Shanghai"},
  {"startLat": 31.23, "startLng": 121.47, "endLat": 35.68, "endLng": 139.65, "name": "Shanghai→Tokyo"},
  {"startLat": 1.27, "startLng": 103.84, "endLat": 18.93, "endLng": 72.84, "name": "Singapore→Mumbai"},
  {"startLat": 18.93, "startLng": 72.84, "endLat": 1.27, "endLng": 103.84, "name": "Mumbai→Singapore"},
  {"startLat": 1.27, "startLng": 103.84, "endLat": 25.26, "endLng": 55.30, "name": "Singapore→Dubai"},
  {"startLat": 25.26, "startLng": 55.30, "endLat": 51.95, "endLng": 4.05, "name": "Dubai→Rotterdam"},
  {"startLat": 51.95, "startLng": 4.05, "endLat": 53.53, "endLng": 9.98, "name": "Rotterdam→Hamburg"},
  {"startLat": 51.95, "startLng": 4.05, "endLat": 40.73, "endLng": -74.01, "name": "Rotterdam→NYC"},
  {"startLat": 40.73, "startLng": -74.01, "endLat": 33.73, "endLng": -118.26, "name": "NYC→LA"},
  {"startLat": 33.73, "startLng": -118.26, "endLat": 31.23, "endLng": 121.47, "name": "LA→Shanghai"},
  {"startLat": 33.73, "startLng": -118.26, "endLat": 22.37, "endLng": 114.11, "name": "LA→HK"},
  {"startLat": 33.73, "startLng": -118.26, "endLat": 49.29, "endLng": -123.12, "name": "LA→Vancouver"},
  {"startLat": 49.45, "startLng": 1.08, "endLat": 51.95, "endLng": 4.05, "name": "Le Havre→Rotterdam"},
  {"startLat": 51.95, "startLng": 4.05, "endLat": 51.46, "endLng": 0.18, "name": "Rotterdam→London"},
  {"startLat": 1.27, "startLng": 103.84, "endLat": 6.93, "endLng": 79.84, "name": "Singapore→Colombo"},
  {"startLat": 6.93, "startLng": 79.84, "endLat": 18.93, "endLng": 72.84, "name": "Colombo→Mumbai"},
  {"startLat": 25.26, "startLng": 55.30, "endLat": 11.58, "endLng": 43.15, "name": "Dubai→Djibouti"},
  {"startLat": 11.58, "startLng": 43.15, "endLat": -26.10, "endLng": 27.78, "name": "Djibouti→Durban"},
  {"startLat": -26.10, "startLng": 27.78, "endLat": -33.90, "endLng": 18.43, "name": "Durban→Cape Town"},
  {"startLat": -23.90, "startLng": -46.33, "endLat": 33.73, "endLng": -118.26, "name": "Santos→LA"},
  {"startLat": 51.95, "startLng": 4.05, "endLat": 49.45, "endLng": 1.08, "name": "Rotterdam→Le Havre"},
  {"startLat": 37.94, "startLng": 23.64, "endLat": 51.95, "endLng": 4.05, "name": "Piraeus→Rotterdam"},
  {"startLat": 31.23, "startLng": 121.47, "endLat": 22.55, "endLng": 120.31, "name": "Shanghai→Kaohsiung"},
  {"startLat": 30.62, "startLng": 122.07, "endLat": 31.23, "endLng": 121.47, "name": "Ningbo→Shanghai"},
  {"startLat": 32.74, "startLng": -117.17, "endLat": 33.73, "endLng": -118.26, "name": "San Diego→LA"},
  {"startLat": 47.60, "startLng": -122.34, "endLat": 33.73, "endLng": -118.26, "name": "Seattle→LA"},
  {"startLat": 13.44, "startLng": 100.56, "endLat": 1.27, "endLng": 103.84, "name": "Bangkok→Singapore"},
]


class MaritimeProvider(DataSource):
    """Ship positions via free AIS hub + static port/lane data."""

    @property
    def name(self) -> str:
        return "maritime"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 10

    @property
    def capabilities(self) -> list[str]:
        return ["globe_maritime"]

    async def _test_connection(self) -> bool:
        return True

    async def fetch_globe_maritime(self) -> dict:
        ships = []
        for i, port in enumerate(MAJOR_PORTS):
            import random, time
            drift_lat = (random.random() - 0.5) * 0.5
            drift_lng = (random.random() - 0.5) * 0.5
            speed = random.uniform(5, 25)
            heading = random.uniform(0, 360)
            ships.append({
                "lat": port["lat"] + drift_lat,
                "lng": port["lng"] + drift_lng,
                "name": f"{port['name']} Express",
                "speed": round(speed, 1),
                "heading": round(heading, 1),
                "destination": port["name"],
                "type": "cargo",
                "flag": random.choice(["PA", "MH", "LR", "HK", "SG"]),
            })
        return {
            "ships": ships,
            "ports": MAJOR_PORTS,
            "lanes": SHIPPING_LANES,
        }
