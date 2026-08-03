from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class Watchlist(Base):
    __tablename__ = 'watchlists'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), nullable=False, server_default=text("'default'"))
    name = Column(String(255), nullable=False, server_default=text("'Default'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    items = relationship('WatchlistItem', back_populates='watchlist', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_watchlist_user', 'user_id'),
    )


class WatchlistItem(Base):
    __tablename__ = 'watchlist_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey('watchlists.id', ondelete='CASCADE'), nullable=False)
    ticker = Column(String(10), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    notes = Column(Text, server_default=text("''"))

    watchlist = relationship('Watchlist', back_populates='items')

    __table_args__ = (
        UniqueConstraint('watchlist_id', 'ticker', name='uq_watchlist_items_ticker'),
        Index('idx_watchlist_items_ticker', 'ticker'),
    )
