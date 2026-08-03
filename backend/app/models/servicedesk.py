from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class ServiceDeskTicket(Base):
    """Support ticket for the Miau Fire Brigade service desk."""
    __tablename__ = 'service_desk_tickets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    category = Column(String(32), nullable=False, server_default=text("'question'"))
    priority = Column(String(16), nullable=False, server_default=text("'medium'"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    author = Column(String(100), nullable=True)
    service = Column(String(64), nullable=True)
    status = Column(String(32), nullable=False, server_default=text("'open'"))
    assigned_to = Column(String(100), nullable=True)
    pokes = Column(Integer, nullable=False, server_default=text('0'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'), onupdate=text('NOW()'))

    __table_args__ = (
        Index('idx_sd_status', 'status'),
        Index('idx_sd_category', 'category'),
        Index('idx_sd_created', 'created_at'),
    )
