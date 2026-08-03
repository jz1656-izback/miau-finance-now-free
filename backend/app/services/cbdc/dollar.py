import logging
logger = logging.getLogger(__name__)

NAME = "Digital Dollar (FedNow + CBDC)"
CODE = "DUSD"
CENTRAL_BANK = "Federal Reserve"
STATUS = "development"

async def get_info() -> dict:
    return {
        "name": NAME, "code": CODE, "central_bank": CENTRAL_BANK, "status": STATUS,
        "issuance": "500M (pilot)", "circulation": "120M", "wallets_active": 85000,
        "interest_rate_pct": 4.50, "launch_date": "2027-01-01", "pegged_to": "USD",
        "exchange_rate": 1.0, "fednow_integrated": True,
    }

async def get_rates() -> dict:
    return {
        "usd_eur": 0.93, "usd_gbp": 0.79, "usd_jpy": 151.0, "usd_cny": 7.24, "usd_chf": 0.87,
    }

async def simulate_transfer(amount_usd: float, to_currency: str) -> dict:
    rates = await get_rates()
    rate = rates.get(f"usd_{to_currency.lower()}", 0.93)
    return {
        "from": "DUSD", "to": to_currency.upper(), "amount": amount_usd,
        "rate": rate, "converted": round(amount_usd * rate, 2),
        "fee_usd": round(amount_usd * 0.0005, 4), "settlement_time": "instant (FedNow)",
    }
