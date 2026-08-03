import { describe, it, expect, vi, beforeEach } from 'vitest'

const store: Record<string, string> = { token: 'test-token' }
globalThis.localStorage = {
  getItem: (k: string) => store[k] ?? null,
  setItem: (k: string, v: string) => { store[k] = v },
  removeItem: (k: string) => { delete store[k] },
  clear: () => { Object.keys(store).forEach(k => delete store[k]) },
  length: 0, key: () => null,
}

const mockFetch = vi.fn()
globalThis.fetch = mockFetch

beforeEach(() => { mockFetch.mockReset() })

async function exec(cmd: string) {
  const addLine = vi.fn()
  const { executeCommand } = await import('../src/lib/commands')
  await executeCommand(cmd, addLine)
  return addLine
}

describe('Terminal Commands', () => {
  it('help returns available commands', async () => {
    mockFetch.mockRejectedValue(new Error('no network'))
    const addLine = await exec('help')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls[0][0].text).toContain('help')
  })

  it('whoami returns identity', async () => {
    const addLine = await exec('whoami')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls[0][0].text).toContain('miau')
  })

  it('price AAPL calls API', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ data: { AAPL: { price: 150, change_pct: 1.5, high: 151, low: 149, volume: 1000000, name: 'Apple' } } }) })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ records: [{ close: 148 }, { close: 149 }, { close: 150 }] }) })
    const addLine = await exec('price AAPL')
    expect(addLine).toHaveBeenCalled()
  })

  it('unknown command shows error', async () => {
    const addLine = await exec('nonexistent')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls[0][0].text).toContain('not found')
  })

  it('clear does not crash', async () => {
    const addLine = await exec('clear')
    expect(addLine).not.toHaveBeenCalled()
  })

  it('cat returns ASCII art', async () => {
    const addLine = await exec('cat')
    expect(addLine).toHaveBeenCalled()
  })

  it('fx USD fetches FX rates', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ base: 'USD', rates: { EUR: 0.92 }, count: 3 }) })
    const addLine = await exec('fx USD')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('EUR')
  })

  it('fxconvert converts currency', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ amount: 100, from: 'USD', to: 'EUR', rate: 0.92, result: 92.00 }) })
    const addLine = await exec('fxconvert 100 USD EUR')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('EUR')
  })

  it('quanthealth AAPL fetches quant scores', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ piotroski_f_score: 7, altman_z_score: 3.5, beneish_m_score: -2.5 }) })
    const addLine = await exec('quanthealth AAPL')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('QUANT')
  })

  it('fairvalue AAPL fetches DCF', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ current_price: 150, fair_price: 180, upside_pct: 20 }) })
    const addLine = await exec('fairvalue AAPL')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('FAIR')
  })

  it('defillama fetches protocols', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ protocols: [{ name: 'Lido', tvl: 20000000000, chain: 'ethereum' }], count: 1 }) })
    const addLine = await exec('defillama')
    expect(addLine).toHaveBeenCalled()
  })

  it('dca calculator returns results', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ total_invested: 120000, final_value: 280000, cagr: 8.5 }) })
    const addLine = await exec('dca 500 monthly 20 7')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('280000')
  })

  it('compound calculator returns schedule', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ final_value: 500000, schedule: [{ year: 1, value: 20000, contributions: 16000 }] }) })
    const addLine = await exec('compound 10000 7 30 500')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('500000')
  })

  it('loan calculator returns amortization', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ monthly_payment: 3160, amortization_schedule: [{ payment: 1, monthly: 3160, principal: 450, interest: 2710, balance: 499550 }] }) })
    const addLine = await exec('loan 500000 6.5 30')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('3160')
  })

  it('retirement calculator projects balance', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ retirement_age: 65, projected_balance: 2500000, schedule: [{ year: 5, age: 35, balance: 150000 }] }) })
    const addLine = await exec('retirement 30 50000 1000 7 65')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('2500000')
  })

  it('margin calculator returns liquidation price', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ total_value: 15000, liquidation_price: 75 }) })
    const addLine = await exec('margin 150 100 2')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('75')
  })

  it('montecarlo runs simulation', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ num_simulations: 1000, starting_price: 150, expected_price: 165, prob_of_loss: 0.3 }) })
    const addLine = await exec('montecarlo AAPL 1000 252')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('MONTE')
  })

  it('correlation matrix returns data', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ tickers: ['AAPL', 'MSFT', 'GOOGL'], correlation_matrix: { AAPL: { AAPL: 1, MSFT: 0.7 } }, periods: 252 }) })
    const addLine = await exec('correlation AAPL,MSFT,GOOGL')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('CORRELATION')
  })

  it('pairtrade analyzes pair', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ is_cointegrated: true, current_z_score: 2.5, recent_signals: [{ date: '2026-01-01', z_score: 2.5, action: 'LONG' }] }) })
    const addLine = await exec('pairtrade XOM CVX')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('PAIRS')
  })

  it('datasources fetches provider health', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ providers: [{ provider: 'yahoo', healthy: true, latency_ms: 45, remaining_quota: 55, stats: { rate_limit: 60, success_count: 100, error_count: 0 } }], total: 1, healthy: 1, cache: { memory_entries: 15, hits: 50, misses: 10, hit_rate_pct: 83.3, tiers: ['fast'] }, updated_at: '2026-01-01T00:00:00Z' }) })
    const addLine = await exec('datasources')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('yahoo')
  })

  it('fallback shows chains', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ capabilities: { quote: [{ name: 'yahoo', fallback_order: 1, requires_key: false, rate_limit: 30 }] }, total_capabilities: 1 }) })
    const addLine = await exec('fallback')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('FALLBACK')
  })

  it('gas 1 fetches gas prices', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ chain: 'ethereum-mainnet', safe_gwei: 10, propose_gwei: 15, fast_gwei: 20 }) })
    const addLine = await exec('gas 1')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('GAS')
  })

  it('apikey create calls API', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ raw_key: 'miau_abc123_def456', id: 'key-1', name: 'test-key', key_prefix: 'miau_ab' }) })
    const addLine = await exec('apikey create test-key')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('miau_abc123')
  })

  it('apikey list returns keys', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ keys: [{ provider: 'finnhub', configured: true, masked: 'abc1****xyz9' }] }) })
    const addLine = await exec('apikey list')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('API KEYS')
  })

  it('apikey revoke calls DELETE', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) })
    const addLine = await exec('apikey revoke key-1')
    expect(addLine).toHaveBeenCalled()
    expect(mockFetch.mock.calls[0][1]?.method).toBe('DELETE')
  })

  it('blacklitterman computes portfolio', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ method: 'Market Equilibrium', tickers: ['SPY', 'TLT', 'GLD'], posterior_weights: { SPY: 60, TLT: 20, GLD: 20 } }) })
    const addLine = await exec('blacklitterman SPY,TLT,GLD')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('BLACK-LITTERMAN')
  })

  it('riskparity computes weights', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ target_volatility: 15, portfolio_volatility: 12.5, weights: { SPY: 0.5, TLT: 0.3, GLD: 0.2 }, risk_contributions: { SPY: 0.5, TLT: 0.3, GLD: 0.2 } }) })
    const addLine = await exec('riskparity SPY,TLT,GLD')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('RISK PARITY')
  })

  it('benchmark compares to index', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ ticker: 'AAPL', benchmark: 'SPY', alpha: 2.5, beta: 1.1, tracking_error: 5.2, sharpe_ratio: 1.2 }) })
    const addLine = await exec('benchmark AAPL SPY')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('BENCHMARK')
  })

  it('drawdown analyzes historical data', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ ticker: 'AAPL', max_drawdown: -35.2 }) })
    const addLine = await exec('drawdown AAPL')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('DRAWDOWN')
  })

  it('autodiscover probes API', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ url: 'https://api.example.com', endpoints_found: 3, endpoints_tested: 20, detected_models: [{ endpoint: '/api/v1/quote/AAPL', detected_type: 'Quote', status: 200 }], recommendation: 'Found' }) })
    const addLine = await exec('autodiscover https://api.example.com AAPL')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('AUTO-INTEGRATE')
  })

  it('daily claims free tuna', async () => {
    const addLine = await exec('daily')
    expect(addLine).toHaveBeenCalled()
    expect(addLine.mock.calls.map((c: any) => c[0].text).join(' ')).toContain('DAILY BONUS')
  })
})
