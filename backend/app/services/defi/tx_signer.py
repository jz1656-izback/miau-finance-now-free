"""Real transaction signing via web3.py — sign messages and send transactions."""
from __future__ import annotations

import logging
import os
from typing import Any, Optional
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account

logger = logging.getLogger(__name__)

ETH_RPC_URL = os.getenv("ETH_RPC_URL", "")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "")
MERCHANT_KEY = os.getenv("CRYPTO_MERCHANT_EVM_PRIVATE_KEY", "")

_web3_instances: dict[str, Web3] = {}


def _get_web3(chain: str = "ethereum") -> Optional[Web3]:
    if chain in _web3_instances:
        return _web3_instances[chain]
    urls = {
        "ethereum": ETH_RPC_URL,
        "polygon": POLYGON_RPC_URL,
    }
    url = urls.get(chain, ETH_RPC_URL)
    if not url:
        return None
    try:
        w3 = Web3(Web3.HTTPProvider(url))
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        if w3.is_connected():
            _web3_instances[chain] = w3
            return w3
    except Exception as e:
        logger.warning("Failed to connect to %s RPC: %s", chain, e)
    return None


async def sign_message(topic: str, message: str, address: str) -> dict[str, Any]:
    if MERCHANT_KEY:
        try:
            acct = Account.from_key(MERCHANT_KEY)
            signed = Account.sign_message(
                Account._add_eth_prefix(message) if not message.startswith("\x19") else message,
                acct.key,
            )
            sig = signed.signature.hex()
            return {
                "topic": topic,
                "address": acct.address,
                "message": message,
                "signature": f"0x{sig}",
                "status": "signed",
            }
        except Exception as e:
            logger.error("sign_message failed: %s", e)
    return {
        "topic": topic,
        "address": address,
        "message": message,
        "signature": "0x" + "ff" * 32,
        "status": "simulated",
    }


async def send_transaction(topic: str, tx: dict[str, Any]) -> dict[str, Any]:
    w3 = _get_web3(tx.get("chain", "ethereum"))
    if w3 and MERCHANT_KEY:
        try:
            acct = Account.from_key(MERCHANT_KEY)
            nonce = w3.eth.get_transaction_count(acct.address)
            gas_price = w3.eth.gas_price
            chain_id = w3.eth.chain_id
            built_tx = {
                "nonce": nonce,
                "to": Web3.to_checksum_address(tx["to"]) if isinstance(tx.get("to"), str) else tx.get("to"),
                "value": tx.get("value", 0),
                "gas": tx.get("gas", 21000),
                "gasPrice": tx.get("gasPrice", gas_price),
                "chainId": chain_id,
            }
            if "data" in tx:
                built_tx["data"] = tx["data"]
            signed = acct.sign_transaction(built_tx)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            return {
                "topic": topic,
                "tx_hash": tx_hash.hex(),
                "status": "sent",
                "from": acct.address,
                "to": built_tx["to"],
                "value": built_tx["value"],
            }
        except Exception as e:
            logger.error("send_transaction failed: %s", e)
    return {
        "topic": topic,
        "tx_hash": "0x" + "aa" * 32,
        "status": "simulated",
        "from": tx.get("from", ""),
        "to": tx.get("to", ""),
        "value": tx.get("value", 0),
    }


async def get_eth_balance(address: str, chain: str = "ethereum") -> float:
    w3 = _get_web3(chain)
    if not w3:
        return 0.0
    try:
        addr = Web3.to_checksum_address(address)
        bal_wei = w3.eth.get_balance(addr)
        return float(w3.from_wei(bal_wei, "ether"))
    except Exception as e:
        logger.warning("get_eth_balance failed: %s", e)
        return 0.0


async def get_usdc_balance(address: str, chain: str = "ethereum") -> float:
    USDC_ADDRESSES = {
        "ethereum": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    }
    addr = USDC_ADDRESSES.get(chain)
    if not addr:
        return 0.0
    w3 = _get_web3(chain)
    if not w3:
        return 0.0
    try:
        erc20_abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
        contract = w3.eth.contract(address=Web3.to_checksum_address(addr), abi=erc20_abi)
        bal = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        return bal / 10 ** 6
    except Exception as e:
        logger.warning("get_usdc_balance failed: %s", e)
        return 0.0
