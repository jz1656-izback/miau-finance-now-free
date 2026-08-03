-- Seed the financial ontology types

-- Instrument type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000001', 'Instrument', 'Financial Instrument', 'A financial instrument such as equity, bond, derivative, or currency pair', 'trending-up', '#10b981', '{
  "search_fields": ["ticker", "name", "isin", "sedol"],
  "display_template": "{{ticker}} - {{name}}",
  "default_view": "table"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000001', 'ticker', 'Ticker', 'string', true, true, false, 1),
('a0000000-0000-0000-0000-000000000001', 'isin', 'ISIN', 'string', false, true, false, 2),
('a0000000-0000-0000-0000-000000000001', 'name', 'Instrument Name', 'string', true, true, false, 3),
('a0000000-0000-0000-0000-000000000001', 'instrument_type', 'Type', 'string', true, false, true, 4),
('a0000000-0000-0000-0000-000000000001', 'currency', 'Currency', 'string', true, false, true, 5),
('a0000000-0000-0000-0000-000000000001', 'exchange', 'Exchange', 'string', false, false, true, 6),
('a0000000-0000-0000-0000-000000000001', 'sector', 'Sector', 'string', false, false, true, 7),
('a0000000-0000-0000-0000-000000000001', 'maturity_date', 'Maturity Date', 'date', false, false, false, 8);

-- Counterparty type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000002', 'Counterparty', 'Counterparty', 'An institution or entity that participates in financial transactions', 'building', '#8b5cf6', '{
  "search_fields": ["short_name", "legal_name", "lei"],
  "display_template": "{{short_name}}",
  "default_view": "table"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000002', 'short_name', 'Short Name', 'string', true, true, false, 1),
('a0000000-0000-0000-0000-000000000002', 'legal_name', 'Legal Name', 'string', true, true, false, 2),
('a0000000-0000-0000-0000-000000000002', 'counterparty_type', 'Type', 'string', true, false, true, 3),
('a0000000-0000-0000-0000-000000000002', 'country', 'Country', 'string', false, false, true, 4),
('a0000000-0000-0000-0000-000000000002', 'credit_rating', 'Credit Rating', 'string', false, false, true, 5);

-- Portfolio type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000003', 'Portfolio', 'Portfolio', 'A collection of financial instruments held by an investor', 'briefcase', '#f59e0b', '{
  "search_fields": ["name"],
  "display_template": "{{name}}",
  "default_view": "card"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000003', 'name', 'Portfolio Name', 'string', true, true, false, 1),
('a0000000-0000-0000-0000-000000000003', 'portfolio_type', 'Type', 'string', true, false, true, 2),
('a0000000-0000-0000-0000-000000000003', 'base_currency', 'Base Currency', 'string', true, false, true, 3),
('a0000000-0000-0000-0000-000000000003', 'management_style', 'Management Style', 'string', false, false, true, 4);

-- Trade type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000004', 'Trade', 'Trade', 'A financial transaction to buy or sell an instrument', 'arrow-left-right', '#ef4444', '{
  "search_fields": ["trade_id", "trader"],
  "display_template": "{{side}} {{quantity}} {{_links.instrument.ticker}} @ {{price}}",
  "default_view": "table"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000004', 'trade_id', 'Trade ID', 'string', false, true, false, 1),
('a0000000-0000-0000-0000-000000000004', 'trade_type', 'Trade Type', 'string', true, false, true, 2),
('a0000000-0000-0000-0000-000000000004', 'side', 'Side', 'string', true, false, true, 3),
('a0000000-0000-0000-0000-000000000004', 'quantity', 'Quantity', 'number', true, false, false, 4),
('a0000000-0000-0000-0000-000000000004', 'price', 'Price', 'number', true, false, false, 5),
('a0000000-0000-0000-0000-000000000004', 'notional', 'Notional', 'number', false, false, false, 6),
('a0000000-0000-0000-0000-000000000004', 'trader', 'Trader', 'string', false, true, true, 7),
('a0000000-0000-0000-0000-000000000004', 'status', 'Status', 'string', false, false, true, 8);

