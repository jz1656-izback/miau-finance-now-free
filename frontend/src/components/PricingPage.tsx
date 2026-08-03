import { useState } from 'react'

const TIERS = [
  {
    name: 'Cat Tamagotchi',
    price: '€0',
    originalPrice: null,
    period: '',
    desc: 'Just a cat. No finance. Pet it daily.',
    features: ['Virtual pet cat in terminal', 'Feed, pet, and play', 'Login streak rewards', 'Unlockable cat hats', '🐱 Zero stock data — pet game only'],
    cta: 'Play Free',
    tier: 'tamagotchi',
    highlighted: false,
    seatBased: false,
    barks: 0,
  },
  {
    name: 'Trial Trader',
    price: '€2.49',
    originalPrice: '€4.99',
    period: '/month',
    desc: 'Test the real terminal. 50 calls/day.',
    features: ['50 API calls per day', '7-day price history', '5 data providers', 'Basic terminal commands', 'No AI advisor'],
    cta: 'Try Now',
    tier: 'trial',
    highlighted: false,
    seatBased: false,
    barks: 0,
  },
  {
    name: 'Starter Cat',
    price: '€25',
    originalPrice: '€50',
    period: '/month',
    desc: 'Real data. 500 calls/day. Full history.',
    features: ['500 API calls per day', '1 year price history', '15 data providers', 'Technical indicators (RSI, MACD, SMA)', 'Basic portfolio tracking'],
    cta: 'Subscribe',
    tier: 'starter',
    highlighted: false,
    seatBased: false,
    barks: 0,
  },
  {
    name: 'Pro Cat',
    price: '€49.50',
    originalPrice: '€99',
    period: '/month',
    desc: 'Unlimited data. AI advisor. Full power.',
    features: ['3,000 API calls per day', 'Unlimited price history', 'All 37 data providers', 'AI advisor (real LLM analysis)', 'Risk analytics (VaR, beta, stress)', 'Trading signals & backtesting', '1 bark included (extra: €9,999)'],
    cta: 'Subscribe',
    tier: 'pro',
    highlighted: false,
    seatBased: false,
    barks: 1,
  },
  {
    name: '🐱 Adopt Cat 🐱',
    price: '€33.5M',
    originalPrice: '€67M',
    period: 'one-time',
    desc: 'Buy the whole project. 50% launch discount. All IP. All cats.',
    features: ['👑 Full ownership of Miau Finance', '📦 All source code & IP', '🌐 All domains & infrastructure', '📡 37 data provider integrations', '📚 230 education courses', '🎨 Frontend + backend + docs', '🐋 Docker + K8s deployment', '🐱 This cat will work for YOU now'],
    cta: '🐱👑 Adopt Cat — €33.5M',
    tier: 'adopt',
    featured: true,
    seatBased: false,
    barks: 9999,
  },
  {
    name: 'Fund Cat',
    price: '€75',
    originalPrice: '€150',
    period: '/month',
    desc: 'For teams. 3 seats. 10k calls/day each.',
    features: ['10,000 API calls/day per user', '3 team seats included', 'Team workspaces & roles', 'Shared portfolios & watchlists', 'Custom alerts & notifications', 'Priority support', '2 barks included (extra: €9,999)'],
    cta: 'Subscribe',
    tier: 'fund',
    highlighted: false,
    seatBased: true,
    barks: 2,
  },
  {
    name: 'Enterprise',
    price: '€349.84',
    originalPrice: '€699.67',
    period: '/user/month',
    desc: 'Per-user pricing for real companies.',
    features: ['Unlimited API calls per user', 'On-premise deployment', 'SSO/SAML authentication', 'Custom integrations', 'Dedicated support & SLA (99.9%)', '10 barks included (extra: €9,999 each)'],
    cta: 'Contact Sales',
    tier: 'enterprise',
    highlighted: false,
    seatBased: true,
    barks: 10,
  },
]

