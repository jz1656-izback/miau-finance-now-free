import { useState, useEffect, useCallback } from 'react'
import { isAuthenticated } from '../lib/auth'

interface ApiKey {
  id: string; name: string; key_prefix: string; scopes: Record<string, boolean>
  last_used_at: string | null; is_active: boolean; created_at: string
}

interface Webhook {
  id: string; url: string; events: string[]; is_active: boolean; created_at: string
}

interface DashboardStats {
  total_api_keys: number; active_webhooks: number
  requests_today: number; requests_this_month: number
  tier: string; tier_key_limit: number; tier_webhook_limit: number
}

const TIER_BADGES: Record<string, string> = {
  free: 'bg-gray-700 text-gray-300',
  pro: 'bg-purple-900/50 text-purple-300 border border-purple-700/50',
  enterprise: 'bg-amber-900/50 text-amber-300 border border-amber-700/50',
}

const TIER_LABELS: Record<string, string> = {
  free: 'Free',
  pro: 'Pro',
  enterprise: 'Enterprise',
}

function Skeleton({ className = '' }: { className?: string }) {
  return <div className={`animate-pulse bg-gray-700/50 rounded ${className}`} />
}

function ProgressBar({ used, limit }: { used: number; limit: number }) {
  const pct = limit > 0 ? Math.min(100, Math.round((used / limit) * 100)) : 0
  const color = pct >= 90 ? 'bg-red-500' : pct >= 70 ? 'bg-yellow-500' : 'bg-green-500'
  return (
    <div className="flex items-center gap-2 text-xs">
      <div className="flex-1 h-1.5 bg-gray-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all duration-500`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-dim w-12 text-right">{used}/{limit}</span>
    </div>
  )
}

