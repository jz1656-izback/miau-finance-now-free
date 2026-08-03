"""initial

Revision ID: 55820b47cdb0
Revises: 
Create Date: 2026-05-18 21:55:29.009649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55820b47cdb0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from app.models import Base, Instrument, MarketData

    # Create instruments table
    op.create_table(
        'instruments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ontology_object_id', sa.UUID(), nullable=True),
        sa.Column('ticker', sa.String(32), nullable=False),
        sa.Column('isin', sa.String(12), nullable=True),
        sa.Column('sedol', sa.String(7), nullable=True),
        sa.Column('cusip', sa.String(9), nullable=True),
        sa.Column('name', sa.String(500), nullable=False),
        sa.Column('instrument_type', sa.String(64), nullable=False),
        sa.Column('currency', sa.String(3), server_default=sa.text("'USD'"), nullable=False),
        sa.Column('exchange', sa.String(64), nullable=True),
        sa.Column('sector', sa.String(128), nullable=True),
        sa.Column('industry', sa.String(128), nullable=True),
        sa.Column('country', sa.String(64), nullable=True),
        sa.Column('issue_date', sa.Date(), nullable=True),
        sa.Column('maturity_date', sa.Date(), nullable=True),
        sa.Column('coupon_rate', sa.Numeric(10, 6), nullable=True),
        sa.Column('underlying_instrument_id', sa.UUID(), nullable=True),
        sa.Column('strike_price', sa.Numeric(18, 6), nullable=True),
        sa.Column('option_type', sa.String(16), nullable=True),
        sa.Column('lot_size', sa.Integer(), server_default=sa.text('1')),
        sa.Column('status', sa.String(32), server_default=sa.text("'active'")),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['underlying_instrument_id'], ['instruments.id']),
    )
    op.create_index('idx_instruments_ticker', 'instruments', ['ticker'])
    op.create_index('idx_instruments_isin', 'instruments', ['isin'])
    op.create_index('idx_instruments_type', 'instruments', ['instrument_type'])

    # Create market_data table
    op.create_table(
        'market_data',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('instrument_id', sa.UUID(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('open', sa.Numeric(18, 6), nullable=True),
        sa.Column('high', sa.Numeric(18, 6), nullable=True),
        sa.Column('low', sa.Numeric(18, 6), nullable=True),
        sa.Column('close', sa.Numeric(18, 6), nullable=True),
        sa.Column('volume', sa.BigInteger(), nullable=True),
        sa.Column('adj_close', sa.Numeric(18, 6), nullable=True),
        sa.Column('bid', sa.Numeric(18, 6), nullable=True),
        sa.Column('ask', sa.Numeric(18, 6), nullable=True),
        sa.Column('source', sa.String(64), server_default=sa.text("'manual'")),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'::jsonb")),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
        sa.UniqueConstraint('instrument_id', 'date', name='uq_market_data_instrument_date'),
    )
    op.create_index('idx_market_data_instrument', 'market_data', ['instrument_id'])
    op.create_index('idx_market_data_date', 'market_data', ['date'])


def downgrade() -> None:
    op.drop_table('market_data')
    op.drop_table('instruments')
