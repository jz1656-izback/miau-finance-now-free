from abc import ABC, abstractmethod
from typing import Any, Optional


class BrokerBase(ABC):
    name: str = ""
    display_name: str = ""

    @abstractmethod
    async def get_account(self) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_positions(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        ...
