import { useState, useEffect, useCallback } from 'react'

interface Member {
  id: string
  name: string
  role: string
}

interface SharedPortfolioItem {
  id: string
  name: string
  owner: string
  members: Member[]
  total_value: number
  num_positions: number
  performance_pct: number
}

const BASE = '/api/v1'

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}

export default function SharedPortfolio() {
  const [portfolios, setPortfolios] = useState<SharedPortfolioItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    fetchJSON<SharedPortfolioItem[]>('/portfolios/shared')
      .then(data => setPortfolios(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const requestEditAccess = useCallback(async (portfolioId: string) => {
    try {
      const res = await fetch(`${BASE}/portfolios/${portfolioId}/request-access`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ access_level: 'edit' }),
      })
      if (res.ok) {
        setError(null)
        alert('Edit access requested!')
      } else {
        const data = await res.json()
        setError(data.detail || 'Request failed')
      }
    } catch {
      setError('Network error')
    }
  }, [])

  const fmt = (n: number | null | undefined): string => {
    if (n == null) return '-'
    if (Math.abs(n) >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(2)}B`
    if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
    if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`
    return `$${n.toFixed(2)}`
  }

  if (loading) {
    return (
      <div className="glass-panel rounded-lg p-4">
        <div className="text-dim text-sm">Loading shared portfolios...</div>
      </div>
    )
  }

  if (portfolios.length === 0) {
    return (
      <div className="glass-panel rounded-lg p-4">
        <div className="text-dim text-sm">No shared portfolios yet</div>
      </div>
    )
  }

  return (
    <div className="glass-panel rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-green font-bold text-sm">Shared Portfolios</h3>
        <span className="text-dim text-xs">{portfolios.length} shared</span>
      </div>

      {error && (
        <div className="text-red text-xs mb-2">{error}</div>
      )}

      <div className="space-y-2">
        {portfolios.map(pf => (
          <div
            key={pf.id}
            className="border border-[#1a3a2a] rounded-lg p-3 hover:border-green/30 transition-colors cursor-pointer"
            onClick={() => setSelected(selected === pf.id ? null : pf.id)}
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="text-green text-sm font-semibold">{pf.name}</div>
                <div className="text-dim text-xs mt-0.5">Owner: {pf.owner}</div>
              </div>
              <div className="text-right">
                <div className="text-green text-sm">{fmt(pf.total_value)}</div>
                <div className={`text-xs ${pf.performance_pct >= 0 ? 'text-green' : 'text-red'}`}>
                  {pf.performance_pct >= 0 ? '+' : ''}{pf.performance_pct.toFixed(2)}%
                </div>
              </div>
            </div>

            {selected === pf.id && (
              <div className="mt-3 pt-3 border-t border-[#1a3a2a]">
                <div className="text-xs text-dim mb-2">
                  {pf.num_positions} positions · {pf.members.length} members
                </div>
                {pf.members.length > 0 && (
                  <div className="space-y-1 mb-3">
                    <div className="text-xs text-dim font-semibold">Members:</div>
                    {pf.members.map(m => (
                      <div key={m.id} className="flex items-center gap-2 text-xs text-dim">
                        <span>• {m.name}</span>
                        <span className="text-[#4a7a5a]">({m.role})</span>
                      </div>
                    ))}
                  </div>
                )}
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    requestEditAccess(pf.id)
                  }}
                  className="text-xs text-cyan hover:text-green transition-colors px-2 py-1 rounded border border-[#1a3a2a] hover:border-green/30"
                >
                  Request edit access
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
