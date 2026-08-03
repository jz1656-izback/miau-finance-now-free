"""add currencies table

Revision ID: j1j2k3l4m5n6
Revises: i1j2k3l4m5n6
Create Date: 2026-05-19 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


revision: str = 'j1j2k3l4m5n6'
down_revision: Union[str, Sequence[str], None] = 'i1j2k3l4m5n6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'currencies',
        sa.Column('code', sa.String(8), nullable=False),
        sa.Column('symbol', sa.String(8), nullable=False),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('decimal_places', sa.Integer(), server_default=sa.text('2'), nullable=False),
        sa.Column('fx_rate', sa.Numeric(18, 8), server_default=sa.text('1.0'), nullable=False),
        sa.Column('fx_updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_crypto', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('code'),
    )

    op.execute("""
        INSERT INTO currencies (code, symbol, name, decimal_places, is_crypto) VALUES
        ('USD', '$', 'US Dollar', 2, FALSE),
        ('EUR', '€', 'Euro', 2, FALSE),
        ('GBP', '£', 'British Pound', 2, FALSE),
        ('JPY', '¥', 'Japanese Yen', 0, FALSE),
        ('CHF', 'CHF', 'Swiss Franc', 2, FALSE),
        ('CAD', 'C$', 'Canadian Dollar', 2, FALSE),
        ('AUD', 'A$', 'Australian Dollar', 2, FALSE),
        ('CNY', '¥', 'Chinese Yuan', 2, FALSE),
        ('HKD', 'HK$', 'Hong Kong Dollar', 2, FALSE),
        ('SGD', 'S$', 'Singapore Dollar', 2, FALSE),
        ('INR', '₹', 'Indian Rupee', 2, FALSE),
        ('MXN', 'Mex$', 'Mexican Peso', 2, FALSE),
        ('BRL', 'R$', 'Brazilian Real', 2, FALSE),
        ('ZAR', 'R', 'South African Rand', 2, FALSE),
        ('SEK', 'kr', 'Swedish Krona', 2, FALSE),
        ('NOK', 'kr', 'Norwegian Krone', 2, FALSE),
        ('KRW', '₩', 'South Korean Won', 0, FALSE),
        ('BTC', '₿', 'Bitcoin', 8, TRUE),
        ('ETH', 'Ξ', 'Ethereum', 8, TRUE),
        ('USDT', '₮', 'Tether', 2, TRUE)
    """)


def downgrade() -> None:
    op.drop_table('currencies')
