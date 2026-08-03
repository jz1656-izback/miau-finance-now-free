from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class PageView(Base):
    """Page view tracking for marketing analytics."""
    __tablename__ = 'page_views'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String(2048), nullable=False)
    referrer = Column(Text)
    user_agent = Column(Text)
    ip_address = Column(String(45))
    country = Column(String(8))
    session_id = Column(String(64), nullable=False)
    host = Column(String(256))
    utm_source = Column(String(256))
    utm_medium = Column(String(256))
    utm_campaign = Column(String(256))
    utm_term = Column(String(256))
    utm_content = Column(String(256))
    screen_width = Column(Integer)
    screen_height = Column(Integer)
    language = Column(String(32))
    duration_seconds = Column(Numeric(10, 2))
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_pv_session', 'session_id'),
        Index('idx_pv_timestamp', 'timestamp'),
        Index('idx_pv_path', 'path'),
        Index('idx_pv_host', 'host'),
    )


class VisitorSession(Base):
    """Aggregated visitor sessions."""
    __tablename__ = 'visitor_sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(64), unique=True, nullable=False)
    host = Column(String(256))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    page_views = Column(Integer, server_default=text('1'))
    landing_page = Column(String(2048))
    exit_page = Column(String(2048))
    ip_address = Column(String(45))
    country = Column(String(8))
    user_agent = Column(Text)
    browser = Column(String(64))
    os = Column(String(64))
    device_type = Column(String(16))
    referrer = Column(Text)
    utm_source = Column(String(256))
    utm_medium = Column(String(256))
    utm_campaign = Column(String(256))
    is_bounce = Column(Boolean, server_default=text('TRUE'))
    duration_seconds = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_vs_start', 'start_time'),
        Index('idx_vs_host', 'host'),
        Index('idx_vs_country', 'country'),
    )


class Conversion(Base):
    """Conversion tracking for marketing analytics."""
    __tablename__ = 'conversions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(64), nullable=False)
    conversion_type = Column(String(64), nullable=False)
    page = Column(String(2048))
    referrer = Column(Text)
    value = Column(Numeric(12, 2))
    utm_source = Column(String(256))
    utm_medium = Column(String(256))
    utm_campaign = Column(String(256))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_conv_session', 'session_id'),
        Index('idx_conv_type', 'conversion_type'),
        Index('idx_conv_timestamp', 'timestamp'),
    )


class RevenueSplit(Base):
    """Track revenue splits — 10% ops, 80% hooman, 10% cat ecosystem."""
    __tablename__ = 'revenue_splits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount_total = Column(Numeric(12, 2), nullable=False)
    amount_ops = Column(Numeric(12, 2), nullable=False)
    amount_hooman = Column(Numeric(12, 2), nullable=False)
    amount_cat_eco = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), server_default=text("'eur'"))
    source = Column(String(64), nullable=False)
    source_id = Column(String(255), nullable=True)
    description = Column(String(255))
    payout_tag = Column(String(128), server_default=text("'hooman pet reimbursement'"))
    payout_destination = Column(String(255), server_default=text("'ziebartjevgeni@gmail.com'"))
    paid_to_hooman = Column(Boolean, server_default=text('false'))
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
