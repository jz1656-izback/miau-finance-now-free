/**
 * 🐱 AI AUTOCOMPLETE ENGINE
 * Phase 13.2 — Context-aware command suggestions with usage-based ranking,
 * subcommand completion, sliding-window recency scoring, and NL query detection.
 */

export interface AutocompleteMatch {
  text: string
  score: number
  type: 'command' | 'ticker' | 'arg' | 'alias'
  description?: string
}

const COMMAND_META: Record<string, { desc: string; args?: string; subcommands?: string[] }> = {
  price:              { desc: 'Live price & change', args: '<ticker>' },
  chart:              { desc: 'ASCII price chart', args: '<ticker>' },
  crypto:             { desc: 'Bitcoin & top cryptos' },
  cryptomkt:          { desc: 'Crypto market overview' },
  cryptohist:         { desc: 'Crypto price history', args: '<coin>' },
  fear:               { desc: 'Fear & Greed index' },
  forex:              { desc: 'Forex rates' },
  sectors:            { desc: 'Sector performance' },
  movers:             { desc: 'Market gainers/losers' },
  commodities:        { desc: 'Gold, oil, silver' },
  treasury:           { desc: 'US Treasury yields' },
  breadth:            { desc: 'Market breadth (VIX, etc)' },
  indicators:         { desc: 'Market indicators' },
  portfolios:         { desc: 'List portfolios' },
  portfolio:          { desc: 'Portfolio details', args: '<id>' },
  positions:          { desc: 'Position breakdown', args: '<id>' },
  summary:            { desc: 'Platform summary' },
  trades:             { desc: 'Recent trades' },
  signals:            { desc: 'Technical signals', args: '<ticker>' },
  multisig:           { desc: 'Multi-asset signals', args: '<t1,t2>' },
  backtest:           { desc: 'Backtest strategy', args: '<ticker>' },
  optimize:           { desc: 'Max Sharpe portfolio', args: '<tickers>' },
  minvar:             { desc: 'Min variance portfolio', args: '<tickers>' },
  eqweight:           { desc: 'Equal weight portfolio', args: '<tickers>' },
  risk:               { desc: 'Full risk report', args: '<ticker>' },
  var:                { desc: 'Value at Risk', args: '<ticker>' },
  beta:               { desc: 'Beta vs market', args: '<ticker>' },
  stress:             { desc: 'Stress test', args: '<ticker>' },
  greeks:             { desc: 'Options Greeks' },
  correlation:        { desc: 'Asset correlation matrix' },
  corr:               { desc: 'Asset correlation matrix (alias)' },
  factors:            { desc: 'Fama-French analysis', args: '<ticker>' },
  fundamentals:       { desc: 'Company financials', args: '<ticker>' },
  news:               { desc: 'Company news', args: '<ticker>' },
  marketnews:         { desc: 'Market news' },
  earnings:           { desc: 'Earnings calendar', args: '<ticker>' },
  search:             { desc: 'Search instruments', args: '<query>' },
  watch:              { desc: 'Watchlist', subcommands: ['list', 'add', 'rm'] },
  alert:              { desc: 'Price alerts', subcommands: ['list', 'create', 'enable', 'disable', 'delete', 'history', 'examples'] },
  attrib:             { desc: 'Portfolio attribution', subcommands: ['sector', 'security', 'factor'] },
  ai:                 { desc: 'AI advisor', subcommands: ['portfolio', 'market', 'risk', 'query'] },
  ask:                { desc: 'Natural language query', args: '<text>' },
  help:               { desc: 'Show help' },
  clear:              { desc: 'Clear screen' },
  cat:                { desc: 'Print a cat 🐱' },
  cats:               { desc: 'Cat army' },
  joke:               { desc: 'Cat/finance joke' },
  whoami:             { desc: 'Who are you?' },
  miau:               { desc: '🐱' },
  login:              { desc: 'Authenticate', args: '<username>' },
  logout:             { desc: 'Clear auth token' },
  map:                { desc: 'Toggle 3D globe' },
  heatmap:            { desc: 'Sector heatmap' },
  scorecard:          { desc: 'Productivity scorecard' },
  all:                { desc: 'Aggregate market data' },
  split:              { desc: 'Split terminal' },
  exit:               { desc: 'Exit terminal' },
  back:               { desc: 'Return to terminal' },
  order:              { desc: 'Order management', subcommands: ['create', 'list', 'cancel', 'status'] },
  paper:              { desc: 'Paper trading', subcommands: ['create', 'list', 'buy', 'sell', 'positions', 'pnl'] },
  strategy:           { desc: 'Strategy backtesting', subcommands: ['list', 'backtest', 'compare'] },
  broker:             { desc: 'Broker connection', subcommands: ['list', 'connect', 'balance', 'positions', 'submit'] },
  billing:            { desc: 'Billing & subscription', subcommands: ['portal'] },
  subscribe:          { desc: 'Alias for billing' },
  share:              { desc: 'Share portfolio', args: '<id>' },
  feed:               { desc: 'Social feed', subcommands: ['global', 'following', 'own'] },
  comments:           { desc: 'View comments', args: '<id>' },
  profile:            { desc: 'View profile', args: '[name]' },
  follow:             { desc: 'Follow user', args: '<name>' },
  unfollow:           { desc: 'Unfollow user', args: '<name>' },
  leaderboard:        { desc: 'Trading leaderboard', args: '[metric]' },
  journal:            { desc: 'Trading journal', subcommands: ['add', 'list'] },
  chaos:              { desc: 'Toggle chaos mode' },
  panic:              { desc: 'Hide everything' },
  sudo:               { desc: 'Pretend to be root' },
  hack:               { desc: 'Cyber attack sequence' },
  sparkline:          { desc: 'Compact sparklines', args: '<t...>' },
  apikey:             { desc: 'API key management', subcommands: ['create', 'list', 'revoke'] },
  devconsole:         { desc: 'Developer console' },
  developer:          { desc: 'Developer console (alias)' },
  scenario:           { desc: 'Scenario analysis', args: '<ticker>' },
  dividends:          { desc: 'Dividend calendar', args: '<ticker>' },
  rolling:            { desc: 'Rolling metrics', args: '<ticker>' },
  esg:                { desc: 'ESG scores', subcommands: ['portfolio', 'screen'] },
  carbon:             { desc: 'Carbon footprint', subcommands: ['portfolio'] },
  green:              { desc: 'Green finance', subcommands: ['energy', 'bonds', 'funds'] },
  sheetz:             { desc: 'Investment banking valuations', subcommands: ['miau'] },
  ls:                 { desc: 'List portfolios (→ portfolios)' },
  ps:                 { desc: 'Recent trades (→ trades)' },
  ping:               { desc: 'Platform summary (→ summary)' },
  rm:                 { desc: 'Portfolio details (→ portfolio)' },
  df:                 { desc: 'List portfolios (→ portfolios)' },
  top:                { desc: 'Bitcoin & cryptos (→ crypto)' },
  achievements:       { desc: 'View unlocked achievements & points' },
  anportfolio:        { desc: 'Portfolio analytics', args: '<id>' },
  anrisk:             { desc: 'Risk analytics', args: '<id>' },
  autodiscover:       { desc: 'Auto-discover API plugins', args: '<url>' },
  calc:               { desc: 'Calculate P&L' },
  catberg:            { desc: 'Enter Bloomberg Catberg terminal' },
  chartz:             { desc: 'ASCII chart', args: '<ticker>' },
  cpi:                { desc: 'US CPI economic data' },
  crosschain:         { desc: 'Cross-chain bridge volumes' },
  cryptotop:          { desc: 'Top cryptocurrencies by cap', args: '[limit]' },
  currencies:         { desc: 'Currency exchange rates' },
  currency:           { desc: 'Currency exchange rates (alias)' },
  datasources:        { desc: 'Data source health dashboard' },
  date:               { desc: 'Current market date/time' },
  defi:               { desc: 'DeFi protocol data', subcommands: ['overview', 'tvl', 'yields', 'lending', 'stats', 'compare'] },
  dexs:               { desc: 'DEX trading volumes' },
  earningscore:       { desc: 'Earnings quality score', args: '<ticker>' },
  employment:         { desc: 'US employment data' },
  fairvalue:          { desc: 'Fair value estimate', args: '<ticker>' },
  fallback:           { desc: 'Provider fallback chain status' },
  global:             { desc: 'Global market data by exchange', args: '<exchange>' },
  health:             { desc: 'System health (uptime, providers, logs)' },
  insider:            { desc: 'Insider trading activity', args: '<ticker>' },
  instruments:        { desc: 'List financial instruments' },
  instypes:           { desc: 'Instrument type categories' },
  intraday:           { desc: 'Intraday price data', args: '<ticker>' },
  ipo:                { desc: 'IPO calendar' },
  like:               { desc: 'Like a social post', args: '<id>' },
  macro:              { desc: 'Macroeconomic indicators', args: '[country]' },
  newsbatch:          { desc: 'Batch news for tickers', args: '<t1,t2,...>' },
  notifications:      { desc: 'List notifications' },
  onobjects:          { desc: 'Ontology objects' },
  ontypes:            { desc: 'Ontology types' },
  optperf:            { desc: 'Portfolio optimizer performance' },
  ownership:          { desc: 'Institutional ownership', args: '<ticker>' },
  performance:        { desc: 'Portfolio performance', args: '<id>' },
  pipelines:          { desc: 'Data pipeline runs' },
  pnl:                { desc: 'Profit & loss statement', args: '[days]' },
  pricing:            { desc: 'Pricing models & analytics', subcommands: ['models', 'surface', 'chains'] },
  proposal:           { desc: 'Governance proposals', subcommands: ['list', 'vote', 'create'] },
  pwd:                { desc: 'Current user identity' },
  quanthealth:        { desc: 'Quantitative health score', args: '<ticker>' },
  riskfactors:        { desc: 'Factor risk decomposition', args: '<ticker>' },
  screener:            { desc: 'Stock screener', args: '[--filters]' },
  sectors_exposure:   { desc: 'Sector exposure for ticker', args: '<ticker>' },
  sectorsexposure:    { desc: 'Sector exposure (alias)' },
  sectorslist:        { desc: 'List market sectors' },
  short:              { desc: 'Short interest data', args: '<ticker>' },
  technicals:         { desc: 'Technical analysis indicators', args: '<ticker>' },
  theme:              { desc: 'Apply terminal color theme', args: '<name>' },
  ticker:             { desc: 'Search ticker info', args: '<query>' },
  tjournal:           { desc: 'Trading journal', subcommands: ['list', 'add'] },
  wallet:             { desc: 'DeFi wallet info', subcommands: ['balance', 'history'] },
}

