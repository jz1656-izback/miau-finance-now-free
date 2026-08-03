import { useState } from 'react'

const MOCK_NFTS = [
  { id: '1', name: 'Bored Ape #8874', collection: 'BAYC', floor: 32.5, image: '🦧', rarity: 'legendary' },
  { id: '2', name: 'CryptoPunk #5822', collection: 'CryptoPunks', floor: 4500, image: '👾', rarity: 'mythic' },
  { id: '3', name: 'Azuki #1234', collection: 'Azuki', floor: 6.2, image: '🌸', rarity: 'rare' },
  { id: '4', name: 'Doodle #5678', collection: 'Doodles', floor: 3.8, image: '🎨', rarity: 'uncommon' },
  { id: '5', name: 'CloneX #9012', collection: 'CloneX', floor: 2.1, image: '🤖', rarity: 'rare' },
  { id: '6', name: 'Moonbird #3456', collection: 'Moonbirds', floor: 8.5, image: '🐦', rarity: 'epic' },
]

const RARITY_COLORS: Record<string, string> = {
  common: 'text-gray-400', uncommon: 'text-green', rare: 'text-blue', epic: 'text-purple', legendary: 'text-orange', mythic: 'text-red'
}

export default function NFTGallery() {
  const [nfts] = useState(MOCK_NFTS)
  const [filter, setFilter] = useState('')

  const filtered = filter ? nfts.filter(n => n.collection.toLowerCase().includes(filter.toLowerCase())) : nfts

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🖼️ NFT Gallery</h2>
      <input
        value={filter} onChange={e => setFilter(e.target.value)}
        placeholder="Filter by collection..."
        className="w-full bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green outline-none"
      />
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {filtered.map(nft => (
          <div key={nft.id} className="p-3 bg-gray-800/80 rounded border border-gray-700/50 hover:border-cyan/50 transition-colors">
            <div className="text-4xl mb-2">{nft.image}</div>
            <div className="text-xs text-green font-bold truncate">{nft.name}</div>
            <div className="text-[10px] text-dim truncate">{nft.collection}</div>
            <div className="flex items-center justify-between mt-1">
              <span className={`text-[10px] ${RARITY_COLORS[nft.rarity]}`}>{nft.rarity}</span>
              <span className="text-[10px] text-yellow">{nft.floor}Ξ</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
