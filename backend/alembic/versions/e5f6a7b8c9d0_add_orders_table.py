"""add orders table

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-05-19 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5f6a7b8c9d0'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('instrument_id', sa.UUID(), nullable=False),
        sa.Column('order_type', sa.Enum('MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', name='order_type'), nullable=False),
        sa.Column('side', sa.String(8), nullable=False),
        sa.Column('quantity', sa.Numeric(18, 6), nullable=False),
        sa.Column('price', sa.Numeric(18, 6), nullable=True),
        sa.Column('stop_price', sa.Numeric(18, 6), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'SUBMITTED', 'PARTIALLY_FILLED', 'FILLED', 'CANCELLED', 'REJECTED', 'EXPIRED', name='order_status'), nullable=False, server_default=sa.text("'PENDING'")),
        sa.Column('filled_qty', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('filled_avg_price', sa.Numeric(18, 6), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('filled_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint("side IN ('BUY', 'SELL')", name='ck_orders_side'),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
    )
    op.create_index('idx_orders_portfolio', 'orders', ['portfolio_id'])
    op.create_index('idx_orders_instrument', 'orders', ['instrument_id'])
    op.create_index('idx_orders_status', 'orders', ['status'])


def downgrade() -> None:
    op.drop_table('orders')
    op.execute('DROP TYPE IF EXISTS order_type')
    op.execute('DROP TYPE IF EXISTS order_status')
