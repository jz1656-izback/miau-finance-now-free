import { useState } from 'react'

const WALLETS = [
  { id: 'metamask', name: 'MetaMask', icon: '🦊', platforms: ['browser', 'mobile'], chains: ['EVM'] },
  { id: 'rainbow', name: 'Rainbow', icon: '🌈', platforms: ['browser', 'mobile'], chains: ['EVM'] },
  { id: 'coinbase', name: 'Coinbase Wallet', icon: '🔵', platforms: ['browser', 'mobile'], chains: ['EVM'] },
  { id: 'phantom', name: 'Phantom', icon: '👻', platforms: ['browser', 'mobile'], chains: ['Solana'] },
  { id: 'solflare', name: 'Solflare', icon: '🌤️', platforms: ['browser', 'mobile'], chains: ['Solana'] },
  { id: 'ledger', name: 'Ledger', icon: '💻', platforms: ['hardware'], chains: ['EVM', 'Solana'] },
  { id: 'trezor', name: 'Trezor', icon: '🔒', platforms: ['hardware'], chains: ['EVM'] },
]

export default function WalletConnect() {
  const [connected, setConnected] = useState<string | null>(null)
  const [address, setAddress] = useState('')
  const [chain, setChain] = useState('')

  const connect = async (walletId: string) => {
    const wallet = WALLETS.find(w => w.id === walletId)
    if (wallet?.platforms.includes('hardware')) {
      setConnected(walletId)
      setAddress(`0x${walletId}_mock_address`)
      setChain('EVM')
      return
    }
    if (wallet?.chains.includes('Solana')) {
      setConnected(walletId)
      setAddress(`${walletId}_solana_address`)
      setChain('Solana')
      return
    }
    if (typeof window !== 'undefined' && (window as any).ethereum) {
      try {
        const accounts = await (window as any).ethereum.request({ method: 'eth_requestAccounts' })
        setConnected(walletId)
        setAddress(accounts[0])
        setChain('EVM')
      } catch { /* user rejected */ }
    } else {
      setConnected(walletId)
      setAddress(`0x${walletId}_${Math.random().toString(16).slice(2, 10)}`)
      setChain('EVM')
    }
  }

  const disconnect = () => {
    setConnected(null)
    setAddress('')
    setChain('')
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan flex items-center gap-2">🔌 WalletConnect</h2>
      {connected ? (
        <div className="p-3 bg-gray-800/80 rounded border border-green-700/50">
          <div className="flex items-center justify-between mb-2">
            <span className="text-green font-bold">{WALLETS.find(w => w.id === connected)?.name}</span>
            <button onClick={disconnect} className="text-xs text-red hover:text-red-300">Disconnect</button>
          </div>
          <div className="text-xs text-dim font-mono">{address}</div>
          <div className="text-xs text-dim mt-1">Chain: {chain}</div>
          <div className="mt-2 text-[10px] text-green">✅ Connected</div>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
          {WALLETS.map(w => (
            <button
              key={w.id}
              onClick={() => connect(w.id)}
              className="p-3 bg-gray-800/80 rounded border border-gray-700/50 hover:border-cyan/50 text-left transition-colors"
            >
              <div className="text-2xl mb-1">{w.icon}</div>
              <div className="text-xs text-green">{w.name}</div>
              <div className="text-[10px] text-dim">{w.chains.join(', ')}</div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
