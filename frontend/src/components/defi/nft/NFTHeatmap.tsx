import { useState } from 'react'

const COLLECTIONS = [
  { name: 'BAYC', floor: 32.5, volume7d: 12500, holders: 6200, items: 10000, rarity_score: 85 },
  { name: 'CryptoPunks', floor: 4500, volume7d: 8900, holders: 3600, items: 10000, rarity_score: 95 },
  { name: 'Azuki', floor: 6.2, volume7d: 4500, holders: 4800, items: 10000, rarity_score: 72 },
  { name: 'Doodles', floor: 3.8, volume7d: 2100, holders: 5200, items: 10000, rarity_score: 65 },
  { name: 'CloneX', floor: 2.1, volume7d: 1800, holders: 7100, items: 20000, rarity_score: 58 },
  { name: 'Moonbirds', floor: 8.5, volume7d: 3200, holders: 4100, items: 10000, rarity_score: 78 },
]

function getColor(val: number, max: number): string {
  const pct = val / max
  if (pct > 0.8) return 'bg-green-600'
  if (pct > 0.6) return 'bg-green-500'
  if (pct > 0.4) return 'bg-yellow-500'
  if (pct > 0.2) return 'bg-orange-500'
  return 'bg-red-500'
}

export default function NFTHeatmap() {
  const [metric, setMetric] = useState<'floor' | 'volume' | 'rarity'>('floor')
  const maxVal = Math.max(...COLLECTIONS.map(c => c[metric === 'floor' ? 'floor' : metric === 'volume' ? 'volume7d' : 'rarity_score']))

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🔥 NFT Heatmap</h2>
      <div className="flex gap-2">
        {(['floor', 'volume', 'rarity'] as const).map(m => (
          <button
            key={m}
            onClick={() => setMetric(m)}
            className={`text-xs px-2 py-1 rounded border ${metric === m ? 'bg-green-800 border-green-600 text-green' : 'bg-gray-800 border-gray-700 text-dim'}`}
          >
            {m}
          </button>
        ))}
      </div>
      <div className="space-y-1">
        {COLLECTIONS.map(c => {
          const val = metric === 'floor' ? c.floor : metric === 'volume' ? c.volume7d : c.rarity_score
          const pct = (val / maxVal) * 100
          return (
            <div key={c.name} className="flex items-center gap-3">
              <span className="text-xs text-green w-24 truncate">{c.name}</span>
              <div className="flex-1 h-6 bg-gray-900 rounded overflow-hidden">
                <div className={`h-full ${getColor(val, maxVal)} rounded flex items-center px-2 transition-all duration-500`} style={{ width: `${pct}%` }}>
                  <span className="text-[10px] text-white font-mono">{metric === 'floor' ? `${val}Ξ` : metric === 'volume' ? `${(val / 1000).toFixed(1)}K` : val}</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
