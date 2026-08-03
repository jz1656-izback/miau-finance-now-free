"""add tiny_catfund tier, bark_requests table, seat/bark/license columns to subscriptions

Revision ID: o1p2q3r4s5t6
Revises: n1o2p3q4r5s6
Create Date: 2026-05-21 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

revision: str = 'o1p2q3r4s5t6'
down_revision: Union[str, None] = 'n1o2p3q4r5s6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('subscriptions', sa.Column('seats', sa.Integer(), server_default=sa.text('1'), nullable=True))
    op.add_column('subscriptions', sa.Column('barks_remaining', sa.Integer(), server_default=sa.text('0'), nullable=True))
    op.add_column('subscriptions', sa.Column('barks_used', sa.Integer(), server_default=sa.text('0'), nullable=True))
    op.add_column('subscriptions', sa.Column('bark_year', sa.Integer(), nullable=True))
    op.add_column('subscriptions', sa.Column('on_premise_license', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('subscriptions', sa.Column('license_key', sa.String(128), nullable=True))

    op.execute("ALTER TYPE subscription_tier ADD VALUE IF NOT EXISTS 'tiny_catfund'")

    op.create_table(
        'bark_requests',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(32), server_default=sa.text("'pending'")),
        sa.Column('bark_year', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_bark_user', 'bark_requests', ['user_id'])
    op.create_index('idx_bark_year', 'bark_requests', ['bark_year'])


def downgrade() -> None:
    op.drop_index('idx_bark_user', table_name='bark_requests')
    op.drop_index('idx_bark_year', table_name='bark_requests')
    op.drop_table('bark_requests')

    op.drop_column('subscriptions', 'license_key')
    op.drop_column('subscriptions', 'on_premise_license')
    op.drop_column('subscriptions', 'bark_year')
    op.drop_column('subscriptions', 'barks_used')
    op.drop_column('subscriptions', 'barks_remaining')
    op.drop_column('subscriptions', 'seats')

    op.execute("DELETE FROM pg_enum WHERE enumlabel = 'tiny_catfund' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'subscription_tier')")
