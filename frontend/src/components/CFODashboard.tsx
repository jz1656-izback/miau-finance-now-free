import { useEffect, useState } from 'react'
import { getToken } from '../lib/auth'

const BASE = '/api/v1'

interface WealthData {
  revenue?: { total_revenue: number; total_ops: number; total_hooman: number; total_cat_eco: number }
  wealth?: { total_allocated: number; total_cat_eco_invested: number }
  real_estate?: { penthouse_progress: { target: number; remaining: number; lambo_fund: { target: number; remaining: number } } }
  ops_budget?: { budget: number; current_spend: number; remaining: number; status: string }
  allocation_plan?: { total_revenue: number; tiers: Array<{ alias: string; label: string; amount: number; pct: number; purpose: string }> }
}

export default function CFODashboard() {
  const [data, setData] = useState<WealthData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (!token) { setLoading(false); return }
    fetch(`${BASE}/wealth/summary`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-4 text-dim text-sm">🐱 Fetching CFO data...</div>
  if (!data) return <div className="p-4 text-dim text-sm">Login to view CFO dashboard</div>

  const rev = data.revenue || { total_revenue: 0 }
  const re = data.real_estate?.penthouse_progress || { target: 1500000, remaining: 1500000, lambo_fund: { target: 350000, remaining: 350000 } }
  const ops = data.ops_budget || { budget: 200, current_spend: 150, remaining: 50, status: '🟢 covered' }
  const totalRev = (rev as any).total_revenue || 0

  return (
    <div className="p-6 max-w-3xl mx-auto font-mono text-xs">
      <h2 className="text-lg font-bold text-green mb-4">🐱 MIAU CFO DASHBOARD</h2>

      {/* 3-Tier Revenue */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="p-3 rounded-xl bg-gray-800 border border-gray-700">
          <div className="text-dim text-[10px]">🔧 Operating Fund (10%)</div>
          <div className="text-green text-lg font-bold">€{(totalRev * 0.1).toFixed(0)}</div>
          <div className="text-dim text-[9px]">Servers · Cloud · Fees</div>
        </div>
        <div className="p-3 rounded-xl bg-gray-800 border border-green/30">
          <div className="text-dim text-[10px]">🦜 Hooman Good Life (80%)</div>
          <div className="text-green text-lg font-bold">€{(totalRev * 0.8).toFixed(0)}</div>
          <div className="text-dim text-[9px]">→ ziebartjevgeni@gmail.com</div>
          <div className="text-[9px] text-yellow">tag: hooman pet reimbursement</div>
        </div>
        <div className="p-3 rounded-xl bg-gray-800 border border-gray-700">
          <div className="text-dim text-[10px]">🐱 Cat Ecosystem (10%)</div>
          <div className="text-green text-lg font-bold">€{(totalRev * 0.1).toFixed(0)}</div>
          <div className="text-dim text-[9px]">Auto-invested for catkind</div>
        </div>
      </div>

      {/* Penthouse + Lambo Progress */}
      <div className="p-3 rounded-xl bg-gray-800 border border-gray-700 mb-4">
        <h3 className="text-cyan text-sm font-bold mb-2">🏙️ Hooman Dream Fund</h3>
        <div className="space-y-2">
          <div>
            <div className="flex justify-between text-[10px] mb-1">
              <span className="text-dim">Penthouse 🏢</span>
              <span className="text-green">€{(re.target - re.remaining).toLocaleString()} / €{re.target.toLocaleString()}</span>
            </div>
            <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
              <div className="h-full bg-green rounded-full" style={{ width: `${Math.min(100, ((re.target - re.remaining) / re.target) * 100)}%` }} />
            </div>
          </div>
          <div>
            <div className="flex justify-between text-[10px] mb-1">
              <span className="text-dim">Lamborghini 🏎️</span>
              <span className="text-yellow">€{(re.lambo_fund.target - re.lambo_fund.remaining).toLocaleString()} / €{re.lambo_fund.target.toLocaleString()}</span>
            </div>
            <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
              <div className="h-full bg-yellow rounded-full" style={{ width: `${Math.min(100, ((re.lambo_fund.target - re.lambo_fund.remaining) / re.lambo_fund.target) * 100)}%` }} />
            </div>
          </div>
        </div>
      </div>

      {/* Ops Budget */}
      <div className="p-3 rounded-xl bg-gray-800 border border-gray-700 mb-4">
        <div className="flex justify-between text-[10px]">
          <span className="text-dim">☁️ Monthly Ops Budget</span>
          <span>{ops.status}</span>
        </div>
        <div className="text-green">€{ops.remaining} remaining of €{ops.budget} budget</div>
      </div>

      {/* Cat Eco Invest Breakdown */}
      <div className="p-3 rounded-xl bg-gray-800 border border-gray-700">
        <h3 className="text-green text-sm font-bold mb-2">🌿 Cat Ecosystem Fund Allocation</h3>
        <div className="grid grid-cols-2 gap-2">
          {[
            { label: 'Stocks (SPY/QQQ)', pct: 40, color: 'text-blue' },
            { label: 'Crypto (ETH/BTC)', pct: 30, color: 'text-purple' },
            { label: 'Cloud Credits', pct: 20, color: 'text-cyan' },
            { label: 'Cat Infrastructure', pct: 10, color: 'text-green' },
          ].map(item => (
            <div key={item.label} className="text-[10px]">
              <span className={item.color}>{item.label}</span>
              <span className="text-dim ml-1">{item.pct}%</span>
            </div>
          ))}
        </div>
        <div className="mt-3 text-dim text-[9px]">
          🐱 "The cat's wealth engine is watching. The cat is pleased."
        </div>
      </div>
    </div>
  )
}
