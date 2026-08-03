"""add api_keys and webhook_endpoints tables

Revision ID: h1i2j3k4l5m6
Revises: g1h2i3j4k5l6
Create Date: 2026-05-19 03:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


revision: str = 'h1i2j3k4l5m6'
down_revision: Union[str, Sequence[str], None] = 'g1h2i3j4k5l6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'api_keys',
        sa.Column('id', UUID(), nullable=False),
        sa.Column('user_id', UUID(), nullable=False),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('key_prefix', sa.String(8), nullable=False),
        sa.Column('key_hash', sa.String(255), nullable=False),
        sa.Column('scopes', JSON(), server_default=sa.text("'{\"read\": true}'")),
        sa.Column('rate_limit_multiplier', sa.Integer(), server_default=sa.text('1')),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_api_keys_user', 'api_keys', ['user_id'])
    op.create_index('idx_api_keys_prefix', 'api_keys', ['key_prefix'])

    op.create_table(
        'webhook_endpoints',
        sa.Column('id', UUID(), nullable=False),
        sa.Column('user_id', UUID(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('events', JSON(), server_default=sa.text("'[]'")),
        sa.Column('secret', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE')),
        sa.Column('last_triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_webhooks_user', 'webhook_endpoints', ['user_id'])


def downgrade() -> None:
    op.drop_table('webhook_endpoints')
    op.drop_table('api_keys')
