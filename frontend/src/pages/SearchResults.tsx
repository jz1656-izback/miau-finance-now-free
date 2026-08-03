import { useSearchParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { Search } from 'lucide-react'

export default function SearchResults() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const q = searchParams.get('q') || ''

  const { data, isLoading } = useQuery({
    queryKey: ['search', q],
    queryFn: () => api.search(q),
    enabled: q.length > 0,
  })

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">
          <span className="text-slate-500">Search: </span>"{q}"
        </h1>
        {data && (
          <p className="text-sm text-slate-500 mt-1">{data.total} results found</p>
        )}
      </div>

      {isLoading ? (
        <div className="text-slate-500">Searching...</div>
      ) : (
        <div className="space-y-2">
          {(data?.results || []).length > 0 ? (
            data!.results.map((result: any) => (
              <div
                key={result.id}
                onClick={() => navigate(`/objects/${result.id}`)}
                className="card cursor-pointer hover:border-slate-700 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center text-white text-sm font-bold flex-shrink-0"
                    style={{ backgroundColor: result.type_color || '#6366f1' }}
                  >
                    {result.display_name.slice(0, 2).toUpperCase()}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-medium text-slate-200">
                      {result.display_name}
                    </div>
                    <div className="text-xs text-slate-500 mt-0.5">
                      {result.type_display_name}
                    </div>
                    {result.description && (
                      <p className="text-xs text-slate-500 mt-1 line-clamp-2">
                        {result.description}
                      </p>
                    )}
                  </div>
                  <div className="text-xs text-slate-600">
                    {(result.rank || 0).toFixed(2)}
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center text-slate-500 py-12">
              <Search size={32} className="mx-auto mb-3 opacity-50" />
              <p>No results found for "{q}"</p>
              <p className="text-sm mt-1">Try different search terms</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
