import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

export default function StrategyDetail() {
  const { id } = useParams()
  const [strategy, setStrategy] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  useEffect(() => {
    if (!id) return
    fetch(`/api/v1/network/strategies/${id}`, { headers })
      .then(r => r.json()).then(setStrategy).catch(() => {}).finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="p-4 text-dim">Loading strategy...</div>
  if (!strategy) return <div className="p-4 text-red">Strategy not found</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">📋 {strategy.name}</h2>
      <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50 space-y-2">
        <div className="flex justify-between"><span className="text-dim text-xs">Author</span><span className="text-green text-xs">{strategy.author}</span></div>
        <div className="flex justify-between"><span className="text-dim text-xs">License</span><span className="text-xs">{strategy.license}</span></div>
        <div className="flex justify-between"><span className="text-dim text-xs">Rating</span><span className="text-yellow text-xs">⭐ {strategy.reputation?.average_rating?.toFixed(1) || 'N/A'} ({strategy.reputation?.total_ratings || 0} reviews)</span></div>
        <div className="flex justify-between"><span className="text-dim text-xs">Downloads</span><span className="text-xs">{strategy.downloads}</span></div>
      </div>
      {strategy.backtest_stats && (
        <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
          <h3 className="text-sm font-bold text-cyan mb-2">Backtest Results</h3>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div><span className="text-dim">Return:</span> <span className="text-green">{strategy.backtest_stats.total_return_pct}%</span></div>
            <div><span className="text-dim">Sharpe:</span> <span className="text-yellow">{strategy.backtest_stats.sharpe_ratio}</span></div>
            <div><span className="text-dim">Max DD:</span> <span className="text-red">{strategy.backtest_stats.max_drawdown_pct}%</span></div>
            <div><span className="text-dim">Win Rate:</span> <span className="text-green">{strategy.backtest_stats.win_rate_pct}%</span></div>
          </div>
        </div>
      )}
    </div>
  )
}
