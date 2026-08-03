"""OpenSky Network — live ADS-B aircraft tracking (free, no key)."""
import httpx
from app.services.data.base import DataSource


class OpenSkyProvider(DataSource):
    """Live aircraft positions from OpenSky Network. Free tier: 10 req/min."""

    @property
    def name(self) -> str:
        return "opensky"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 8

    @property
    def capabilities(self) -> list[str]:
        return ["globe_aircraft"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get("https://opensky-network.org/api/states/all")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_globe_aircraft(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://opensky-network.org/api/states/all")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"OpenSky returned {r.status_code}")
            data = r.json()
            states = data.get("states", [])[:500]
            result = []
            for s in states:
                if s[5] is not None and s[6] is not None:
                    result.append({
                        "icao24": s[0],
                        "callsign": (s[1] or "").strip(),
                        "origin": s[2] or "",
                        "lat": s[6],
                        "lng": s[5],
                        "altitude": s[7] or 0,
                        "velocity": s[9] or 0,
                        "heading": s[10] or 0,
                        "vertical_rate": s[11] or 0,
                    })
            return result
