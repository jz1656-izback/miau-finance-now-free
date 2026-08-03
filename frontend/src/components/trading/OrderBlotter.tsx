import { useState, useEffect, useCallback } from 'react'

interface Order {
  id: string
  instrument_id: string
  ticker?: string
  side: string
  quantity: number
  order_type: string
  price?: number
  status: string
  created_at?: string
}

const BASE = '/api/v1'

export default function OrderBlotter() {
  const [orders, setOrders] = useState<Order[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')
  const [expanded, setExpanded] = useState<string | null>(null)

  const fetchOrders = useCallback(async () => {
    setLoading(true)
    try {
      const url = filter ? `${BASE}/orders?status=${filter}` : `${BASE}/orders`
      const res = await fetch(url)
      const data = await res.json()
      setOrders(data.items || [])
    } catch {}
    setLoading(false)
  }, [filter])

  useEffect(() => { fetchOrders() }, [fetchOrders])

  const cancelOrder = useCallback(async (id: string) => {
    try {
      await fetch(`${BASE}/orders/${id}`, { method: 'DELETE' })
      fetchOrders()
    } catch {}
  }, [fetchOrders])

  const statusColor = (s: string) => {
    switch (s) {
      case 'filled': return 'text-green'
      case 'cancelled': case 'rejected': return 'text-red'
      case 'pending': case 'submitted': return 'text-yellow'
      default: return 'text-dim'
    }
  }

  return (
    <div className="glass-panel rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-green font-bold text-sm">Order Blotter</h3>
        <button
          onClick={fetchOrders}
          className="text-xs text-dim hover:text-green transition-colors"
        >
          ⟳ Refresh
        </button>
      </div>

      <div className="flex gap-1 mb-3 flex-wrap">
        {['', 'pending', 'filled', 'cancelled'].map(s => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-2 py-1 text-xs rounded border transition-colors ${
              filter === s
                ? 'border-green text-green bg-green/10'
                : 'border-[#1a3a2a] text-dim hover:border-green/30'
            }`}
          >
            {s || 'All'}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="text-dim text-xs">Loading...</div>
      ) : orders.length === 0 ? (
        <div className="text-dim text-xs">No orders</div>
      ) : (
        <div className="space-y-1 max-h-64 overflow-y-auto">
          {orders.map(o => (
            <div
              key={o.id}
              className="border border-[#1a3a2a] rounded p-2 cursor-pointer hover:border-green/30 transition-colors"
              onClick={() => setExpanded(expanded === o.id ? null : o.id)}
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="text-green font-semibold">{(o.ticker || o.instrument_id || '').substring(0, 8)}</span>
                  <span className={o.side === 'BUY' ? 'text-green' : 'text-red'}>{o.side}</span>
                  <span className="text-dim">{o.quantity}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={statusColor(o.status)}>{o.status}</span>
                  <span className="text-dim">{o.order_type}</span>
                </div>
              </div>
              {expanded === o.id && (
                <div className="mt-2 pt-2 border-t border-[#1a3a2a] text-xs text-dim space-y-1">
                  <div>ID: {o.id}</div>
                  <div>Type: {o.order_type}{o.price ? ` @ ${o.price}` : ''}</div>
                  <div>Created: {o.created_at || 'N/A'}</div>
                  {o.status === 'pending' && (
                    <button
                      onClick={e => { e.stopPropagation(); cancelOrder(o.id) }}
                      className="text-red hover:text-red/80 transition-colors mt-1"
                    >
                      Cancel order
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
