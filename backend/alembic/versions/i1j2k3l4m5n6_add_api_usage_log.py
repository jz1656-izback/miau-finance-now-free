"""add api_usage_log table for per-request tracking

Revision ID: i1j2k3l4m5n6
Revises: h2i3j4k5l6m7
Create Date: 2026-05-19 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'i1j2k3l4m5n6'
down_revision: Union[str, Sequence[str], None] = 'h2i3j4k5l6m7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'api_usage_log',
        sa.Column('id', UUID(), nullable=False),
        sa.Column('user_id', UUID(), nullable=False),
        sa.Column('api_key_id', UUID(), nullable=True),
        sa.Column('endpoint', sa.Text(), nullable=False),
        sa.Column('method', sa.String(16), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('logged_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['api_key_id'], ['api_keys.id'], ondelete='SET NULL'),
    )
    op.create_index('idx_api_usage_log_user', 'api_usage_log', ['user_id'])
    op.create_index('idx_api_usage_log_logged_at', 'api_usage_log', ['logged_at'])
    op.create_index('idx_api_usage_log_user_logged_at', 'api_usage_log', ['user_id', 'logged_at'])


def downgrade() -> None:
    op.drop_table('api_usage_log')
