import { useState, useEffect } from 'react'

interface LeaderboardEntry {
  rank: number
  user_id: string
  username: string
  value: number
  positions: number
}

export default function LeaderboardUI() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([])
  const [period, setPeriod] = useState('all_time')
  const [metric, setMetric] = useState('total_return')
  const [loading, setLoading] = useState(true)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  const fetchLeaderboard = async () => {
    setLoading(true)
    try {
      const res = await fetch(`/api/v1/social/leaderboard?period=${period}&metric=${metric}&limit=50`, { headers })
      if (res.ok) {
        const data = await res.json()
        setEntries(data.leaderboard || [])
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => { fetchLeaderboard() }, [period, metric])

  const fmtVal = (v: number) => metric === 'gain_amount' ? `$${v.toLocaleString()}` : `${v.toFixed(2)}%`

  return (
    <div className="p-4 space-y-3">
      <div className="flex items-center gap-3">
        <h2 className="text-lg font-bold text-yellow">🏆 Leaderboard</h2>
        <select value={period} onChange={e => setPeriod(e.target.value)}
          className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-xs text-white">
          <option value="all_time">All Time</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
        <select value={metric} onChange={e => setMetric(e.target.value)}
          className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-xs text-white">
          <option value="total_return">Total Return</option>
          <option value="sharpe_ratio">Sharpe Ratio</option>
          <option value="gain_amount">Gain Amount</option>
        </select>
      </div>

      {loading ? (
        <p className="text-dim text-sm">Loading leaderboard...</p>
      ) : entries.length === 0 ? (
        <p className="text-dim text-sm">No leaderboard data yet. Start trading to get ranked!</p>
      ) : (
        <table className="w-full text-xs">
          <thead>
            <tr className="text-dim border-b border-gray-700">
              <th className="text-left py-1 w-10">Rank</th>
              <th className="text-left py-1">User</th>
              <th className="text-right py-1">{metric === 'total_return' ? 'Return' : metric === 'sharpe_ratio' ? 'Sharpe' : 'Gain'}</th>
              <th className="text-right py-1">Positions</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((e, i) => (
              <tr key={i} className={`border-b border-gray-800 ${e.rank <= 3 ? 'bg-gray-800/50' : ''}`}>
                <td className="py-2">
                  {e.rank === 1 ? '🥇' : e.rank === 2 ? '🥈' : e.rank === 3 ? '🥉' : `#${e.rank}`}
                </td>
                <td className="py-2 text-green font-bold">{e.username}</td>
                <td className={`py-2 text-right ${e.value >= 0 ? 'text-green' : 'text-red'}`}>
                  {fmtVal(e.value)}
                </td>
                <td className="py-2 text-right text-dim">{e.positions}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
