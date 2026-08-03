import { useState } from 'react'

const MOCK_FLOOR_HISTORY = [
  { date: 'May 1', bayc: 28.5, punk: 4200, azuki: 5.8 },
  { date: 'May 5', bayc: 29.2, punk: 4300, azuki: 6.0 },
  { date: 'May 9', bayc: 30.1, punk: 4400, azuki: 6.2 },
  { date: 'May 13', bayc: 31.8, punk: 4450, azuki: 6.1 },
  { date: 'May 17', bayc: 32.5, punk: 4500, azuki: 6.2 },
]

const COLLECTIONS = [
  { name: 'BAYC', floor: 32.5, change: '+14%', items: 10000 },
  { name: 'CryptoPunks', floor: 4500, change: '+7.1%', items: 10000 },
  { name: 'Azuki', floor: 6.2, change: '+6.9%', items: 10000 },
  { name: 'Doodles', floor: 3.8, change: '-2.5%', items: 10000 },
  { name: 'CloneX', floor: 2.1, change: '+5%', items: 20000 },
  { name: 'Moonbirds', floor: 8.5, change: '+12%', items: 10000 },
]

export default function NFTChart() {
  const [collection, setCollection] = useState('BAYC')

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">📊 NFT Floor Prices</h2>
      <div className="flex gap-2 flex-wrap">
        {COLLECTIONS.map(c => (
          <button
            key={c.name}
            onClick={() => setCollection(c.name)}
            className={`text-xs px-2 py-1 rounded border ${collection === c.name ? 'bg-cyan-900/30 border-cyan-700 text-cyan' : 'bg-gray-800 border-gray-700 text-dim'}`}
          >
            {c.name}
          </button>
        ))}
      </div>
      <div className="bg-gray-900 p-3 rounded">
        <div className="flex items-end gap-1 h-32">
          {MOCK_FLOOR_HISTORY.map((d, i) => {
            const val = d.bayc
            const max = Math.max(...MOCK_FLOOR_HISTORY.map(x => x.bayc))
            const h = (val / max) * 100
            return (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <span className="text-[9px] text-dim">{val.toFixed(1)}</span>
                <div className="w-full bg-gradient-to-t from-cyan-600 to-cyan-400 rounded-t" style={{ height: `${h}%` }} />
                <span className="text-[9px] text-dim">{d.date}</span>
              </div>
            )
          })}
        </div>
      </div>
      <div className="text-xs text-dim text-center">Floor price trend — {collection}</div>
    </div>
  )
}
