import { useState, useEffect } from 'react'

interface PluginMeta {
  name: string; version: string; description: string; author: string
  hooks: string[]; permissions: string[]; is_active: boolean
}

export default function PluginConfig() {
  const [plugins, setPlugins] = useState<PluginMeta[]>([])
  const [loading, setLoading] = useState(true)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  useEffect(() => {
    fetch('/api/v1/plugins', { headers })
      .then(r => r.json())
      .then(d => setPlugins(Array.isArray(d) ? d : []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const togglePlugin = async (name: string, active: boolean) => {
    await fetch(`/api/v1/plugins/${name}/${active ? 'enable' : 'disable'}`, { method: 'POST', headers })
    setPlugins(plugins.map(p => p.name === name ? { ...p, is_active: active } : p))
  }

  if (loading) return <div className="p-4 text-dim text-sm">Loading plugins...</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan flex items-center gap-2">🧩 Plugin Manager</h2>
      {plugins.length === 0 ? (
        <p className="text-dim text-xs">No plugins installed. Plugins go in <code>plugins/</code> directory.</p>
      ) : (
        plugins.map(p => (
          <div key={p.name} className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-bold text-green">{p.name}</span>
              <button
                onClick={() => togglePlugin(p.name, !p.is_active)}
                className={`text-xs px-2 py-0.5 rounded ${p.is_active ? 'bg-green-800 text-green' : 'bg-gray-700 text-dim'}`}
              >
                {p.is_active ? 'Enabled' : 'Disabled'}
              </button>
            </div>
            <div className="text-xs text-dim">{p.description}</div>
            <div className="text-xs text-dim mt-1">v{p.version} by {p.author}</div>
            <div className="flex gap-1 mt-1">
              {p.hooks.map(h => <span key={h} className="text-[10px] bg-gray-900 text-cyan px-1 rounded">{h}</span>)}
            </div>
          </div>
        ))
      )}
    </div>
  )
}
