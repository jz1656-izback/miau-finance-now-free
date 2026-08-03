import { useState, useEffect, useCallback } from 'react'

interface ChatEntry {
  query: string
  response: string
  timestamp: number
}

const STORAGE_KEY = 'miau:ai:chat_history'

function loadHistory(): ChatEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

interface ChatHistoryProps {
  onReplay: (query: string) => void
}

export default function ChatHistory({ onReplay }: ChatHistoryProps) {
  const [open, setOpen] = useState(false)
  const [history, setHistory] = useState<ChatEntry[]>([])

  useEffect(() => {
    setHistory(loadHistory())
  }, [])

  const clearHistory = useCallback(() => {
    setHistory([])
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const handleReplay = useCallback((query: string) => {
    onReplay(query)
    setOpen(false)
  }, [onReplay])

  const formatTime = (ts: number) => {
    const d = new Date(ts)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="text-xs text-dim hover:text-green transition-colors px-2 py-1 rounded border border-[#1a3a2a] hover:border-green/30 flex items-center gap-1"
      >
        <span>{open ? '▼' : '▶'}</span>
        <span>History ({history.length})</span>
      </button>

      {open && (
        <div className="absolute bottom-full left-0 mb-2 w-80 glass-panel rounded-lg max-h-64 overflow-y-auto z-50">
          {history.length === 0 ? (
            <div className="text-dim text-xs p-3 text-center">No AI queries yet</div>
          ) : (
            <div className="p-2 space-y-1">
              {history.map((entry) => (
                <div
                  key={entry.timestamp}
                  className="flex items-start gap-2 p-2 rounded hover:bg-[#1a3a2a]/50 cursor-pointer transition-colors"
                  onClick={() => handleReplay(entry.query)}
                >
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-green truncate">{entry.query}</div>
                    <div className="text-xs text-dim truncate mt-0.5">{entry.response.slice(0, 60)}</div>
                  </div>
                  <div className="text-xs text-dim shrink-0">{formatTime(entry.timestamp)}</div>
                </div>
              ))}
            </div>
          )}
          {history.length > 0 && (
            <div className="border-t border-[#1a3a2a] p-2">
              <button
                onClick={clearHistory}
                className="text-xs text-red hover:text-red/80 transition-colors w-full text-center"
              >
                Clear history
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
