const PRICE_HISTORY = [
  { month: 'Jan', floor: 28, volume: 120 },
  { month: 'Feb', floor: 31, volume: 145 },
  { month: 'Mar', floor: 35, volume: 200 },
  { month: 'Apr', floor: 33, volume: 180 },
  { month: 'May', floor: 38, volume: 220 },
  { month: 'Jun', floor: 42, volume: 260 },
]

export default function NFTChart() {
  const maxFloor = Math.max(...PRICE_HISTORY.map(p => p.floor))

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-purple">📈 NFT Floor Price Trend</h2>
      <div className="flex items-end gap-1 h-32" style={{ minHeight: 128 }}>
        {PRICE_HISTORY.map((p, i) => (
          <div key={i} className="flex flex-col items-center flex-1 gap-1">
            <div className="text-[9px] text-dim">{p.floor} ETH</div>
            <div className="w-full rounded-t" style={{
              height: `${(p.floor / maxFloor) * 80}px`,
              background: 'linear-gradient(to top, #a855f7, #d8b4fe)',
              opacity: 0.7 + (p.floor / maxFloor) * 0.3,
            }} />
            <div className="text-[9px] text-dim">{p.month}</div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="p-2 bg-gray-800/50 rounded">
          <div className="text-dim">Current Floor</div>
          <div className="text-purple font-bold">{PRICE_HISTORY[PRICE_HISTORY.length - 1].floor} ETH</div>
        </div>
        <div className="p-2 bg-gray-800/50 rounded">
          <div className="text-dim">30d Volume</div>
          <div className="text-cyan font-bold">{PRICE_HISTORY[PRICE_HISTORY.length - 1].volume} ETH</div>
        </div>
      </div>
    </div>
  )
}
