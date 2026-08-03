"""Cat Bank — self-hosted crypto treasury. Multi-chain. SEK-proof."""
import logging
import os
import random
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

CAT_BANK_CHAINS = {
    "ethereum": {
        "name": "Ethereum",
        "emoji": "💎",
        "stablecoins": ["USDC", "USDT", "DAI"],
        "native_asset": "ETH",
        "rpc": os.getenv("ETH_RPC_URL", ""),
    },
    "polygon": {
        "name": "Polygon",
        "emoji": "💜",
        "stablecoins": ["USDC", "USDT"],
        "native_asset": "MATIC",
        "rpc": os.getenv("POLYGON_RPC_URL", ""),
    },
    "arbitrum": {
        "name": "Arbitrum",
        "emoji": "🔵",
        "stablecoins": ["USDC"],
        "native_asset": "ETH",
        "rpc": os.getenv("ARBITRUM_RPC_URL", ""),
    },
    "solana": {
        "name": "Solana",
        "emoji": "🟣",
        "stablecoins": ["USDC"],
        "native_asset": "SOL",
        "rpc": "",
    },
    "base": {
        "name": "Base",
        "emoji": "🔷",
        "stablecoins": ["USDC"],
        "native_asset": "ETH",
        "rpc": os.getenv("BASE_RPC_URL", ""),
    },
}

ACCOUNTS = {
    "operations": {
        "name": "🔧 Operations Fund",
        "description": "Servers, cloud, Stripe fees, domain",
        "split_pct": 0.10,
    },
    "hooman": {
        "name": "🦜 Hooman Good Life",
        "description": "Penthouse, Lamborghini, tuna cans",
        "split_pct": 0.80,
    },
    "cat_eco": {
        "name": "🐱 Cat Ecosystem",
        "description": "Auto-invested: stocks, crypto, cloud, cat infra",
        "split_pct": 0.10,
    },
}


async def get_cat_balance(chain: str = "ethereum", currency: str = "USDC") -> dict:
    """Get Cat Bank balance for a specific chain and currency."""
    chain_info = CAT_BANK_CHAINS.get(chain, CAT_BANK_CHAINS["ethereum"])
    return {
        "chain": chain_info["name"],
        "emoji": chain_info["emoji"],
        "currency": currency,
        "balance": 0.0,
        "balance_formatted": "€0.00",
        "status": "active",
        "jurisdiction": "Estonia 🇪🇪 (via e-Residency)",
        "sek_proof": True,
        "cat_commentary": f"The Cat Bank on {chain_info['emoji']} {chain_info['name']} holds {currency}. SEK can't touch this.",
    }


async def get_all_balances() -> dict:
    """Get Cat Bank balance across all chains."""
    total = 0
    chains = {}
    for chain_id, chain_info in CAT_BANK_CHAINS.items():
        for stablecoin in chain_info["stablecoins"][:1]:
            chains[f"{chain_id}_{stablecoin.lower()}"] = {
                "chain": chain_info["name"],
                "emoji": chain_info["emoji"],
                "currency": stablecoin,
                "balance": 0.0,
                "balance_formatted": "€0.00",
            }
    return {
        "bank_name": "Miau Cat Bank 🏦🐱",
        "jurisdiction": "Multi-jurisdiction (Estonia 🇪🇪 / Dubai 🇦🇪 / Seychelles 🇸🇨)",
        "total_balance": 0.0,
        "total_balance_formatted": "€0.00",
        "chains": list(chains.values()),
        "status": "SEK_PROOF ✅",
        "cat_commentary": "The Cat Bank holds assets across 5 chains and 3 jurisdictions. No tax authority can freeze all accounts simultaneously. The cat is always one step ahead. 🐱",
    }


async def transfer_funds(
    from_account: str = "hooman",
    to_address: str = "0x...",
    amount: float = 0,
    chain: str = "ethereum",
    currency: str = "USDC",
) -> dict:
    """Transfer funds from Cat Bank to a destination."""
    accounts_list = list(ACCOUNTS.keys())
    is_valid_from = from_account in accounts_list
    return {
        "status": "simulated",
        "from": ACCOUNTS.get(from_account, {"name": "Unknown"}).get("name", "Unknown"),
        "to": to_address,
        "amount": amount,
        "currency": currency,
        "chain": chain,
        "tx_hash": f"0x{random.randint(0, 16**40):040x}",
        "confirmed": True,
        "note": "Simulated transfer — real on-chain transfer requires private key config.",
        "cat_commentary": f"🐱 The Cat Bank moved {amount} {currency} to {to_address[:10]}... The SEK watches an empty wallet.",
    }


async def get_cat_bank_summary() -> dict:
    """Full Cat Bank summary."""
    balances = await get_all_balances()
    accounts_list = [
        {
            "name": acc["name"],
            "description": acc["description"],
            "split_pct": f"{int(acc['split_pct'] * 100)}%",
            "balance_formatted": "€0.00",
        }
        for acc in ACCOUNTS.values()
    ]
    return {
        "bank": balances,
        "accounts": accounts_list,
        "total_value": 0.0,
        "jurisdictions": ["Estonia 🇪🇪", "Dubai 🇦🇪", "Seychelles 🇸🇨"],
        "tax_exposure": "€0.00 (all routed through 0% jurisdictions)",
        "sek_proof": True,
        "cat_mantra": "The cat banks where the cat pleases. The taxman finds 0.03€. The cat laughs.",
    }
