import { useState } from 'react'

interface BacktestMetrics {
  strategy: string
  ticker: string
  period: string
  total_return_pct: number
  buy_and_hold_return_pct: number
  outperformance_pct: number
  sharpe_ratio: number
  max_drawdown_pct: number
  win_rate_pct: number
  num_trades: number
  final_capital: number
  equity_curve?: { date: string; value: number }[]
  trades?: { date: string; side: string; price: number; quantity: number; pnl: number }[]
  parameters?: Record<string, string>
}

export default function BacktestResults() {
  const [strategy, setStrategy] = useState('sma_cross')
  const [ticker, setTicker] = useState('AAPL')
  const [period, setPeriod] = useState('1y')
  const [results, setResults] = useState<BacktestMetrics | null>(null)
  const [loading, setLoading] = useState(false)
  const [compareResults, setCompareResults] = useState<BacktestMetrics[]>([])
  const [compareMode, setCompareMode] = useState(false)

  const runBacktest = async () => {
    setLoading(true)
    setResults(null)
    setCompareResults([])
    const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
    try {
      if (compareMode) {
        const strategies = strategy.split(',')
        const allResults = await Promise.all(
          strategies.map(async (s) => {
            const res = await fetch(`/api/v1/backtest?strategy=${s.trim()}&ticker=${ticker}&period=${period}`, { headers })
            if (!res.ok) return null
            return res.json()
          })
        )
        setCompareResults(allResults.filter(Boolean) as BacktestMetrics[])
      } else {
        const res = await fetch(`/api/v1/backtest?strategy=${strategy}&ticker=${ticker}&period=${period}`, { headers })
        if (res.ok) setResults(await res.json())
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  const MetricCard = ({ label, value, color = 'text-white' }: { label: string; value: string; color?: string }) => (
    <div className="p-3 bg-gray-800 rounded">
      <div className="text-dim text-xs">{label}</div>
      <div className={`font-bold ${color}`}>{value}</div>
    </div>
  )

  const renderMetrics = (bt: BacktestMetrics) => (
    <div className="grid grid-cols-3 gap-2">
      <MetricCard label="Total Return" value={bt.total_return_pct >= 0 ? `+${bt.total_return_pct.toFixed(2)}%` : `${bt.total_return_pct.toFixed(2)}%`} color={bt.total_return_pct >= 0 ? 'text-green' : 'text-red'} />
      <MetricCard label="Buy & Hold" value={bt.buy_and_hold_return_pct >= 0 ? `+${bt.buy_and_hold_return_pct.toFixed(2)}%` : `${bt.buy_and_hold_return_pct.toFixed(2)}%`} />
      <MetricCard label="Alpha" value={bt.outperformance_pct >= 0 ? `+${bt.outperformance_pct.toFixed(2)}%` : `${bt.outperformance_pct.toFixed(2)}%`} color={bt.outperformance_pct >= 0 ? 'text-green' : 'text-red'} />
      <MetricCard label="Sharpe Ratio" value={bt.sharpe_ratio?.toFixed(2) || 'N/A'} color={bt.sharpe_ratio >= 1 ? 'text-green' : bt.sharpe_ratio >= 0 ? 'text-yellow' : 'text-red'} />
      <MetricCard label="Max Drawdown" value={`${bt.max_drawdown_pct?.toFixed(2) || '0'}%`} color="text-red" />
      <MetricCard label="Win Rate" value={bt.win_rate_pct != null ? `${bt.win_rate_pct.toFixed(1)}%` : 'N/A'} color={bt.win_rate_pct >= 50 ? 'text-green' : 'text-yellow'} />
      <MetricCard label="Trades" value={`${bt.num_trades || 0}`} />
      <MetricCard label="Final Capital" value={`$${(bt.final_capital || 0).toLocaleString()}`} />
      <MetricCard label="Strategy" value={bt.strategy || strategy} color="text-cyan" />
    </div>
  )

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-lg font-bold text-cyan">📊 Backtest</h2>

      <div className="flex gap-2 items-end">
        <div>
          <label className="text-dim text-xs block mb-1">Strategy</label>
          <input value={strategy} onChange={e => setStrategy(e.target.value)} className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm text-white w-40" />
        </div>
        <div>
          <label className="text-dim text-xs block mb-1">Ticker</label>
          <input value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm text-white w-24" />
        </div>
        <div>
          <label className="text-dim text-xs block mb-1">Period</label>
          <select value={period} onChange={e => setPeriod(e.target.value)} className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-sm text-white">
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="6mo">6 Months</option>
            <option value="1y">1 Year</option>
            <option value="2y">2 Years</option>
          </select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-dim text-xs">Compare</label>
          <input type="checkbox" checked={compareMode} onChange={e => setCompareMode(e.target.checked)} className="accent-cyan" />
        </div>
        <button onClick={runBacktest} disabled={loading} className="px-4 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-sm disabled:opacity-50">
          {loading ? 'Running...' : 'Run'}
        </button>
      </div>

      {results && (
        <div>
          <h3 className="text-sm font-bold text-cyan mb-2">{results.strategy || strategy} on {ticker} ({period})</h3>
          {renderMetrics(results)}
          {results.parameters && Object.keys(results.parameters).length > 0 && (
            <div className="mt-3 p-3 bg-gray-800 rounded">
              <h4 className="text-xs font-bold text-dim mb-1">Parameters</h4>
              <div className="text-xs text-dim">{Object.entries(results.parameters).map(([k, v]) => `${k}: ${v}`).join(', ')}</div>
            </div>
          )}
        </div>
      )}

      {compareResults.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-cyan mb-2">Strategy Comparison on {ticker}</h3>
          <div className="space-y-3">
            {compareResults.map((bt, i) => (
              <div key={i} className="p-3 bg-gray-800 rounded">
                <h4 className="text-xs font-bold text-cyan mb-2">{bt.strategy || strategy.split(',')[i]}</h4>
                {renderMetrics(bt)}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
