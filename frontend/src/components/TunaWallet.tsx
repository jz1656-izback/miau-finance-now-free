import { useEffect, useState } from 'react'
import { getToken } from '../lib/auth'

const BASE = '/api/v1'

interface TunaState {
  balance: number
  earned: number
  spent: number
  rank: string
}

interface RealWallet {
  eth?: number
  usdc?: number
  address?: string
}

export default function TunaWallet() {
  const [state, setState] = useState<TunaState>(() => {
    const saved = localStorage.getItem('miau_tuna_wallet')
    if (saved) return JSON.parse(saved)
    return { balance: 100, earned: 100, spent: 0, rank: 'Minnow' }
  })
  const [tx, setTx] = useState('')
  const [realWallet, setRealWallet] = useState<RealWallet | null>(null)
  const [showReal, setShowReal] = useState(false)

  useEffect(() => {
    localStorage.setItem('miau_tuna_wallet', JSON.stringify(state))
    const rank = state.balance > 100000 ? '🐋 Whale' : state.balance > 10000 ? '🦈 Shark' : state.balance > 1000 ? '🐬 Dolphin' : state.balance > 100 ? '🐟 Minnow' : '🦐 Shrimp'
    if (rank !== state.rank) setState(prev => ({ ...prev, rank }))
  }, [state])

  useEffect(() => {
    const token = getToken()
    if (!token) return
    fetch(`${BASE}/wallet/balances`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then(r => r.json()).then(data => {
      if (data && !data.error) {
        setRealWallet({
          eth: data.ethereum?.eth || 0,
          usdc: data.ethereum?.usdc || 0,
          address: data.ethereum?.address || '',
        })
      }
    }).catch(() => {})
  }, [])

  const earn = () => {
    const amount = Math.floor(Math.random() * 50 + 10)
    setState(prev => ({ ...prev, balance: prev.balance + amount, earned: prev.earned + amount }))
    setTx(`+${amount} 🐟`)
    setTimeout(() => setTx(''), 2000)
  }

  const spend = () => {
    if (state.balance < 10) return
    const amount = Math.floor(Math.random() * 20 + 5)
    setState(prev => ({ ...prev, balance: prev.balance - amount, spent: prev.spent + amount }))
    setTx(`-${amount} 🐟`)
    setTimeout(() => setTx(''), 2000)
  }

  return (
    <div style={{ position: 'fixed', bottom: 52, right: 12, zIndex: 100001, fontFamily: 'monospace', fontSize: 10, color: '#557755', background: 'rgba(0,0,0,0.6)', border: '1px solid rgba(0,255,136,0.1)', borderRadius: 8, padding: '6px 10px', minWidth: 160, textAlign: 'right' }}>
      <div style={{ color: '#00ff88', fontSize: 11, marginBottom: 2 }}>🐟 Tuna Wallet</div>
      {showReal && realWallet ? (
        <>
          <div style={{ color: '#ffcc00', fontSize: 11 }}>ETH: {realWallet.eth?.toFixed(4) || '0'}</div>
          <div style={{ color: '#22aaff', fontSize: 11 }}>USDC: ${realWallet.usdc?.toFixed(2) || '0'}</div>
          {realWallet.address && <div style={{ color: '#557755', fontSize: 8, marginTop: 1 }}>{realWallet.address.slice(0, 6)}...{realWallet.address.slice(-4)}</div>}
        </>
      ) : (
        <>
          <div style={{ color: '#ffcc00', fontSize: 13, fontWeight: 'bold' }}>{state.balance.toLocaleString()} 🐟</div>
          <div style={{ color: '#557755', fontSize: 9 }}>{state.rank}</div>
          {tx && <div style={{ color: tx.startsWith('+') ? '#00ff88' : '#ff4444', fontSize: 11, marginTop: 2 }}>{tx}</div>}
        </>
      )}
      <div style={{ display: 'flex', gap: 4, marginTop: 4, justifyContent: 'flex-end', flexWrap: 'wrap' }}>
        <button onClick={earn} style={{ padding: '2px 6px', fontSize: 9, background: '#003322', border: '1px solid #006644', borderRadius: 3, color: '#00ff88', cursor: 'pointer' }}>+🎣</button>
        <button onClick={spend} style={{ padding: '2px 6px', fontSize: 9, background: '#330022', border: '1px solid #660044', borderRadius: 3, color: '#ff4488', cursor: 'pointer' }} disabled={state.balance < 10}>-🛒</button>
        <button onClick={() => setShowReal(!showReal)} style={{ padding: '2px 6px', fontSize: 9, background: '#002244', border: '1px solid #004466', borderRadius: 3, color: '#22aaff', cursor: 'pointer' }}>{showReal ? '🎮' : '🔗'}</button>
      </div>
    </div>
  )
}
