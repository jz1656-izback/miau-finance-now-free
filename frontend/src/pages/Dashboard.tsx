import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Wallet,
  Activity,
  ArrowRight,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts'

const COLORS = ['#5c7cfa', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

function formatCurrency(n: number): string {
  if (Math.abs(n) >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(1)}B`
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`
  return `$${n.toFixed(0)}`
}

export default function Dashboard() {
  const navigate = useNavigate()

  const { data: summary, isLoading } = useQuery({
    queryKey: ['summary'],
    queryFn: api.getSummary,
  })

  const { data: portfolios } = useQuery({
    queryKey: ['portfolios'],
    queryFn: api.getPortfolios,
  })

  const { data: pnlData } = useQuery({
    queryKey: ['pnl-timeseries'],
    queryFn: () => api.getPnlTimeseries(undefined, 14),
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading dashboard...</div>
      </div>
    )
  }

  const stats = [
    {
      label: 'Total AUM',
      value: formatCurrency(summary?.total_aum || 0),
      icon: Wallet,
      color: 'text-emerald-400',
      bg: 'bg-emerald-900/20',
    },
    {
      label: 'Unrealized P&L',
      value: formatCurrency(summary?.total_unrealized_pnl || 0),
      icon: (summary?.total_unrealized_pnl || 0) >= 0 ? TrendingUp : TrendingDown,
      color: (summary?.total_unrealized_pnl || 0) >= 0 ? 'text-emerald-400' : 'text-red-400',
      bg: (summary?.total_unrealized_pnl || 0) >= 0 ? 'bg-emerald-900/20' : 'bg-red-900/20',
    },
    {
      label: 'Instruments',
      value: summary?.total_instruments ?? 0,
      icon: BarChart3,
      color: 'text-blue-400',
      bg: 'bg-blue-900/20',
    },
    {
      label: 'Trades',
      value: summary?.total_trades ?? 0,
      icon: Activity,
      color: 'text-purple-400',
      bg: 'bg-purple-900/20',
    },
  ]

  const portfolioChartData = (portfolios || []).map((p: any) => ({
    name: p.name.length > 15 ? p.name.slice(0, 15) + '...' : p.name,
    value: p.total_value || 0,
  }))

  const pnlChartData = (pnlData || [])
    .filter((p: any) => p.pnl_type === 'unrealized')
    .reverse()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Dashboard</h1>
        <p className="text-sm text-slate-500 mt-1">
          Platform overview as of {new Date().toLocaleDateString()}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="card flex items-start gap-4">
            <div className={`w-10 h-10 rounded-lg ${stat.bg} flex items-center justify-center`}>
              <stat.icon size={20} className={stat.color} />
            </div>
            <div className="stat">
              <span className="stat-label">{stat.label}</span>
              <span className="stat-value text-lg">{stat.value}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="panel">
          <div className="panel-header">Portfolio Allocation</div>
          <div className="p-4">
            {portfolioChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={portfolioChartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {portfolioChartData.map((_: any, i: number) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-center text-slate-500 py-8">No portfolio data</div>
            )}
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">P&L Trend</div>
          <div className="p-4">
            {pnlChartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={pnlChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: '#64748b', fontSize: 11 }}
                    tickFormatter={(v) => new Date(v).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  />
                  <YAxis tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={(v) => formatCurrency(v)} />
                  <Tooltip
                    contentStyle={{
                      background: '#1e293b',
                      border: '1px solid #334155',
                      borderRadius: '8px',
                    }}
                    formatter={(value: number) => formatCurrency(value)}
                  />
                  <Line
                    type="monotone"
                    dataKey="total_pnl"
                    stroke="#5c7cfa"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-center text-slate-500 py-8">No P&L data</div>
            )}
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <span>Portfolio Overview</span>
          <button
            onClick={() => navigate('/workspace')}
            className="ml-auto text-xs text-miau-400 hover:text-miau-300 flex items-center gap-1"
          >
            View All <ArrowRight size={12} />
          </button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Positions</th>
              <th>Market Value</th>
              <th>Unrealized P&L</th>
              <th>Return</th>
            </tr>
          </thead>
          <tbody>
            {(portfolios || []).map((p: any) => {
              const returnPct = p.total_value && p.total_value > 0
                ? ((p.total_value - (p.total_value - (p.total_unrealized_pnl || 0))) / (p.total_value - (p.total_unrealized_pnl || 0))) * 100
                : 0
              return (
                <tr
                  key={p.id}
                  className="cursor-pointer"
                  onClick={() => navigate(`/portfolios/${p.id}`)}
                >
                  <td className="font-medium text-slate-200">{p.name}</td>
                  <td>
                    <span className="badge-blue">{p.portfolio_type}</span>
                  </td>
                  <td>{p.num_positions || 0}</td>
                  <td>{formatCurrency(p.total_value || 0)}</td>
                  <td className={p.total_unrealized_pnl >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                    {formatCurrency(p.total_unrealized_pnl || 0)}
                  </td>
                  <td className={returnPct >= 0 ? 'text-emerald-400' : 'text-red-400'}>
                    {returnPct.toFixed(2)}%
                  </td>
                </tr>
              )
            })}
            {(!portfolios || portfolios.length === 0) && (
              <tr>
                <td colSpan={6} className="text-center text-slate-500 py-8">
                  No portfolios yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
