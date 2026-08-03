import { useState, useEffect } from 'react'

interface UsageStats {
  period: string
  total: number
  unique_endpoints: number
  avg_latency_ms: number
  errors: number
  top_endpoints: { endpoint: string; count: number; avg_latency: number }[]
}

export default function UsageDashboard() {
  const [stats, setStats] = useState<UsageStats | null>(null)
  const [period, setPeriod] = useState('daily')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }
      try {
        const res = await fetch(`/api/v1/developer/usage?period=${period}`, { headers })
        if (res.ok) setStats(await res.json())
      } catch { /* ignore */ }
      setLoading(false)
    }
    fetchStats()
  }, [period])

  if (loading) return <div className="p-4 text-dim">Loading usage stats...</div>
  if (!stats) return <div className="p-4 text-red">No usage data available</div>

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold text-cyan">📊 API Usage</h2>
        <select value={period} onChange={e => setPeriod(e.target.value)}
          className="bg-gray-800 border border-gray-700 rounded px-2 py-1 text-xs text-white">
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>

      <div className="grid grid-cols-4 gap-3">
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Total Requests</div>
          <div className="text-white font-bold text-lg">{stats.total.toLocaleString()}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Endpoints</div>
          <div className="text-cyan font-bold text-lg">{stats.unique_endpoints}</div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Avg Latency</div>
          <div className={`font-bold text-lg ${stats.avg_latency_ms > 500 ? 'text-red' : 'text-green'}`}>
            {stats.avg_latency_ms}ms
          </div>
        </div>
        <div className="p-3 bg-gray-800 rounded">
          <div className="text-dim text-xs">Errors</div>
          <div className={`font-bold text-lg ${stats.errors > 0 ? 'text-red' : 'text-green'}`}>
            {stats.errors}
          </div>
        </div>
      </div>

      {stats.top_endpoints.length > 0 && (
        <div className="p-3 bg-gray-800 rounded">
          <h3 className="text-sm font-bold text-cyan mb-2">Top Endpoints</h3>
          <table className="w-full text-xs">
            <thead>
              <tr className="text-dim border-b border-gray-700">
                <th className="text-left py-1">Endpoint</th>
                <th className="text-right py-1">Requests</th>
                <th className="text-right py-1">Avg Latency</th>
              </tr>
            </thead>
            <tbody>
              {stats.top_endpoints.map((e, i) => (
                <tr key={i} className="border-b border-gray-800">
                  <td className="py-1 text-green font-mono text-xs">{e.endpoint}</td>
                  <td className="text-right py-1">{e.count}</td>
                  <td className="text-right py-1">{e.avg_latency?.toFixed(0)}ms</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
