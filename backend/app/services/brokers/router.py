from decimal import Decimal
from typing import Optional
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import get_broker


async def route_order_to_broker(
    broker_name: str,
    action: str,
    ticker: str,
    quantity: Decimal,
    order_type: str = "MARKET",
    price: Optional[Decimal] = None,
) -> dict:
    cls = get_broker(broker_name)
    if not cls:
        raise ValueError(f"Unknown broker: {broker_name}")
    broker = cls()
    if action == "submit":
        return await broker.submit_order(ticker, quantity, order_type, price)
    elif action == "cancel":
        return await broker.cancel_order(ticker)
    elif action == "status":
        return await broker.get_order_status(ticker)
    raise ValueError(f"Unknown action: {action}")
