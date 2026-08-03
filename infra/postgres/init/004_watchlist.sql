-- Miau Finance: Watchlist table
-- Schema version 1.0

CREATE TABLE IF NOT EXISTS watchlists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL DEFAULT 'default',
    name VARCHAR(255) NOT NULL DEFAULT 'Default',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS watchlist_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    watchlist_id UUID NOT NULL REFERENCES watchlists(id) ON DELETE CASCADE,
    ticker VARCHAR(10) NOT NULL,
    added_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT DEFAULT '',
    UNIQUE(watchlist_id, ticker)
);

CREATE INDEX IF NOT EXISTS idx_watchlist_items_ticker ON watchlist_items(ticker);
CREATE INDEX IF NOT EXISTS idx_watchlist_user ON watchlists(user_id);
