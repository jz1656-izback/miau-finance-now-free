"""add esg_scores and carbon_footprints tables

Revision ID: k1l2m3n4o5p6
Revises: j1j2k3l4m5n6
Create Date: 2026-05-19 23:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'k1l2m3n4o5p6'
down_revision: Union[str, Sequence[str], None] = 'j1j2k3l4m5n6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'esg_scores',
        sa.Column('id', UUID(), nullable=False),
        sa.Column('ticker', sa.String(16), nullable=False),
        sa.Column('total_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('environmental_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('social_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('governance_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('controversy_score', sa.Numeric(5, 2), nullable=True),
        sa.Column('percentile', sa.Numeric(5, 2), nullable=True),
        sa.Column('rating', sa.String(8), nullable=True),
        sa.Column('source', sa.String(32), server_default=sa.text("'yahoo'"), nullable=True),
        sa.Column('retrieved_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'source', name='uq_esg_ticker_source'),
    )
    op.create_index('idx_esg_ticker', 'esg_scores', ['ticker'])

    op.create_table(
        'carbon_footprints',
        sa.Column('id', UUID(), nullable=False),
        sa.Column('ticker', sa.String(16), nullable=False),
        sa.Column('scope1_tons', sa.Numeric(18, 2), nullable=True),
        sa.Column('scope2_tons', sa.Numeric(18, 2), nullable=True),
        sa.Column('scope3_tons', sa.Numeric(18, 2), nullable=True),
        sa.Column('total_tons', sa.Numeric(18, 2), nullable=True),
        sa.Column('intensity_per_revenue', sa.Numeric(12, 2), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(32), server_default=sa.text("'yahoo'"), nullable=True),
        sa.Column('retrieved_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'year', name='uq_carbon_ticker_year'),
    )
    op.create_index('idx_carbon_ticker', 'carbon_footprints', ['ticker'])


def downgrade() -> None:
    op.drop_table('carbon_footprints')
    op.drop_table('esg_scores')
