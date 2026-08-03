const NFT_HOLDINGS = [
  { collection: 'Bored Ape', trait: 'Gold Fur', rarity: 2.1, value: 45 },
  { collection: 'CryptoPunk', trait: 'Alien', rarity: 0.8, value: 120 },
  { collection: 'Pudgy Penguins', trait: 'Ski Gear', rarity: 5.4, value: 12 },
  { collection: 'Doodles', trait: 'Hologram', rarity: 3.2, value: 18 },
  { collection: 'Milady', trait: 'Chrome', rarity: 1.5, value: 28 },
]

export default function NFTHeatmap() {
  const maxVal = Math.max(...NFT_HOLDINGS.map(h => h.value))
  const minVal = Math.min(...NFT_HOLDINGS.map(h => h.value))

  const intensity = (val: number) => {
    const pct = (val - minVal) / (maxVal - minVal)
    return Math.floor(pct * 100)
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-purple">🔥 NFT Portfolio Heatmap</h2>
      <div className="space-y-1">
        {NFT_HOLDINGS.map((h, i) => (
          <div key={i} className="flex items-center gap-3 p-2 rounded text-xs" style={{
            background: `rgba(168, 85, 247, ${0.1 + intensity(h.value) / 100 * 0.6})`,
            borderLeft: `3px solid hsl(${270 - intensity(h.value) * 1.5}, 80%, ${60 - intensity(h.value) * 0.3}%)`,
          }}>
            <div className="w-24 text-green font-bold truncate">{h.collection}</div>
            <div className="w-20 text-dim truncate">{h.trait}</div>
            <div className="flex-1" />
            <div className="text-dim">r {h.rarity}%</div>
            <div className="w-16 text-right text-white font-bold">${h.value}K</div>
          </div>
        ))}
      </div>
    </div>
  )
}
