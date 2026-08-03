from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class OrderType(str, enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class PaperPortfolio(Base):
    __tablename__ = 'paper_portfolios'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    initial_cash = Column(Numeric(18, 2), nullable=False)
    current_cash = Column(Numeric(18, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    trades = relationship('PaperTrade', back_populates='paper_portfolio', cascade='all, delete-orphan')


class PaperTrade(Base):
    __tablename__ = 'paper_trades'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paper_portfolio_id = Column(UUID(as_uuid=True), ForeignKey('paper_portfolios.id', ondelete='CASCADE'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'), nullable=False)
    side = Column(String(8), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    price = Column(Numeric(18, 6), nullable=False)
    commission = Column(Numeric(18, 6), server_default=text('0'))
    slippage = Column(Numeric(18, 6), server_default=text('0'))
    tca_cost = Column(Numeric(18, 6), server_default=text('0'))
    executed_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    paper_portfolio = relationship('PaperPortfolio', back_populates='trades')

    __table_args__ = (
        Index('idx_paper_trades_portfolio', 'paper_portfolio_id'),
        Index('idx_paper_trades_instrument', 'instrument_id'),
    )


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id'), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey('instruments.id'), nullable=False)
    order_type = Column(SAEnum(OrderType, name='order_type', create_constraint=False), nullable=False)
    side = Column(String(8), nullable=False)
    quantity = Column(Numeric(18, 6), nullable=False)
    price = Column(Numeric(18, 6))
    stop_price = Column(Numeric(18, 6))
    status = Column(SAEnum(OrderStatus, name='order_status', create_constraint=False), nullable=False, server_default=text("'PENDING'"))
    filled_qty = Column(Numeric(18, 6), server_default=text('0'))
    filled_avg_price = Column(Numeric(18, 6))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    updated_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
    filled_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint("side IN ('BUY', 'SELL')", name='ck_orders_side'),
        Index('idx_orders_portfolio', 'portfolio_id'),
        Index('idx_orders_instrument', 'instrument_id'),
        Index('idx_orders_status', 'status'),
    )


class SharedPortfolioView(Base):
    __tablename__ = 'shared_portfolio_views'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    share_token = Column(String(64), unique=True, nullable=False)
    is_public = Column(Boolean, server_default=text('TRUE'))
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
