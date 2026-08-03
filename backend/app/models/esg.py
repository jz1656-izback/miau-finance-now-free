from app.models.base import Base
from sqlalchemy import (
    Column, String, Integer, Numeric, Date, DateTime, BigInteger, JSON, Boolean, Text,
    ForeignKey, UniqueConstraint, Index, text, CheckConstraint, func, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
import enum
import uuid


class EsgScore(Base):
    """ESG score model — environmental, social, governance ratings."""

    __tablename__ = 'esg_scores'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(16), nullable=False, index=True)
    total_score = Column(Numeric(5, 2))  # 0-100
    environmental_score = Column(Numeric(5, 2))
    social_score = Column(Numeric(5, 2))
    governance_score = Column(Numeric(5, 2))
    controversy_score = Column(Numeric(5, 2))  # 0 = clean, 100 = severe
    percentile = Column(Numeric(5, 2))  # industry percentile 0-100
    rating = Column(String(8))  # AAA, AA, A, BBB, BB, B, CCC
    source = Column(String(32), server_default=text("'yahoo'"))
    retrieved_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_esg_ticker', 'ticker'),
        UniqueConstraint('ticker', 'source', name='uq_esg_ticker_source'),
    )


class CarbonFootprint(Base):
    """Carbon footprint data per company."""

    __tablename__ = 'carbon_footprints'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String(16), nullable=False, index=True)
    scope1_tons = Column(Numeric(18, 2))  # Direct emissions
    scope2_tons = Column(Numeric(18, 2))  # Energy indirect
    scope3_tons = Column(Numeric(18, 2))  # Supply chain
    total_tons = Column(Numeric(18, 2))
    intensity_per_revenue = Column(Numeric(12, 2))  # tCO2e / $M revenue
    year = Column(Integer, nullable=False)
    source = Column(String(32), server_default=text("'yahoo'"))
    retrieved_at = Column(DateTime(timezone=True), server_default=text('NOW()'))

    __table_args__ = (
        Index('idx_carbon_ticker', 'ticker'),
        UniqueConstraint('ticker', 'year', name='uq_carbon_ticker_year'),
    )
