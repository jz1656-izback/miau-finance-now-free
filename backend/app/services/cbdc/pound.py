import logging
logger = logging.getLogger(__name__)

NAME = "Digital Pound (Britcoin)"
CODE = "GBP+"
CENTRAL_BANK = "Bank of England"
STATUS = "development"

async def get_info() -> dict:
    return {
        "name": NAME, "code": CODE, "central_bank": CENTRAL_BANK, "status": STATUS,
        "issuance": "£800M (pilot)", "circulation": "£250M", "wallets_active": 120000,
        "interest_rate_pct": 4.25, "launch_date": "2027-06-01", "pegged_to": "GBP",
        "exchange_rate": 1.0, "privacy_tier": "programmable",
    }

async def get_rates() -> dict:
    return {
        "gbp_usd": 1.26, "gbp_eur": 1.16, "gbp_jpy": 190.8, "gbp_cny": 9.15, "gbp_chf": 1.09,
    }

async def simulate_transfer(amount_gbp: float, to_currency: str) -> dict:
    rates = await get_rates()
    rate = rates.get(f"gbp_{to_currency.lower()}", 1.26)
    return {
        "from": "GBP+", "to": to_currency.upper(), "amount": amount_gbp,
        "rate": rate, "converted": round(amount_gbp * rate, 2),
        "fee_gbp": round(amount_gbp * 0.0008, 4), "settlement_time": "1-3 min",
    }
