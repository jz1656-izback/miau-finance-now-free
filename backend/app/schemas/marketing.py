from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class TrackEvent(BaseModel):
    event: str = Field(..., description="Event type: page_view, click, conversion, timing")
    path: str
    referrer: Optional[str] = None
    session_id: str
    host: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    utm_term: Optional[str] = None
    utm_content: Optional[str] = None
    screen_width: Optional[int] = None
    screen_height: Optional[int] = None
    language: Optional[str] = None
    conversion_type: Optional[str] = None
    conversion_value: Optional[float] = None
    metadata: Optional[dict[str, Any]] = None
    timestamp: Optional[datetime] = None


class PageViewResponse(BaseModel):
    id: str
    path: str
    referrer: Optional[str] = None
    session_id: str
    host: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    timestamp: datetime


class AnalyticsOverview(BaseModel):
    total_visitors: int
    total_page_views: int
    bounce_rate: float
    avg_session_duration: float
    conversion_rate: float
    active_sessions: int
    total_conversions: int


class PageAnalytics(BaseModel):
    path: str
    views: int
    unique_views: int
    avg_time_on_page: float
    bounce_rate: float
    exits: int


class ReferrerAnalytics(BaseModel):
    source: str
    visitors: int
    page_views: int
    bounce_rate: float
    conversions: int


class CampaignAnalytics(BaseModel):
    campaign: str
    source: str
    medium: str
    visitors: int
    conversions: int
    conversion_rate: float
    revenue: float


class TrendPoint(BaseModel):
    date: str
    visitors: int
    page_views: int
    conversions: int


class ConversionResponse(BaseModel):
    id: str
    conversion_type: str
    page: Optional[str] = None
    referrer: Optional[str] = None
    value: Optional[float] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    timestamp: datetime


class SEOPageCheck(BaseModel):
    path: str
    title: Optional[str] = None
    description: Optional[str] = None
    og_title: Optional[str] = None
    og_description: Optional[str] = None
    has_og_image: bool = False
    has_canonical: bool = False
    status_code: int = 200
    issues: list[str] = []


class CreateLink(BaseModel):
    url: str
    slug: Optional[str] = None
    title: Optional[str] = None
    campaign: Optional[str] = None
    source: Optional[str] = None
    medium: Optional[str] = None


class CreateExperiment(BaseModel):
    name: str
    page: str
    description: Optional[str] = None
    metric: str = "conversion_rate"
    min_sample_size: int = 1000


class CreateExperimentVariant(BaseModel):
    name: str
    is_control: bool = False
    traffic_pct: float = 50.0
    description: Optional[str] = None


class CreateAlert(BaseModel):
    name: str
    metric: str
    condition: str
    threshold: float
    period_minutes: int = 60
    channel: str = "dashboard"
    webhook_url: Optional[str] = None
