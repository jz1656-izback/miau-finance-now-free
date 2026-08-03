from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


class PaperPortfolioCreate(BaseModel):
    name: str
    initial_cash: Decimal = Decimal("100000.00")


class PaperPortfolioResponse(BaseModel):
    id: str
    user_id: str
    name: str
    initial_cash: str
    current_cash: str
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}


class PaperTradeResponse(BaseModel):
    id: str
    paper_portfolio_id: str
    instrument_id: str
    side: str
    quantity: str
    price: str
    commission: str
    slippage: str
    tca_cost: str
    executed_at: Optional[str] = None

    model_config = {"from_attributes": True}
