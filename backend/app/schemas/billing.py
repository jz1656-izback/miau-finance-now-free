from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubscriptionCreate(BaseModel):
    tier: str = "pro"
    seats: int = 1


class SubscriptionResponse(BaseModel):
    id: str
    user_id: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    tier: str
    status: str
    trial_ends_at: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    seats: Optional[int] = 1
    barks_remaining: Optional[int] = 0
    barks_used: Optional[int] = 0
    on_premise_license: Optional[bool] = False
    license_key: Optional[str] = None
    created_at: Optional[datetime] = None


class CheckoutRequest(BaseModel):
    tier: str = "pro"
    seats: int = 1
    success_url: str = "http://localhost:5173/billing/success"
    cancel_url: str = "http://localhost:5173/billing/cancel"


class CheckoutResponse(BaseModel):
    session_url: str


class WebhookResponse(BaseModel):
    status: str = "ok"


class UsageRecordResponse(BaseModel):
    id: str
    user_id: str
    api_key_id: Optional[str] = None
    date: str
    request_count: int
    data_transfer_bytes: int
    created_at: Optional[datetime] = None


class PricingTier(BaseModel):
    id: str
    name: str
    description: str
    amount_monthly: int
    amount_yearly: int
    currency: str
    features: list[str]
    requests_per_minute: int
    requests_per_hour: int
    concurrent_connections: int
    data_providers: int
    barks_included: Optional[int] = 0
    seat_based: Optional[bool] = False
    original_amount_monthly: Optional[int] = None
    original_amount_yearly: Optional[int] = None
    discount_percent: Optional[int] = None
    discount_message: Optional[str] = None

class PricingResponse(BaseModel):
    tiers: list[PricingTier]
    discount_active: Optional[bool] = False
    discount_percent: Optional[int] = None
    discount_message: Optional[str] = None
    discount_expiry: Optional[str] = None

class BarkRequestCreate(BaseModel):
    title: str
    description: str = ""

class BarkRequestResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    status: str
    bark_year: int
    created_at: Optional[datetime] = None

class LicenseKeyResponse(BaseModel):
    license_key: str
    tier: str
    seats: int
    expires_at: Optional[datetime] = None
    on_premise: bool = True

class InvoiceResponse(BaseModel):
    id: str
    user_id: str
    stripe_invoice_id: Optional[str] = None
    amount: str
    currency: str
    status: str
    period_start: str
    period_end: str
    paid_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
