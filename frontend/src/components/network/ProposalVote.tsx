import { useState, useEffect } from 'react'

interface Proposal {
  id: string; title: string; proposer: string; status: string
  for_votes: number; against_votes: number; abstain_votes: number; voting_days: number
}

export default function ProposalVote() {
  const [proposals, setProposals] = useState<Proposal[]>([])
  const [loading, setLoading] = useState(true)
  const [voting, setVoting] = useState<string | null>(null)

  const headers = { Authorization: `Bearer ${localStorage.getItem('token')}` }

  const fetchProposals = () => {
    fetch('/api/v1/network/governance/proposals', { headers })
      .then(r => r.json()).then(setProposals).catch(() => {}).finally(() => setLoading(false))
  }

  useEffect(() => { fetchProposals() }, [])

  const vote = async (pid: string, vote: string) => {
    setVoting(pid)
    await fetch(`/api/v1/network/governance/proposals/${pid}/vote?vote=${vote}`, { method: 'POST', headers })
    fetchProposals()
    setVoting(null)
  }

  if (loading) return <div className="p-4 text-dim">Loading proposals...</div>

  return (
    <div className="p-4 space-y-3">
      <h2 className="text-lg font-bold text-cyan">🗳️ Governance Voting</h2>
      {proposals.length === 0 ? (
        <p className="text-dim text-xs">No active proposals. Create one with `network propose`!</p>
      ) : (
        proposals.map(p => {
          const total = p.for_votes + p.against_votes + p.abstain_votes
          const forPct = total > 0 ? (p.for_votes / total * 100).toFixed(1) : '0'
          return (
            <div key={p.id} className="p-3 bg-gray-800/80 rounded border border-gray-700/50">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-green">{p.title}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${p.status === 'passed' ? 'bg-green-900/30 text-green' : p.status === 'active' ? 'bg-blue-900/30 text-blue' : 'bg-gray-700 text-dim'}`}>{p.status}</span>
              </div>
              <div className="text-[10px] text-dim mt-1">by {p.proposer}</div>
              <div className="mt-2 bg-gray-900 rounded h-2 flex overflow-hidden">
                <div className="bg-green-600 h-full" style={{ width: `${forPct}%` }} />
                <div className="bg-red-600 h-full" style={{ width: `${total > 0 ? (p.against_votes / total * 100).toFixed(1) : '0'}%` }} />
              </div>
              <div className="flex items-center gap-3 mt-1 text-[10px]">
                <span className="text-green">{p.for_votes.toFixed(0)} for</span>
                <span className="text-red">{p.against_votes.toFixed(0)} against</span>
                <span className="text-dim">{p.abstain_votes.toFixed(0)} abstain</span>
              </div>
              {p.status === 'active' && (
                <div className="flex gap-2 mt-2">
                  <button onClick={() => vote(p.id, 'for')} disabled={voting === p.id} className="px-2 py-0.5 bg-green-800 text-green text-[10px] rounded disabled:opacity-50">Vote For</button>
                  <button onClick={() => vote(p.id, 'against')} disabled={voting === p.id} className="px-2 py-0.5 bg-red-800 text-red text-[10px] rounded disabled:opacity-50">Vote Against</button>
                  <button onClick={() => vote(p.id, 'abstain')} disabled={voting === p.id} className="px-2 py-0.5 bg-gray-700 text-dim text-[10px] rounded disabled:opacity-50">Abstain</button>
                </div>
              )}
            </div>
          )
        })
      )}
    </div>
  )
}
