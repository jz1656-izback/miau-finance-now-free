import { useState, useEffect } from 'react'

interface Broker {
  id: string
  name: string
  status: 'connected' | 'disconnected' | 'error'
  balance?: number
  mode: 'paper' | 'live'
}

export default function BrokerConfig() {
  const [brokers, setBrokers] = useState<Broker[]>([])
  const [loading, setLoading] = useState(true)
  const [showConnect, setShowConnect] = useState(false)
  const [connectName, setConnectName] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [mode, setMode] = useState<'paper' | 'live'>('paper')
  const [testing, setTesting] = useState(false)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }

  const fetchBrokers = async () => {
    try {
      const res = await fetch('/api/v1/brokers', { headers })
      if (res.ok) {
        const data = await res.json()
        setBrokers(data.brokers || data || [])
      }
    } catch { /* ignore */ }
    setLoading(false)
  }

  useEffect(() => { fetchBrokers() }, [])

  const connectBroker = async () => {
    if (!connectName) return
    try {
      const res = await fetch('/api/v1/brokers/connect', {
        method: 'POST',
        headers,
        body: JSON.stringify({ name: connectName, api_key: apiKey || undefined, mode }),
      })
      if (res.ok) {
        setShowConnect(false)
        setConnectName('')
        setApiKey('')
        fetchBrokers()
      }
    } catch { /* ignore */ }
  }

  const disconnectBroker = async (name: string) => {
    try {
      await fetch(`/api/v1/brokers/${name}/disconnect`, {
        method: 'POST',
        headers,
      })
      fetchBrokers()
    } catch { /* ignore */ }
  }

  const testConnection = async () => {
    setTesting(true)
    try {
      const res = await fetch('/api/v1/brokers/test', {
        method: 'POST',
        headers,
        body: JSON.stringify({ name: connectName || 'test', api_key: apiKey || undefined }),
      })
      if (res.ok) alert('Connection successful!')
      else alert('Connection failed')
    } catch { alert('Connection test error') }
    setTesting(false)
  }

  if (loading) return <div className="p-4 text-dim">Loading broker configuration...</div>

  return (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-bold text-cyan">🔌 Broker Configuration</h2>
        <button onClick={() => setShowConnect(!showConnect)} className="px-3 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-sm">
          {showConnect ? 'Cancel' : '+ Connect'}
        </button>
      </div>

      {showConnect && (
        <div className="p-4 bg-gray-800 rounded space-y-3">
          <h3 className="text-sm font-bold text-cyan">Connect Broker</h3>
          <div>
            <label className="text-dim text-xs block mb-1">Broker Name</label>
            <input value={connectName} onChange={e => setConnectName(e.target.value)} placeholder="e.g. alpaca, ibkr" className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-sm text-white w-full" />
          </div>
          <div>
            <label className="text-dim text-xs block mb-1">API Key (optional for paper)</label>
            <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} className="bg-gray-700 border border-gray-600 rounded px-2 py-1 text-sm text-white w-full" />
          </div>
          <div>
            <label className="text-dim text-xs block mb-1">Mode</label>
            <div className="flex gap-2">
              <button onClick={() => setMode('paper')} className={`px-3 py-1 rounded text-xs ${mode === 'paper' ? 'bg-green-700 text-white' : 'bg-gray-700 text-dim'}`}>Paper</button>
              <button onClick={() => setMode('live')} className={`px-3 py-1 rounded text-xs ${mode === 'live' ? 'bg-red-700 text-white' : 'bg-gray-700 text-dim'}`}>Live</button>
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={connectBroker} className="px-4 py-1 bg-cyan-700 hover:bg-cyan-600 text-white rounded text-sm">Connect</button>
            <button onClick={testConnection} disabled={testing} className="px-4 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm disabled:opacity-50">
              {testing ? 'Testing...' : 'Test Connection'}
            </button>
          </div>
        </div>
      )}

      <div className="space-y-2">
        {brokers.length === 0 ? (
          <p className="text-dim text-sm">No brokers configured. Click "+ Connect" to add one.</p>
        ) : (
          brokers.map((broker) => (
            <div key={broker.id || broker.name} className="p-3 bg-gray-800 rounded flex justify-between items-center">
              <div>
                <div className="text-white font-bold">{broker.name}</div>
                <div className="flex gap-2 text-xs mt-1">
                  <span className={`px-2 py-0.5 rounded ${broker.status === 'connected' ? 'bg-green-900 text-green' : broker.status === 'error' ? 'bg-red-900 text-red' : 'bg-gray-700 text-dim'}`}>
                    {broker.status}
                  </span>
                  <span className={`px-2 py-0.5 rounded ${broker.mode === 'live' ? 'bg-red-900 text-red' : 'bg-blue-900 text-blue'}`}>
                    {broker.mode}
                  </span>
                  {broker.balance != null && <span className="text-green">${broker.balance.toLocaleString()}</span>}
                </div>
              </div>
              <div className="flex gap-2">
                <button onClick={() => fetch(`/api/v1/brokers/${broker.name}/sync`, { method: 'POST', headers })} className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-xs">Sync</button>
                <button onClick={() => disconnectBroker(broker.name)} className="px-2 py-1 bg-red-800 hover:bg-red-700 text-white rounded text-xs">Disconnect</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
