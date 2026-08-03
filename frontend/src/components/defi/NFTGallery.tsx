import { useState } from 'react'

const NFT_COLLECTIONS = [
  { name: 'Bored Ape Yacht Club', floor: 32.5, change: 2.1, items: 1, image: '🐵' },
  { name: 'CryptoPunks', floor: 45.0, change: -0.8, items: 2, image: '👾' },
  { name: 'Pudgy Penguins', floor: 8.2, change: 5.3, items: 5, image: '🐧' },
  { name: 'Azuki', floor: 6.8, change: -1.2, items: 0, image: '🌸' },
  { name: 'Doodles', floor: 3.5, change: 0.4, items: 3, image: '🎨' },
  { name: 'Milady Maker', floor: 7.1, change: 12.0, items: 1, image: '👁️' },
]

export default function NFTGallery() {
  const [collections] = useState(NFT_COLLECTIONS)

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-purple flex items-center gap-2">🖼️ NFT Gallery</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {collections.map((c, i) => (
          <div key={i} className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
            <div className="text-3xl mb-2">{c.image}</div>
            <div className="text-xs text-green font-bold">{c.name}</div>
            <div className="flex justify-between mt-1 text-xs">
              <span className="text-dim">Floor: {c.floor} ETH</span>
              <span className={c.change >= 0 ? 'text-green' : 'text-red'}>{c.change >= 0 ? '+' : ''}{c.change}%</span>
            </div>
            <div className="text-[10px] text-dim mt-1">{c.items} owned</div>
          </div>
        ))}
      </div>
    </div>
  )
}
