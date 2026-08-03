import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { Search } from 'lucide-react'

function formatCurrency(n: number): string {
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(2)}K`
  return `$${n.toFixed(2)}`
}

export default function TradeView() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  const { data: trades, isLoading } = useQuery({
    queryKey: ['trades', statusFilter],
    queryFn: () => {
      const params: Record<string, string> = {}
      if (statusFilter) params.status = statusFilter
      return api.getTrades(params)
    },
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Trades</h1>
        <p className="text-sm text-slate-500 mt-1">
          Browse and search financial transactions
        </p>
      </div>

      <div className="flex gap-4 items-center">
        <div className="relative flex-1 max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search trades..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-9"
          />
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="input w-auto"
        >
          <option value="">All Status</option>
          <option value="settled">Settled</option>
          <option value="pending">Pending</option>
          <option value="new">New</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>

      <div className="panel overflow-hidden">
        <table className="data-table">
          <thead>
            <tr>
              <th>Trade ID</th>
              <th>Date</th>
              <th>Instrument</th>
              <th>Side</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Notional</th>
              <th>Trader</th>
              <th>Status</th>
              <th>Portfolio</th>
            </tr>
          </thead>
          <tbody>
            {(trades || []).map((trade: any) => (
              <tr
                key={trade.id}
                className="cursor-pointer"
                onClick={() => navigate(`/objects/${trade.ontology_object_id}`)}
              >
                <td className="font-mono text-xs text-slate-400">
                  {trade.trade_id || trade.id.slice(0, 8)}
                </td>
                <td className="text-xs text-slate-400">
                  {new Date(trade.trade_date).toLocaleDateString()}
                </td>
                <td className="font-medium text-slate-200">
                  {trade.ticker}
                  <span className="text-xs text-slate-500 ml-1">{trade.instrument_name}</span>
                </td>
                <td>
                  <span className={`badge text-xs ${
                    trade.side === 'BUY' ? 'badge-green' : 'badge-red'
                  }`}>
                    {trade.side}
                  </span>
                </td>
                <td className="text-right font-mono">{trade.quantity.toLocaleString()}</td>
                <td className="text-right font-mono">${trade.price.toFixed(2)}</td>
                <td className="text-right font-mono">
                  {trade.notional ? formatCurrency(trade.notional) : '-'}
                </td>
                <td className="text-sm text-slate-300">{trade.trader || '-'}</td>
                <td>
                  <span className={`badge text-xs ${
                    trade.status === 'settled' ? 'badge-green' :
                    trade.status === 'pending' ? 'badge-yellow' :
                    trade.status === 'cancelled' ? 'badge-red' : 'badge-blue'
                  }`}>
                    {trade.status}
                  </span>
                </td>
                <td className="text-xs text-slate-400">{trade.portfolio_name || '-'}</td>
              </tr>
            ))}
            {(!trades || trades.length === 0) && !isLoading && (
              <tr>
                <td colSpan={10} className="text-center text-slate-500 py-8">
                  No trades found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