-- Position type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000005', 'Position', 'Position', 'Current holding of an instrument in a portfolio', 'layers', '#06b6d4', '{
  "search_fields": [],
  "display_template": "{{quantity}} x {{_links.instrument.ticker}}",
  "default_view": "table"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000005', 'quantity', 'Quantity', 'number', true, false, false, 1),
('a0000000-0000-0000-0000-000000000005', 'average_price', 'Avg Price', 'number', false, false, false, 2),
('a0000000-0000-0000-0000-000000000005', 'market_value', 'Market Value', 'number', false, false, false, 3),
('a0000000-0000-0000-0000-000000000005', 'unrealized_pnl', 'Unrealized P&L', 'number', false, false, false, 4),
('a0000000-0000-0000-0000-000000000005', 'realized_pnl', 'Realized P&L', 'number', false, false, false, 5);

-- MarketData type
INSERT INTO ontology_types (id, name, display_name, description, icon, color, config) VALUES
('a0000000-0000-0000-0000-000000000006', 'MarketData', 'Market Data', 'Historical and real-time market price data for instruments', 'chart-line', '#3b82f6', '{
  "search_fields": [],
  "display_template": "{{_links.instrument.ticker}}: Close={{close}}",
  "default_view": "chart"
}');

INSERT INTO ontology_properties (type_id, name, display_name, data_type, is_required, is_searchable, is_faceted, sort_order) VALUES
('a0000000-0000-0000-0000-000000000006', 'date', 'Date', 'datetime', true, false, false, 1),
('a0000000-0000-0000-0000-000000000006', 'open', 'Open', 'number', false, false, false, 2),
('a0000000-0000-0000-0000-000000000006', 'high', 'High', 'number', false, false, false, 3),
('a0000000-0000-0000-0000-000000000006', 'low', 'Low', 'number', false, false, false, 4),
('a0000000-0000-0000-0000-000000000006', 'close', 'Close', 'number', false, false, false, 5),
('a0000000-0000-0000-0000-000000000006', 'volume', 'Volume', 'number', false, false, false, 6);

-- ============================================
-- ONTOLOGY LINKS: Define relationships
-- ============================================

-- Instrument -> MarketData
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000001', 'has_market_data', 'Has Market Data', 'Market price data for this instrument',
 'a0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000006', 'one_to_many', 'of_instrument', 'ONE_TO_MANY');

-- Portfolio -> Position
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000002', 'holds_position', 'Holds Position', 'Positions held in this portfolio',
 'a0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000005', 'one_to_many', 'in_portfolio', 'ONE_TO_MANY');

-- Portfolio -> Trade
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000003', 'has_trade', 'Has Trade', 'Trades executed in this portfolio',
 'a0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000004', 'one_to_many', 'in_portfolio', 'ONE_TO_MANY');

-- Instrument -> Position
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000004', 'has_position', 'Has Position', 'Positions for this instrument',
 'a0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000005', 'one_to_many', 'of_instrument', 'ONE_TO_MANY');

-- Instrument -> Trade
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000005', 'traded_as', 'Traded As', 'Trades for this instrument',
 'a0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000004', 'one_to_many', 'of_instrument', 'ONE_TO_MANY');

-- Counterparty -> Trade
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000006', 'executed_trade', 'Executed Trade', 'Trades executed with this counterparty',
 'a0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000004', 'one_to_many', 'with_counterparty', 'ONE_TO_MANY');

-- Instrument has underlying (for derivatives)
INSERT INTO ontology_links (id, name, display_name, description, source_type_id, target_type_id, link_type, reverse_name, cardinality) VALUES
('b0000000-0000-0000-0000-000000000007', 'has_underlying', 'Has Underlying', 'Underlying instrument for derivatives',
 'a0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'many_to_one', 'is_underlying_of', 'MANY_TO_ONE');