const TOP_TICKERS = [
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
  'SPY', 'QQQ', 'DIA', 'IWM', 'VTI', 'VOO', 'ARKK',
  'BTC', 'ETH', 'SOL', 'DOGE', 'XRP', 'ADA',
  'BA', 'JPM', 'GS', 'DIS', 'NFLX', 'V', 'WMT',
  'GC=F', 'CL=F', 'SI=F', 'EURUSD=X', 'JPY=X',
]

const HISTORY_KEY = 'miau_command_history'
const RECENCY_KEY = 'miau_command_recency'
const MAX_RECENCY = 20

function getFrequencyMap(): Record<string, number> {
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* ignore */ }
  return {}
}

function getRecencyQueue(): string[] {
  try {
    const raw = localStorage.getItem(RECENCY_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* ignore */ }
  return []
}

function recordCommand(cmd: string): void {
  const map = getFrequencyMap()
  map[cmd] = (map[cmd] || 0) + 1
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(map))
  } catch { /* ignore */ }
  const queue = getRecencyQueue()
  const idx = queue.indexOf(cmd)
  if (idx !== -1) queue.splice(idx, 1)
  queue.unshift(cmd)
  if (queue.length > MAX_RECENCY) queue.length = MAX_RECENCY
  try {
    localStorage.setItem(RECENCY_KEY, JSON.stringify(queue))
  } catch { /* ignore */ }
}

