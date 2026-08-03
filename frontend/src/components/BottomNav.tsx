import { useCallback } from 'react'

const NAV_ITEMS = [
  { id: 'terminal', label: 'Terminal', icon: '>' },
  { id: 'portfolios', label: 'Portfolios', icon: '📁' },
  { id: 'market', label: 'Market', icon: '📊' },
  { id: 'trades', label: 'Trades', icon: '📋' },
  { id: 'ai', label: 'AI', icon: '🤖' },
]

export default function BottomNav() {
  const navigate = useCallback((cmd: string) => {
    window.dispatchEvent(new CustomEvent('terminal-command', { detail: cmd }))
  }, [])

  return (
    <nav
      className="flex items-center justify-around px-2 py-1 border-t"
      style={{ background: '#0d2018', borderColor: '#1a3a2a' }}
    >
      {NAV_ITEMS.map(item => (
        <button
          key={item.id}
          onClick={() => navigate(item.id === 'terminal' ? '' : item.id)}
          className="flex flex-col items-center gap-0.5 px-3 py-1 text-xs text-dim hover:text-green transition-colors"
        >
          <span>{item.icon}</span>
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  )
}
