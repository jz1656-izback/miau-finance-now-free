import { useState, useCallback } from 'react'
import { getToken } from '../lib/auth'

const BASE = '/api/v1'

interface CheckoutButtonProps {
  tier: string
  label?: string
  className?: string
  onComplete?: () => void
}

export default function CheckoutButton({ tier, label, className = '', onComplete }: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCheckout = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const token = getToken()
      const headers: Record<string, string> = { 'Content-Type': 'application/json' }
      if (token) headers['Authorization'] = `Bearer ${token}`
      const res = await fetch(`${BASE}/billing/checkout`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          tier,
          success_url: `${window.location.origin}/billing/success`,
          cancel_url: `${window.location.origin}/billing/cancel`,
        }),
      })
      const data = await res.json()
      if (res.ok && data.session_url) {
        window.location.href = data.session_url
      } else {
        setError(data.detail || 'Checkout failed')
      }
    } catch {
      setError('Network error')
    }
    setLoading(false)
    onComplete?.()
  }, [tier, onComplete])

  return (
    <div>
      <button
        onClick={handleCheckout}
        disabled={loading}
        className={`px-4 py-2 text-xs rounded-lg border border-green text-green hover:bg-green/10 transition-colors disabled:opacity-40 ${className}`}
      >
        {loading ? 'Processing...' : (label || `Upgrade to ${tier}`)}
      </button>
      {error && <div className="text-xs text-red mt-1">{error}</div>}
    </div>
  )
}
