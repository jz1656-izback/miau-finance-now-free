import { useState, useEffect } from 'react'

interface Order {
  id: string
  ticker?: string
  side: string
  quantity: number
  order_type: string
  price?: number
  status: string
  filled_quantity?: number
  filled_price?: number
  created_at?: string
  updated_at?: string
}

interface Fill {
  id: string
  order_id: string
  ticker: string
  side: string
  quantity: number
  price: number
  filled_at: string
}

interface Props {
  orderId: string
  onClose: () => void
}

export default function OrderDetail({ orderId, onClose }: Props) {
  const [order, setOrder] = useState<Order | null>(null)
  const [fills, setFills] = useState<Fill[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true)
      try {
        const res = await fetch(`/api/v1/orders/${orderId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        })
        if (!res.ok) return
        const data = await res.json()
        setOrder(data.order || data)
      } catch { /* ignore */ }
      try {
        const res = await fetch(`/api/v1/orders/${orderId}/fills`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        })
        if (res.ok) {
          const data = await res.json()
          setFills(data.fills || data || [])
        }
      } catch { /* ignore */ }
      setLoading(false)
    }
    fetchDetail()
  }, [orderId])

  const cancelOrder = async () => {
    try {
      const res = await fetch(`/api/v1/orders/${orderId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      })
      if (res.ok) {
        setOrder(prev => prev ? { ...prev, status: 'cancelled' } : null)
      }
    } catch { /* ignore */ }
  }

  if (loading) return <div className="p-4 text-dim">Loading order...</div>
  if (!order) return <div className="p-4 text-red">Order not found</div>

  const canCancel = ['pending', 'submitted'].includes(order.status)

  return (
    <div className="p-4 border border-gray-700 rounded-lg bg-gray-900">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-cyan">Order Detail</h3>
        <button onClick={onClose} className="text-dim hover:text-white">✕</button>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div><span className="text-dim">ID:</span> <span className="text-green">{order.id}</span></div>
        <div><span className="text-dim">Ticker:</span> <span className="text-green">{order.ticker}</span></div>
        <div><span className="text-dim">Side:</span> <span className={order.side === 'BUY' ? 'text-green' : 'text-red'}>{order.side}</span></div>
        <div><span className="text-dim">Type:</span> <span className="text-cyan">{order.order_type}</span></div>
        <div><span className="text-dim">Quantity:</span> <span className="text-white">{order.quantity}</span></div>
        <div><span className="text-dim">Price:</span> <span className="text-white">{order.price ? `$${order.price}` : 'Market'}</span></div>
        <div><span className="text-dim">Filled:</span> <span className="text-white">{order.filled_quantity || 0} / {order.quantity}</span></div>
        <div><span className="text-dim">Status:</span> <span className={`text-${order.status === 'filled' ? 'green' : order.status === 'cancelled' ? 'red' : 'yellow'}`}>{order.status}</span></div>
        <div><span className="text-dim">Created:</span> <span className="text-dim">{order.created_at ? new Date(order.created_at).toLocaleString() : '-'}</span></div>
        <div><span className="text-dim">Updated:</span> <span className="text-dim">{order.updated_at ? new Date(order.updated_at).toLocaleString() : '-'}</span></div>
      </div>

      <div className="mb-4">
        <h4 className="text-sm font-bold text-cyan mb-2">Status Timeline</h4>
        <div className="flex items-center gap-2 text-xs">
          <span className={`px-2 py-1 rounded ${order.status === 'pending' || order.filled_quantity ? 'bg-green-800 text-green' : 'bg-gray-700 text-dim'}`}>Created</span>
          <span className="text-dim">→</span>
          <span className={`px-2 py-1 rounded ${order.filled_quantity ? 'bg-blue-800 text-blue' : 'bg-gray-700 text-dim'}`}>Partially Filled</span>
          <span className="text-dim">→</span>
          <span className={`px-2 py-1 rounded ${order.status === 'filled' ? 'bg-green-800 text-green' : 'bg-gray-700 text-dim'}`}>Filled</span>
          <span className="text-dim">→</span>
          <span className={`px-2 py-1 rounded ${order.status === 'cancelled' ? 'bg-red-800 text-red' : 'bg-gray-700 text-dim'}`}>Cancelled</span>
        </div>
      </div>

      {fills.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-bold text-cyan mb-2">Fill History</h4>
          <table className="w-full text-xs">
            <thead>
              <tr className="text-dim border-b border-gray-700">
                <th className="text-left py-1">Time</th>
                <th className="text-right py-1">Qty</th>
                <th className="text-right py-1">Price</th>
              </tr>
            </thead>
            <tbody>
              {fills.map((f, i) => (
                <tr key={i} className="border-b border-gray-800">
                  <td className="py-1">{new Date(f.filled_at).toLocaleTimeString()}</td>
                  <td className="text-right py-1">{f.quantity}</td>
                  <td className="text-right py-1">${f.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {canCancel && (
        <button onClick={cancelOrder} className="px-4 py-2 bg-red-700 hover:bg-red-600 text-white rounded text-sm">
          Cancel Order
        </button>
      )}
    </div>
  )
}
