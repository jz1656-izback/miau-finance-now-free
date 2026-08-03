import { useState } from 'react'

export default function ProposalCreate() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<any>(null)

  const submit = async () => {
    if (!title) return
    setSubmitting(true)
    try {
      const res = await fetch(`/api/v1/network/governance/proposals?title=${encodeURIComponent(title)}&description=${encodeURIComponent(description)}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      })
      const data = await res.json()
      setResult(data)
    } catch { setResult({ error: 'Failed to create proposal' }) }
    setSubmitting(false)
  }

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🗳️ Create Proposal</h2>
      <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Proposal title" className="w-full bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green outline-none" />
      <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Description..." className="w-full bg-gray-900 border border-gray-700 rounded px-2 py-1 text-sm text-green outline-none h-20" />
      <button onClick={submit} disabled={submitting || !title} className="px-3 py-1 bg-purple-800 text-purple rounded text-sm disabled:opacity-50">
        {submitting ? 'Creating...' : 'Submit Proposal'}
      </button>
      {result && (
        <div className="p-2 bg-gray-800 rounded text-xs text-green">
          {result.id ? `✅ Proposal created: ${result.id}` : `❌ ${result.error}`}
        </div>
      )}
    </div>
  )
}
