import { useState } from 'react'

const MOCK_DEFI = [
  { protocol: 'Uniswap', type: 'LP', value: 15000, apy: 12.5, risk: 'low' },
  { protocol: 'Aave', type: 'Lending', value: 25000, apy: 4.2, risk: 'low' },
  { protocol: 'Lido', type: 'Staking', value: 10000, apy: 5.8, risk: 'low' },
  { protocol: 'Curve', type: 'LP', value: 8000, apy: 8.3, risk: 'medium' },
  { protocol: 'Yearn', type: 'Vault', value: 12000, apy: 15.0, risk: 'medium' },
  { protocol: 'Jupiter', type: 'DCA', value: 5000, apy: 6.0, risk: 'medium' },
]

const RISK_COLORS: Record<string, string> = { low: 'text-green', medium: 'text-yellow', high: 'text-red' }

export default function DefiDashboard() {
  const [positions] = useState(MOCK_DEFI)
  const totalValue = positions.reduce((s, p) => s + p.value, 0)
  const weightedApy = positions.reduce((s, p) => s + p.value * p.apy, 0) / totalValue

  if (positions.length === 0) {
    return <div className="p-4 text-dim text-sm">No DeFi positions. Connect a wallet to get started.</div>
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🏦 DeFi Portfolio</h2>
      <div className="grid grid-cols-3 gap-3">
        <div className="p-3 bg-gray-800/80 rounded"><div className="text-dim text-xs">Total Value</div><div className="text-green font-bold">${totalValue.toLocaleString()}</div></div>
        <div className="p-3 bg-gray-800/80 rounded"><div className="text-dim text-xs">Weighted APY</div><div className="text-yellow font-bold">{weightedApy.toFixed(1)}%</div></div>
        <div className="p-3 bg-gray-800/80 rounded"><div className="text-dim text-xs">Positions</div><div className="text-cyan font-bold">{positions.length}</div></div>
      </div>
      <div className="space-y-1">
        {positions.map((p, i) => (
          <div key={i} className="flex items-center justify-between p-2 bg-gray-800/50 rounded text-xs">
            <div>
              <span className="text-green font-bold">{p.protocol}</span>
              <span className="text-dim ml-2">{p.type}</span>
            </div>
            <div className="flex items-center gap-3">
              <span className={`${RISK_COLORS[p.risk]}`}>{p.risk}</span>
              <span className="text-yellow">{p.apy}%</span>
              <span className="text-white">${p.value.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
