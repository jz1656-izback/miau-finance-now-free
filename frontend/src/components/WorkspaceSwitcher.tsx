import { useState, useEffect, useCallback } from 'react'

interface Workspace {
  id: string
  name: string
  role?: string
  member_count?: number
}

const BASE = '/api/v1'

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(`${BASE}${url}`)
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}

export default function WorkspaceSwitcher() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([])
  const [current, setCurrent] = useState<Workspace | null>(null)
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchJSON<Workspace[]>('/teams')
      .then(data => {
        setWorkspaces(data)
        if (data.length > 0) {
          const saved = localStorage.getItem('miau:workspace_id')
          const found = saved ? data.find(w => w.id === saved) : null
          setCurrent(found || data[0])
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const switchWorkspace = useCallback((ws: Workspace) => {
    setCurrent(ws)
    localStorage.setItem('miau:workspace_id', ws.id)
    setOpen(false)
    window.dispatchEvent(new CustomEvent('workspace-changed', { detail: ws }))
  }, [])

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-3 py-1">
        <div className="w-24 h-4 rounded bg-[#1a3a2a] animate-pulse" />
      </div>
    )
  }

  if (workspaces.length === 0) return null

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-2 py-1 text-xs text-green hover:text-glow-green transition-colors rounded border border-[#1a3a2a] hover:border-green/30"
      >
        <span>📁</span>
        <span className="max-w-[120px] truncate">{current?.name || 'Select workspace'}</span>
        <span className="text-dim">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="absolute top-full left-0 mt-1 w-56 glass-panel rounded-lg overflow-hidden z-50 shadow-lg">
          <div className="p-2 border-b border-[#1a3a2a]">
            <div className="text-xs text-dim font-semibold">Workspaces</div>
          </div>
          <div className="py-1 max-h-48 overflow-y-auto">
            {workspaces.map(ws => (
              <button
                key={ws.id}
                onClick={() => switchWorkspace(ws)}
                className={`w-full text-left px-3 py-2 text-xs transition-colors flex items-center justify-between ${
                  current?.id === ws.id
                    ? 'text-green bg-[#1a3a2a]/50'
                    : 'text-dim hover:text-green hover:bg-[#1a3a2a]/30'
                }`}
              >
                <span className="truncate">{ws.name}</span>
                {current?.id === ws.id && <span className="text-green shrink-0 ml-2">✓</span>}
              </button>
            ))}
          </div>
          <div className="border-t border-[#1a3a2a] p-2">
            <button
              onClick={() => {
                setOpen(false)
                window.dispatchEvent(new CustomEvent('create-workspace'))
              }}
              className="w-full text-left text-xs text-cyan hover:text-green transition-colors px-1 py-1"
            >
              + Create workspace
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
