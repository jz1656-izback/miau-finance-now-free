import { useState, useEffect } from 'react'
import { Eye, EyeOff, Save, CheckCircle, AlertCircle } from 'lucide-react'
import { getToken } from '../lib/auth'

const API_KEY_FIELDS = [
  { key: 'finnhub_api_key', label: 'Finnhub API Key' },
  { key: 'twelvedata_api_key', label: 'Twelve Data API Key' },
  { key: 'bls_api_key', label: 'BLS API Key' },
  { key: 'etherscan_api_key', label: 'Etherscan API Key' },
  { key: 'eia_api_key', label: 'EIA API Key' },
  { key: 'imf_api_key', label: 'IMF API Key' },
]

const BASE = '/api/v1'

function getCSRFToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]*)/)
  return match ? decodeURIComponent(match[1]) : null
}

async function fetchKeys(): Promise<Record<string, string>> {
  const token = getToken()
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE}/api-keys/external`, { headers })
  if (!res.ok) throw new Error('Failed to load API keys')
  const data = await res.json()
  return data.keys || {}
}

async function saveKeys(keys: Record<string, string>): Promise<void> {
  const token = getToken()
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const csrf = getCSRFToken()
  if (csrf) headers['X-CSRF-Token'] = csrf
  const res = await fetch(`${BASE}/api-keys/external`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ keys }),
  })
  if (!res.ok) {
    const err = await res.text()
    throw new Error(err || 'Failed to save API keys')
  }
}

export default function Settings() {
  const [values, setValues] = useState<Record<string, string>>({})
  const [visible, setVisible] = useState<Record<string, boolean>>({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    fetchKeys()
      .then((keys) => {
        setValues(keys)
        const initVisible: Record<string, boolean> = {}
        for (const f of API_KEY_FIELDS) {
          initVisible[f.key] = false
        }
        setVisible(initVisible)
      })
      .catch((e) => {
        setMessage({ type: 'error', text: e.message })
      })
      .finally(() => setLoading(false))
  }, [])

  const toggleVisibility = (key: string) => {
    setVisible((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  const handleChange = (key: string, value: string) => {
    setValues((prev) => ({ ...prev, [key]: value }))
  }

  const handleSave = async () => {
    setSaving(true)
    setMessage(null)
    try {
      await saveKeys(values)
      setMessage({ type: 'success', text: 'API keys saved successfully' })
    } catch (e: any) {
      setMessage({ type: 'error', text: e.message || 'Failed to save API keys' })
    } finally {
      setSaving(false)
    }
  }

  const inputDisplayValue = (key: string) => {
    if (visible[key]) return values[key] || ''
    if (values[key]) return values[key]
    return ''
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Settings</h1>
        <p className="text-sm text-slate-500 mt-1">
          Configure your account and data source preferences
        </p>
      </div>

      <div className="glass-panel rounded-lg p-4">
        <div className="text-sm text-green font-semibold mb-4 flex items-center gap-2">
          <span>🔑</span> API Keys
        </div>

        {loading ? (
          <div className="text-xs text-dim py-4">Loading API keys...</div>
        ) : (
          <div className="space-y-4">
            {API_KEY_FIELDS.map((field) => (
              <div key={field.key}>
                <label className="block text-xs text-dim mb-1">{field.label}</label>
                <div className="flex items-center gap-2">
                  <div className="relative flex-1">
                    <input
                      type={visible[field.key] ? 'text' : 'password'}
                      value={inputDisplayValue(field.key)}
                      onChange={(e) => handleChange(field.key, e.target.value)}
                      placeholder={values[field.key] ? '••••••••' : 'Not configured'}
                      className="w-full bg-[#0a1a14] border border-[#1a3a2a] rounded px-3 py-2 text-xs text-green font-mono placeholder:text-[#2a4a3a] focus:outline-none focus:border-green/50 transition-colors pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => toggleVisibility(field.key)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-dim hover:text-green transition-colors"
                      aria-label={visible[field.key] ? 'Hide key' : 'Show key'}
                    >
                      {visible[field.key] ? (
                        <EyeOff size={14} />
                      ) : (
                        <Eye size={14} />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            ))}

            <div className="flex items-center gap-3 pt-2">
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex items-center gap-2 px-4 py-2 text-xs rounded border border-green text-green hover:bg-green/10 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Save size={14} />
                {saving ? 'Saving...' : 'Save'}
              </button>

              {message && (
                <span
                  className={`flex items-center gap-1.5 text-xs ${
                    message.type === 'success' ? 'text-green' : 'text-red'
                  }`}
                >
                  {message.type === 'success' ? (
                    <CheckCircle size={14} />
                  ) : (
                    <AlertCircle size={14} />
                  )}
                  {message.text}
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
