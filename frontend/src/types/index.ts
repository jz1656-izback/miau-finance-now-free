export interface OntologyType {
  id: string
  name: string
  display_name: string
  description: string | null
  namespace: string
  icon: string
  color: string
  config: Record<string, any>
  is_abstract: boolean
  created_at: string
  updated_at: string
  properties?: OntologyProperty[]
  links?: OntologyLink[]
}

export interface OntologyProperty {
  id: string
  type_id: string
  name: string
  display_name: string
  description: string | null
  data_type: string
  is_required: boolean
  is_unique: boolean
  is_searchable: boolean
  is_faceted: boolean
  default_value: string | null
  sort_order: number
}

export interface OntologyLink {
  id: string
  name: string
  display_name: string
  description: string | null
  source_type_id: string
  target_type_id: string
  link_type: string
  reverse_name: string | null
  cardinality: string
  source_type_name?: string
  target_type_name?: string
}

export interface OntologyObject {
  id: string
  type_id: string
  display_name: string
  description: string | null
  properties: Record<string, any>
  status: string
  tags: string[]
  created_by: string | null
  created_at: string
  updated_at: string
  type_name?: string
  type_icon?: string
  type_color?: string
  links?: ObjectLink[]
}

export interface ObjectLink {
  id: string
  link_id: string
  source_object_id: string
  target_object_id: string
  properties: Record<string, any>
  created_at: string
  link_name?: string
  link_display_name?: string
  reverse_name?: string | null
  cardinality?: string
  source_name?: string
  target_name?: string
  source_type_id?: string
  target_type_id?: string
  source_type_name?: string
  target_type_name?: string
}

export interface Instrument {
  id: string
  ontology_object_id: string
  ticker: string
  isin: string | null
  sedol: string | null
  cusip: string | null
  name: string
  instrument_type: string
  currency: string
  exchange: string | null
  sector: string | null
  industry: string | null
  status: string
  created_at: string
}

export interface Portfolio {
  id: string
  name: string
  portfolio_type: string
  base_currency: string
  management_style: string | null
  status: string
  num_positions?: number
  total_value?: number
  positions?: Position[]
}

export interface Position {
  id: string
  instrument_id: string
  portfolio_id: string
  quantity: number
  average_price: number | null
  cost_basis: number | null
  market_value: number | null
  unrealized_pnl: number | null
  realized_pnl: number | null
  ticker?: string
  instrument_name?: string
  instrument_type?: string
  sector?: string
}

export interface Trade {
  id: string
  trade_id: string | null
  instrument_id: string
  portfolio_id: string | null
  counterparty_id: string | null
  trade_date: string
  trade_type: string
  side: string
  quantity: number
  price: number
  notional: number | null
  trader: string | null
  status: string
  ticker?: string
  instrument_name?: string
  portfolio_name?: string
  counterparty_name?: string
}

export interface MarketData {
  id: string
  instrument_id: string
  date: string
  open: number | null
  high: number | null
  low: number | null
  close: number | null
  volume: number | null
}

export interface DashboardSummary {
  total_portfolios: number
  total_instruments: number
  total_trades: number
  total_aum: number
  total_unrealized_pnl: number
  total_realized_pnl: number
}

export interface PortfolioAnalytics {
  summary: {
    id: string
    name: string
    portfolio_type: string
    base_currency: string
    num_positions: number
    total_market_value: number
    total_unrealized_pnl: number
    total_realized_pnl: number
    num_trades: number
    total_pnl: number
  }
  pnl_timeseries: PnLRow[]
  risk_metrics: RiskMetric[]
}

export interface PnLRow {
  date: string
  portfolio_id: string
  pnl_type: string
  total_pnl: number
}

export interface RiskMetric {
  metric_name: string
  metric_value: number
  metric_type: string | null
  currency: string
  as_of_date: string
}

export interface SearchResult {
  id: string
  display_name: string
  description: string | null
  type_name: string
  type_display_name: string
  type_icon: string
  type_color: string
  rank: number | null
}
