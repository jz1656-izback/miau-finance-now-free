import logging
logger = logging.getLogger(__name__)

NAME = "Digital Yuan (e-CNY)"
CODE = "ECNY"
CENTRAL_BANK = "People's Bank of China"
STATUS = "active"

async def get_info() -> dict:
    return {
        "name": NAME, "code": CODE, "central_bank": CENTRAL_BANK, "status": STATUS,
        "issuance": "¥15.8B", "circulation": "¥12.3B", "wallets_active": 52000000,
        "interest_rate_pct": 1.75, "launch_date": "2024-01-01", "pegged_to": "CNY",
        "exchange_rate": 1.0, "offline_capable": True,
    }

async def get_rates() -> dict:
    return {
        "cny_usd": 0.14, "cny_eur": 0.13, "cny_gbp": 0.11, "cny_jpy": 21.8, "cny_krw": 190.5,
    }

async def simulate_transfer(amount_cny: float, to_currency: str) -> dict:
    rates = await get_rates()
    rate = rates.get(f"cny_{to_currency.lower()}", 0.14)
    return {
        "from": "ECNY", "to": to_currency.upper(), "amount": amount_cny,
        "rate": rate, "converted": round(amount_cny * rate, 2),
        "fee_cny": round(amount_cny * 0.0001, 4), "settlement_time": "1-5 min",
    }
