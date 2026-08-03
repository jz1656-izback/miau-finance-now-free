import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { ArrowLeft, ExternalLink, Edit3, Clock, Tag } from 'lucide-react'

export default function ObjectDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data: obj, isLoading } = useQuery({
    queryKey: ['ontology-object', id],
    queryFn: () => api.getObject(id!),
    enabled: !!id,
  })

  if (isLoading) {
    return <div className="text-slate-500">Loading...</div>
  }

  if (!obj) {
    return <div className="text-red-400">Object not found</div>
  }

  const props = obj.properties || {}
  const links = obj.links || []

  const groupedLinks: Record<string, any[]> = {}
  links.forEach((link: any) => {
    const key = link.link_display_name || link.link_name || 'Related'
    if (!groupedLinks[key]) groupedLinks[key] = []
    groupedLinks[key].push(link)
  })

  return (
    <div className="space-y-6 max-w-5xl">
      <button
        onClick={() => navigate(-1)}
        className="btn-ghost flex items-center gap-1 text-xs"
      >
        <ArrowLeft size={14} /> Back
      </button>

      <div className="flex items-start gap-4">
        <div
          className="w-14 h-14 rounded-xl flex items-center justify-center text-white text-2xl flex-shrink-0"
          style={{ backgroundColor: obj.type_color || '#6366f1' }}
        >
          {obj.display_name.slice(0, 2).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-slate-100">{obj.display_name}</h1>
            <span className={`badge ${
              obj.status === 'active' ? 'badge-green' : 'badge-yellow'
            }`}>
              {obj.status}
            </span>
            <span className="badge-blue">{obj.type_name}</span>
          </div>
          {obj.description && (
            <p className="text-sm text-slate-400 mt-1">{obj.description}</p>
          )}
          <div className="flex items-center gap-3 mt-2 text-xs text-slate-600">
            <span className="flex items-center gap-1">
              <Clock size={12} /> Updated {new Date(obj.updated_at).toLocaleString()}
            </span>
            {obj.created_by && (
              <span>Created by {obj.created_by}</span>
            )}
          </div>
        </div>
        <button className="btn-secondary flex items-center gap-1.5">
          <Edit3 size={14} /> Edit
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="panel">
            <div className="panel-header">Properties</div>
            <div className="p-4">
              {Object.keys(props).length > 0 ? (
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(props).map(([key, value]) => (
                    <div key={key}>
                      <div className="text-xs text-slate-500 uppercase tracking-wider mb-1">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-sm text-slate-200 font-medium">
                        {typeof value === 'number'
                          ? value.toLocaleString(undefined, {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 6,
                            })
                          : String(value)}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-slate-500 text-sm">No properties</div>
              )}
            </div>
          </div>

          {obj.tags?.length > 0 && (
            <div className="panel">
              <div className="panel-header">
                <Tag size={14} /> Tags
              </div>
              <div className="p-4 flex flex-wrap gap-2">
                {obj.tags.map((tag: string) => (
                  <span
                    key={tag}
                    className="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-md text-xs border border-slate-700"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div className="panel">
            <div className="panel-header">Data Lineage</div>
            <div className="p-4 text-sm text-slate-500">
              Lineage tracking is enabled for this object.
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {Object.entries(groupedLinks).map(([groupName, groupLinks]) => (
            <div key={groupName} className="panel">
              <div className="panel-header text-xs uppercase tracking-wider text-slate-400">
                {groupName} ({groupLinks.length})
              </div>
              <div className="p-2 space-y-1">
                {groupLinks.map((link: any) => {
                  const isSource = link.source_object_id === id
                  const linkedObjName = isSource ? link.target_name : link.source_name
                  const linkedObjId = isSource ? link.target_object_id : link.source_object_id
                  const linkedTypeName = isSource ? link.target_type_name : link.source_type_name

                  return (
                    <button
                      key={link.id}
                      onClick={() => navigate(`/objects/${linkedObjId}`)}
                      className="w-full flex items-center gap-2 p-2 rounded-md hover:bg-slate-800 text-left text-sm"
                    >
                      <ExternalLink size={12} className="text-slate-500 flex-shrink-0" />
                      <div className="min-w-0">
                        <div className="text-slate-200 truncate font-medium">
                          {linkedObjName}
                        </div>
                        <div className="text-xs text-slate-500">{linkedTypeName}</div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
