"""add service_desk_tickets table

Revision ID: p1q2r3s4t5u6
Revises: o1p2q3r4s5t6
Create Date: 2026-05-21 22:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = 'p1q2r3s4t5u6'
down_revision: Union[str, None] = 'o1p2q3r4s5t6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'service_desk_tickets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('category', sa.String(32), nullable=False, server_default=sa.text("'question'")),
        sa.Column('priority', sa.String(16), nullable=False, server_default=sa.text("'medium'")),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('author', sa.String(100), nullable=True),
        sa.Column('status', sa.String(32), nullable=False, server_default=sa.text("'open'")),
        sa.Column('assigned_to', sa.String(100), nullable=True),
        sa.Column('pokes', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
    )
    op.create_index('idx_sd_status', 'service_desk_tickets', ['status'])
    op.create_index('idx_sd_category', 'service_desk_tickets', ['category'])
    op.create_index('idx_sd_created', 'service_desk_tickets', ['created_at'])


def downgrade() -> None:
    op.drop_table('service_desk_tickets')
