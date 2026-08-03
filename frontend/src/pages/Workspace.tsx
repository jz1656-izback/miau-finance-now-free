import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '../lib/api'
import {
  Workflow,
  BarChart3,
  Database,
  Play,
  History,
  ArrowRight,
} from 'lucide-react'

const WIDGETS = [
  {
    title: 'P&L Analysis',
    description: 'Run portfolio P&L calculations and attribution analysis',
    icon: BarChart3,
    color: 'text-emerald-400',
    bg: 'bg-emerald-900/20',
    action: 'Run Analysis',
  },
  {
    title: 'Data Pipeline',
    description: 'Ingest and transform financial data from connected sources',
    icon: Database,
    color: 'text-blue-400',
    bg: 'bg-blue-900/20',
    action: 'Configure',
  },
  {
    title: 'Risk Monitor',
    description: 'Real-time risk metrics and limit monitoring dashboards',
    icon: Workflow,
    color: 'text-purple-400',
    bg: 'bg-purple-900/20',
    action: 'View',
  },
]

export default function Workspace() {
  const navigate = useNavigate()

  const { data: instruments } = useQuery({
    queryKey: ['instruments'],
    queryFn: () => api.getInstruments(),
  })

  const { data: portfolios } = useQuery({
    queryKey: ['portfolios'],
    queryFn: api.getPortfolios,
  })

  const { data: trades } = useQuery({
    queryKey: ['trades'],
    queryFn: () => api.getTrades(),
  })

  const { data: pipelineRuns } = useQuery({
    queryKey: ['pipeline-runs'],
    queryFn: api.getPipelineRuns,
  })

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Workspace</h1>
        <p className="text-sm text-slate-500 mt-1">
          Financial data platform operations and analytics
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {WIDGETS.map((widget) => (
          <div key={widget.title} className="card">
            <div className="flex items-start gap-3 mb-3">
              <div className={`w-10 h-10 rounded-lg ${widget.bg} flex items-center justify-center`}>
                <widget.icon size={20} className={widget.color} />
              </div>
              <div>
                <h3 className="text-sm font-medium text-slate-200">{widget.title}</h3>
                <p className="text-xs text-slate-500 mt-1">{widget.description}</p>
              </div>
            </div>
            <button className="btn-primary w-full text-xs flex items-center justify-center gap-1.5">
              <Play size={12} /> {widget.action}
            </button>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="panel">
          <div className="panel-header">
            <Database size={14} />
            Data Sources Overview
          </div>
          <div className="p-4 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-slate-200">Instruments</div>
                <div className="text-xs text-slate-500">Financial instruments catalog</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold text-slate-100">
                  {instruments?.length || 0}
                </span>
                <button
                  onClick={() => navigate('/instruments')}
                  className="btn-ghost p-1"
                >
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-slate-200">Portfolios</div>
                <div className="text-xs text-slate-500">Investment portfolios</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold text-slate-100">
                  {portfolios?.length || 0}
                </span>
                <button
                  onClick={() => navigate('/portfolios')}
                  className="btn-ghost p-1"
                >
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-slate-200">Trades</div>
                <div className="text-xs text-slate-500">Executed transactions</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold text-slate-100">
                  {trades?.length || 0}
                </span>
                <button
                  onClick={() => navigate('/trades')}
                  className="btn-ghost p-1"
                >
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            <History size={14} />
            Pipeline Runs
          </div>
          <div className="p-4">
            {(pipelineRuns || []).length > 0 ? (
              <div className="space-y-2">
                {(pipelineRuns || []).slice(0, 10).map((run: any) => (
                  <div
                    key={run.id}
                    className="flex items-center justify-between py-2 border-b border-slate-800 last:border-0"
                  >
                    <div>
                      <div className="text-sm text-slate-200">{run.pipeline_name}</div>
                      <div className="text-xs text-slate-500">
                        {new Date(run.created_at).toLocaleString()}
                      </div>
                    </div>
                    <span className={`badge text-xs ${
                      run.status === 'completed' ? 'badge-green' :
                      run.status === 'running' ? 'badge-blue' :
                      run.status === 'failed' ? 'badge-red' : 'badge-yellow'
                    }`}>
                      {run.status}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-slate-500 py-8">
                <Play size={24} className="mx-auto mb-2 opacity-50" />
                <p className="text-sm">No pipeline runs yet</p>
                <p className="text-xs mt-1">Run calculations from the widgets above</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
