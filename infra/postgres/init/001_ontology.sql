-- Miau Finance: Purrantir-like Ontology for Finance
-- Schema version 1.0

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- ONTOLOGY CORE: Dynamic type system
-- ============================================

CREATE TABLE ontology_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    namespace VARCHAR(255) DEFAULT 'default',
    icon VARCHAR(64) DEFAULT 'database',
    color VARCHAR(7) DEFAULT '#6366f1',
    config JSONB DEFAULT '{}',
    is_abstract BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ontology_properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type_id UUID NOT NULL REFERENCES ontology_types(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    data_type VARCHAR(64) NOT NULL,
    is_required BOOLEAN DEFAULT FALSE,
    is_unique BOOLEAN DEFAULT FALSE,
    is_searchable BOOLEAN DEFAULT FALSE,
    is_faceted BOOLEAN DEFAULT FALSE,
    default_value TEXT,
    validation_rules JSONB DEFAULT '{}',
    ui_config JSONB DEFAULT '{}',
    sort_order INTEGER DEFAULT 0,
    UNIQUE(type_id, name)
);

CREATE TABLE ontology_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    source_type_id UUID NOT NULL REFERENCES ontology_types(id) ON DELETE CASCADE,
    target_type_id UUID NOT NULL REFERENCES ontology_types(id) ON DELETE CASCADE,
    link_type VARCHAR(64) DEFAULT 'many_to_many',
    reverse_name VARCHAR(255),
    cardinality VARCHAR(32) DEFAULT 'ONE_TO_MANY',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- ONTOLOGY OBJECTS: Instances of types
-- ============================================

CREATE TABLE ontology_objects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type_id UUID NOT NULL REFERENCES ontology_types(id) ON DELETE CASCADE,
    display_name VARCHAR(500) NOT NULL,
    description TEXT,
    properties JSONB DEFAULT '{}',
    status VARCHAR(64) DEFAULT 'active',
    tags TEXT[] DEFAULT '{}',
    created_by VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ontology_objects_type ON ontology_objects(type_id);
CREATE INDEX idx_ontology_objects_status ON ontology_objects(status);
CREATE INDEX idx_ontology_objects_name ON ontology_objects USING gin(display_name gin_trgm_ops);
CREATE INDEX idx_ontology_objects_properties ON ontology_objects USING gin(properties);
CREATE INDEX idx_ontology_objects_tags ON ontology_objects USING gin(tags);

CREATE TABLE ontology_object_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    link_id UUID NOT NULL REFERENCES ontology_links(id) ON DELETE CASCADE,
    source_object_id UUID NOT NULL REFERENCES ontology_objects(id) ON DELETE CASCADE,
    target_object_id UUID NOT NULL REFERENCES ontology_objects(id) ON DELETE CASCADE,
    properties JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(link_id, source_object_id, target_object_id)
);

CREATE INDEX idx_object_links_source ON ontology_object_links(source_object_id);
CREATE INDEX idx_object_links_target ON ontology_object_links(target_object_id);

-- ============================================
-- AUDIT & LINEAGE
-- ============================================

CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    object_id UUID REFERENCES ontology_objects(id),
    object_type_id UUID REFERENCES ontology_types(id),
    action VARCHAR(64) NOT NULL,
    field_name VARCHAR(255),
    old_value TEXT,
    new_value TEXT,
    performed_by VARCHAR(255),
    performed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_object ON audit_log(object_id);
CREATE INDEX idx_audit_time ON audit_log(performed_at DESC);

CREATE TABLE data_lineage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_object_id UUID REFERENCES ontology_objects(id),
    target_object_id UUID REFERENCES ontology_objects(id),
    pipeline_name VARCHAR(255),
    transformation_type VARCHAR(64),
    metadata JSONB DEFAULT '{}',
    run_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- FINANCIAL ONTOLOGY: Domain-specific views
-- ============================================

-- These are convenience views that mirror the ontology
-- but provide typed columns for common financial concepts

CREATE TABLE instruments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ontology_object_id UUID UNIQUE REFERENCES ontology_objects(id) ON DELETE CASCADE,
    ticker VARCHAR(32) NOT NULL,
    isin VARCHAR(12),
    sedol VARCHAR(7),
    cusip VARCHAR(9),
    name VARCHAR(500) NOT NULL,
    instrument_type VARCHAR(64) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    exchange VARCHAR(64),
    sector VARCHAR(128),
    industry VARCHAR(128),
    country VARCHAR(64),
    issue_date DATE,
    maturity_date DATE,
    coupon_rate DECIMAL(10,6),
    underlying_instrument_id UUID REFERENCES instruments(id),
    strike_price DECIMAL(18,6),
    option_type VARCHAR(16),
    lot_size INTEGER DEFAULT 1,
    status VARCHAR(32) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_instruments_ticker ON instruments(ticker);
