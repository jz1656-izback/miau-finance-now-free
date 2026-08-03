import threading
from dataclasses import dataclass, field
from typing import Optional
from decimal import Decimal
from app.models import OrderStatus


@dataclass
class OrderBookEntry:
    order_id: str
    portfolio_id: str
    instrument_id: str
    side: str
    quantity: Decimal
    price: Optional[Decimal]
    stop_price: Optional[Decimal]
    status: OrderStatus
    created_at: str


class OrderBook:
    def __init__(self):
        self._lock = threading.Lock()
        self._orders: dict[str, OrderBookEntry] = {}
        self._buys: list[OrderBookEntry] = []
        self._sells: list[OrderBookEntry] = []
        self._portfolio_orders: dict[str, set[str]] = {}

    def add_order(self, entry: OrderBookEntry) -> None:
        with self._lock:
            self._orders[entry.order_id] = entry
            if entry.side == "BUY":
                self._buys.append(entry)
                self._buys.sort(key=lambda o: o.price or 0, reverse=True)
            else:
                self._sells.append(entry)
                self._sells.sort(key=lambda o: o.price or 0)

            if entry.portfolio_id not in self._portfolio_orders:
                self._portfolio_orders[entry.portfolio_id] = set()
            self._portfolio_orders[entry.portfolio_id].add(entry.order_id)

    def update_status(self, order_id: str, status: OrderStatus) -> bool:
        with self._lock:
            if order_id not in self._orders:
                return False
            self._orders[order_id].status = status
            return True

    def remove_order(self, order_id: str) -> Optional[OrderBookEntry]:
        with self._lock:
            entry = self._orders.pop(order_id, None)
            if not entry:
                return None
            self._buys = [o for o in self._buys if o.order_id != order_id]
            self._sells = [o for o in self._sells if o.order_id != order_id]
            if entry.portfolio_id in self._portfolio_orders:
                self._portfolio_orders[entry.portfolio_id].discard(order_id)
            return entry

    def get_order(self, order_id: str) -> Optional[OrderBookEntry]:
        with self._lock:
            return self._orders.get(order_id)

    def get_open_orders(self, portfolio_id: Optional[str] = None) -> list[OrderBookEntry]:
        with self._lock:
            if portfolio_id:
                ids = self._portfolio_orders.get(portfolio_id, set())
                return [self._orders[oid] for oid in ids if oid in self._orders and self._orders[oid].status in (OrderStatus.PENDING, OrderStatus.SUBMITTED)]
            return [o for o in self._orders.values() if o.status in (OrderStatus.PENDING, OrderStatus.SUBMITTED)]

    def match_orders(self, instrument_id: str) -> list[tuple[OrderBookEntry, OrderBookEntry, Decimal]]:
        matches = []
        with self._lock:
            instrument_buys = [o for o in self._buys if o.instrument_id == instrument_id and o.status == OrderStatus.SUBMITTED]
            instrument_sells = [o for o in self._sells if o.instrument_id == instrument_id and o.status == OrderStatus.SUBMITTED]

            for buy in instrument_buys:
                for sell in instrument_sells:
                    buy_price = buy.price or Decimal("Infinity")
                    sell_price = sell.price or Decimal("0")
                    if buy_price >= sell_price:
                        fill_qty = min(buy.quantity, sell.quantity)
                        matches.append((buy, sell, fill_qty))
                        break
        return matches
