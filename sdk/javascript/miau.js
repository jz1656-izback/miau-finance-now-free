/**
 * Miau Finance JavaScript SDK
 * Lightweight fetch-based client for the Miau Finance REST API.
 *
 * ```js
 * import { MiauClient } from './miau.js'
 * const api = new MiauClient({ apiKey: 'miau_abc...' })
 * const price = await api.get('/api/v1/market/live?tickers=AAPL')
 * ```
 */

export class MiauClient {
  constructor(opts = {}) {
    this.baseURL = opts.baseURL || 'http://localhost:8000'
    this.apiKey = opts.apiKey || ''
    this.timeout = opts.timeout || 30000
  }

  async request(method, path, opts = {}) {
    const url = `${this.baseURL}${path}`
    const headers = { 'Content-Type': 'application/json' }
    if (this.apiKey) headers['Authorization'] = `Bearer ${this.apiKey}`

    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)

    try {
      const res = await fetch(url, {
        method,
        headers,
        body: opts.body ? JSON.stringify(opts.body) : undefined,
        signal: controller.signal,
      })
      clearTimeout(timeoutId)
      if (!res.ok) {
        const err = await res.text().catch(() => '')
        throw new Error(`Miau API ${res.status}: ${err || res.statusText}`)
      }
      return res.json()
    } catch (e) {
      clearTimeout(timeoutId)
      throw e
    }
  }

  get(path, params) {
    if (params) {
      const qs = Object.entries(params)
        .filter(([, v]) => v != null)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&')
      path += (path.includes('?') ? '&' : '?') + qs
    }
    return this.request('GET', path)
  }

  post(path, body) { return this.request('POST', path, { body }) }
  put(path, body) { return this.request('PUT', path, { body }) }
  delete(path) { return this.request('DELETE', path) }

  // --- Convenience methods ---

  // Market
  getPrice(ticker) { return this.get('/api/v1/market/live', { tickers: ticker }) }
  getHistory(ticker, period = '1mo') { return this.get(`/api/v1/market/historical/${ticker}`, { period }) }
  getSectors() { return this.get('/api/v1/market/sectors') }
  getMovers() { return this.get('/api/v1/economics/gainers-losers') }

  // Portfolio
  listPortfolios() { return this.get('/api/v1/portfolios') }
  getPortfolio(id) { return this.get(`/api/v1/portfolios/${id}`) }
  getPositions(id) { return this.get(`/api/v1/portfolios/${id}/positions`) }

  // Trading
  listOrders(params) { return this.get('/api/v1/orders', params) }
  createOrder(order) { return this.post('/api/v1/orders', order) }
  cancelOrder(id) { return this.delete(`/api/v1/orders/${id}`) }

  // ESG & Carbon
  getESG(ticker) { return this.get(`/api/v1/esg/${ticker}`) }
  getCarbon(ticker) { return this.get(`/api/v1/carbon/${ticker}`) }
  getGreenOverview() { return this.get('/api/v1/green/overview') }

  // Billing
  getSubscription() { return this.get('/api/v1/billing/subscription') }
  listInvoices() { return this.get('/api/v1/billing/invoices') }

  // Developer
  getDashboard() { return this.get('/api/v1/developer/dashboard') }
  createApiKey(name) { return this.post('/api/v1/developer/api-keys', { name }) }
  revokeApiKey(id) { return this.delete(`/api/v1/developer/api-keys/${id}`) }

  // AI
  aiQuery(query) { return this.post('/api/v1/ai/query', { query }) }
  aiPortfolio(id) { return this.post('/api/v1/ai/advisor/portfolio', { portfolio_id: id }) }
}

export default MiauClient
