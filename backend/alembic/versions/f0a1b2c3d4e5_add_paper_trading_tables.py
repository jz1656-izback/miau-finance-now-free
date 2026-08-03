"""add paper trading tables

Revision ID: f0a1b2c3d4e5
Revises: e5f6a7b8c9d0
Create Date: 2026-05-19 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f0a1b2c3d4e5'
down_revision: Union[str, Sequence[str], None] = 'e5f6a7b8c9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'paper_portfolios',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('initial_cash', sa.Numeric(18, 2), nullable=False),
        sa.Column('current_cash', sa.Numeric(18, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
    )

    op.create_table(
        'paper_trades',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('paper_portfolio_id', sa.UUID(), nullable=False),
        sa.Column('instrument_id', sa.UUID(), nullable=False),
        sa.Column('side', sa.String(8), nullable=False),
        sa.Column('quantity', sa.Numeric(18, 6), nullable=False),
        sa.Column('price', sa.Numeric(18, 6), nullable=False),
        sa.Column('commission', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('slippage', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('tca_cost', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('executed_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['paper_portfolio_id'], ['paper_portfolios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
    )
    op.create_index('idx_paper_trades_portfolio', 'paper_trades', ['paper_portfolio_id'])
    op.create_index('idx_paper_trades_instrument', 'paper_trades', ['instrument_id'])


def downgrade() -> None:
    op.drop_table('paper_trades')
    op.drop_table('paper_portfolios')
