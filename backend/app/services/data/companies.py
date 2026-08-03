"""Global company database — 100000 companies from real tickers + curated + synthetic cover."""
import json, os

_data = None


def _load():
    global _data
    if _data is not None:
        return _data
    # Load from per-continent JSON files in frontend/public/data/
    _all = []
    _base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                         "frontend", "public", "data")
    _continents = ["north_america", "europe", "asia", "south_america",
                   "africa", "oceania", "other"]
    for _c in _continents:
        _fp = os.path.join(_base, f"companies_{_c}.json")
        if os.path.exists(_fp):
            with open(_fp) as _f:
                _d = json.load(_f)
            _all.extend(_d.get("companies", []))
    _data = {"companies": _all, "total": len(_all)}
    return _data
    for p in [path, alt]:
        if os.path.exists(p):
            with open(p) as f:
                _data = json.load(f)
            return _data
    _data = {"companies": [], "total": 0}
    return _data

# Continent centroids for map centering
CONTINENT_CENTROIDS = {
    "north_america": {"lat": 20, "lng": -60},
    "europe": {"lat": 45, "lng": 20},
    "asia": {"lat": 35, "lng": 110},
    "south_america": {"lat": -15, "lng": -60},
    "africa": {"lat": -5, "lng": 25},
    "middle_east": {"lat": 25, "lng": 50},
    "oceania": {"lat": -28, "lng": 135},
}

CONTINENTS = list(CONTINENT_CENTROIDS.keys())
ALL_COMPANIES = []

# Map country codes to continents
COUNTRY_CONTINENT = {
    "US": "north_america", "CA": "north_america", "MX": "north_america",
    "GB": "europe", "DE": "europe", "FR": "europe", "IT": "europe",
    "ES": "europe", "NL": "europe", "CH": "europe", "BE": "europe",
    "AT": "europe", "IE": "europe", "PT": "europe", "DK": "europe",
    "SE": "europe", "NO": "europe", "FI": "europe", "PL": "europe",
    "CZ": "europe", "RU": "europe", "RO": "europe", "GR": "europe",
    "HU": "europe", "UA": "europe", "BG": "europe", "SK": "europe",
    "BY": "europe", "LT": "europe", "LV": "europe", "EE": "europe",
    "LU": "europe", "HR": "europe", "SI": "europe", "RS": "europe",
    "JP": "asia", "CN": "asia", "HK": "asia", "KR": "asia",
    "IN": "asia", "SG": "asia", "TW": "asia", "TH": "asia",
    "PH": "asia", "MY": "asia", "ID": "asia", "VN": "asia",
    "BD": "asia", "LK": "asia", "PK": "asia", "NP": "asia",
    "UZ": "asia", "KZ": "asia", "KG": "asia", "TJ": "asia",
    "AF": "asia", "IR": "asia", "IQ": "asia", "IL": "asia",
    "SA": "middle_east", "AE": "middle_east", "QA": "middle_east",
    "KW": "middle_east", "OM": "middle_east", "BH": "middle_east",
    "JO": "middle_east", "YE": "middle_east", "LB": "middle_east",
    "BR": "south_america", "AR": "south_america", "CL": "south_america",
    "PE": "south_america", "CO": "south_america", "EC": "south_america",
    "VE": "south_america", "UY": "south_america", "PY": "south_america",
    "BO": "south_america", "GY": "south_america", "SR": "south_america",
    "ZA": "africa", "EG": "africa", "NG": "africa", "KE": "africa",
    "MA": "africa", "TN": "africa", "SN": "africa", "GH": "africa",
    "TZ": "africa", "RW": "africa", "UG": "africa", "CD": "africa",
    "DZ": "africa", "LY": "africa", "BF": "africa", "ML": "africa",
    "NE": "africa", "BJ": "africa", "TG": "africa", "CM": "africa",
    "CI": "africa", "ZW": "africa", "MZ": "africa", "AO": "africa",
    "ZM": "africa", "MW": "africa", "BW": "africa", "NA": "africa",
    "AU": "oceania", "NZ": "oceania", "FJ": "oceania", "PG": "oceania",
    "SB": "oceania", "PF": "oceania", "TO": "oceania", "WS": "oceania",
}


def get_company_count() -> int:
    return _load().get("total", 0)


def get_all_companies() -> list[dict]:
    return _load().get("companies", [])


def get_companies_by_continent(continent: str | None = None) -> list[dict]:
    data = _load().get("companies", [])
    if continent is None or continent == "all":
        return data
    return [c for c in data if COUNTRY_CONTINENT.get(c["co"], "") == continent]


def get_continent_centroid(continent: str) -> dict:
    return CONTINENT_CENTROIDS.get(continent, {"lat": 0, "lng": 0})
