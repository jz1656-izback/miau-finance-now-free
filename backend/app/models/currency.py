from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class Currency(Base):
    """ISO 4217 currency configuration model."""

    __tablename__ = 'currencies'

    code = Column(String(8), primary_key=True)
    symbol = Column(String(8), nullable=False)
    name = Column(String(64), nullable=False)
    decimal_places = Column(Integer, nullable=False, server_default=text('2'))
    fx_rate = Column(Numeric(18, 8), nullable=False, server_default=text('1.0'))
    fx_updated_at = Column(DateTime(timezone=True))
    is_crypto = Column(Boolean, server_default=text('FALSE'))
    is_active = Column(Boolean, server_default=text('TRUE'))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
