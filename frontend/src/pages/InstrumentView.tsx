import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { ArrowLeft } from 'lucide-react'
import {
  LineChart,
  Line,
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

export default function InstrumentView() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: instrument, isLoading } = useQuery({
    queryKey: ['instrument', id],
    queryFn: () => api.getInstrument(id!),
    enabled: !!id,
  })

  const { data: marketData } = useQuery({
    queryKey: ['market-data', id],
    queryFn: () => api.getMarketData(id!, { limit: '500' }),
    enabled: !!id,
  })

  const { data: performance } = useQuery({
    queryKey: ['instrument-performance', id],
    queryFn: () => api.getInstrumentPerformance(id!),
    enabled: !!id,
  })

  if (isLoading || !instrument) {
    return <div className="text-slate-500">Loading...</div>
  }

  const chartData = (marketData || []).reverse().slice(-100)

  return (
    <div className="space-y-6 max-w-5xl">
      <button
        onClick={() => navigate(-1)}
        className="btn-ghost flex items-center gap-1 text-xs"
      >
        <ArrowLeft size={14} /> Back
      </button>

      <div className="flex items-start gap-4">
        <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center text-white text-xl font-bold flex-shrink-0">
          {instrument.ticker?.slice(0, 2)}
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-100">{instrument.name}</h1>
          <div className="flex gap-2 mt-1">
            <span className="badge-blue">{instrument.ticker}</span>
            <span className="badge-purple">{instrument.instrument_type}</span>
            <span className="badge-cyan">{instrument.exchange}</span>
            <span className="badge-green">{instrument.currency}</span>
          </div>
        </div>
      </div>

      {performance && performance.length > 0 && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {performance.map((p: any) => (
            <div key={p.id} className="card">
              <div className="stat">
                <span className="stat-label">in Portfolio</span>
                <span className="text-sm text-slate-300 font-medium">{p.portfolio_name || 'N/A'}</span>
                <div className="flex justify-between mt-2">
                  <span className="text-xs text-slate-500">Mkt Value</span>
                  <span className="text-sm font-medium">{formatCurrency(p.market_value || 0)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-slate-500">Return</span>
                  <span className={`text-sm font-medium ${p.return_pct >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                    {p.return_pct}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="panel">
        <div className="panel-header">Price History</div>
        <div className="p-4">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="date"
                  tick={{ fill: '#64748b', fontSize: 11 }}
                  tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis
                  tick={{ fill: '#64748b', fontSize: 11 }}
                  tickFormatter={(v) => formatCurrency(v)}
                  domain={['auto', 'auto']}
                />
                <Tooltip
                  contentStyle={{
                    background: '#1e293b',
                    border: '1px solid #334155',
                    borderRadius: '8px',
                  }}
                  formatter={(value: number) => formatCurrency(value)}
                />
                <Line type="monotone" dataKey="close" stroke="#5c7cfa" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-slate-500 text-sm text-center py-8">No market data available</div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="panel">
          <div className="panel-header">Details</div>
          <div className="p-4 space-y-3">
            {[
              ['ISIN', instrument.isin || '-'],
              ['SEDOL', instrument.sedol || '-'],
              ['CUSIP', instrument.cusip || '-'],
              ['Sector', instrument.sector || '-'],
              ['Industry', instrument.industry || '-'],
              ['Country', instrument.country || '-'],
            ].map(([label, value]) => (
              <div key={label} className="flex justify-between py-1.5 border-b border-slate-800 last:border-0">
                <span className="text-xs text-slate-500">{label}</span>
                <span className="text-sm text-slate-200">{value}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">Related Objects</div>
          <div className="p-4 text-sm text-slate-500">
            View related trades, positions, and market data for this instrument.
          </div>
        </div>
      </div>
    </div>
  )
}
