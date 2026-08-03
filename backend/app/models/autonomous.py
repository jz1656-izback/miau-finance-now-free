from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class AutonomousConfig(Base):
    """Autonomous Wealth Engine configuration."""
    __tablename__ = 'autonomous_engine_config'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(64), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    description = Column(String(255))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
