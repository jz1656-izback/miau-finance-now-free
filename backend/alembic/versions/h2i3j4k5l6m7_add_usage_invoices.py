"""add usage records and invoices tables

Revision ID: h2i3j4k5l6m7
Revises: h1i2j3k4l5m6
Create Date: 2026-05-19 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'h2i3j4k5l6m7'
down_revision: Union[str, Sequence[str], None] = 'h1i2j3k4l5m6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usage_records',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('api_key_id', sa.UUID(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('request_count', sa.Integer(), server_default=sa.text('0'), nullable=True),
        sa.Column('data_transfer_bytes', sa.BigInteger(), server_default=sa.text('0'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'date', name='uq_usage_user_date'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['api_key_id'], ['api_keys.id'], ondelete='SET NULL'),
    )
    op.create_index('idx_usage_user', 'usage_records', ['user_id'])
    op.create_index('idx_usage_date', 'usage_records', ['date'])

    op.create_table(
        'invoices',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('stripe_invoice_id', sa.String(255), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency', sa.String(3), server_default=sa.text("'usd'"), nullable=True),
        sa.Column('status', sa.String(32), server_default=sa.text("'draft'"), nullable=True),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_invoice_user', 'invoices', ['user_id'])
    op.create_index('idx_invoice_period', 'invoices', ['period_start'])


def downgrade() -> None:
    op.drop_table('invoices')
    op.drop_table('usage_records')