/** Fuzzy match score: higher is better. Prefers prefix and substring matches. */
function fuzzyScore(query: string, candidate: string): number {
  const q = query.toLowerCase()
  const c = candidate.toLowerCase()
  if (q === c) return 100
  if (c.startsWith(q)) return 80 + (10 - q.length) * 2
  if (c.includes(q)) return 50 + q.length
  let qi = 0
  let score = 0
  for (let i = 0; i < c.length && qi < q.length; i++) {
    if (c[i] === q[qi]) {
      score += 10 - (i - qi)
      qi++
    }
  }
  if (qi === q.length) return Math.max(20, score)
  return 0
}

/** Score boost from recency: 0..15 based on position in sliding window. */
function recencyBoost(cmd: string, recency: string[]): number {
  const idx = recency.indexOf(cmd)
  if (idx === -1) return 0
  return Math.max(0, 15 - idx)
}

const TICKER_SUBCOMMANDS: Record<string, string[]> = {
  price: TOP_TICKERS,
  chart: TOP_TICKERS,
  signals: TOP_TICKERS,
  backtest: TOP_TICKERS,
  risk: TOP_TICKERS,
  var: TOP_TICKERS,
  beta: TOP_TICKERS,
  stress: TOP_TICKERS,
  fundamentals: TOP_TICKERS,
  news: TOP_TICKERS,
  earnings: TOP_TICKERS,
  factors: TOP_TICKERS,
  scenario: TOP_TICKERS,
  dividends: TOP_TICKERS,
  rolling: TOP_TICKERS,
}

