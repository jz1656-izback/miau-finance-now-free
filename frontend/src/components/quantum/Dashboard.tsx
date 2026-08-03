import { useState } from 'react'

export default function QuantumDashboard() {
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [problem, setProblem] = useState('portfolio')
  const [error, setError] = useState('')

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}`, 'Content-Type': 'application/json' }

  const runQuantum = async () => {
    setLoading(true)
    setError('')
    try {
      let res
      if (problem === 'portfolio') {
        res = await fetch('/api/v1/quantum/portfolio', {
          method: 'POST', headers,
          body: JSON.stringify({ expected_returns: [0.12, 0.08, 0.15, 0.10], covariance: [[0.1, 0.02, 0.04, 0.03], [0.02, 0.08, 0.01, 0.02], [0.04, 0.01, 0.12, 0.05], [0.03, 0.02, 0.05, 0.09]], gamma: 1.0 }),
        })
      } else if (problem === 'qubo') {
        res = await fetch('/api/v1/quantum/qubo/solve', {
          method: 'POST', headers,
          body: JSON.stringify({ Q: [[-1, 1], [1, -1]], num_reads: 10 }),
        })
      } else {
        res = await fetch('/api/v1/quantum/hybrid/qaoa', {
          method: 'POST', headers,
          body: JSON.stringify({ Q: [[-1, 0.5, 0.3], [0.5, -1, 0.2], [0.3, 0.2, -1]], p_layers: 2 }),
        })
      }
      const data = await res.json()
      setResult(data)
    } catch (e: any) {
      setError(e.message)
    }
    setLoading(false)
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">⚛️ Quantum Computing</h2>
      <div className="flex gap-2">
        {['portfolio', 'qubo', 'qaoa'].map(p => (
          <button key={p} onClick={() => setProblem(p)}
            className={`text-xs px-2 py-1 rounded border ${problem === p ? 'bg-purple-900/30 border-purple-700 text-purple' : 'bg-gray-800 border-gray-700 text-dim'}`}>{p}</button>
        ))}
      </div>
      <button onClick={runQuantum} disabled={loading}
        className="px-3 py-1 bg-purple-800 text-purple rounded text-sm disabled:opacity-50">
        {loading ? 'Solving...' : '🚀 Run Quantum'}
      </button>
      {error && <div className="text-red text-xs bg-red-900/20 p-2 rounded">❌ {error}</div>}
      {result && (
        <pre className="bg-gray-900 p-3 rounded text-xs text-green font-mono overflow-x-auto max-h-64">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  )
}
