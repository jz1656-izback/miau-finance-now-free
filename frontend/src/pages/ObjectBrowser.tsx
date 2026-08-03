import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import { Search, Grid3X3, List } from 'lucide-react'

const TYPE_ICONS: Record<string, string> = {
  Instrument: '📈',
  Counterparty: '🏛️',
  Portfolio: '💼',
  Trade: '🔄',
  Position: '📊',
  MarketData: '📉',
}

export default function ObjectBrowser() {
  const navigate = useNavigate()
  const [selectedType, setSelectedType] = useState<string>('')
  const [search, setSearch] = useState('')
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid')

  const { data: types } = useQuery({
    queryKey: ['ontology-types'],
    queryFn: api.getTypes,
  })

  const { data: objects, isLoading } = useQuery({
    queryKey: ['ontology-objects', selectedType, search],
    queryFn: () => {
      const params: Record<string, string> = {}
      if (selectedType) params.type_id = selectedType
      if (search) params.search = search
      return api.getObjects(params)
    },
  })

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Object Explorer</h1>
          <p className="text-sm text-slate-500 mt-1">
            Browse and manage financial ontology objects
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode(viewMode === 'grid' ? 'table' : 'grid')}
            className="btn-secondary p-2"
          >
            {viewMode === 'grid' ? <List size={16} /> : <Grid3X3 size={16} />}
          </button>
        </div>
      </div>

      <div className="flex gap-4 items-center flex-wrap">
        <div className="relative flex-1 max-w-md">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Filter objects..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-9"
          />
        </div>

        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setSelectedType('')}
            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              !selectedType
                ? 'bg-miau-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            All Types
          </button>
          {(types || []).map((t: any) => (
            <button
              key={t.id}
              onClick={() => setSelectedType(t.id)}
              className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors flex items-center gap-1.5 ${
                selectedType === t.id
                  ? 'bg-miau-600 text-white'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              <span>{TYPE_ICONS[t.name] || '📦'}</span>
              {t.display_name}
            </button>
          ))}
        </div>
      </div>

      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {(objects || []).map((obj: any) => (
            <div
              key={obj.id}
              onClick={() => navigate(`/objects/${obj.id}`)}
              className="card cursor-pointer hover:border-slate-700 transition-colors"
            >
              <div className="flex items-start gap-3 mb-2">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center text-white text-lg"
                  style={{ backgroundColor: obj.type_color || '#6366f1' }}
                >
                  {TYPE_ICONS[obj.type_name] || '📦'}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-medium text-slate-200 truncate">
                    {obj.display_name}
                  </div>
                  <div className="text-xs text-slate-500">{obj.type_name}</div>
                </div>
              </div>
              {obj.description && (
                <p className="text-xs text-slate-500 line-clamp-2 mb-2">
                  {obj.description}
                </p>
              )}
              <div className="flex items-center gap-2 mt-auto">
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  obj.status === 'active'
                    ? 'bg-emerald-900/50 text-emerald-300'
                    : 'bg-slate-800 text-slate-500'
                }`}>
                  {obj.status}
                </span>
                {obj.tags?.slice(0, 2).map((tag: string) => (
                  <span key={tag} className="text-xs text-slate-600 bg-slate-800 px-1.5 py-0.5 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
          {(!objects || objects.length === 0) && !isLoading && (
            <div className="col-span-full text-center text-slate-500 py-12">
              <p className="text-lg mb-2">No objects found</p>
              <p className="text-sm">Try changing your search or filter criteria</p>
            </div>
          )}
        </div>
      ) : (
        <div className="panel overflow-hidden">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Status</th>
                <th>Tags</th>
                <th>Updated</th>
              </tr>
            </thead>
            <tbody>
              {(objects || []).map((obj: any) => (
                <tr
                  key={obj.id}
                  className="cursor-pointer"
                  onClick={() => navigate(`/objects/${obj.id}`)}
                >
                  <td className="font-medium text-slate-200">{obj.display_name}</td>
                  <td>
                    <span className="badge-blue">{obj.type_name}</span>
                  </td>
                  <td>
                    <span className={`badge ${
                      obj.status === 'active' ? 'badge-green' : 'badge-yellow'
                    }`}>
                      {obj.status}
                    </span>
                  </td>
                  <td>
                    <div className="flex gap-1">
                      {(obj.tags || []).map((tag: string) => (
                        <span key={tag} className="text-xs text-slate-500 bg-slate-800 px-1.5 py-0.5 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="text-xs text-slate-500">
                    {new Date(obj.updated_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
