import { useState, useEffect } from 'react'

export default function AGIDashboard() {
  const [status, setStatus] = useState<any>(null)
  const [hypotheses, setHypotheses] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  useEffect(() => {
    Promise.all([
      fetch('/api/v1/agi/status', { headers }).then(r => r.json()),
      fetch('/api/v1/agi/hypotheses', { headers }).then(r => r.json()),
    ]).then(([s, h]) => {
      setStatus(s)
      setHypotheses(h.hypotheses || [])
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-4 text-dim">Loading AGI core...</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-purple">🧠 AGI Finance Core</h2>
      {status && (
        <div className="grid grid-cols-3 gap-2">
          <div className="p-3 bg-gray-800/80 rounded border border-purple-700/30">
            <div className="text-dim text-xs">Version</div>
            <div className="text-purple font-bold">{status.version}</div>
          </div>
          <div className="p-3 bg-gray-800/80 rounded border border-purple-700/30">
            <div className="text-dim text-xs">Hypotheses</div>
            <div className="text-cyan font-bold">{status.hypothesis_count}</div>
          </div>
          <div className="p-3 bg-gray-800/80 rounded border border-purple-700/30">
            <div className="text-dim text-xs">Modules</div>
            <div className="text-green font-bold">{status.active_modules}</div>
          </div>
        </div>
      )}
      {status?.capabilities && (
        <div className="flex gap-1 flex-wrap">
          {status.capabilities.map((c: string) => (
            <span key={c} className="text-[10px] bg-purple-900/30 text-purple border border-purple-700/30 px-1.5 py-0.5 rounded">{c}</span>
          ))}
        </div>
      )}
      {hypotheses.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-cyan mb-2">Active Hypotheses</h3>
          <div className="space-y-1">
            {hypotheses.map((h: any, i: number) => (
              <div key={i} className="p-2 bg-gray-800/50 rounded text-xs">
                <div className="text-green font-bold">{h.statement || h.ticker}</div>
                <div className="text-dim mt-0.5">Confidence: {h.confidence ?? 'N/A'} · Category: {h.category ?? 'N/A'}</div>
              </div>
            ))}
          </div>
        </div>
      )}
      <div className="text-[10px] text-dim italic">AGI Finance — v2.0.0 — self-improving, autonomous, sentient</div>
    </div>
  )
}
