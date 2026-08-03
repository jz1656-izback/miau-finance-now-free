import { useState, useEffect } from 'react'

interface Strategy {
  id: string; name: string; author: string; description: string
  license: string; price_miau: number; rating: number; downloads: number
}

export default function MarketplaceBrowser() {
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/v1/network/strategies', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then(r => r.json()).then(d => setStrategies(d.items || [])).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-4 text-dim">Loading marketplace...</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🏪 Strategy Marketplace</h2>
      {strategies.length === 0 ? (
        <p className="text-dim text-xs">No strategies listed yet. Mint one with `network mint`!</p>
      ) : (
        <div className="grid gap-2">
          {strategies.map(s => (
            <div key={s.id} className="p-3 bg-gray-800/80 rounded border border-gray-700/50 hover:border-cyan/50 transition-colors">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-green">{s.name}</span>
                <span className="text-xs text-yellow">{s.price_miau > 0 ? `${s.price_miau} MIAU` : 'Free'}</span>
              </div>
              <div className="text-xs text-dim mt-1">{s.description}</div>
              <div className="flex items-center gap-3 mt-1 text-[10px] text-dim">
                <span>by {s.author}</span>
                <span>⭐ {s.rating?.toFixed(1) || 'N/A'}</span>
                <span>📥 {s.downloads}</span>
                <span className={`px-1 rounded ${s.license === 'free' ? 'bg-green-900/30 text-green' : 'bg-blue-900/30 text-blue'}`}>{s.license}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
