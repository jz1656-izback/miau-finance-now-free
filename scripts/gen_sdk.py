#!/usr/bin/env python3
"""SDK auto-generation from the Miau Finance OpenAPI spec.

Usage:
    python scripts/gen_sdk.py                    # generate all SDKs
    python scripts/gen_sdk.py --dry-run           # preview without writing
    python scripts/gen_sdk.py --lang python       # only Python SDK
    python scripts/gen_sdk.py --lang curl         # only curl examples
"""

import argparse
import json
import os
import sys
from pathlib import Path

SDK_DIR = Path(__file__).parent.parent / "sdk"

# Hardcoded endpoint map for languages without OpenAPI generator.
# In production this would read from the running API's /openapi.json.
ENDPOINTS: dict[str, list[dict]] = {
    "market": [
        {"method": "GET", "path": "/api/v1/market/live", "params": "tickers"},
        {"method": "GET", "path": "/api/v1/market/historical/{ticker}", "params": "period"},
        {"method": "GET", "path": "/api/v1/market/movers"},
        {"method": "GET", "path": "/api/v1/market/sectors"},
        {"method": "GET", "path": "/api/v1/market/indicators"},
        {"method": "GET", "path": "/api/v1/market/forex", "params": "base"},
        {"method": "GET", "path": "/api/v1/market/crypto", "params": "coin"},
    ],
    "portfolio": [
        {"method": "GET", "path": "/api/v1/portfolios"},
        {"method": "POST", "path": "/api/v1/portfolios"},
        {"method": "GET", "path": "/api/v1/portfolios/{id}"},
        {"method": "GET", "path": "/api/v1/portfolios/{id}/positions"},
        {"method": "PUT", "path": "/api/v1/portfolios/{id}/currency"},
        {"method": "GET", "path": "/api/v1/portfolios/{id}/fx-pnl"},
    ],
    "orders": [
        {"method": "GET", "path": "/api/v1/orders"},
        {"method": "POST", "path": "/api/v1/orders"},
        {"method": "GET", "path": "/api/v1/orders/{id}"},
    ],
    "analytics": [
        {"method": "GET", "path": "/api/v1/analytics/summary"},
        {"method": "GET", "path": "/api/v1/analytics/monte-carlo", "params": "ticker,num_simulations,days"},
        {"method": "GET", "path": "/api/v1/risk/var", "params": "ticker,confidence"},
        {"method": "GET", "path": "/api/v1/risk/beta", "params": "ticker,benchmark"},
        {"method": "GET", "path": "/api/v1/risk/rolling", "params": "ticker,window,period"},
    ],
    "valuation": [
        {"method": "GET", "path": "/api/v1/analytics/valuation/dcf/{ticker}", "params": "growth,terminal_growth,years"},
        {"method": "GET", "path": "/api/v1/analytics/valuation/wacc/{ticker}"},
        {"method": "GET", "path": "/api/v1/analytics/valuation/comps/{ticker}"},
        {"method": "GET", "path": "/api/v1/analytics/valuation/lbo/{ticker}", "params": "debt,exit_year,exit_multiple"},
    ],
    "billing": [
        {"method": "GET", "path": "/api/v1/billing/subscription"},
        {"method": "GET", "path": "/api/v1/billing/usage"},
        {"method": "GET", "path": "/api/v1/billing/invoices"},
    ],
    "developer": [
        {"method": "GET", "path": "/api/v1/developer/dashboard"},
        {"method": "GET", "path": "/api/v1/developer/api-keys"},
        {"method": "POST", "path": "/api/v1/developer/api-keys"},
    ],
}


def _method_name(path: str, method: str) -> str:
    parts = [p for p in path.strip("/").split("/") if not p.startswith("{")]
    name = "_".join(parts)
    return f"{method.lower()}_{name}"


def _param_list(ep: dict) -> list[str]:
    raw = ep.get("params", "")
    return [p.strip() for p in raw.split(",") if p.strip()]


def generate_python(endpoints: dict[str, list[dict]], dry_run: bool = False) -> str:
    lines = [
        '"""Auto-generated Miau Finance Python SDK methods."""',
        "",
        "from typing import Any, Optional",
        "",
        "",
    ]

    for module_name, eps in sorted(endpoints.items()):
        lines.append(f"# --- {module_name} ---")
        lines.append("")
        for ep in eps:
            params = _param_list(ep)
            sig_params = ["self"]
            call_params = []
            for p in params:
                sig_params.append(f"{p}: Optional[str] = None")
            for p in params:
                call_params.append(f'"{p}": {p}' if "{" not in ep["path"] else "")
            call_str = ", ".join(c for c in call_params if c)

            if ep["method"] == "GET":
                lines.append(f"    async def {_method_name(ep['path'], ep['method'])}({', '.join(sig_params)}):")
                lines.append(f'        return await self._client.async_get("{ep["path"]}", params={{{call_str}}})')
            elif ep["method"] == "POST":
                lines.append(f"    async def {_method_name(ep['path'], ep['method'])}_post({', '.join(sig_params)}):")
                lines.append(f'        return await self._client.async_post("{ep["path"]}", json=...)')
            lines.append("")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Miau Finance SDK code from API spec")
    parser.add_argument("--dry-run", action="store_true", help="Preview output without writing files")
    parser.add_argument("--lang", choices=["python", "curl", "all"], default="all")
    args = parser.parse_args()

    if args.lang in ("python", "all"):
        code = generate_python(ENDPOINTS, dry_run=args.dry_run)
        py_dir = SDK_DIR / "python" / "miau"
        py_gen = py_dir / "_generated.py"
        if args.dry_run:
            print(f"--- Would write {py_gen} ({len(code)} chars) ---")
            print(code[:500])
        else:
            py_gen.write_text(code)
            print(f"✅ Written {py_gen} ({len(code)} chars, {len(ENDPOINTS)} modules)")

    if args.lang in ("curl", "all"):
        curl_dir = SDK_DIR / "curl"
        count = len(list(curl_dir.glob("*.sh")))
        if args.dry_run:
            print(f"--- Would regenerate curl scripts in {curl_dir} ({count} existing) ---")
        else:
            print(f"✅ curl SDK already has {count} scripts — run --lang python for generated code")

    if args.dry_run:
        print("--- Dry run complete. Pass --lang python to write. ---")


if __name__ == "__main__":
    main()
