import { getToken, clearToken } from './auth'
import { getLogger } from './logger'
const log = getLogger('api')

const BASE = '/api/v1'

function getCSRFToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]*)/)
  return match ? decodeURIComponent(match[1]) : null
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms))
}

async function fetchJSON<T>(url: string, init?: RequestInit, retries = 3): Promise<T> {
  const startMs = performance.now()
  const method = (init?.method || 'GET').toUpperCase()
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const token = getToken()
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(init?.headers as Record<string, string> | undefined),
      }
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
      if (method !== 'GET' && method !== 'HEAD' && method !== 'OPTIONS') {
        const csrf = getCSRFToken()
        if (csrf) {
          headers['X-CSRF-Token'] = csrf
        }
      }

      const res = await fetch(`${BASE}${url}`, {
        ...init,
        headers,
        credentials: 'include', // pawdentity session uses an HttpOnly cookie
      })

      const durationMs = Math.round(performance.now() - startMs)
      log.apiCall(method, url, res.status, durationMs)

      if (res.status === 401) {
        log.warn('401 Unauthorized', { url })
        clearToken()
        if (attempt === 0) {
          console.warn('[api] 401 Unauthorized — token cleared. Redirecting to login.')
        }
        throw new Error(`API error 401: Unauthorized — token may be expired`)
      }

      if (res.ok) return res.json()

      const err = await res.text()
      if (res.status < 500) throw new Error(`API error ${res.status}: ${err}`)
      if (attempt === retries) throw new Error(`API error ${res.status}: ${err}`)

      const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 500, 10000)
      log.warn(`retry ${attempt + 1}/${retries}`, { url, status: res.status, delayMs: Math.round(delay) })
      console.warn(`[api] retry ${attempt + 1}/${retries} for ${url} (${res.status}), waiting ${Math.round(delay)}ms`)
      await sleep(delay)
    } catch (e) {
      if (e instanceof TypeError && attempt < retries) {
        const delay = Math.min(1000 * Math.pow(2, attempt) + Math.random() * 500, 10000)
        log.apiError(method || 'GET', url, 0, e instanceof Error ? e : undefined)
        console.warn(`[api] network retry ${attempt + 1}/${retries} for ${url}, waiting ${Math.round(delay)}ms`)
        await sleep(delay)
        continue
      }
      throw e
    }
  }
  throw new Error('unreachable')
}

export const api = {
  getTypes: () => fetchJSON<any[]>('/ontology/types'),
  getType: (id: string) => fetchJSON<any>(`/ontology/types/${id}`),
  getObjects: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/ontology/objects${qs}`)
  },
  getObject: (id: string) => fetchJSON<any>(`/ontology/objects/${id}`),
  getLinks: (typeId?: string) => {
    const qs = typeId ? `?type_id=${typeId}` : ''
    return fetchJSON<any[]>(`/ontology/links${qs}`)
  },

  getInstruments: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/instruments${qs}`)
  },
  getInstrument: (id: string) => fetchJSON<any>(`/instruments/${id}`),
  getMarketData: (id: string, params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/instruments/${id}/market-data${qs}`)
  },
  getSectors: () => fetchJSON<string[]>('/instruments/sectors/list'),
  getInstrumentTypes: () => fetchJSON<string[]>('/instruments/types/list'),

  getPortfolios: () => fetchJSON<any[]>('/portfolios'),
  getPortfolio: (id: string) => fetchJSON<any>(`/portfolios/${id}`),
  getPortfolioPositions: (id: string) => fetchJSON<any[]>(`/portfolios/${id}/positions`),
  getPortfolioTrades: (id: string) => fetchJSON<any[]>(`/portfolios/${id}/trades`),

  getTrades: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/trades${qs}`)
  },
  getTrade: (id: string) => fetchJSON<any>(`/trades/${id}`),

  getSummary: () => fetchJSON<any>('/analytics/summary'),
  getPortfolioAnalytics: (id: string) => fetchJSON<any>(`/analytics/portfolios/${id}`),
  getInstrumentPerformance: (id: string) => fetchJSON<any[]>(`/analytics/instruments/${id}/performance`),
  getPnlTimeseries: (portfolioId?: string, days = 30) => {
    const params = new URLSearchParams()
    if (portfolioId) params.set('portfolio_id', portfolioId)
    params.set('days', String(days))
    return fetchJSON<any[]>(`/analytics/pnl/timeseries?${params}`)
  },

  search: (q: string, type?: string) => {
    const params = new URLSearchParams({ q })
    if (type) params.set('type', type)
    return fetchJSON<{ query: string; total: number; results: any[] }>(`/search?${params}`)
  },

  getPipelineRuns: () => fetchJSON<any[]>('/pipelines/runs'),
  calculatePnl: () => fetchJSON<any>('/pipelines/calculate/pnl', { method: 'POST' }),

  // Orders
  getOrders: (params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/orders${qs}`)
  },
  getOrder: (id: string) => fetchJSON<any>(`/orders/${id}`),
  createOrder: (data: Record<string, any>) =>
    fetchJSON<any>('/orders', { method: 'POST', body: JSON.stringify(data) }),
  cancelOrder: (id: string) =>
    fetchJSON<any>(`/orders/${id}`, { method: 'DELETE' }),
  updateOrder: (id: string, data: Record<string, any>) =>
    fetchJSON<any>(`/orders/${id}`, { method: 'PUT', body: JSON.stringify(data) }),

  // Paper Trading
  getPaperPortfolios: () => fetchJSON<any[]>('/paper/portfolios'),
  getPaperPortfolio: (id: string) => fetchJSON<any>(`/paper/portfolios/${id}`),
  createPaperPortfolio: (name: string, initialCash?: number) =>
    fetchJSON<any>('/paper/portfolios', {
      method: 'POST',
      body: JSON.stringify({ name, initial_cash: initialCash ?? 100000 }),
    }),
  executePaperTrade: (portfolioId: string, data: Record<string, any>) =>
    fetchJSON<any>(`/paper/execute/${portfolioId}`, { method: 'POST', body: JSON.stringify(data) }),
  getPaperTrades: (portfolioId: string, params?: Record<string, string>) => {
    const qs = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchJSON<any[]>(`/paper/trades/${portfolioId}${qs}`)
  },

  // Strategies
  getStrategies: () => fetchJSON<any[]>('/strategies'),
  getStrategy: (name: string) => fetchJSON<any>(`/strategies/${name}`),
  getStrategyParams: (name: string) => fetchJSON<any>(`/strategies/${name}/params`),
  runBacktest: (data: Record<string, any>) =>
    fetchJSON<any>('/strategies/backtest', { method: 'POST', body: JSON.stringify(data) }),

  // Brokers
  getBrokerAccounts: () => fetchJSON<any[]>('/brokers/accounts'),
  getBrokerOrders: () => fetchJSON<any[]>('/brokers/orders'),
  submitBrokerOrder: (data: Record<string, any>) =>
    fetchJSON<any>('/brokers/orders', { method: 'POST', body: JSON.stringify(data) }),
}