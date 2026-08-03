import { useState, useEffect } from 'react'

interface SharedPortfolioData {
  portfolio_name: string
  owner: string
  total_value: number
  total_return_pct: number
  positions: { ticker: string; quantity: number; market_value: number; unrealized_pnl: number }[]
}

interface Props {
  shareToken?: string
}

export default function SharedPortfolioUI({ shareToken }: Props) {
  const [data, setData] = useState<SharedPortfolioData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!shareToken) return
    const fetchShared = async () => {
      try {
        const res = await fetch(`/api/v1/public/portfolio/${shareToken}`)
        if (res.ok) {
          setData(await res.json())
        } else {
          setError('Portfolio not found or link expired')
        }
      } catch { setError('Failed to load shared portfolio') }
      setLoading(false)
    }
    fetchShared()
  }, [shareToken])

  if (!shareToken) {
    return (
      <div className="p-4 text-center">
        <p className="text-dim text-sm mb-2">Enter a share token to view a public portfolio</p>
        <p className="text-cyan text-xs">Use: share create &lt;portfolio_id&gt; from the terminal</p>
      </div>
    )
  }

  if (loading) return <div className="p-4 text-dim text-center">Loading shared portfolio...</div>
  if (error) return <div className="p-4 text-red text-center">{error}</div>
  if (!data) return <div className="p-4 text-dim text-center">No data</div>

  return (
    <div className="p-4 space-y-4">
      <div className="text-center">
        <h2 className="text-xl font-bold text-green">📂 {data.portfolio_name}</h2>
        <p className="text-dim text-xs">by {data.owner}</p>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="p-3 bg-gray-800 rounded text-center">
          <div className="text-dim text-xs">Total Value</div>
          <div className="text-white font-bold text-lg">${(data.total_value || 0).toLocaleString()}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded text-center">
          <div className="text-dim text-xs">Return</div>
          <div className={`font-bold text-lg ${(data.total_return_pct || 0) >= 0 ? 'text-green' : 'text-red'}`}>
            {(data.total_return_pct || 0) >= 0 ? '+' : ''}{data.total_return_pct?.toFixed(2)}%
          </div>
        </div>
      </div>

      {data.positions && data.positions.length > 0 ? (
        <div>
          <h3 className="text-sm font-bold text-cyan mb-2">Positions</h3>
          <table className="w-full text-xs">
            <thead>
              <tr className="text-dim border-b border-gray-700">
                <th className="text-left py-1">Ticker</th>
                <th className="text-right py-1">Qty</th>
                <th className="text-right py-1">Value</th>
                <th className="text-right py-1">P&L</th>
              </tr>
            </thead>
            <tbody>
              {data.positions.map((p, i) => (
                <tr key={i} className="border-b border-gray-800">
                  <td className="py-1 text-green font-bold">{p.ticker}</td>
                  <td className="text-right py-1">{p.quantity}</td>
                  <td className="text-right py-1">${(p.market_value || 0).toLocaleString()}</td>
                  <td className={`text-right py-1 ${(p.unrealized_pnl || 0) >= 0 ? 'text-green' : 'text-red'}`}>
                    {(p.unrealized_pnl || 0) >= 0 ? '+' : ''}${(p.unrealized_pnl || 0).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-dim text-xs text-center">No positions in this portfolio</p>
      )}

      <p className="text-dim text-xs text-center">Shared from Miau Finance — view only</p>
    </div>
  )
}