export default function DeveloperConsole() {
  const [keys, setKeys] = useState<ApiKey[]>([])
  const [webhooks, setWebhooks] = useState<Webhook[]>([])
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [keyName, setKeyName] = useState('')
  const [webhookUrl, setWebhookUrl] = useState('')
  const [newKey, setNewKey] = useState<string | null>(null)
  const [actionLoading, setActionLoading] = useState<string | null>(null)

  const headers = { Authorization: `Bearer ${localStorage.getItem('miau_token')}`, 'Content-Type': 'application/json' }

  const fetchDashboard = useCallback(async () => {
    if (!isAuthenticated()) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/v1/developer/dashboard', { headers: { Authorization: headers.Authorization } })
      if (!res.ok) {
        const text = await res.text().catch(() => '')
        throw new Error(text || `HTTP ${res.status}`)
      }
      const d = await res.json()
      setKeys(d.api_keys || [])
      setWebhooks(d.webhooks || [])
      setStats({
        total_api_keys: d.total_api_keys ?? d.api_keys?.length ?? 0,
        active_webhooks: d.active_webhooks ?? d.webhooks?.length ?? 0,
        requests_today: d.requests_today ?? d.today ?? 0,
        requests_this_month: d.requests_this_month ?? d.month ?? 0,
        tier: d.tier ?? 'free',
        tier_key_limit: d.tier_key_limit ?? 2,
        tier_webhook_limit: d.tier_webhook_limit ?? 1,
      })
    } catch (e: any) {
      setError(e.message || 'Failed to load dashboard')
    }
    setLoading(false)
  }, [])

  useEffect(() => { fetchDashboard() }, [fetchDashboard])

  const createKey = async () => {
    if (!keyName) return
    setActionLoading('create-key')
    try {
      const res = await fetch('/api/v1/developer/api-keys', {
        method: 'POST', headers, body: JSON.stringify({ name: keyName }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Failed to create key' }))
        setError(err.detail || 'Failed to create key')
      } else {
        const d = await res.json()
        setNewKey(d.raw_key)
        setKeyName('')
        setError(null)
        fetchDashboard()
      }
    } catch (e: any) {
      setError(e.message || 'Failed to create key')
    }
    setActionLoading(null)
  }

  const revokeKey = async (id: string) => {
    setActionLoading(`revoke-${id}`)
    setError(null)
    try {
      const res = await fetch(`/api/v1/developer/api-keys/${id}`, { method: 'DELETE', headers })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Failed to revoke' }))
        setError(err.detail || 'Failed to revoke')
      } else {
        fetchDashboard()
      }
    } catch { /* ignore */ }
    setActionLoading(null)
  }

  const createWebhook = async () => {
    if (!webhookUrl) return
    setActionLoading('create-webhook')
    setError(null)
    try {
      const res = await fetch('/api/v1/developer/webhooks', {
        method: 'POST', headers, body: JSON.stringify({ url: webhookUrl, events: ['price_alert', 'trade'] }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Failed to create webhook' }))
        setError(err.detail || 'Failed to create webhook')
      } else {
        setWebhookUrl('')
        setError(null)
        fetchDashboard()
      }
    } catch (e: any) {
      setError(e.message || 'Failed to create webhook')
    }
    setActionLoading(null)
  }

  const deleteWebhook = async (id: string) => {
    setActionLoading(`del-webhook-${id}`)
    setError(null)
    try {
      const res = await fetch(`/api/v1/developer/webhooks/${id}`, { method: 'DELETE', headers })
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Failed to delete' }))
        setError(err.detail || 'Failed to delete')
      } else {
        fetchDashboard()
      }
    } catch { /* ignore */ }
    setActionLoading(null)
  }

  if (loading) {
    return (
      <div className="p-4 space-y-4">
        <Skeleton className="h-6 w-48" />
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-20" />)}
        </div>
        <Skeleton className="h-48" />
        <Skeleton className="h-40" />
      </div>
    )
  }

  const tier = stats?.tier ?? 'free'
  const keyLimit = stats?.tier_key_limit ?? 2
  const whLimit = stats?.tier_webhook_limit ?? 1

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <h2 className="text-lg font-bold text-cyan flex items-center gap-2">
          <span>🔧</span> Developer Console
        </h2>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${TIER_BADGES[tier] || TIER_BADGES.free}`}>
          {TIER_LABELS[tier] || tier} Plan
        </span>
      </div>

      {error && (
        <div className="p-2 bg-red-900/30 border border-red-700/50 rounded text-xs text-red-300 flex items-start gap-2">
          <span>⚠️</span>
          <span className="flex-1">{error}</span>
          <button onClick={() => setError(null)} className="text-red-400 hover:text-red-200">&times;</button>
        </div>
      )}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
          <div className="text-dim text-xs">API Keys</div>
          <div className="text-green font-bold text-lg">{stats?.total_api_keys ?? 0}</div>
          <ProgressBar used={stats?.total_api_keys ?? 0} limit={keyLimit} />
        </div>
        <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
          <div className="text-dim text-xs">Webhooks</div>
          <div className="text-cyan font-bold text-lg">{stats?.active_webhooks ?? 0}</div>
          <ProgressBar used={stats?.active_webhooks ?? 0} limit={whLimit} />
        </div>
        <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
          <div className="text-dim text-xs">Today</div>
          <div className="text-white font-bold text-lg">{(stats?.requests_today ?? 0).toLocaleString()}</div>
          <div className="text-dim text-xs">API requests</div>
        </div>
        <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
          <div className="text-dim text-xs">This Month</div>
          <div className="text-yellow font-bold text-lg">{(stats?.requests_this_month ?? 0).toLocaleString()}</div>
          <div className="text-dim text-xs">API requests</div>
        </div>
      </div>

      <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
        <h3 className="text-sm font-bold text-green mb-2 flex items-center gap-1.5">
          <span>🔑</span> API Keys <span className="text-dim font-normal text-xs">({stats?.total_api_keys ?? 0}/{keyLimit})</span>
        </h3>
        <div className="flex gap-2 mb-3">
          <input
            value={keyName}
            onChange={e => setKeyName(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && createKey()}
            placeholder="Key name..."
            className="flex-1 bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green outline-none focus:border-green/50 transition-colors"
            aria-label="API key name"
          />
          <button
            onClick={createKey}
            disabled={!keyName || actionLoading === 'create-key'}
            className="px-3 py-1 bg-green-800 text-green rounded text-sm disabled:opacity-50 hover:bg-green-700 transition-colors tap-target"
          >
            {actionLoading === 'create-key' ? 'Creating...' : 'Create'}
          </button>
        </div>
        {newKey && (
          <div className="p-2 bg-yellow-900/40 border border-yellow-700/50 rounded mb-3 text-xs">
            <div className="text-yellow font-bold mb-1">⚠️ Copy your API key now — it won't be shown again!</div>
            <code className="text-white break-all select-all">{newKey}</code>
            <button
              onClick={() => { navigator.clipboard.writeText(newKey); setNewKey(null) }}
              className="ml-2 text-cyan hover:text-white transition-colors"
            >
              Copy
            </button>
          </div>
        )}
        {keys.length === 0 ? (
          <p className="text-dim text-xs py-2">No API keys yet. Create one above.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-dim border-b border-gray-700">
                  <th className="text-left py-1.5 pr-2">Name</th>
                  <th className="text-left py-1.5 px-2">Prefix</th>
                  <th className="text-left py-1.5 px-2 hidden sm:table-cell">Scopes</th>
                  <th className="text-left py-1.5 px-2 hidden md:table-cell">Last Used</th>
                  <th className="text-right py-1.5 pl-2"></th>
                </tr>
              </thead>
              <tbody>
                {keys.map(k => (
                  <tr key={k.id} className="border-b border-gray-800 hover:bg-gray-800/50 transition-colors">
                    <td className="py-1.5 pr-2 text-green">{k.name}</td>
                    <td className="py-1.5 px-2 text-dim font-mono">{k.key_prefix}...</td>
                    <td className="py-1.5 px-2 text-dim hidden sm:table-cell">
                      {Object.entries(k.scopes || {}).filter(([,v]) => v).map(([s]) => s).join(', ') || 'read'}
                    </td>
                    <td className="py-1.5 px-2 text-dim hidden md:table-cell">
                      {k.last_used_at ? new Date(k.last_used_at).toLocaleDateString() : 'Never'}
                    </td>
                    <td className="py-1.5 pl-2 text-right">
                      <button
                        onClick={() => revokeKey(k.id)}
                        disabled={actionLoading === `revoke-${k.id}`}
                        className="text-red-500 hover:text-red-300 text-xs transition-colors disabled:opacity-50 tap-target"
                      >
                        {actionLoading === `revoke-${k.id}` ? 'Revoking...' : 'Revoke'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
        <h3 className="text-sm font-bold text-cyan mb-2 flex items-center gap-1.5">
          <span>🔗</span> Webhooks <span className="text-dim font-normal text-xs">({stats?.active_webhooks ?? 0}/{whLimit})</span>
        </h3>
        <div className="flex gap-2 mb-3">
          <input
            value={webhookUrl}
            onChange={e => setWebhookUrl(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && createWebhook()}
            placeholder="https://example.com/webhook"
            className="flex-1 bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green outline-none focus:border-cyan/50 transition-colors"
            aria-label="Webhook URL"
          />
          <button
            onClick={createWebhook}
            disabled={!webhookUrl || actionLoading === 'create-webhook'}
            className="px-3 py-1 bg-cyan-800 text-cyan rounded text-sm disabled:opacity-50 hover:bg-cyan-700 transition-colors tap-target"
          >
            {actionLoading === 'create-webhook' ? 'Adding...' : 'Add'}
          </button>
        </div>
        {webhooks.length === 0 ? (
          <p className="text-dim text-xs py-2">No webhooks configured. Add one above.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-dim border-b border-gray-700">
                  <th className="text-left py-1.5 pr-2">URL</th>
                  <th className="text-left py-1.5 px-2 hidden sm:table-cell">Events</th>
                  <th className="text-right py-1.5 pl-2"></th>
                </tr>
              </thead>
              <tbody>
                {webhooks.map(w => (
                  <tr key={w.id} className="border-b border-gray-800 hover:bg-gray-800/50 transition-colors">
                    <td className="py-1.5 pr-2 text-green text-xs truncate max-w-[200px] sm:max-w-xs font-mono">{w.url}</td>
                    <td className="py-1.5 px-2 text-dim hidden sm:table-cell">{(w.events || []).join(', ')}</td>
                    <td className="py-1.5 pl-2 text-right">
                      <button
                        onClick={() => deleteWebhook(w.id)}
                        disabled={actionLoading === `del-webhook-${w.id}`}
                        className="text-red-500 hover:text-red-300 text-xs transition-colors disabled:opacity-50 tap-target"
                      >
                        {actionLoading === `del-webhook-${w.id}` ? 'Deleting...' : 'Delete'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
