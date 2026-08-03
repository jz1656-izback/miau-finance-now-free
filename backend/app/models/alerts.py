from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(String(16), server_default=text("'info'"))
    category = Column(String(64))
    source_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id'))
    condition_expr = Column(Text)
    is_active = Column(Boolean, server_default=text('TRUE'))
    last_triggered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class PushSubscription(Base):
    __tablename__ = 'push_subscriptions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    endpoint = Column(Text, nullable=False)
    p256dh_key = Column(String(255))
    auth_key = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        UniqueConstraint('user_id', 'endpoint', name='uq_push_sub_user_endpoint'),
    )


class NotificationHistory(Base):
    __tablename__ = 'notification_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    channel = Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    body = Column(Text)
    deep_link = Column(String(500))
    delivered = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_notif_history_user', 'user_id'),
        Index('idx_notif_history_created', 'created_at'),
    )
