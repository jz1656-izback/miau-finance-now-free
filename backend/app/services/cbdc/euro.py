import logging
logger = logging.getLogger(__name__)

NAME = "Digital Euro (CBDC)"
CODE = "DEUR"
CENTRAL_BANK = "European Central Bank"
STATUS = "trial"

async def get_info() -> dict:
    return {
        "name": NAME, "code": CODE, "central_bank": CENTRAL_BANK, "status": STATUS,
        "issuance": "€1.2B", "circulation": "€890M", "wallets_active": 450000,
        "interest_rate_pct": 3.25, "launch_date": "2026-06-01", "trial_end": "2027-06-01",
        "pegged_to": "EUR", "exchange_rate": 1.0,
    }

async def get_rates() -> dict:
    return {
        "eur_usd": 1.08, "eur_gbp": 0.86, "eur_jpy": 162.5, "eur_cny": 7.85, "eur_chf": 0.94,
    }

async def simulate_transfer(amount_eur: float, to_currency: str) -> dict:
    rates = await get_rates()
    rate = rates.get(f"eur_{to_currency.lower()}", 1.0)
    return {
        "from": "DEUR", "to": to_currency.upper(), "amount": amount_eur,
        "rate": rate, "converted": round(amount_eur * rate, 2),
        "fee_eur": round(amount_eur * 0.001, 4), "settlement_time": "instant",
    }
