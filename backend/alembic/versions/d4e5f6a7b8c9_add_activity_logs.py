"""add activity logs

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-05-19 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'activity_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('workspace_id', sa.UUID(), nullable=True),
        sa.Column('action', sa.String(64), nullable=False),
        sa.Column('resource_type', sa.String(64), nullable=False),
        sa.Column('resource_id', sa.String(255), nullable=True),
        sa.Column('details', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id']),
    )
    op.create_index('idx_activity_user', 'activity_logs', ['user_id'])
    op.create_index('idx_activity_workspace', 'activity_logs', ['workspace_id'])
    op.create_index('idx_activity_created', 'activity_logs', ['created_at'])


def downgrade() -> None:
    op.drop_table('activity_logs')
