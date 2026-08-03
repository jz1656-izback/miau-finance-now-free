import { useState, useEffect } from 'react'

const MOCK_BALANCES = {
  eth: { balance: 12.5, usd: 41250, token: 'ETH' },
  sol: { balance: 250, usd: 45000, token: 'SOL' },
  usdc: { balance: 25000, usd: 25000, token: 'USDC' },
  btc: { balance: 0.85, usd: 55250, token: 'BTC' },
}

export default function WalletBalance() {
  const [balances, setBalances] = useState<Record<string, { balance: number; usd: number; token: string }>>({})
  const [total, setTotal] = useState(0)

  useEffect(() => {
    const stored = localStorage.getItem('miau-wallet-chain')
    if (!stored) return
    setBalances(MOCK_BALANCES)
    setTotal(Object.values(MOCK_BALANCES).reduce((s, v) => s + v.usd, 0))
  }, [])

  if (Object.keys(balances).length === 0) {
    return <div className="p-4 text-dim text-sm">Connect a wallet to see balances.</div>
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">💰 Wallet Balance</h2>
      <div className="text-2xl font-bold text-green">${total.toLocaleString()}</div>
      <div className="space-y-2">
        {Object.entries(balances).map(([key, b]) => (
          <div key={key} className="flex items-center justify-between p-2 bg-gray-800/50 rounded">
            <div>
              <span className="text-sm text-green">{b.token}</span>
              <span className="text-xs text-dim ml-2">{b.balance.toLocaleString()}</span>
            </div>
            <span className="text-sm text-white">${b.usd.toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
