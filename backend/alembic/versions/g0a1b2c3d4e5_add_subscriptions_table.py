"""add subscriptions table

Revision ID: g0a1b2c3d4e5
Revises: f0a1b2c3d4e5
Create Date: 2026-05-19 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'g0a1b2c3d4e5'
down_revision: Union[str, Sequence[str], None] = 'f0a1b2c3d4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('stripe_customer_id', sa.String(255)),
        sa.Column('stripe_subscription_id', sa.String(255)),
        sa.Column('tier', sa.String(32), nullable=False, server_default=sa.text("'free'")),
        sa.Column('status', sa.String(32), nullable=False, server_default=sa.text("'active'")),
        sa.Column('trial_ends_at', sa.DateTime(timezone=True)),
        sa.Column('current_period_end', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', name='uq_subscriptions_user'),
    )
    op.create_index('idx_subscriptions_stripe_customer', 'subscriptions', ['stripe_customer_id'])
    op.create_index('idx_subscriptions_stripe_sub', 'subscriptions', ['stripe_subscription_id'])
    op.create_index('idx_subscriptions_tier', 'subscriptions', ['tier'])
    op.create_index('idx_subscriptions_status', 'subscriptions', ['status'])


def downgrade() -> None:
    op.drop_table('subscriptions')
