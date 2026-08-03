#!/usr/bin/env python3
"""Override map shard entries with curated REAL company data (HQ coords, industry).

The shards are built from DumbStockAPI (ticker+name only) + exchange→city jitter,
so every NASDAQ company lands in NYC with industry "Tech". The curated list
(companies_curated.py) has verified HQ coordinates + industries for ~600 known
companies — apply it as an override so TSLA shows Austin/Automotive, AAPL shows
Cupertino/Tech, etc.
"""
import json
import os
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # backend/scripts -> backend -> repo root
DATA_DIR = os.path.join(ROOT, "frontend", "public", "data")
sys.path.insert(0, os.path.join(ROOT, "backend", "app", "services", "data"))

from companies_curated import CURATED  # (ticker, name, industry, lat, lng, country, mc)

def main() -> None:
    overrides: dict[str, tuple] = {c[0].upper(): c for c in CURATED}
    total_overridden = 0
    for path in sorted(glob.glob(os.path.join(DATA_DIR, "companies_*.json"))):
        with open(path) as f:
            data = json.load(f)
        changed = 0
        for co in data.get("companies", []):
            ticker = (co.get("t") or "").upper()
            cur = overrides.get(ticker)
            if cur is None:
                continue
            co["n"] = cur[1]
            co["i"] = cur[2]
            co["lat"] = cur[3]
            co["lng"] = cur[4]
            co["co"] = cur[5]
            co["mc"] = cur[6]
            changed += 1
        if changed:
            with open(path, "w") as f:
                json.dump(data, f)
        print(f"{os.path.basename(path)}: {changed} entries overridden")
        total_overridden += changed
    print(f"Total overridden: {total_overridden}")

if __name__ == "__main__":
    main()