CREATE INDEX idx_instruments_isin ON instruments(isin);
CREATE INDEX idx_instruments_type ON instruments(instrument_type);

CREATE TABLE counterparties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ontology_object_id UUID UNIQUE REFERENCES ontology_objects(id) ON DELETE CASCADE,
    short_name VARCHAR(64) NOT NULL,
    legal_name VARCHAR(500) NOT NULL,
    counterparty_type VARCHAR(64) NOT NULL,
    country VARCHAR(64),
    credit_rating VARCHAR(8),
    sector VARCHAR(128),
    lei VARCHAR(20),
    status VARCHAR(32) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ontology_object_id UUID UNIQUE REFERENCES ontology_objects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    portfolio_type VARCHAR(64) NOT NULL DEFAULT 'trading',
    base_currency VARCHAR(3) DEFAULT 'USD',
    management_style VARCHAR(64),
    benchmark_id VARCHAR(64),
    status VARCHAR(32) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ontology_object_id UUID UNIQUE REFERENCES ontology_objects(id) ON DELETE CASCADE,
    trade_id VARCHAR(128),
    instrument_id UUID NOT NULL REFERENCES instruments(id),
    portfolio_id UUID REFERENCES portfolios(id),
    counterparty_id UUID REFERENCES counterparties(id),
    trade_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    settlement_date TIMESTAMPTZ,
    trade_type VARCHAR(32) NOT NULL,
    side VARCHAR(8) NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity DECIMAL(18,6) NOT NULL,
    price DECIMAL(18,6) NOT NULL,
    notional DECIMAL(24,6),
    commission DECIMAL(18,6) DEFAULT 0,
    fees DECIMAL(18,6) DEFAULT 0,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    trader VARCHAR(128),
    broker VARCHAR(128),
    status VARCHAR(32) DEFAULT 'new',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_trades_instrument ON trades(instrument_id);
CREATE INDEX idx_trades_portfolio ON trades(portfolio_id);
CREATE INDEX idx_trades_date ON trades(trade_date DESC);

CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ontology_object_id UUID UNIQUE REFERENCES ontology_objects(id) ON DELETE CASCADE,
    instrument_id UUID NOT NULL REFERENCES instruments(id),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    quantity DECIMAL(18,6) NOT NULL DEFAULT 0,
    average_price DECIMAL(18,6),
    cost_basis DECIMAL(24,6),
    market_value DECIMAL(24,6),
    unrealized_pnl DECIMAL(24,6),
    realized_pnl DECIMAL(24,6) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'USD',
    as_of_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(instrument_id, portfolio_id)
);

CREATE TABLE market_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    instrument_id UUID NOT NULL REFERENCES instruments(id),
    date TIMESTAMPTZ NOT NULL,
    open DECIMAL(18,6),
    high DECIMAL(18,6),
    low DECIMAL(18,6),
    close DECIMAL(18,6),
    volume BIGINT,
    adj_close DECIMAL(18,6),
    bid DECIMAL(18,6),
    ask DECIMAL(18,6),
    source VARCHAR(64) DEFAULT 'manual',
    metadata JSONB DEFAULT '{}',
    UNIQUE(instrument_id, date)
);

CREATE INDEX idx_market_data_instrument ON market_data(instrument_id);
CREATE INDEX idx_market_data_date ON market_data(date DESC);

CREATE TABLE risk_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    instrument_id UUID REFERENCES instruments(id),
    metric_name VARCHAR(128) NOT NULL,
    metric_value DECIMAL(24,6),
    metric_type VARCHAR(64),
    currency VARCHAR(3) DEFAULT 'USD',
    as_of_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    parameters JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_risk_portfolio ON risk_metrics(portfolio_id);
CREATE INDEX idx_risk_date ON risk_metrics(as_of_date DESC);

CREATE TABLE pnl (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id),
    instrument_id UUID REFERENCES instruments(id),
    pnl_type VARCHAR(32) NOT NULL,
    pnl_amount DECIMAL(24,6) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    source VARCHAR(64),
    from_date TIMESTAMPTZ,
    to_date TIMESTAMPTZ,
    attribution JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_pnl_portfolio ON pnl(portfolio_id);
CREATE INDEX idx_pnl_date ON pnl(to_date DESC);

-- ============================================
-- PIPELINE METADATA
-- ============================================

CREATE TABLE pipeline_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pipeline_name VARCHAR(255) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    records_processed INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(16) DEFAULT 'info',
    category VARCHAR(64),
    source_object_id UUID REFERENCES ontology_objects(id),
    condition_expr TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
