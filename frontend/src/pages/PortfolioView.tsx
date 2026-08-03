import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { ArrowLeft } from 'lucide-react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

function formatCurrency(n: number): string {
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`
  return `$${n.toFixed(2)}`
}

export default function PortfolioView() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: portfolio, isLoading } = useQuery({
    queryKey: ['portfolio', id],
    queryFn: () => api.getPortfolio(id!),
    enabled: !!id,
  })

  const { data: analytics } = useQuery({
    queryKey: ['portfolio-analytics', id],
    queryFn: () => api.getPortfolioAnalytics(id!),
    enabled: !!id,
  })

  if (isLoading || !portfolio) {
    return <div className="text-slate-500">Loading...</div>
  }

  const summary = analytics?.summary
  const pnlData = (analytics?.pnl_timeseries || [])
    .filter((p: any) => p.pnl_type === 'unrealized')
    .reverse()

  return (
    <div className="space-y-6">
      <button
        onClick={() => navigate(-1)}
        className="btn-ghost flex items-center gap-1 text-xs"
      >
        <ArrowLeft size={14} /> Back
      </button>

      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">{portfolio.name}</h1>
          <p className="text-sm text-slate-500 mt-1">
            {portfolio.portfolio_type.replace('_', ' ')} · {portfolio.base_currency}
          </p>
        </div>
      </div>

      {summary && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="card">
            <div className="stat">
              <span className="stat-label">Market Value</span>
              <span className="stat-value text-lg">{formatCurrency(summary.total_market_value)}</span>
            </div>
          </div>
          <div className="card">
            <div className="stat">
              <span className="stat-label">Unrealized P&L</span>
              <span className={`stat-value text-lg ${summary.total_unrealized_pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                {summary.total_unrealized_pnl >= 0 ? '+' : ''}{formatCurrency(summary.total_unrealized_pnl)}
              </span>
            </div>
          </div>
          <div className="card">
            <div className="stat">
              <span className="stat-label">Positions</span>
              <span className="stat-value text-lg">{summary.num_positions}</span>
            </div>
          </div>
          <div className="card">
            <div className="stat">
              <span className="stat-label">Trades</span>
              <span className="stat-value text-lg">{summary.num_trades}</span>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="panel">
          <div className="panel-header">P&L Trend</div>
          <div className="p-4">
            {pnlData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={pnlData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#64748b', fontSize: 11 }}
                    tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={(v) => formatCurrency(v)} />
                  <Tooltip
                    contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Bar dataKey="total_pnl" fill="#5c7cfa" radius={[2, 2, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-slate-500 text-sm text-center py-8">No P&L data</div>
            )}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">Risk Metrics</div>
          <div className="p-4">
            {(analytics?.risk_metrics || []).length > 0 ? (
              <div className="space-y-3">
                {analytics.risk_metrics.map((rm: any, i: number) => (
                  <div key={i} className="flex items-center justify-between py-2 border-b border-slate-800 last:border-0">
                    <span className="text-sm text-slate-300">{rm.metric_name}</span>
                    <span className="text-sm font-medium text-slate-100">{rm.metric_value.toFixed(4)}</span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-slate-500 text-sm text-center py-8">No risk metrics</div>
            )}
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">Positions ({portfolio.positions?.length || 0})</div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Instrument</th>
              <th>Type</th>
              <th>Qty</th>
              <th>Avg Price</th>
              <th>Market Value</th>
              <th>Unrealized P&L</th>
              <th>Return</th>
            </tr>
          </thead>
          <tbody>
            {(portfolio.positions || []).map((pos: any) => {
              const returnPct = pos.cost_basis && pos.cost_basis !== 0
                ? ((pos.market_value - pos.cost_basis) / Math.abs(pos.cost_basis)) * 100
                : 0
              return (
                <tr
                  key={pos.id}
                  className="cursor-pointer"
                  onClick={() => navigate(`/instruments/${pos.instrument_id}`)}
                >
                  <td className="font-medium text-slate-200">{pos.ticker}</td>
                  <td><span className="badge-blue text-xs">{pos.instrument_type}</span></td>
                  <td>{pos.quantity.toLocaleString()}</td>
                  <td>${pos.average_price?.toFixed(2) || '-'}</td>
                  <td>{formatCurrency(pos.market_value || 0)}</td>
                  <td className={pos.unrealized_pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                    {formatCurrency(pos.unrealized_pnl || 0)}
                  </td>
                  <td className={returnPct >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                    {returnPct.toFixed(2)}%
                  </td>
                </tr>
              )
            })}
            {(!portfolio.positions || portfolio.positions.length === 0) && (
              <tr>
                <td colSpan={7} className="text-center text-slate-500 py-8">
                  No positions
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
