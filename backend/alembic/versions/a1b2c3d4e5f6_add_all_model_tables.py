"""add_all_model_tables

Revision ID: a1b2c3d4e5f6
Revises: 55820b47cdb0
Create Date: 2026-05-18 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '55820b47cdb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ontology_types',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('namespace', sa.String(255), server_default=sa.text("'default'"), nullable=True),
        sa.Column('icon', sa.String(64), server_default=sa.text("'database'"), nullable=True),
        sa.Column('color', sa.String(7), server_default=sa.text("'#6366f1'"), nullable=True),
        sa.Column('config', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('is_abstract', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'ontology_properties',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('type_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('data_type', sa.String(64), nullable=False),
        sa.Column('is_required', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('is_unique', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('is_searchable', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('is_faceted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('validation_rules', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('ui_config', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('sort_order', sa.Integer(), server_default=sa.text('0'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('type_id', 'name', name='uq_ontology_properties_type_name'),
        sa.ForeignKeyConstraint(['type_id'], ['ontology_types.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'ontology_links',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('source_type_id', sa.UUID(), nullable=False),
        sa.Column('target_type_id', sa.UUID(), nullable=False),
        sa.Column('link_type', sa.String(64), server_default=sa.text("'many_to_many'"), nullable=True),
        sa.Column('reverse_name', sa.String(255), nullable=True),
        sa.Column('cardinality', sa.String(32), server_default=sa.text("'ONE_TO_MANY'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.ForeignKeyConstraint(['source_type_id'], ['ontology_types.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_type_id'], ['ontology_types.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'ontology_objects',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('type_id', sa.UUID(), nullable=False),
        sa.Column('display_name', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('properties', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('status', sa.String(64), server_default=sa.text("'active'"), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_by', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['type_id'], ['ontology_types.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_ontology_objects_type', 'ontology_objects', ['type_id'])
    op.create_index('idx_ontology_objects_status', 'ontology_objects', ['status'])

    op.create_table(
        'ontology_object_links',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('link_id', sa.UUID(), nullable=False),
        sa.Column('source_object_id', sa.UUID(), nullable=False),
        sa.Column('target_object_id', sa.UUID(), nullable=False),
        sa.Column('properties', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('link_id', 'source_object_id', 'target_object_id', name='uq_object_links'),
        sa.ForeignKeyConstraint(['link_id'], ['ontology_links.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_object_links_source', 'ontology_object_links', ['source_object_id'])
    op.create_index('idx_object_links_target', 'ontology_object_links', ['target_object_id'])

    op.create_table(
        'audit_log',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('object_id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(32), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('changes', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'data_lineage',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('source_system', sa.String(128), nullable=False),
        sa.Column('source_id', sa.String(255), nullable=False),
        sa.Column('target_table', sa.String(128), nullable=False),
        sa.Column('target_id', sa.UUID(), nullable=False),
        sa.Column('operation', sa.String(32), nullable=False),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # Add FK for instruments -> ontology_objects (now ontology_objects exists)
    op.create_foreign_key(
        'fk_instruments_ontology_object',
        'instruments', 'ontology_objects',
        ['ontology_object_id'], ['id'],
        ondelete='CASCADE',
    )

    op.create_table(
        'counterparties',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ontology_object_id', sa.UUID(), nullable=True),
        sa.Column('short_name', sa.String(64), nullable=False),
        sa.Column('legal_name', sa.String(500), nullable=False),
        sa.Column('counterparty_type', sa.String(64), nullable=False),
        sa.Column('country', sa.String(64), nullable=True),
        sa.Column('credit_rating', sa.String(8), nullable=True),
        sa.Column('sector', sa.String(128), nullable=True),
        sa.Column('lei', sa.String(20), nullable=True),
        sa.Column('status', sa.String(32), server_default=sa.text("'active'"), nullable=True),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ontology_object_id'),
        sa.ForeignKeyConstraint(['ontology_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'portfolios',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ontology_object_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('portfolio_type', sa.String(64), nullable=False, server_default=sa.text("'trading'")),
        sa.Column('base_currency', sa.String(3), server_default=sa.text("'USD'"), nullable=True),
        sa.Column('management_style', sa.String(64), nullable=True),
        sa.Column('benchmark_id', sa.String(64), nullable=True),
        sa.Column('status', sa.String(32), server_default=sa.text("'active'"), nullable=True),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ontology_object_id'),
        sa.ForeignKeyConstraint(['ontology_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'positions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ontology_object_id', sa.UUID(), nullable=True),
        sa.Column('instrument_id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.Numeric(18, 6), nullable=False, server_default=sa.text('0')),
        sa.Column('average_price', sa.Numeric(18, 6), nullable=True),
        sa.Column('cost_basis', sa.Numeric(24, 6), nullable=True),
        sa.Column('market_value', sa.Numeric(24, 6), nullable=True),
        sa.Column('unrealized_pnl', sa.Numeric(24, 6), nullable=True),
        sa.Column('realized_pnl', sa.Numeric(24, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('currency', sa.String(3), server_default=sa.text("'USD'"), nullable=True),
        sa.Column('as_of_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ontology_object_id'),
        sa.UniqueConstraint('instrument_id', 'portfolio_id', name='uq_positions_instrument_portfolio'),
        sa.ForeignKeyConstraint(['ontology_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
    )

    op.create_table(
        'trades',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('ontology_object_id', sa.UUID(), nullable=True),
        sa.Column('trade_id', sa.String(128), nullable=True),
        sa.Column('instrument_id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=True),
        sa.Column('counterparty_id', sa.UUID(), nullable=True),
        sa.Column('trade_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('settlement_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trade_type', sa.String(32), nullable=False),
        sa.Column('side', sa.String(8), nullable=False),
        sa.Column('quantity', sa.Numeric(18, 6), nullable=False),
        sa.Column('price', sa.Numeric(18, 6), nullable=False),
        sa.Column('notional', sa.Numeric(24, 6), nullable=True),
        sa.Column('commission', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('fees', sa.Numeric(18, 6), server_default=sa.text('0'), nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, server_default=sa.text("'USD'")),
        sa.Column('trader', sa.String(128), nullable=True),
        sa.Column('broker', sa.String(128), nullable=True),
        sa.Column('status', sa.String(32), server_default=sa.text("'new'"), nullable=True),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ontology_object_id'),
        sa.CheckConstraint("side IN ('BUY', 'SELL')", name='ck_trades_side'),
        sa.ForeignKeyConstraint(['ontology_object_id'], ['ontology_objects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['counterparty_id'], ['counterparties.id']),
    )
    op.create_index('idx_trades_instrument', 'trades', ['instrument_id'])
    op.create_index('idx_trades_portfolio', 'trades', ['portfolio_id'])
    op.create_index('idx_trades_date', 'trades', ['trade_date'])

    op.create_table(
        'pnl',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('instrument_id', sa.UUID(), nullable=True),
        sa.Column('pnl_type', sa.String(32), nullable=False),
        sa.Column('pnl_amount', sa.Numeric(24, 6), nullable=False),
        sa.Column('currency', sa.String(3), server_default=sa.text("'USD'"), nullable=True),
        sa.Column('source', sa.String(64), nullable=True),
        sa.Column('from_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('to_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('attribution', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
    )
    op.create_index('idx_pnl_portfolio', 'pnl', ['portfolio_id'])
    op.create_index('idx_pnl_date', 'pnl', ['to_date'])

    op.create_table(
        'risk_metrics',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('instrument_id', sa.UUID(), nullable=True),
        sa.Column('metric_name', sa.String(128), nullable=False),
        sa.Column('metric_value', sa.Numeric(24, 6), nullable=True),
        sa.Column('metric_type', sa.String(64), nullable=True),
        sa.Column('currency', sa.String(3), server_default=sa.text("'USD'"), nullable=True),
        sa.Column('as_of_date', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('parameters', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id']),
        sa.ForeignKeyConstraint(['instrument_id'], ['instruments.id']),
    )
    op.create_index('idx_risk_portfolio', 'risk_metrics', ['portfolio_id'])
    op.create_index('idx_risk_date', 'risk_metrics', ['as_of_date'])

    op.create_table(
        'pipeline_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipeline_name', sa.String(255), nullable=False),
        sa.Column('status', sa.String(32), nullable=False, server_default=sa.text("'pending'")),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('records_processed', sa.Integer(), server_default=sa.text('0'), nullable=True),
        sa.Column('metadata', sa.JSON(), server_default=sa.text("'{}'"), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'watchlists',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False, server_default=sa.text("'default'")),
        sa.Column('name', sa.String(255), nullable=False, server_default=sa.text("'Default'")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_watchlist_user', 'watchlists', ['user_id'])

    op.create_table(
        'watchlist_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('watchlist_id', sa.UUID(), nullable=False),
        sa.Column('ticker', sa.String(10), nullable=False),
        sa.Column('added_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.Column('notes', sa.Text(), server_default=sa.text("''"), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('watchlist_id', 'ticker', name='uq_watchlist_items_ticker'),
        sa.ForeignKeyConstraint(['watchlist_id'], ['watchlists.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_watchlist_items_ticker', 'watchlist_items', ['ticker'])

    op.create_table(
        'alerts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(16), server_default=sa.text("'info'"), nullable=True),
        sa.Column('category', sa.String(64), nullable=True),
        sa.Column('source_object_id', sa.UUID(), nullable=True),
        sa.Column('condition_expr', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('TRUE'), nullable=True),
        sa.Column('last_triggered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['source_object_id'], ['ontology_objects.id']),
    )


def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('watchlist_items')
    op.drop_table('watchlists')
    op.drop_table('pipeline_runs')
    op.drop_table('risk_metrics')
    op.drop_table('pnl')
    op.drop_table('trades')
    op.drop_table('positions')
    op.drop_table('portfolios')
    op.drop_table('counterparties')
    op.drop_table('data_lineage')
    op.drop_table('audit_log')
    op.drop_table('ontology_object_links')
    op.drop_table('ontology_objects')
    op.drop_table('ontology_links')
    op.drop_table('ontology_properties')
    op.drop_table('ontology_types')
    op.drop_constraint('fk_instruments_ontology_object', 'instruments', type_='foreignkey')