export default function PricingPage() {
  const [billing, setBilling] = useState<'monthly' | 'yearly'>('monthly')
  const [seats, setSeats] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState<string | null>(null)

  const getSeats = (tier: string) => seats[tier] || 1

  const handleSubscribe = async (tier: string) => {
    setLoading(tier)
    try {
      const csrf = document.cookie.split('; ').find(r => r.startsWith('csrf_token='))?.split('=')[1] || ''
      const res = await fetch('/api/v1/billing/checkout', {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('miau_token')}`, 'Content-Type': 'application/json', 'X-CSRF-Token': csrf },
        body: JSON.stringify({ tier, seats: getSeats(tier), success_url: window.location.origin + '/billing/success', cancel_url: window.location.origin + '/pricing' }),
      })
      if (res.ok) {
        const data = await res.json()
        if (data.session_url) window.location.href = data.session_url
      }
    } catch { /* ignore */ }
    setLoading(null)
  }

  const formatPrice = (tier: typeof TIERS[0]) => {
    const isFree = tier.price === '€0'
    if (isFree) return '€0'
    return tier.price
  }

  const renderCard = (tier: typeof TIERS[0], isSeatBased: boolean, getSeats: any, handleSubscribe: any, loading: any, billing: any, setSeats: any, _compact: boolean) => (
    <div key={tier.tier} className={`p-4 rounded-xl border flex flex-col ${tier.highlighted ? 'border-green/50 bg-gray-800/80 ring-1 ring-green/30 scale-105' : 'border-gray-700 bg-gray-900'}`}>
      {tier.highlighted && <div className="text-[10px] text-green font-mono mb-1 uppercase tracking-wider text-center">🐟 Most Tuna</div>}
      <h3 className="text-sm font-bold text-white mb-1">{tier.name}</h3>
      <p className="text-[10px] text-dim mb-2">{tier.desc}</p>
      <div className="mb-2">
        {tier.originalPrice && (
          <span className="text-xs text-dim line-through mr-2">{tier.originalPrice}{tier.tier !== 'adopt' ? '/mo' : ''}</span>
        )}
        <span className="text-2xl font-bold text-green">{formatPrice(tier)}</span>
        <span className="text-dim text-xs">/{isSeatBased ? 'user/' : ''}{billing === 'monthly' ? 'mo' : 'yr'}</span>
        {tier.originalPrice && <span className="text-yellow text-[10px] ml-2">🎉 50% off</span>}
      </div>
      {isSeatBased && (
        <div className="flex items-center gap-2 mb-2">
          <span className="text-[10px] text-dim">Seats:</span>
          <button onClick={() => setSeats((s: any) => ({...s, [tier.tier]: Math.max(1, getSeats(tier.tier) - 1)}))} className="px-2 py-0.5 bg-gray-800 rounded text-xs text-dim hover:text-white">-</button>
          <span className="text-xs text-white font-bold w-4 text-center">{getSeats(tier.tier)}</span>
          <button onClick={() => setSeats((s: any) => ({...s, [tier.tier]: getSeats(tier.tier) + 1}))} className="px-2 py-0.5 bg-gray-800 rounded text-xs text-dim hover:text-white">+</button>
        </div>
      )}
      <ul className="space-y-1 mb-3 flex-1">
        {tier.features.map((f: string, i: number) => (
          <li key={i} className="text-[10px] text-dim flex items-center gap-1">
            <span className="text-green shrink-0">✓</span> {f}
          </li>
        ))}
      </ul>
      <button
        onClick={() => handleSubscribe(tier.tier)}
        disabled={loading !== null || tier.tier === 'free' || tier.tier === 'tamagotchi'}
        className={`w-full py-1.5 rounded-lg text-xs font-bold transition-all tap-target ${
          tier.highlighted
            ? 'bg-green-800 text-green hover:bg-green-700'
            : 'bg-gray-800 text-dim hover:bg-gray-700'
        } disabled:opacity-50`}
      >
        {loading === tier.tier ? 'Processing...' : tier.cta}
      </button>
    </div>
  )

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <div className="bg-yellow-900/30 border border-yellow-700/50 rounded-lg p-3 mb-4 max-w-xl mx-auto">
          <p className="text-yellow text-sm font-bold">🚧 90% DEVELOPMENT DISCOUNT 🚧</p>
          <p className="text-yellow/70 text-xs mt-1">Still in development — prices return to normal after 1 year. The cat believes in you.</p>
        </div>
        <h1 className="text-2xl font-bold text-green mb-2">🐱 Choose Your Plan</h1>
        <p className="text-dim text-sm">Unlock the full power of Miau Finance. Barks are feature requests — use them to shape the product.</p>
        <div className="flex justify-center gap-2 mt-4">
          <button onClick={() => setBilling('monthly')} className={`px-4 py-1.5 rounded text-sm ${billing === 'monthly' ? 'bg-green-800 text-green' : 'bg-gray-800 text-dim'}`}>Monthly</button>
          <button onClick={() => setBilling('yearly')} className={`px-4 py-1.5 rounded text-sm ${billing === 'yearly' ? 'bg-green-800 text-green' : 'bg-gray-800 text-dim'}`}>Yearly <span className="text-green text-xs">-20%</span></button>
        </div>
      </div>

      <div className="flex flex-col items-center gap-6">
        {/* Top row: smaller tiers */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3 w-full max-w-5xl">
          {TIERS.filter(t => !t.featured).slice(0, 3).map((tier) => {
            const isSeatBased = tier.seatBased && tier.tier !== 'free'
            return renderCard(tier, isSeatBased, getSeats, handleSubscribe, loading, billing, setSeats, false)
          })}
        </div>

        {/* Featured: Adopt Cat */}
        {TIERS.filter(t => t.featured).map((tier) => (
          <div key={tier.tier} className="w-full max-w-3xl">
            <div className="relative bg-gradient-to-br from-yellow-900/40 via-gray-900 to-yellow-900/40 border-2 border-yellow-500/60 rounded-2xl p-8 shadow-2xl shadow-yellow-500/10 scale-110 my-4">
              {/* Floating cats */}
              <div className="absolute -top-6 -left-6 text-5xl animate-bounce">🐱</div>
              <div className="absolute -top-4 -right-4 text-4xl animate-ping">😸</div>
              <div className="absolute -bottom-4 -left-4 text-4xl animate-bounce" style={{ animationDelay: '0.5s' }}>😻</div>
              <div className="absolute -bottom-6 -right-6 text-5xl animate-pulse">🙀</div>
              <div className="absolute top-1/2 -left-8 text-3xl animate-spin-slow">🐈</div>
              <div className="absolute top-1/2 -right-8 text-3xl animate-spin-slow" style={{ animationDirection: 'reverse' }}>🐈‍⬛</div>

              <div className="text-center mb-6">
                <div className="text-yellow text-sm font-mono mb-2 uppercase tracking-[0.3em]">⭐ THE ULTIMATE TIER ⭐</div>
                <h3 className="text-4xl font-bold text-white mb-2">{tier.name}</h3>
                <p className="text-yellow/80 text-sm">{tier.desc}</p>
              </div>

              <div className="text-center mb-6">
                {tier.originalPrice && (
                  <span className="text-lg text-dim line-through mr-3">{tier.originalPrice}</span>
                )}
                <span className="text-5xl font-bold text-yellow">€33.5M</span>
                <span className="text-dim text-lg">/once</span>
                <span className="text-yellow text-sm ml-3">🎉 50% off</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                {tier.features.map((f, i) => (
                  <div key={i} className="bg-black/40 rounded-lg p-3 text-center border border-yellow-500/20">
                    <span className="text-yellow text-xl block mb-1">{f.split(' ')[0]}</span>
                    <span className="text-xs text-dim">{f.replace(/^[^\s]+\s/, '')}</span>
                  </div>
                ))}
              </div>

              <button
                onClick={() => handleSubscribe(tier.tier)}
                disabled={loading !== null}
                className="w-full py-4 rounded-xl text-lg font-bold transition-all bg-yellow-500 text-black hover:bg-yellow-400 disabled:opacity-50 shadow-lg shadow-yellow-500/25"
              >
                {loading === tier.tier ? 'Processing...' : tier.cta}
              </button>

              <div className="text-center text-yellow/40 text-[10px] mt-3">∞ barks included · ∞ tuna · ∞ cats</div>
            </div>
          </div>
        ))}

        {/* Bottom row: remaining smaller tiers */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3 w-full max-w-5xl">
          {TIERS.filter(t => !t.featured).slice(3).map((tier) => {
            const isSeatBased = tier.seatBased && tier.tier !== 'free'
            return renderCard(tier, isSeatBased, getSeats, handleSubscribe, loading, billing, setSeats, false)
          })}
        </div>
      </div>

      <div className="mt-8 p-4 bg-gray-800 rounded-xl text-center">
        <h3 className="text-sm font-bold text-cyan mb-2">Compare Plans</h3>
        <table className="w-full text-xs">
          <thead>
            <tr className="text-dim border-b border-gray-700">
              <th className="text-left py-1">Feature</th>
              <th className="text-center py-1">Tamagotchi</th>
              <th className="text-center py-1 text-gray">Trial</th>
              <th className="text-center py-1 text-yellow">Starter</th>
              <th className="text-center py-1 text-green">Pro</th>
              <th className="text-center py-1 text-cyan">Fund</th>
              <th className="text-center py-1 text-purple">Enterprise</th>
              <th className="text-center py-1 text-gold">🏆 Adopt</th>
            </tr>
          </thead>
          <tbody>
            {[
              ['Price', '€0', '€2.49', '€25', '€49.50', '€75', '€349.84/user', '€33.5M'],
              ['API calls/day', '0', '50', '500', '3,000', '10,000', 'Unlimited', '∞'],
              ['Data providers', '0', '5', '15', '37', '37', '37', '37'],
              ['AI Advisor', '—', '—', '—', '✓', '✓', '✓', '✓'],
              ['Risk analytics', '—', '—', '—', '✓', '✓', '✓', '✓'],
              ['Team seats', '—', '—', '—', '—', '3', 'Unlimited', '∞'],
              ['Free Barks/yr', '0', '0', '0', '1', '2', '10', '∞'],
              ['On-Premise', '—', '—', '—', '—', '—', '✓', '✓'],
              ['SSO/SAML', '—', '—', '—', '—', '—', '✓', '✓'],
              ['SLA', '—', '—', '—', '—', '—', '99.9%', '✓'],
            ].map(([feature, ...vals], i) => (
              <tr key={i} className="border-b border-gray-800">
                <td className="py-1.5 text-left text-dim font-medium">{feature}</td>
                {vals.map((v, j) => (
                  <td key={j} className="text-center py-1.5">{v === '✓' ? '✅' : v === '—' ? '❌' : v}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
