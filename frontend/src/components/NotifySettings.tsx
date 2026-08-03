import { useState } from 'react'

interface NotifySetting {
  type: string
  label: string
  enabled: boolean
}

const ALL_SETTINGS: NotifySetting[] = [
  { type: 'price_alert', label: 'Price Alerts', enabled: true },
  { type: 'trade_executed', label: 'Trade Execution', enabled: true },
  { type: 'ai_insight', label: 'AI Insights', enabled: false },
  { type: 'daily_summary', label: 'Daily Summary', enabled: false },
]

export default function NotifySettings() {
  const [settings, setSettings] = useState<NotifySetting[]>(ALL_SETTINGS)
  const [saved, setSaved] = useState(false)

  const toggle = (type: string) => {
    setSettings(prev => prev.map(s => s.type === type ? { ...s, enabled: !s.enabled } : s))
    setSaved(false)
  }

  const save = async () => {
    try {
      await fetch('/api/v1/social/notify/settings', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ settings }),
      })
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } catch { /* offline */ }
  }

  return (
    <div className="glass-panel rounded-lg p-4">
      <div className="text-sm text-green font-semibold mb-3">Notification Settings</div>
      {settings.map(s => (
        <label key={s.type} className="flex items-center justify-between py-2 border-b border-[#1a3a2a] last:border-0">
          <span className="text-xs text-dim">{s.label}</span>
          <button
            onClick={() => toggle(s.type)}
            className={`w-10 h-5 rounded-full transition-colors relative ${s.enabled ? 'bg-green/40' : 'bg-[#1a3a2a]'}`}
          >
            <span className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-transform ${s.enabled ? 'translate-x-5' : 'translate-x-0.5'}`} />
          </button>
        </label>
      ))}
      <button onClick={save} className="mt-3 px-4 py-1 text-xs rounded border border-green text-green hover:bg-green/10 transition-colors">
        {saved ? 'Saved' : 'Save Settings'}
      </button>
    </div>
  )
}
