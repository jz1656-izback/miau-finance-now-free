from pydantic import BaseModel
from typing import Optional


class ApiKeyCreate(BaseModel):
    name: str
    scopes: list[str] = ["read"]
    expires_in_days: Optional[int] = None


class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key_prefix: str
    scopes: dict | list = {}
    last_used_at: Optional[str] = None
    expires_at: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None


class ApiKeyCreatedResponse(ApiKeyResponse):
    key: str = ""
    raw_key: str


class WebhookEndpointCreate(BaseModel):
    url: str
    events: list[str] = []


class WebhookEndpointResponse(BaseModel):
    id: str
    url: str
    events: Optional[list] = None
    is_active: Optional[bool] = True
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}


class DeveloperDashboardResponse(BaseModel):
    tier: str = "free"
    tier_key_limit: int = 2
    tier_webhook_limit: int = 1
    total_api_keys: int = 0
    active_webhooks: int = 0
    requests_today: int = 0
    requests_this_month: int = 0
    api_keys: list[ApiKeyResponse] = []
    webhooks: list[WebhookEndpointResponse] = []

    model_config = {"from_attributes": True}
