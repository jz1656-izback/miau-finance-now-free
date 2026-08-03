import { useState, useEffect, useCallback } from 'react'

interface SharedPortfolioView {
  id: string
  name: string
  owner: string
  total_value: number
  total_return_pct: number
  num_positions: number
  is_public: boolean
}

const BASE = '/api/v1'

export default function SharedPortfolioUI() {
  const [portfolios, setPortfolios] = useState<SharedPortfolioView[]>([])
  const [loading, setLoading] = useState(true)

  const fetchShared = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${BASE}/portfolios/shared`)
      setPortfolios(await res.json())
    } catch {}
    setLoading(false)
  }, [])

  useEffect(() => { fetchShared() }, [fetchShared])

  const toggleVisibility = useCallback(async (id: string, makePublic: boolean) => {
    try {
      await fetch(`${BASE}/portfolios/${id}/visibility`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_public: makePublic }),
      })
      fetchShared()
    } catch {}
  }, [fetchShared])

  const fmt = (n: number | null | undefined) => {
    if (n == null) return '-'
    if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
    if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`
    return `$${n.toFixed(2)}`
  }

  return (
    <div className="glass-panel rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-green font-bold text-sm">Shared Portfolios</h3>
        <button onClick={fetchShared} className="text-xs text-dim hover:text-green transition-colors">⟳</button>
      </div>

      {loading ? (
        <div className="text-dim text-xs">Loading...</div>
      ) : portfolios.length === 0 ? (
        <div className="text-dim text-xs">No shared portfolios found</div>
      ) : (
        <div className="space-y-2">
          {portfolios.map(pf => (
            <div key={pf.id} className="border border-[#1a3a2a] rounded-lg p-3">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-green text-sm font-semibold">{pf.name}</div>
                  <div className="text-dim text-xs">by {pf.owner} · {pf.num_positions} positions</div>
                </div>
                <div className="text-right">
                  <div className="text-green text-sm">{fmt(pf.total_value)}</div>
                  <div className={`text-xs ${pf.total_return_pct >= 0 ? 'text-green' : 'text-red'}`}>
                    {pf.total_return_pct >= 0 ? '+' : ''}{pf.total_return_pct.toFixed(2)}%
                  </div>
                </div>
              </div>
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => toggleVisibility(pf.id, !pf.is_public)}
                  className={`px-2 py-1 text-xs rounded border transition-colors ${
                    pf.is_public
                      ? 'border-yellow text-yellow hover:bg-yellow/10'
                      : 'border-[#1a3a2a] text-dim hover:text-green hover:border-green/30'
                  }`}
                >
                  {pf.is_public ? '🌍 Public' : '🔒 Private'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
