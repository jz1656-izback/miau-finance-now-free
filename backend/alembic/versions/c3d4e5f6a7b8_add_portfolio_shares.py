"""add portfolio shares

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-05-19 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'portfolio_shares',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('workspace_id', sa.UUID(), nullable=False),
        sa.Column('shared_by', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('portfolio_id', 'workspace_id', name='uq_portfolio_shares'),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['shared_by'], ['users.id']),
    )


def downgrade() -> None:
    op.drop_table('portfolio_shares')
