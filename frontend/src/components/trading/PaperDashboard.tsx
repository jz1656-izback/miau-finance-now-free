import { useState, useEffect } from 'react'

interface PaperPortfolio {
  id: string
  name: string
  cash: number
  market_value: number
  total_value: number
  return_pct: number
  unrealized_pnl: number
  realized_pnl: number
}

interface Position {
  ticker: string
  quantity: number
  avg_price: number
  market_value: number
  unrealized_pnl: number
  return_pct: number
}

interface Trade {
  id: string
  ticker: string
  side: string
  quantity: number
  price: number
  created_at: string
}

export default function PaperDashboard() {
  const [portfolio, setPortfolio] = useState<PaperPortfolio | null>(null)
  const [positions, setPositions] = useState<Position[]>([])
  const [trades, setTrades] = useState<Trade[]>([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
    try {
      const [portRes, posRes, tradeRes] = await Promise.all([
        fetch('/api/v1/paper-portfolios', { headers }),
        fetch('/api/v1/paper-positions', { headers }),
        fetch('/api/v1/paper-trades', { headers }),
      ])
      if (portRes.ok) {
        const data = await portRes.json()
        const items = data.items || data || []
        setPortfolio(items[0] || null)
      }
      if (posRes.ok) {
        const data = await posRes.json()
        setPositions(data.positions || data || [])
      }
      if (tradeRes.ok) {
        const data = await tradeRes.json()
        setTrades(data.trades || data || [])
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div className="p-4 text-dim">Loading paper dashboard...</div>

  const totalValue = portfolio?.total_value || 0
  const totalPnl = (portfolio?.unrealized_pnl || 0) + (portfolio?.realized_pnl || 0)

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-lg font-bold text-cyan">📄 Paper Trading Dashboard</h2>

      <div className="grid grid-cols-4 gap-3">
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Cash</div>
          <div className="text-green font-bold">${(portfolio?.cash || 0).toLocaleString()}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Market Value</div>
          <div className="text-cyan font-bold">${(portfolio?.market_value || 0).toLocaleString()}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Total Value</div>
          <div className="text-white font-bold">${totalValue.toLocaleString()}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Total P&L</div>
          <div className={`font-bold ${totalPnl >= 0 ? 'text-green' : 'text-red'}`}>
            {totalPnl >= 0 ? '+' : ''}{totalPnl.toLocaleString()} ({portfolio?.return_pct?.toFixed(2) || '0.00'}%)
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-cyan mb-2">Positions</h3>
          {positions.length === 0 ? (
            <p className="text-dim text-xs">No open positions</p>
          ) : (
            <table className="w-full text-xs">
              <thead>
                <tr className="text-dim border-b border-gray-700">
                  <th className="text-left py-1">Ticker</th>
                  <th className="text-right py-1">Qty</th>
                  <th className="text-right py-1">Avg Price</th>
                  <th className="text-right py-1">Value</th>
                  <th className="text-right py-1">P&L</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((p, i) => (
                  <tr key={i} className="border-b border-gray-800">
                    <td className="py-1 text-green">{p.ticker}</td>
                    <td className="text-right py-1">{p.quantity}</td>
                    <td className="text-right py-1">${p.avg_price?.toFixed(2)}</td>
                    <td className="text-right py-1">${(p.market_value || 0).toLocaleString()}</td>
                    <td className={`text-right py-1 ${p.unrealized_pnl >= 0 ? 'text-green' : 'text-red'}`}>
                      {p.unrealized_pnl >= 0 ? '+' : ''}{p.unrealized_pnl?.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-cyan mb-2">Recent Trades</h3>
          {trades.length === 0 ? (
            <p className="text-dim text-xs">No trades yet</p>
          ) : (
            <table className="w-full text-xs">
              <thead>
                <tr className="text-dim border-b border-gray-700">
                  <th className="text-left py-1">Time</th>
                  <th className="text-left py-1">Ticker</th>
                  <th className="text-left py-1">Side</th>
                  <th className="text-right py-1">Qty</th>
                  <th className="text-right py-1">Price</th>
                </tr>
              </thead>
              <tbody>
                {trades.slice(0, 10).map((t, i) => (
                  <tr key={i} className="border-b border-gray-800">
                    <td className="py-1 text-dim">{new Date(t.created_at).toLocaleTimeString()}</td>
                    <td className="py-1 text-green">{t.ticker}</td>
                    <td className={`py-1 ${t.side === 'BUY' ? 'text-green' : 'text-red'}`}>{t.side}</td>
                    <td className="text-right py-1">{t.quantity}</td>
                    <td className="text-right py-1">${t.price?.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
