import { useState } from 'react'

export default function ApiPlayground() {
  const [method, setMethod] = useState('GET')
  const [path, setPath] = useState('/api/v1/market/live?tickers=AAPL')
  const [body, setBody] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }

  const METHODS = ['GET', 'POST', 'PUT', 'DELETE']

  const examples = [
    { label: 'Market price', method: 'GET', path: '/api/v1/market/live?tickers=AAPL' },
    { label: 'Portfolios', method: 'GET', path: '/api/v1/portfolios' },
    { label: 'ESG score', method: 'GET', path: '/api/v1/esg/AAPL' },
    { label: 'Carbon data', method: 'GET', path: '/api/v1/carbon/AAPL' },
    { label: 'Create order', method: 'POST', path: '/api/v1/orders', body: '{"portfolio_id":"...","symbol":"AAPL","side":"BUY","qty":1}' },
    { label: 'Subscription', method: 'GET', path: '/api/v1/billing/subscription' },
    { label: 'Green finance', method: 'GET', path: '/api/v1/green/overview' },
  ]

  const execute = async () => {
    setLoading(true)
    setError('')
    setResponse('')
    try {
      const opts: RequestInit = { method, headers }
      if (body && (method === 'POST' || method === 'PUT')) opts.body = body
      const res = await fetch(path.startsWith('http') ? path : `http://localhost:8000${path}`, opts)
      const text = await res.text()
      try { setResponse(JSON.stringify(JSON.parse(text), null, 2)) } catch { setResponse(text) }
    } catch (e: any) {
      setError(e.message)
    }
    setLoading(false)
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan flex items-center gap-2">🔌 API Playground</h2>

      <div className="flex flex-wrap gap-2 mb-2">
        {examples.map(ex => (
          <button
            key={ex.label}
            onClick={() => { setMethod(ex.method); setPath(ex.path); setBody(ex.body || '') }}
            className="text-xs bg-gray-800 text-dim hover:text-green px-2 py-1 rounded border border-gray-700"
          >
            {ex.label}
          </button>
        ))}
      </div>

      <div className="flex gap-2">
        <select value={method} onChange={e => setMethod(e.target.value)} className="bg-gray-900 text-green border border-gray-700 rounded px-2 py-1 text-sm">
          {METHODS.map(m => <option key={m} value={m}>{m}</option>)}
        </select>
        <input
          value={path} onChange={e => setPath(e.target.value)}
          placeholder="/api/v1/..."
          className="flex-1 bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green font-mono outline-none"
        />
        <button onClick={execute} disabled={loading} className="px-3 py-1 bg-cyan-800 text-cyan rounded text-sm disabled:opacity-50">
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>

      {(method === 'POST' || method === 'PUT') && (
        <textarea
          value={body} onChange={e => setBody(e.target.value)}
          placeholder='{"key": "value"}'
          className="w-full bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green font-mono h-20 outline-none"
        />
      )}

      {error && <div className="text-red text-xs bg-red-900/20 p-2 rounded">❌ {error}</div>}
      {response && (
        <pre className="bg-gray-900 p-3 rounded text-xs text-green font-mono overflow-x-auto max-h-96">
          {response}
        </pre>
      )}
    </div>
  )
}
