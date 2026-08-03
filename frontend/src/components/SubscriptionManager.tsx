import { useState, useEffect, useCallback } from 'react'

interface Subscription {
  id: string
  user_id: string
  tier: string
  status: string
  current_period_end?: string
  trial_ends_at?: string
}

const BASE = '/api/v1'

export default function SubscriptionManager() {
  const [sub, setSub] = useState<Subscription | null>(null)
  const [loading, setLoading] = useState(true)
  const [cancelling, setCancelling] = useState(false)

  const fetchSub = useCallback(async () => {
    try {
      const res = await fetch(`${BASE}/billing/subscription`)
      setSub(await res.json())
    } catch {}
    setLoading(false)
  }, [])

  useEffect(() => { fetchSub() }, [fetchSub])

  const cancel = useCallback(async () => {
    if (!confirm('Cancel subscription? You will lose access at the end of the billing period.')) return
    setCancelling(true)
    try {
      await fetch(`${BASE}/billing/cancel`, { method: 'POST' })
      fetchSub()
    } catch {}
    setCancelling(false)
  }, [fetchSub])

  const formatDate = (d?: string) => d ? new Date(d).toLocaleDateString() : 'N/A'

  if (loading) return <div className="text-dim text-xs p-4">Loading subscription...</div>

  return (
    <div className="glass-panel rounded-lg p-4">
      <h3 className="text-green font-bold text-sm mb-3">Subscription</h3>

      <div className="space-y-2 text-xs">
        <div className="flex justify-between items-center p-3 border border-[#1a3a2a] rounded-lg">
          <span className="text-dim">Current Plan</span>
          <span className="text-green font-semibold capitalize">{sub?.tier || 'Free'}</span>
        </div>

        <div className="flex justify-between items-center p-3 border border-[#1a3a2a] rounded-lg">
          <span className="text-dim">Status</span>
          <span className={`font-semibold ${sub?.status === 'active' ? 'text-green' : 'text-yellow'}`}>
            {sub?.status || 'active'}
          </span>
        </div>

        {sub?.current_period_end && (
          <div className="flex justify-between items-center p-3 border border-[#1a3a2a] rounded-lg">
            <span className="text-dim">Renewal Date</span>
            <span className="text-cyan">{formatDate(sub.current_period_end)}</span>
          </div>
        )}

        {sub?.trial_ends_at && (
          <div className="flex justify-between items-center p-3 border border-[#1a3a2a] rounded-lg">
            <span className="text-dim">Trial Ends</span>
            <span className="text-yellow">{formatDate(sub.trial_ends_at)}</span>
          </div>
        )}
      </div>

      {sub?.tier && sub.tier !== 'free' && sub.status === 'active' && (
        <button
          onClick={cancel}
          disabled={cancelling}
          className="w-full mt-3 px-3 py-2 text-xs rounded border border-red/30 text-red hover:bg-red/10 transition-colors disabled:opacity-40"
        >
          {cancelling ? 'Cancelling...' : 'Cancel Subscription'}
        </button>
      )}
    </div>
  )
}