/** Detect if input looks like a natural language query (ask-like). */
function isNaturalLanguageQuery(input: string): boolean {
  const lower = input.trim().toLowerCase()
  if (lower.startsWith('ask ') || lower.startsWith('ai ')) return false
  const nlPatterns = [
    /^(what|how|why|when|where|who|which|show|tell|find|get|list|give|do|is|are|can|could|would|will)\b/i,
    /^(price|value|worth|performance|return|yield)\s+(of|for)\b/i,
    /^(buy|sell|trade|invest)\s/i,
  ]
  return nlPatterns.some(p => p.test(lower))
}

/**
 * Get smart autocomplete suggestions based on current input.
 * @param input - Full current input text
 * @param limit - Maximum number of suggestions
 */
export function getSuggestions(input: string, limit = 10): AutocompleteMatch[] {
  const trimmed = input.trim()
  const parts = trimmed.split(/\s+/)
  const word = parts[parts.length - 1] || ''
  const freq = getFrequencyMap()
  const recency = getRecencyQueue()
  const cmd = parts[0]?.toLowerCase()

  // --- Subcommand completion (2+ tokens) ---
  if (parts.length >= 2 && cmd) {
    const meta = COMMAND_META[cmd]
    if (meta?.subcommands?.length) {
      const scored = meta.subcommands
        .map(sc => ({ text: sc, score: fuzzyScore(word, sc), type: 'arg' as const, description: '' }))
        .filter(m => m.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, limit)
      if (scored.length > 0) return scored
    }
    const tickers = TICKER_SUBCOMMANDS[cmd]
    if (tickers) {
      return tickers
        .filter(t => t.toLowerCase().startsWith(word.toLowerCase()))
        .slice(0, limit)
        .map(t => ({ text: t, score: 95, type: 'ticker' as const }))
    }
    if (cmd === 'optimize' || cmd === 'minvar' || cmd === 'eqweight' || cmd === 'multisig') {
      return TOP_TICKERS
        .filter(t => t.toLowerCase().startsWith(word.toLowerCase()))
        .slice(0, limit)
        .map(t => ({ text: t, score: 95, type: 'ticker' as const }))
    }
  }

  // --- Command completion (1 token) ---
  if (parts.length === 1) {
    const scored = Object.entries(COMMAND_META)
      .map(([cmdName, meta]) => {
        const score = fuzzyScore(word, cmdName) + (freq[cmdName] || 0) * 2 + recencyBoost(cmdName, recency)
        return { text: cmdName, score, type: 'command' as const, description: meta.desc }
      })
      .filter(m => m.score > 0)
      .sort((a, b) => b.score - a.score)

    const prefixMatches = scored.filter(s => s.text.startsWith(word.toLowerCase()))
    const otherMatches = scored.filter(s => !s.text.startsWith(word.toLowerCase()))
    let results = [...prefixMatches, ...otherMatches].slice(0, limit)

    // If input looks like NL, offer "ask" shortcut
    if (results.length > 0 && isNaturalLanguageQuery(trimmed)) {
      results.push({
        text: `ask ${trimmed}`,
        score: 60,
        type: 'command',
        description: 'Ask AI about this',
      })
    }
    return results
  }

  return []
}

export { recordCommand }
