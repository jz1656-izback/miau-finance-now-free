"""stub for marketing tables (already applied manually)

Revision ID: m1n2o3p4q5r6
Revises: a1b2c3d4e5f6
Create Date: 2026-05-19
"""
from typing import Sequence, Union
from alembic import op

revision: str = 'm1n2o3p4q5r6'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
