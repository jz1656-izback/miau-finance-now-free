import { useState, useEffect, useRef } from 'react'

const DEFAULT_COMMANDS = [
  'price AAPL', 'chart TSLA', 'crypto', 'fear', 'sectors', 'movers',
  'portfolios', 'summary', 'trades', 'signals AAPL',
  'optimize AAPL,MSFT,GOOGL', 'risk SPY', 'beta AAPL',
  'fundamentals AAPL', 'news AAPL', 'earnings AAPL',
  'help', 'cat', 'miau',
]

interface CommandPaletteProps {
  onSelect: (command: string) => void
  onClose: () => void
}

export default function CommandPalette({ onSelect, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('')
  const [index, setIndex] = useState(0)
  const filtered = query
    ? DEFAULT_COMMANDS.filter(c => c.toLowerCase().includes(query.toLowerCase()))
    : DEFAULT_COMMANDS
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => { inputRef.current?.focus() }, [])
  useEffect(() => { setIndex(0) }, [query])

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') { e.preventDefault(); setIndex(i => Math.min(i + 1, filtered.length - 1)) }
    if (e.key === 'ArrowUp') { e.preventDefault(); setIndex(i => Math.max(i - 1, 0)) }
    if (e.key === 'Enter' && filtered[index]) { onSelect(filtered[index]); onClose() }
    if (e.key === 'Escape') onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-start justify-center pt-20" onClick={onClose}>
      <div className="bg-[#0a1a14] border border-green-700/50 rounded-lg w-full max-w-lg mx-4 overflow-hidden shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="p-3 border-b border-green-800/40">
          <input
            ref={inputRef}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Type a command..."
            className="w-full bg-transparent text-green-400 font-mono text-sm outline-none placeholder-green-700"
            style={{ fontSize: '16px' }}
          />
        </div>
        <div className="max-h-64 overflow-y-auto">
          {filtered.map((cmd, i) => (
            <div
              key={cmd}
              onClick={() => { onSelect(cmd); onClose() }}
              className={`px-4 py-2 font-mono text-sm cursor-pointer ${
                i === index ? 'bg-green-900/30 text-green-300' : 'text-green-500'
              }`}
            >
              {cmd}
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="px-4 py-3 text-green-700 text-sm font-mono">No commands match</div>
          )}
        </div>
      </div>
    </div>
  )
}
