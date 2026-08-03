from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class SubscriptionTier(str, enum.Enum):
    free = "free"
    pro = "pro"
    tiny_catfund = "tiny_catfund"
    enterprise = "enterprise"


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)
    stripe_customer_id = Column(String(255))
    stripe_subscription_id = Column(String(255))
    tier = Column(SAEnum(SubscriptionTier, name='subscription_tier', create_constraint=False), nullable=False, server_default=text("'free'"))
    status = Column(String(32), nullable=False, server_default=text("'active'"))
    trial_ends_at = Column(DateTime(timezone=True))
    current_period_end = Column(DateTime(timezone=True))
    seats = Column(Integer, server_default=text('1'))
    barks_remaining = Column(Integer, server_default=text('0'))
    barks_used = Column(Integer, server_default=text('0'))
    bark_year = Column(Integer)
    on_premise_license = Column(Boolean, server_default=text('false'))
    license_key = Column(String(128))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class BarkRequest(Base):
    __tablename__ = 'bark_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(32), server_default=text("'pending'"))
    bark_year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_bark_user', 'user_id'),
        Index('idx_bark_year', 'bark_year'),
    )


class ApiKey(Base):
    __tablename__ = 'api_keys'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(128), nullable=False)
    key_prefix = Column(String(8), nullable=False)
    key_hash = Column(String(255), nullable=False)
    scopes = Column(JSON, server_default=text("'{\"read\": true}'"))
    rate_limit_multiplier = Column(Integer, server_default=text('1'))
    last_used_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_api_keys_user', 'user_id'),
        Index('idx_api_keys_prefix', 'key_prefix'),
    )


class WebhookEndpoint(Base):
    __tablename__ = 'webhook_endpoints'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    url = Column(Text, nullable=False)
    events = Column(JSON, server_default=text("'[]'"))
    is_active = Column(Boolean, server_default=text('TRUE'))
    secret = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_webhook_user', 'user_id'),
    )


class UsageRecord(Base):
    __tablename__ = 'usage_records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    api_key_id = Column(UUID(as_uuid=True), ForeignKey('api_keys.id', ondelete='SET NULL'))
    date = Column(Date, nullable=False)
    request_count = Column(Integer, server_default=text('0'))
    data_transfer_bytes = Column(BigInteger, server_default=text('0'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='uq_usage_user_date'),
        Index('idx_usage_user', 'user_id'),
        Index('idx_usage_date', 'date'),
    )


class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    stripe_invoice_id = Column(String(255))
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), server_default=text("'usd'"))
    status = Column(String(32), server_default=text("'draft'"))
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_invoice_user', 'user_id'),
        Index('idx_invoice_period', 'period_start'),
    )
