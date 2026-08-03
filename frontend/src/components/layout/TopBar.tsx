import { useState, useCallback, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Bell, User } from 'lucide-react'
import { api } from '../../lib/api'
import type { SearchResult } from '../../types'

export default function TopBar() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [showResults, setShowResults] = useState(false)
  const searchRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClick(e: MouseEvent) {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowResults(false)
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  const handleSearch = useCallback(async (q: string) => {
    setQuery(q)
    if (q.length < 2) {
      setResults([])
      setShowResults(false)
      return
    }
    try {
      const res = await api.search(q)
      setResults(res.results)
      setShowResults(true)
    } catch (e) {
      console.error(e)
    }
  }, [])

  const handleSelect = (result: SearchResult) => {
    setShowResults(false)
    setQuery('')
    navigate(`/objects/${result.id}`)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      navigate(`/search?q=${encodeURIComponent(query)}`)
      setShowResults(false)
    }
  }

  return (
    <header className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-6 gap-4 flex-shrink-0">
      <div ref={searchRef} className="relative flex-1 max-w-xl">
        <form onSubmit={handleSubmit}>
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search instruments, trades, portfolios..."
            value={query}
            onChange={(e) => handleSearch(e.target.value)}
            className="input pl-9 pr-4"
          />
        </form>

        {showResults && results.length > 0 && (
          <div className="absolute top-full left-0 right-0 mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-h-96 overflow-y-auto z-50">
            {results.map((r) => (
              <button
                key={r.id}
                onClick={() => handleSelect(r)}
                className="w-full px-4 py-3 flex items-start gap-3 hover:bg-slate-700 text-left border-b border-slate-700/50 last:border-0"
              >
                <div
                  className="w-8 h-8 rounded-md flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-0.5"
                  style={{ backgroundColor: r.type_color || '#6366f1' }}
                >
                  {r.display_name.slice(0, 2).toUpperCase()}
                </div>
                <div className="min-w-0">
                  <div className="text-sm font-medium text-slate-200 truncate">
                    {r.display_name}
                  </div>
                  <div className="text-xs text-slate-500">
                    {r.type_display_name}
                    {r.description && ` — ${r.description.slice(0, 80)}`}
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      <button className="btn-ghost relative">
        <Bell size={18} />
        <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-red-500 rounded-full" />
      </button>

      <button className="flex items-center gap-2 btn-ghost">
        <div className="w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center">
          <User size={14} />
        </div>
        <span className="text-sm text-slate-300">Admin</span>
      </button>
    </header>
  )
}
