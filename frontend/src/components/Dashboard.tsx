import { useEffect, useState } from 'react'
import { createPortal } from 'react-dom'

interface IndexData { ticker: string; name: string; price: number; change: number; change_pct: number }
interface PortfolioItem { ticker: string; shares: number; avgCost: number; price?: number; change?: number }

export default function Dashboard({ onClose }: { onClose: () => void }) {
  const [indices, setIndices] = useState<IndexData[]>([])
  const [portfolio, setPortfolio] = useState<PortfolioItem[]>([])
  const [loading, setLoading] = useState(true)
  const tier = localStorage.getItem('miau_tier') || 'free'
  const isPro = tier !== 'free'

  useEffect(() => {
    const load = async () => {
      const token = localStorage.getItem('miau_token')
      const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

      const idxSymbols = ['^GSPC', '^IXIC', '^DJI', '^FTSE', '^N225', '^HSI']
      const idxNames: Record<string, string> = {
        '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ', '^DJI': 'DOW',
        '^FTSE': 'FTSE 100', '^N225': 'NIKKEI 225', '^HSI': 'HANG SENG',
      }

      try {
        const res = await fetch(`/api/v1/market/live?tickers=${idxSymbols.join(',')}`, { headers })
        const json = await res.json()
        const data = json?.data || json || {}
        const idxList: IndexData[] = idxSymbols.map(s => {
          const d = data[s] || data[s.replace('^', '')] || {}
          return {
            ticker: idxNames[s] || s,
            name: idxNames[s] || s,
            price: d.price || d.regularMarketPrice || 0,
            change: d.change || d.regularMarketChange || 0,
            change_pct: d.change_pct || d.regularMarketChangePercent || 0,
          }
        })
        setIndices(idxList)
      } catch {}

      // Load portfolio holdings
      try {
        const raw = JSON.parse(localStorage.getItem('miau_portfolio') || '{}')
        const tickers = Object.keys(raw)
        if (tickers.length > 0) {
          const pRes = await fetch(`/api/v1/market/live?tickers=${tickers.join(',')}`, { headers })
          const pJson = await pRes.json()
          const pData = pJson?.data || pJson || {}
          const items: PortfolioItem[] = tickers.map(t => ({
            ticker: t,
            shares: raw[t].shares || 0,
            avgCost: raw[t].price || raw[t].avgCost || raw[t].avg_cost || 0,
            price: pData[t]?.price || 0,
            change: pData[t]?.change_pct || 0,
          }))
          setPortfolio(items)
        }
      } catch {}

      setLoading(false)
    }
    load()
  }, [])

  return createPortal(
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 9000, background: '#05080a', display: 'flex', flexDirection: 'column', fontFamily: 'monospace', color: '#c8d6d0' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 20px', background: '#0a1a14', borderBottom: '1px solid rgba(0,255,136,0.1)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 20 }}>📈</span>
          <span style={{ fontSize: 16, fontWeight: 700, color: '#00ff88' }}>MIAU DASHBOARD</span>
          <span style={{ fontSize: 11, color: 'rgba(200,214,208,0.3)' }}>· World Markets · Portfolio · Terminal</span>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {!isPro && (
            <span style={{ fontSize: 10, padding: '4px 10px', background: 'rgba(255,200,0,0.1)', border: '1px solid rgba(255,200,0,0.2)', borderRadius: 8, color: '#ffcc00' }}>
              🆓 Free Tier — <a href="http://localhost:5173" style={{ color: '#00ff88' }} onClick={() => onClose()}>Upgrade</a>
            </span>
          )}
          <button onClick={onClose} style={{ background: 'none', border: '1px solid rgba(255,255,255,0.1)', color: '#c8d6d0', padding: '4px 12px', borderRadius: 6, cursor: 'pointer', fontSize: 12 }}>✕ Close</button>
        </div>
      </div>

      {/* Body */}
      <div style={{ flex: 1, overflow: 'auto', padding: 20 }}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: 60, color: 'rgba(200,214,208,0.3)' }}>Loading dashboard... 🐱</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, maxWidth: 1200, margin: '0 auto' }}>
            {/* World Indices */}
            <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(0,255,136,0.08)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ fontSize: 13, fontWeight: 700, color: '#00ff88', marginBottom: 16, letterSpacing: 1 }}>🌍 WORLD INDICES</h3>
              {indices.map(idx => (
                <div key={idx.ticker} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                  <span style={{ fontSize: 13, color: '#ffffff' }}>{idx.name}</span>
                  <div style={{ display: 'flex', gap: 12 }}>
                    <span style={{ fontSize: 13, color: '#c8d6d0' }}>${idx.price?.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}</span>
                    <span style={{ fontSize: 13, color: (idx.change_pct || 0) >= 0 ? '#00ff88' : '#ff4444' }}>
                      {(idx.change_pct || 0) >= 0 ? '▲' : '▼'} {Math.abs(idx.change_pct || 0).toFixed(2)}%
                    </span>
                  </div>
                </div>
              ))}
              {indices.length === 0 && <div style={{ fontSize: 12, color: 'rgba(200,214,208,0.3)', textAlign: 'center', padding: 20 }}>No data — login first</div>}
            </div>

            {/* Portfolio */}
            <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(0,255,136,0.08)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ fontSize: 13, fontWeight: 700, color: '#00ff88', marginBottom: 16, letterSpacing: 1 }}>💰 PORTFOLIO</h3>
              {portfolio.length > 0 ? <>
                {portfolio.map(item => {
                  const totalValue = (item.price || 0) * item.shares
                  const totalCost = item.avgCost * item.shares
                  const pnl = totalValue - totalCost
                  const pnlPct = totalCost > 0 ? (pnl / totalCost) * 100 : item.price ? 0 : 0
                  return (
                    <div key={item.ticker} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                      <div>
                        <span style={{ fontSize: 13, color: '#ffffff', fontWeight: 600 }}>{item.ticker}</span>
                        <span style={{ fontSize: 11, color: 'rgba(200,214,208,0.3)', marginLeft: 8 }}>{item.shares} shares{totalCost > 0 ? ` @ $${item.avgCost.toFixed(2)}` : ''}</span>
                      </div>
                      <div style={{ display: 'flex', gap: 12 }}>
                        <span style={{ fontSize: 13, color: '#c8d6d0' }}>${totalValue.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                        {totalCost > 0 && (
                          <span style={{ fontSize: 13, color: pnl >= 0 ? '#00ff88' : '#ff4444' }}>
                            {pnl >= 0 ? '+' : ''}${pnl.toFixed(2)} ({(pnlPct >= 0 ? '+' : '')}{pnlPct.toFixed(1)}%)
                          </span>
                        )}
                      </div>
                    </div>
                  )
                })}
                {/* Total row */}
                {(() => {
                  const totalVal = portfolio.reduce((s, i) => s + (i.price || 0) * i.shares, 0)
                  const totalCst = portfolio.reduce((s, i) => s + i.avgCost * i.shares, 0)
                  const totalPnl = totalVal - totalCst
                  return (
                    <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0 0', marginTop: 4, borderTop: '1px solid rgba(0,255,136,0.15)' }}>
                      <span style={{ fontSize: 13, color: '#00ff88', fontWeight: 700 }}>TOTAL</span>
                      <div style={{ display: 'flex', gap: 12 }}>
                        <span style={{ fontSize: 13, color: '#ffffff', fontWeight: 600 }}>${totalVal.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                        {totalCst > 0 && (
                          <span style={{ fontSize: 13, color: totalPnl >= 0 ? '#00ff88' : '#ff4444', fontWeight: 600 }}>
                            {totalPnl >= 0 ? '+' : ''}${totalPnl.toFixed(2)}
                          </span>
                        )}
                      </div>
                    </div>
                  )
                })()}
              </> : (
                <div style={{ fontSize: 12, color: 'rgba(200,214,208,0.3)', textAlign: 'center', padding: 20 }}>
                  <div style={{ fontSize: 30, marginBottom: 8 }}>📭</div>
                  <div>No holdings yet</div>
                  <div style={{ marginTop: 8, fontSize: 11 }}>Type: <strong>portfolio add AAPL 10 150</strong></div>
                  <div style={{ fontSize: 11 }}>to start tracking your portfolio</div>
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(0,255,136,0.08)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ fontSize: 13, fontWeight: 700, color: '#00ff88', marginBottom: 16, letterSpacing: 1 }}>⚡ QUICK ACTIONS</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                {[
                  { label: '💰 Top Up Tuna', cmd: 'topup --help', icon: '🐟' },
                  { label: '📊 My Status', cmd: 'status', icon: '📋' },
                  { label: '🔍 Stock Screener', cmd: 'screener', icon: '🔎' },
                  { label: '🌍 3D Globe', cmd: 'miaumap', icon: '🌍' },
                  { label: '📈 Price Check', cmd: 'price AAPL', icon: '📈' },
                  { label: '🤖 AI Advisor', cmd: 'chat market outlook', icon: '🤖' },
                ].map(action => (
                  <div key={action.cmd} onClick={() => { localStorage.setItem('miau_cmd', action.cmd); onClose() }}
                    style={{ padding: '10px 12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)', borderRadius: 8, cursor: 'pointer', fontSize: 12, transition: 'all 0.2s' }}
                    onMouseOver={e => { (e.currentTarget as HTMLElement).style.background = 'rgba(0,255,136,0.05)'; (e.currentTarget as HTMLElement).style.borderColor = 'rgba(0,255,136,0.2)' }}
                    onMouseOut={e => { (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.02)'; (e.currentTarget as HTMLElement).style.borderColor = 'rgba(255,255,255,0.06)' }}>
                    <div style={{ fontSize: 16, marginBottom: 4 }}>{action.icon}</div>
                    <div style={{ color: '#ffffff' }}>{action.label}</div>
                    <div style={{ fontSize: 10, color: 'rgba(200,214,208,0.3)', marginTop: 2 }}>{action.cmd}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Account Summary */}
            <div style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(0,255,136,0.08)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ fontSize: 13, fontWeight: 700, color: '#00ff88', marginBottom: 16, letterSpacing: 1 }}>🐱 ACCOUNT</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 20px', fontSize: 12 }}>
                <span style={{ color: 'rgba(200,214,208,0.4)' }}>Tier</span>
                <span style={{ color: isPro ? '#00ff88' : '#c8d6d0' }}>{isPro ? '💎 Pro' : '🐟 Free'}</span>
                <span style={{ color: 'rgba(200,214,208,0.4)' }}>Tuna</span><span style={{ color: '#ffcc00' }}>{parseInt(localStorage.getItem('miau_tuna') || '0').toLocaleString()} 🐟</span>
                <span style={{ color: 'rgba(200,214,208,0.4)' }}>Holdings</span><span style={{ color: '#c8d6d0' }}>{portfolio.length} positions</span>
                <span style={{ color: 'rgba(200,214,208,0.4)' }}>Status</span><span style={{ color: '#00ff88' }}>✅ Active</span>
              </div>
              <div style={{ marginTop: 16, padding: '10px 14px', background: 'rgba(0,255,136,0.03)', border: '1px solid rgba(0,255,136,0.1)', borderRadius: 8, fontSize: 11, color: 'rgba(200,214,208,0.5)' }}>
                🐱 "The cat watches the markets. The cat watches your portfolio. The cat is pleased."
              </div>
            </div>
          </div>
        )}
      </div>
    </div>,
    document.body
  )
}
