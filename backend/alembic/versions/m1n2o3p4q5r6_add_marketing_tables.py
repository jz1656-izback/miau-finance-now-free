"""Add marketing analytics tables (page_views, visitor_sessions, conversions)

Revision ID: m1n2o3p4q5r6
Revises: k1l2m3n4o5p6
Create Date: 2026-05-19

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON

revision: str = 'm1n2o3p4q5r6'
down_revision: Union[str, None] = 'k1l2m3n4o5p6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'page_views',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('path', sa.String(2048), nullable=False),
        sa.Column('referrer', sa.Text),
        sa.Column('user_agent', sa.Text),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('country', sa.String(8)),
        sa.Column('session_id', sa.String(64), nullable=False),
        sa.Column('host', sa.String(256)),
        sa.Column('utm_source', sa.String(256)),
        sa.Column('utm_medium', sa.String(256)),
        sa.Column('utm_campaign', sa.String(256)),
        sa.Column('utm_term', sa.String(256)),
        sa.Column('utm_content', sa.String(256)),
        sa.Column('screen_width', sa.Integer),
        sa.Column('screen_height', sa.Integer),
        sa.Column('language', sa.String(32)),
        sa.Column('duration_seconds', sa.Numeric(10, 2)),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_pv_session', 'page_views', ['session_id'])
    op.create_index('idx_pv_timestamp', 'page_views', ['timestamp'])
    op.create_index('idx_pv_path', 'page_views', ['path'])
    op.create_index('idx_pv_host', 'page_views', ['host'])

    op.create_table(
        'visitor_sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('session_id', sa.String(64), unique=True, nullable=False),
        sa.Column('host', sa.String(256)),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True)),
        sa.Column('page_views', sa.Integer, server_default=sa.text('1')),
        sa.Column('landing_page', sa.String(2048)),
        sa.Column('exit_page', sa.String(2048)),
        sa.Column('ip_address', sa.String(45)),
        sa.Column('country', sa.String(8)),
        sa.Column('user_agent', sa.Text),
        sa.Column('browser', sa.String(64)),
        sa.Column('os', sa.String(64)),
        sa.Column('device_type', sa.String(16)),
        sa.Column('referrer', sa.Text),
        sa.Column('utm_source', sa.String(256)),
        sa.Column('utm_medium', sa.String(256)),
        sa.Column('utm_campaign', sa.String(256)),
        sa.Column('is_bounce', sa.Boolean, server_default=sa.text('TRUE')),
        sa.Column('duration_seconds', sa.Numeric(10, 2)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_vs_start', 'visitor_sessions', ['start_time'])
    op.create_index('idx_vs_host', 'visitor_sessions', ['host'])
    op.create_index('idx_vs_country', 'visitor_sessions', ['country'])

    op.create_table(
        'conversions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('session_id', sa.String(64), nullable=False),
        sa.Column('conversion_type', sa.String(64), nullable=False),
        sa.Column('page', sa.String(2048)),
        sa.Column('referrer', sa.Text),
        sa.Column('value', sa.Numeric(12, 2)),
        sa.Column('utm_source', sa.String(256)),
        sa.Column('utm_medium', sa.String(256)),
        sa.Column('utm_campaign', sa.String(256)),
        sa.Column('metadata', JSON, server_default=sa.text("'{}'")),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
    )
    op.create_index('idx_conv_session', 'conversions', ['session_id'])
    op.create_index('idx_conv_type', 'conversions', ['conversion_type'])
    op.create_index('idx_conv_timestamp', 'conversions', ['timestamp'])


def downgrade() -> None:
    op.drop_table('conversions')
    op.drop_table('visitor_sessions')
    op.drop_table('page_views')
