from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class WealthTransaction(Base):
    """Unified log of wealth allocation and investment transactions."""
    __tablename__ = 'wealth_transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(32), nullable=False)  # 'allocation', 'investment', 'payout'
    asset_class = Column(String(32))  # 'stocks', 'crypto', 'cloud', 'infra', 'real_estate', 'alts'
    amount_total = Column(Numeric(12, 2))
    amount_ops = Column(Numeric(12, 2))
    amount_hooman = Column(Numeric(12, 2))
    amount_cat_eco = Column(Numeric(12, 2))
    amount = Column(Numeric(12, 2))  # For investment transactions
    status = Column(String(32), server_default=text("'pending'"))  # 'pending', 'executed', 'failed'
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_wt_type', 'type'),
        Index('idx_wt_status', 'status'),
        Index('idx_wt_created', 'created_at'),
    )


class RealEstateAsset(Base):
    """Real estate holdings — penthouse, rental properties, land."""
    __tablename__ = 'real_estate_assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    property_type = Column(String(32), server_default=text("'residential'"))
    current_value = Column(Numeric(14, 2), server_default=text('0'))
    mortgage_balance = Column(Numeric(14, 2), server_default=text('0'))
    monthly_rental_income = Column(Numeric(10, 2), server_default=text('0'))
    purchase_price = Column(Numeric(14, 2))
    address = Column(String(512))
    notes = Column(Text)
    last_valuation = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))


class AlternativeAsset(Base):
    """Alternative assets — gold, crypto, art, collectibles, private equity."""
    __tablename__ = 'alternative_assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    asset_type = Column(String(32), nullable=False)  # 'gold', 'crypto', 'art', 'collectible', 'private_equity'
    quantity = Column(Numeric(14, 4), server_default=text('1'))
    current_value = Column(Numeric(14, 2), server_default=text('0'))
    purchase_value = Column(Numeric(14, 2))
    notes = Column(Text)
    last_valuation = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_aa_type', 'asset_type'),
        UniqueConstraint('name', 'asset_type', name='uq_asset_name_type'),
    )


class CloudCredit(Base):
    """Cloud provider credits — AWS, GCP, Azure reserved instances."""
    __tablename__ = 'cloud_credits'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String(32), nullable=False)  # 'AWS', 'GCP', 'Azure'
    amount = Column(Numeric(12, 2), nullable=False)
    remaining = Column(Numeric(12, 2), server_default=text('0'))
    currency = Column(String(3), server_default=text("'usd'"))
    expiry_date = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text('NOW()'))
