import { useState, useEffect, useCallback } from 'react'

interface LeaderboardEntry {
  rank: number
  username: string
  total_return_pct: number
  total_value: number
  portfolio_count: number
  badge?: string
}

const BASE = '/api/v1'

export default function LeaderboardUI() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([])
  const [period, setPeriod] = useState('all')
  const [loading, setLoading] = useState(true)

  const fetchLeaderboard = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${BASE}/social/leaderboard?period=${period}`)
      const data = await res.json()
      setEntries(data.leaderboard || data || [])
    } catch {}
    setLoading(false)
  }, [period])

  useEffect(() => { fetchLeaderboard() }, [fetchLeaderboard])

  const pct = (n: number) => `${n >= 0 ? '+' : ''}${n.toFixed(2)}%`

  return (
    <div className="glass-panel rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-green font-bold text-sm">🏆 Leaderboard</h3>
        <div className="flex gap-1">
          {['1w', '1m', '3m', 'all'].map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-2 py-1 text-xs rounded border transition-colors ${
                period === p ? 'border-green text-green bg-green/10' : 'border-[#1a3a2a] text-dim hover:border-green/30'
              }`}
            >
              {p === 'all' ? 'All' : p}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="text-dim text-xs">Loading...</div>
      ) : entries.length === 0 ? (
        <div className="text-dim text-xs">No leaderboard data yet</div>
      ) : (
        <div className="space-y-1">
          {entries.map((e, i) => (
            <div
              key={e.rank || i}
              className="flex items-center justify-between p-2 rounded border border-[#1a3a2a] hover:border-green/30 transition-colors"
            >
              <div className="flex items-center gap-3">
                <span className={`w-6 text-center font-bold text-sm ${
                  e.rank <= 3 ? 'text-yellow' : 'text-dim'
                }`}>
                  {e.rank <= 3 ? ['🥇', '🥈', '🥉'][e.rank - 1] : `#${e.rank}`}
                </span>
                <div>
                  <div className="text-xs text-green font-semibold">
                    {e.username}
                    {e.badge && <span className="ml-1 text-dim">({e.badge})</span>}
                  </div>
                  <div className="text-xs text-dim">{e.portfolio_count} portfolio{e.portfolio_count !== 1 ? 's' : ''}</div>
                </div>
              </div>
              <div className="text-right">
                <div className={`text-xs font-bold ${e.total_return_pct >= 0 ? 'text-green' : 'text-red'}`}>
                  {pct(e.total_return_pct)}
                </div>
                <div className="text-xs text-dim">{e.total_value.toLocaleString()}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
