"""add service column to service_desk_tickets

Revision ID: q1r2s3t4u5v6
Revises: p1q2r3s4t5u6
Create Date: 2026-05-21 22:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'q1r2s3t4u5v6'
down_revision: Union[str, None] = 'p1q2r3s4t5u6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('service_desk_tickets', sa.Column('service', sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column('service_desk_tickets', 'service')
