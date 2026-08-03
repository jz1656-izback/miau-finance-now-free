from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ontology_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), unique=True)
    name = Column(String(255), nullable=False)
    portfolio_type = Column(String(64), nullable=False, server_default=text("'trading'"))
    base_currency = Column(String(3), server_default=text("'USD'"))
    management_style = Column(String(64))
    benchmark_id = Column(String(64))
    status = Column(String(32), server_default=text("'active'"))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    positions = relationship('Position', back_populates='portfolio', cascade='all, delete-orphan')


class Position(Base):
    __tablename__ = 'positions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ontology_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), unique=True)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'), nullable=False)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False, server_default=text('0'))
    average_price = Column(Numeric(18, 6))
    cost_basis = Column(Numeric(24, 6))
    market_value = Column(Numeric(24, 6))
    unrealized_pnl = Column(Numeric(24, 6))
    realized_pnl = Column(Numeric(24, 6), server_default=text('0'))
    currency = Column(String(3), server_default=text("'USD'"))
    as_of_date = Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    portfolio = relationship('Portfolio', back_populates='positions')

    __table_args__ = (
        UniqueConstraint('instrument_id', 'portfolio_id', name='uq_positions_instrument_portfolio'),
    )


class Trade(Base):
    __tablename__ = 'trades'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ontology_object_id = Column(UUID(as_uuid=True), ForeignKey('ontology_objects.id', ondelete='CASCADE'), unique=True)
    trade_id = Column(String(128))
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'), nullable=False)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'))
    counterparty_id = Column(UUID(as_uuid=True), ForeignKey('counterparties.id'))
    trade_date = Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    settlement_date = Column(DateTime(timezone=True))
    trade_type = Column(String(32), nullable=False)
    side = Column(String(8), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    price = Column(Numeric(18, 6), nullable=False)
    notional = Column(Numeric(24, 6))
    commission = Column(Numeric(18, 6), server_default=text('0'))
    fees = Column(Numeric(18, 6), server_default=text('0'))
    currency = Column(String(3), nullable=False, server_default=text("'USD'"))
    trader = Column(String(128))
    broker = Column(String(128))
    status = Column(String(32), server_default=text("'new'"))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        CheckConstraint("side IN ('BUY', 'SELL')", name='ck_trades_side'),
        Index('idx_trades_instrument', 'instrument_id'),
        Index('idx_trades_portfolio', 'portfolio_id'),
        Index('idx_trades_date', 'trade_date'),
    )


class PnL(Base):
    __tablename__ = 'pnl'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'))
    pnl_type = Column(String(32), nullable=False)
    pnl_amount = Column(Numeric(24, 6), nullable=False)
    currency = Column(String(3), server_default=text("'USD'"))
    source = Column(String(64))
    from_date = Column(DateTime(timezone=True))
    to_date = Column(DateTime(timezone=True))
    attribution = Column(JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_pnl_portfolio', 'portfolio_id'),
        Index('idx_pnl_date', 'to_date'),
    )


class RiskMetric(Base):
    __tablename__ = 'risk_metrics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'))
    metric_name = Column(String(128), nullable=False)
    metric_value = Column(Numeric(24, 6))
    metric_type = Column(String(64))
    currency = Column(String(3), server_default=text("'USD'"))
    as_of_date = Column(DateTime(timezone=True), nullable=False, server_default=text('NOW()'))
    parameters = Column(JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_risk_portfolio', 'portfolio_id'),
        Index('idx_risk_date', 'as_of_date'),
    )


class PipelineRun(Base):
    __tablename__ = 'pipeline_runs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_name = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, server_default=text("'pending'"))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    records_processed = Column(Integer, server_default=text('0'))
    metadata_ = Column('metadata', JSON, server_default=text("'{}'"))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
