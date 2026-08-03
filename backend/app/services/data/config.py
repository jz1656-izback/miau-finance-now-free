"""Config-driven endpoint management.

Loads provider configurations from a YAML file with URLs,
auth methods, rate limits, and fallback chains.

Also provides inline PROVIDER_CONFIGS for code-based configuration.
"""
import os
from dataclasses import dataclass, field
from typing import Any, Optional
from pydantic import BaseModel


class ProviderEndpoint(BaseModel):
    url: str
    method: str = "GET"
    headers: dict[str, str] = {}
    params: dict[str, str] = {}
    auth_type: Optional[str] = None  # "header", "query", "basic"
    auth_key: Optional[str] = None
    fallback: Optional[str] = None  # provider name to fall back to


class ProviderConfig(BaseModel):
    name: str
    display_name: str
    enabled: bool = True
    requires_key: bool = False
    rate_limit_per_minute: int = 60
    base_url: str = ""
    endpoints: dict[str, ProviderEndpoint] = {}
    capabilities: list[str] = []


class DataSourceConfig(BaseModel):
    providers: list[ProviderConfig] = []


def load_config(path: Optional[str] = None) -> DataSourceConfig:
    """Load data source configuration from YAML or return defaults.

    Falls back to an empty config if the file doesn't exist.
    """
    import yaml

    config_path = path or os.getenv(
        "DATA_SOURCE_CONFIG",
        "backend/app/services/data/providers.yaml",
    )
    try:
        with open(config_path) as f:
            raw = yaml.safe_load(f)
            if raw and "providers" in raw:
                return DataSourceConfig(**raw)
    except (FileNotFoundError, yaml.YAMLError, TypeError):
        pass
    return DataSourceConfig()


# ── Inline Configuration ───────────────────────────────────────

@dataclass
class ProviderInlineConfig:
    name: str
    base_url: str
    requires_key: bool = False
    env_key_var: Optional[str] = None
    rate_limit_per_minute: int = 60
    default_key: Optional[str] = None
    fallbacks: list[str] = field(default_factory=list)
    enabled: bool = True


PROVIDER_CONFIGS: dict[str, ProviderInlineConfig] = {
    "finnhub": ProviderInlineConfig(
        name="finnhub",
        base_url="https://finnhub.io/api/v1",
        requires_key=True,
        env_key_var="FINNHUB_API_KEY",
        rate_limit_per_minute=60,
        fallbacks=["yahoo", "stockprices"],
    ),
    "securitiesdb": ProviderInlineConfig(
        name="securitiesdb",
        base_url="https://securitiesdb.com/api/v1",
        requires_key=False,
        rate_limit_per_minute=100,
    ),
    "stockprices": ProviderInlineConfig(
        name="stockprices",
        base_url="https://stockprices.dev/api",
        requires_key=False,
        rate_limit_per_minute=9999,
        fallbacks=["yahoo"],
    ),
    "dumbstock": ProviderInlineConfig(
        name="dumbstock",
        base_url="https://dumbstockapi.com",
        requires_key=False,
        rate_limit_per_minute=60,
    ),
    "twelvedata": ProviderInlineConfig(
        name="twelvedata",
        base_url="https://api.twelvedata.com",
        requires_key=True,
        env_key_var="TWELVEDATA_API_KEY",
        rate_limit_per_minute=800,
        fallbacks=["yahoo", "alpha_vantage"],
    ),
    "alpha_vantage": ProviderInlineConfig(
        name="alpha_vantage",
        base_url="https://www.alphavantage.co/query",
        requires_key=True,
        env_key_var="ALPHA_VANTAGE_API_KEY",
        rate_limit_per_minute=5,
        fallbacks=["yahoo"],
    ),
    "defillama": ProviderInlineConfig(
        name="defillama",
        base_url="https://api.llama.fi",
        requires_key=False,
        rate_limit_per_minute=300,
    ),
    "coinpaprika": ProviderInlineConfig(
        name="coinpaprika",
        base_url="https://api.coinpaprika.com/v1",
        requires_key=True,
        env_key_var="COINPAPRIKA_API_KEY",
        rate_limit_per_minute=30,
        fallbacks=["coingecko"],
    ),
    "blocknative": ProviderInlineConfig(
        name="blocknative",
        base_url="https://api.blocknative.com/gasprices",
        requires_key=False,
        rate_limit_per_minute=12,
        fallbacks=["etherscan"],
    ),
    "etherscan": ProviderInlineConfig(
        name="etherscan",
        base_url="https://api.etherscan.io/api",
        requires_key=True,
        env_key_var="ETHERSCAN_API_KEY",
        rate_limit_per_minute=5,
    ),
    "frankfurter": ProviderInlineConfig(
        name="frankfurter",
        base_url="https://api.frankfurter.dev",
        requires_key=False,
        rate_limit_per_minute=9999,
    ),
    "bls": ProviderInlineConfig(
        name="bls",
        base_url="https://api.bls.gov/publicAPI/v2",
        requires_key=True,
        env_key_var="BLS_API_KEY",
        rate_limit_per_minute=30,
        fallbacks=["fred"],
    ),
    "eia": ProviderInlineConfig(
        name="eia",
        base_url="https://api.eia.gov/v2",
        requires_key=True,
        env_key_var="EIA_API_KEY",
        rate_limit_per_minute=30,
    ),
    "yahoo": ProviderInlineConfig(
        name="yahoo",
        base_url="https://query1.finance.yahoo.com",
        requires_key=False,
        rate_limit_per_minute=30,
    ),
    "coingecko": ProviderInlineConfig(
        name="coingecko",
        base_url="https://api.coingecko.com/api/v3",
        requires_key=False,
        rate_limit_per_minute=10,
    ),
    "fred": ProviderInlineConfig(
        name="fred",
        base_url="https://api.stlouisfed.org/fred",
        requires_key=True,
        env_key_var="FRED_API_KEY",
        rate_limit_per_minute=60,
    ),
}


def get_provider_config(name: str) -> ProviderInlineConfig:
    cfg = PROVIDER_CONFIGS.get(name)
    if not cfg:
        raise KeyError(f"Unknown provider: {name}")
    return cfg
