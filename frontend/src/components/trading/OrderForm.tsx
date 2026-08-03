import { useState, useCallback } from 'react'

const BASE = '/api/v1'
const ORDER_TYPES = ['market', 'limit', 'stop', 'stop_limit']
const SIDES = ['BUY', 'SELL']

export default function OrderForm() {
  const [ticker, setTicker] = useState('')
  const [side, setSide] = useState<'BUY' | 'SELL'>('BUY')
  const [qty, setQty] = useState('')
  const [orderType, setOrderType] = useState('market')
  const [price, setPrice] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{ ok: boolean; message: string } | null>(null)

  const submit = useCallback(async () => {
    if (!ticker || !qty) return
    setLoading(true)
    setResult(null)
    try {
      const body: Record<string, any> = {
        portfolio_id: localStorage.getItem('miau:portfolio_id') || '',
        instrument_id: ticker.toUpperCase(),
        order_type: orderType,
        side,
        quantity: parseFloat(qty),
      }
      if (price && (orderType === 'limit' || orderType === 'stop' || orderType === 'stop_limit')) {
        body.price = parseFloat(price)
      }
      const res = await fetch(`${BASE}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await res.json()
      if (res.ok) {
        setResult({ ok: true, message: `Order created: ${data.id || data.order_id}` })
        setTicker(''); setQty(''); setPrice('')
      } else {
        setResult({ ok: false, message: data.detail || 'Order failed' })
      }
    } catch {
      setResult({ ok: false, message: 'Network error' })
    }
    setLoading(false)
  }, [ticker, side, qty, orderType, price])

  return (
    <div className="glass-panel rounded-lg p-4 space-y-3">
      <h3 className="text-green font-bold text-sm">Place Order</h3>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-dim text-xs block mb-1">Ticker</label>
          <input
            value={ticker}
            onChange={e => setTicker(e.target.value.toUpperCase())}
            className="w-full bg-[#0a1a14] border border-[#1a3a2a] rounded px-2 py-1 text-sm text-green outline-none focus:border-green/50"
            placeholder="AAPL"
          />
        </div>
        <div>
          <label className="text-dim text-xs block mb-1">Quantity</label>
          <input
            value={qty}
            onChange={e => setQty(e.target.value)}
            type="number"
            className="w-full bg-[#0a1a14] border border-[#1a3a2a] rounded px-2 py-1 text-sm text-green outline-none focus:border-green/50"
            placeholder="100"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-dim text-xs block mb-1">Side</label>
          <div className="flex gap-1">
            {SIDES.map(s => (
              <button
                key={s}
                onClick={() => setSide(s as 'BUY' | 'SELL')}
                className={`flex-1 px-2 py-1 text-xs rounded border transition-colors ${
                  side === s
                    ? s === 'BUY' ? 'border-green text-green bg-green/10' : 'border-red text-red bg-red/10'
                    : 'border-[#1a3a2a] text-dim hover:border-green/30'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="text-dim text-xs block mb-1">Order Type</label>
          <select
            value={orderType}
            onChange={e => setOrderType(e.target.value)}
            className="w-full bg-[#0a1a14] border border-[#1a3a2a] rounded px-2 py-1 text-sm text-green outline-none focus:border-green/50"
          >
            {ORDER_TYPES.map(t => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
      </div>

      {(orderType === 'limit' || orderType === 'stop' || orderType === 'stop_limit') && (
        <div>
          <label className="text-dim text-xs block mb-1">Price</label>
          <input
            value={price}
            onChange={e => setPrice(e.target.value)}
            type="number"
            step="0.01"
            className="w-full bg-[#0a1a14] border border-[#1a3a2a] rounded px-2 py-1 text-sm text-green outline-none focus:border-green/50"
            placeholder="150.00"
          />
        </div>
      )}

      <button
        onClick={submit}
        disabled={loading || !ticker || !qty}
        className="w-full px-3 py-2 text-xs font-bold rounded border transition-colors disabled:opacity-40 disabled:cursor-not-allowed
          border-green text-green hover:bg-green/10"
      >
        {loading ? 'Submitting...' : `Place ${side} Order`}
      </button>

      {result && (
        <div className={`text-xs p-2 rounded ${result.ok ? 'text-green bg-green/5 border border-green/20' : 'text-red bg-red/5 border border-red/20'}`}>
          {result.message}
        </div>
      )}
    </div>
  )
}
