"""add billing_balances and billing_transactions tables

Revision ID: n1o2p3q4r5s6
Revises: a1b2c3d4e5f6
Create Date: 2026-05-20
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = 'n1o2p3q4r5s6'
down_revision: Union[str, None] = 'm1n2o3p4q5r6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'billing_balances',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('balance', sa.Numeric(12, 2), server_default=sa.text('0.00')),
        sa.Column('default_payment_id', sa.String(255)),
        sa.Column('stripe_customer_id', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_billing_user', 'billing_balances', ['user_id'])

    op.create_table(
        'billing_transactions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('type', sa.String(32), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('stripe_payment_intent_id', sa.String(255)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_billing_tx_user', 'billing_transactions', ['user_id'])
    op.create_index('idx_billing_tx_created', 'billing_transactions', ['created_at'])


def downgrade() -> None:
    op.drop_table('billing_transactions')
    op.drop_table('billing_balances')
