from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from app.models import OrderType, OrderStatus


class OrderCreate(BaseModel):
    portfolio_id: str
    instrument_id: str
    order_type: OrderType
    side: str
    quantity: Decimal
    price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None

    @field_validator('side')
    @classmethod
    def validate_side(cls, v: str) -> str:
        upper = v.upper()
        if upper not in ('BUY', 'SELL'):
            raise ValueError('side must be BUY or SELL')
        return upper

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Optional[Decimal], info):
        if info.data.get('order_type') in (OrderType.LIMIT, OrderType.STOP_LIMIT) and v is None:
            raise ValueError('price is required for LIMIT and STOP_LIMIT orders')
        return v

    @field_validator('stop_price')
    @classmethod
    def validate_stop_price(cls, v: Optional[Decimal], info):
        if info.data.get('order_type') in (OrderType.STOP, OrderType.STOP_LIMIT, OrderType.TRAILING_STOP) and v is None:
            raise ValueError('stop_price is required for STOP, STOP_LIMIT, and TRAILING_STOP orders')
        return v


class OrderResponse(BaseModel):
    id: str
    portfolio_id: str
    instrument_id: str
    order_type: str
    side: str
    quantity: str
    price: Optional[str] = None
    stop_price: Optional[str] = None
    status: str
    filled_qty: str
    filled_avg_price: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    filled_at: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None
