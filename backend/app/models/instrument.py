from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class Instrument(Base):
    __tablename__ = 'instruments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ontology_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), nullable=True, unique=True)
    ticker = Column(String(32), nullable=False)
    isin = Column(String(12))
    sedol = Column(String(7))
    cusip = Column(String(9))
    name = Column(String(500), nullable=False)
    instrument_type = Column(String(64), nullable=False)
    currency = Column(String(3), nullable=False, server_default=text("'USD'"))
    exchange = Column(String(64))
    sector = Column(String(128))
    industry = Column(String(128))
    country = Column(String(64))
    issue_date = Column(Date)
    maturity_date = Column(Date)
    coupon_rate = Column(Numeric(10, 6))
    underlying_instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'))
    strike_price = Column(Numeric(18, 6))
    option_type = Column(String(16))
    lot_size = Column(Integer, server_default=text('1'))
    status = Column(String(32), server_default=text("'active'"))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'::jsonb"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    underlying = relationship('Instrument', remote_side='Instrument.id', backref='derivatives')
    market_data = relationship('MarketData', back_populates='instrument', lazy='selectin')

    __table_args__ = (
        Index('idx_instruments_ticker', 'ticker'),
        Index('idx_instruments_isin', 'isin'),
        Index('idx_instruments_type', 'instrument_type'),
    )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'isin': self.isin,
            'sedol': self.sedol,
            'cusip': self.cusip,
            'name': self.name,
            'instrument_type': self.instrument_type,
            'currency': self.currency,
            'exchange': self.exchange,
            'sector': self.sector,
            'industry': self.industry,
            'country': self.country,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'maturity_date': self.maturity_date.isoformat() if self.maturity_date else None,
            'coupon_rate': float(self.coupon_rate) if self.coupon_rate else None,
            'strike_price': float(self.strike_price) if self.strike_price else None,
            'option_type': self.option_type,
            'lot_size': self.lot_size,
            'status': self.status,
            'created_at': str(self.created_at) if self.created_at else None,
            'updated_at': str(self.updated_at) if self.updated_at else None,
        }


class MarketData(Base):
    __tablename__ = 'market_data'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(18, 6))
    high = Column(Numeric(18, 6))
    low = Column(Numeric(18, 6))
    close = Column(Numeric(18, 6))
    volume = Column(BigInteger)
    adj_close = Column(Numeric(18, 6))
    bid = Column(Numeric(18, 6))
    ask = Column(Numeric(18, 6))
    source = Column(String(64), server_default=text("'manual'"))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'::jsonb"))

    instrument = relationship('Instrument', back_populates='market_data')

    __table_args__ = (
        UniqueConstraint('instrument_id', 'date', name='uq_market_data_instrument_date'),
        Index('idx_market_data_instrument', 'instrument_id'),
        Index('idx_market_data_date', 'date'),
    )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'instrument_id': str(self.instrument_id),
            'date': self.date.isoformat() if self.date else None,
            'open': float(self.open) if self.open else None,
            'high': float(self.high) if self.high else None,
            'low': float(self.low) if self.low else None,
            'close': float(self.close) if self.close else None,
            'volume': self.volume,
            'adj_close': float(self.adj_close) if self.adj_close else None,
            'bid': float(self.bid) if self.bid else None,
            'ask': float(self.ask) if self.ask else None,
            'source': self.source,
        }


class Counterparty(Base):
    __tablename__ = 'counterparties'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ontology_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), unique=True)
    short_name = Column(String(64), nullable=False)
    legal_name = Column(String(500), nullable=False)
    counterparty_type = Column(String(64), nullable=False)
    country = Column(String(64))
    credit_rating = Column(String(8))
    sector = Column(String(128))
    lei = Column(String(20))
    status = Column(String(32), server_default=text("'active'"))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
