"""change subscriptions.tier from string to enum

Revision ID: g1h2i3j4k5l6
Revises: g0a1b2c3d4e5
Create Date: 2026-05-19 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'g1h2i3j4k5l6'
down_revision: Union[str, Sequence[str], None] = 'g0a1b2c3d4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

subscription_tier_enum = sa.Enum('free', 'pro', 'enterprise', name='subscription_tier')


def upgrade() -> None:
    subscription_tier_enum.create(op.get_bind(), checkfirst=True)
    op.execute("ALTER TABLE subscriptions ALTER COLUMN tier DROP DEFAULT")
    op.alter_column('subscriptions', 'tier',
        existing_type=sa.String(32),
        type_=subscription_tier_enum,
        existing_nullable=False,
        existing_server_default=None,
        postgresql_using='tier::subscription_tier',
    )
    op.execute("ALTER TABLE subscriptions ALTER COLUMN tier SET DEFAULT 'free'::subscription_tier")


def downgrade() -> None:
    op.execute("ALTER TABLE subscriptions ALTER COLUMN tier DROP DEFAULT")
    op.alter_column('subscriptions', 'tier',
        existing_type=subscription_tier_enum,
        type_=sa.String(32),
        existing_nullable=False,
        existing_server_default=None,
    )
    op.execute("ALTER TABLE subscriptions ALTER COLUMN tier SET DEFAULT 'free'")
    op.execute('DROP TYPE IF EXISTS subscription_tier')
