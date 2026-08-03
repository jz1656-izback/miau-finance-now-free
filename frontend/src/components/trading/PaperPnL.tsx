import { useState, useEffect } from 'react'

interface PnLData {
  total_pnl: number
  unrealized_pnl: number
  realized_pnl: number
  daily_pnl: number
  win_rate: number
  total_trades: number
  winning_trades: number
  losing_trades: number
  best_trade: { ticker: string; pnl: number; date: string } | null
  worst_trade: { ticker: string; pnl: number; date: string } | null
  positions: { ticker: string; unrealized_pnl: number; return_pct: number }[]
}

export default function PaperPnL() {
  const [data, setData] = useState<PnLData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPnL = async () => {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
      try {
        const res = await fetch('/api/v1/paper-pnl', { headers })
        if (res.ok) {
          const d = await res.json()
          setData(d)
        }
      } catch { /* ignore */ }
      setLoading(false)
    }
    fetchPnL()
  }, [])

  if (loading) return <div className="p-4 text-dim">Loading P&L...</div>
  if (!data) return <div className="p-4 text-red">No P&L data available</div>

  const totalPnl = data.total_pnl || 0

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-lg font-bold text-cyan">📈 Paper Trading P&L</h2>

      <div className="grid grid-cols-3 gap-3">
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Total P&L</div>
          <div className={`text-xl font-bold ${totalPnl >= 0 ? 'text-green' : 'text-red'}`}>
            {totalPnl >= 0 ? '+' : ''}${totalPnl.toLocaleString()}
          </div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Realized</div>
          <div className={`text-lg font-bold ${(data.realized_pnl || 0) >= 0 ? 'text-green' : 'text-red'}`}>
            {(data.realized_pnl || 0) >= 0 ? '+' : ''}${(data.realized_pnl || 0).toLocaleString()}
          </div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Unrealized</div>
          <div className={`text-lg font-bold ${(data.unrealized_pnl || 0) >= 0 ? 'text-green' : 'text-red'}`}>
            {(data.unrealized_pnl || 0) >= 0 ? '+' : ''}${(data.unrealized_pnl || 0).toLocaleString()}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-3">
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Win Rate</div>
          <div className="text-cyan font-bold">{(data.win_rate * 100 || 0).toFixed(1)}%</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Total Trades</div>
          <div className="text-white font-bold">{data.total_trades || 0}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Winning</div>
          <div className="text-green font-bold">{data.winning_trades || 0}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Losing</div>
          <div className="text-red font-bold">{data.losing_trades || 0}</div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-green mb-2">🏆 Best Trade</h3>
          {data.best_trade ? (
            <div>
              <div className="text-green text-lg font-bold">+${data.best_trade.pnl.toFixed(2)}</div>
              <div className="text-dim text-xs">{data.best_trade.ticker} — {new Date(data.best_trade.date).toLocaleDateString()}</div>
            </div>
          ) : (
            <p className="text-dim text-xs">No trades yet</p>
          )}
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-red mb-2">💀 Worst Trade</h3>
          {data.worst_trade ? (
            <div>
              <div className="text-red text-lg font-bold">{data.worst_trade.pnl.toFixed(2)}</div>
              <div className="text-dim text-xs">{data.worst_trade.ticker} — {new Date(data.worst_trade.date).toLocaleDateString()}</div>
            </div>
          ) : (
            <p className="text-dim text-xs">No trades yet</p>
          )}
        </div>
      </div>

      {data.positions && data.positions.length > 0 && (
        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-cyan mb-2">Per-Position P&L</h3>
          <table className="w-full text-xs">
            <thead>
              <tr className="text-dim border-b border-gray-700">
                <th className="text-left py-1">Ticker</th>
                <th className="text-right py-1">Unrealized P&L</th>
                <th className="text-right py-1">Return</th>
              </tr>
            </thead>
            <tbody>
              {data.positions.map((p, i) => (
                <tr key={i} className="border-b border-gray-800">
                  <td className="py-1 text-green">{p.ticker}</td>
                  <td className={`text-right py-1 ${p.unrealized_pnl >= 0 ? 'text-green' : 'text-red'}`}>
                    {p.unrealized_pnl >= 0 ? '+' : ''}${p.unrealized_pnl.toFixed(2)}
                  </td>
                  <td className={`text-right py-1 ${(p.return_pct || 0) >= 0 ? 'text-green' : 'text-red'}`}>
                    {(p.return_pct || 0) >= 0 ? '+' : ''}{(p.return_pct || 0).toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
