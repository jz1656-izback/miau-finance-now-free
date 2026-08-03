"""Crypto Payment Processing — generate addresses, monitor, confirm subscriptions."""
import logging
import os
import hashlib
from datetime import datetime, timezone
from typing import Optional

from web3 import Web3
from eth_account import Account

logger = logging.getLogger(__name__)

MERCHANT_MNEMONIC = os.getenv("CRYPTO_MERCHANT_MNEMONIC", "")
MERCHANT_KEY = os.getenv("CRYPTO_MERCHANT_EVM_PRIVATE_KEY", "")

SUPPORTED_CHAINS = {
    "ethereum": {"rpc": os.getenv("ETH_RPC_URL", ""), "decimals": 18, "explorer": "https://etherscan.io/tx/"},
    "polygon": {"rpc": os.getenv("POLYGON_RPC_URL", ""), "decimals": 18, "explorer": "https://polygonscan.com/tx/"},
    "arbitrum": {"rpc": os.getenv("ARBITRUM_RPC_URL", ""), "decimals": 18, "explorer": "https://arbiscan.io/tx/"},
    "optimism": {"rpc": os.getenv("OPTIMISM_RPC_URL", ""), "decimals": 18, "explorer": "https://optimistic.etherscan.io/tx/"},
    "base": {"rpc": os.getenv("BASE_RPC_URL", ""), "decimals": 18, "explorer": "https://basescan.org/tx/"},
}

USDC_ADDRESSES = {
    "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    "arbitrum": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "optimism": "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85",
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
}

TIER_PRICES_ETH = {
    "trial": Web3.to_wei(0.005, "ether"),   # ~€2.50 per seat
    "starter": Web3.to_wei(0.025, "ether"),  # ~€25 per seat
    "pro": Web3.to_wei(0.05, "ether"),      # ~€50 per seat
    "fund": Web3.to_wei(0.075, "ether"),    # ~€75 per seat
    "enterprise": Web3.to_wei(0.7, "ether"),  # ~€349.84/user/mo
}

TIER_PRICES_USDC = {
    "trial": 2.50 * 10 ** 6,   # 2.50 USDC
    "starter": 25 * 10 ** 6,   # 25 USDC
    "pro": 50 * 10 ** 6,       # 50 USDC
    "fund": 75 * 10 ** 6,      # 75 USDC
    "enterprise": 349.84 * 10 ** 6, # 349.84 USDC/user/mo
}

_payment_addresses: dict[str, dict] = {}  # invoice_id -> address info (in-memory; production needs DB)


def generate_payment_address(invoice_id: str, chain: str = "ethereum", currency: str = "ETH") -> dict:
    """Generate deterministic deposit address scoped to an invoice."""
    if not MERCHANT_KEY:
        return {"error": "CRYPTO_MERCHANT_EVM_PRIVATE_KEY not set"}

    acct = Account.from_key(MERCHANT_KEY)
    # Generate deterministic sub-address from invoice_id
    seed = hashlib.sha256(f"{invoice_id}:{acct.address}".encode()).hexdigest()
    sub_account = Account.from_key(seed)

    if currency == "USDC":
        expected_amount = TIER_PRICES_USDC.get("pro", 99 * 10 ** 6)
    else:
        expected_amount = TIER_PRICES_ETH.get("pro", Web3.to_wei(0.15, "ether"))

    info = {
        "invoice_id": invoice_id,
        "address": sub_account.address,
        "chain": chain,
        "currency": currency,
        "expected_amount": expected_amount,
        "received_amount": 0,
        "confirmations": 0,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _payment_addresses[invoice_id] = info
    return info


def get_payment_status(invoice_id: str) -> Optional[dict]:
    return _payment_addresses.get(invoice_id)


async def check_payment(invoice_id: str, chain: str = "ethereum") -> dict:
    """Check if a payment has been received for an invoice."""
    payment = _payment_addresses.get(invoice_id)
    if not payment:
        return {"error": "No payment address generated for this invoice"}

    rpc_url = SUPPORTED_CHAINS.get(chain, {}).get("rpc", "")
    if not rpc_url:
        return {"error": f"No RPC for chain: {chain}"}

    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            return {"error": f"Cannot connect to {chain}"}

        address = Web3.to_checksum_address(payment["address"])

        if payment["currency"] == "USDC":
            usdc_addr = USDC_ADDRESSES.get(chain)
            if not usdc_addr:
                return {"error": f"USDC not supported on {chain}"}
            erc20_abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
            contract = w3.eth.contract(address=Web3.to_checksum_address(usdc_addr), abi=erc20_abi)
            balance = contract.functions.balanceOf(address).call()
        else:
            balance = w3.eth.get_balance(address)

        explorer = SUPPORTED_CHAINS.get(chain, {}).get("explorer", "")
        confirmed = balance >= payment["expected_amount"]
        if confirmed:
            payment["status"] = "confirmed"
            payment["received_amount"] = balance

        return {
            "invoice_id": invoice_id,
            "address": payment["address"],
            "expected": payment["expected_amount"],
            "received": balance,
            "currency": payment["currency"],
            "status": payment["status"],
            "confirmed": confirmed,
            "explorer_url": f"{explorer}{address}" if explorer else "",
        }
    except Exception as e:
        logger.error("check_payment failed: %s", e)
        return {"error": str(e)}
