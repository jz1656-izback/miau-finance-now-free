import logging
logger = logging.getLogger(__name__)

NAME = "Digital Yen (DCJPY)"
CODE = "DCJPY"
CENTRAL_BANK = "Bank of Japan"
STATUS = "trial"

async def get_info() -> dict:
    return {
        "name": NAME, "code": CODE, "central_bank": CENTRAL_BANK, "status": STATUS,
        "issuance": "¥3.5B", "circulation": "¥1.8B", "wallets_active": 620000,
        "interest_rate_pct": 0.10, "launch_date": "2026-09-01", "trial_end": "2027-03-01",
        "pegged_to": "JPY", "exchange_rate": 1.0,
    }

async def get_rates() -> dict:
    return {
        "jpy_usd": 0.0066, "jpy_eur": 0.0062, "jpy_gbp": 0.0052, "jpy_cny": 0.047, "jpy_krw": 8.72,
    }

async def simulate_transfer(amount_jpy: float, to_currency: str) -> dict:
    rates = await get_rates()
    rate = rates.get(f"jpy_{to_currency.lower()}", 0.0066)
    return {
        "from": "DCJPY", "to": to_currency.upper(), "amount": amount_jpy,
        "rate": rate, "converted": round(amount_jpy * rate, 2),
        "fee_jpy": round(amount_jpy * 0.0002, 4), "settlement_time": "2-10 min",
    }
