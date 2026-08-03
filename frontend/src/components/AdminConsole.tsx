import { useState, useEffect, useCallback } from 'react'
import { isAuthenticated } from '../lib/auth'

interface Team {
  id: string; name: string; description: string | null
  owner_id: string; owner_username?: string; created_at: string; members?: TeamMember[]
}
interface TeamMember { id: string; user_id: string; username: string; role: string }
interface Subscription { tier: string; status: string; current_period_end?: string }
interface UsageData { requests_today: number; requests_this_month: number; total_api_keys: number; active_webhooks: number }
interface HealthData { status: string; version: string; uptime_seconds: number; services: Record<string, boolean>; provider_health: Record<string, boolean>; data_providers?: number }
interface AuditEntry { id: string; user?: string; username?: string; action: string; resource: string; details?: string; message?: string; timestamp: string; created_at?: string }
interface LogFile { path?: string; name?: string; size_bytes: number; modified: string }

type Tab = 'members' | 'settings' | 'billing' | 'usage' | 'health' | 'logs' | 'audit'

const TIER_COLORS: Record<string, string> = { free: '#4a5568', pro: '#22d3ee', enterprise: '#a855f7' }

function fmtBytes(b: number) { if (b > 1e9) return `${(b / 1e9).toFixed(1)} GB`; if (b > 1e6) return `${(b / 1e6).toFixed(1)} MB`; return `${(b / 1024).toFixed(0)} KB` }
function fmtTime(s: number) { const h = Math.floor(s / 3600); const m = Math.floor((s % 3600) / 60); return `${h}h ${m}m` }
function randomId() { return Math.random().toString(36).slice(2, 9) }

export default function AdminConsole() {
  const [activeTab, setActiveTab] = useState<Tab>('health')
  const [teams, setTeams] = useState<Team[]>([])
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null)
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [usage, setUsage] = useState<UsageData | null>(null)
  const [health, setHealth] = useState<HealthData | null>(null)
  const [logs, setLogs] = useState<LogFile[]>([])
  const [auditLogs, setAuditLogs] = useState<AuditEntry[]>([])
  const [newMemberUsername, setNewMemberUsername] = useState('')
  const [teamName, setTeamName] = useState('')
  const [teamDesc, setTeamDesc] = useState('')
  const [loading, setLoading] = useState<Record<string, boolean>>({})
  const [toasts, setToasts] = useState<{ id: string; msg: string }[]>([])

  const toast = (msg: string) => {
    const id = randomId()
    setToasts(prev => [...prev, { id, msg }])
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000)
  }

  const withLoading = (key: string, fn: () => Promise<void>) => async () => {
    setLoading(prev => ({ ...prev, [key]: true }))
    try { await fn() } catch { /* ignore */ }
    finally { setLoading(prev => ({ ...prev, [key]: false })) }
  }

  const fetchTeams = useCallback(async () => {
    if (!isAuthenticated()) return
    const res = await fetch('/api/v1/teams')
    if (res.ok) { const d = await res.json(); setTeams(d.items || []) }
  }, [])

  const fetchTeam = useCallback(async (id: string) => {
    const res = await fetch(`/api/v1/teams/${id}`)
    if (res.ok) { const d = await res.json(); setSelectedTeam(d); setTeamName(d.name || ''); setTeamDesc(d.description || '') }
  }, [])

  const fetchSubscription = useCallback(async () => {
    if (!isAuthenticated()) return
    const res = await fetch('/api/v1/billing/subscription')
    if (res.ok) setSubscription(await res.json())
  }, [])

  const fetchUsage = useCallback(async () => {
    if (!isAuthenticated()) return
    const res = await fetch('/api/v1/developer/dashboard')
    if (res.ok) setUsage(await res.json())
  }, [])

  const fetchHealth = useCallback(async () => {
    const res = await fetch('/api/v1/health')
    if (res.ok) setHealth(await res.json())
  }, [])

  const fetchLogs = useCallback(async () => {
    if (!isAuthenticated()) return
    const res = await fetch('/api/v1/logs/files')
    if (res.ok) { const d = await res.json(); setLogs(d.files || d.log_files || []) }
  }, [])

  const fetchAudit = useCallback(async () => {
    if (!isAuthenticated()) return
    const res = await fetch('/api/v1/audit/logs?limit=20')
    if (res.ok) { const d = await res.json(); setAuditLogs(d.items || d.logs || d.entries || []) }
  }, [])

  useEffect(() => { fetchTeams(); fetchSubscription(); fetchUsage(); fetchHealth(); fetchLogs(); fetchAudit() }, [])
  useEffect(() => { if (teams.length === 1 && !selectedTeam) fetchTeam(teams[0].id) }, [teams])

  const handleAddMember = async () => {
    if (!selectedTeam || !newMemberUsername.trim()) return
    try {
      const res = await fetch(`/api/v1/users?username=${encodeURIComponent(newMemberUsername.trim())}`)
      const user = await res.json()
      if (!user.id) { toast('User not found'); return }
      const r2 = await fetch(`/api/v1/teams/${selectedTeam.id}/members?user_id=${user.id}&role=member`, { method: 'POST' })
      if (r2.ok) { toast('Member added'); setNewMemberUsername(''); fetchTeam(selectedTeam.id) }
      else toast('Failed to add member')
    } catch { toast('Failed to add member') }
  }

  const handleRemoveMember = async (userId: string) => {
    if (!selectedTeam) return
    try {
      const res = await fetch(`/api/v1/teams/${selectedTeam.id}/members/${userId}`, { method: 'DELETE' })
      if (res.ok) { toast('Member removed'); fetchTeam(selectedTeam.id) }
    } catch { toast('Failed to remove member') }
  }

  const handleUpdateTeam = async () => {
    if (!selectedTeam) return
    try {
      const res = await fetch(`/api/v1/teams/${selectedTeam.id}?name=${encodeURIComponent(teamName)}&description=${encodeURIComponent(teamDesc)}`, { method: 'PUT' })
      if (res.ok) { toast('Team updated'); fetchTeams() }
    } catch { toast('Failed to update team') }
  }

  const TABS: { key: Tab; label: string; icon: string }[] = [
    { key: 'health', label: 'Health', icon: '❤️' },
    { key: 'members', label: 'Members', icon: '👥' },
    { key: 'settings', label: 'Settings', icon: '⚙️' },
    { key: 'billing', label: 'Billing', icon: '💰' },
    { key: 'usage', label: 'API Usage', icon: '📊' },
    { key: 'logs', label: 'Logs', icon: '📋' },
    { key: 'audit', label: 'Audit', icon: '🔍' },
  ]

  const s = {
    card: (highlight = false): React.CSSProperties => ({
      padding: '12px 16px', background: highlight ? 'rgba(0,230,118,0.03)' : 'rgba(19,19,26,0.85)',
      borderRadius: 8, border: highlight ? '1px solid rgba(0,230,118,0.15)' : '1px solid rgba(42,42,64,0.4)',
    }),
    btn: (green = false, small = false): React.CSSProperties => ({
      padding: small ? '3px 8px' : '5px 12px', background: green ? 'rgba(0,230,118,0.12)' : 'transparent',
      border: `1px solid ${green ? 'rgba(0,230,118,0.3)' : 'rgba(42,42,64,0.4)'}`,
      borderRadius: 4, color: green ? '#00e676' : '#8899b0', cursor: 'pointer', fontSize: small ? 10 : 11,
      transition: 'all 0.15s',
    }),
    input: (): React.CSSProperties => ({
      background: 'rgba(0,0,0,0.3)', border: '1px solid rgba(42,42,64,0.5)',
      borderRadius: 4, padding: '5px 8px', color: '#e0e0e0', fontSize: 11,
      outline: 'none', fontFamily: 'monospace', width: '100%',
    }),
    label: (): React.CSSProperties => ({ fontSize: 10, color: '#8899b0', marginBottom: 4, display: 'block' }),
  }

  return (
    <div style={{ minHeight: '100vh', background: 'radial-gradient(ellipse at 50% 0%, #0d1a12 0%, #07090e 100%)', padding: 16, fontFamily: 'monospace', position: 'relative' }}>
      {/* Toasts */}
      <div style={{ position: 'fixed', top: 12, right: 12, zIndex: 10000, display: 'flex', flexDirection: 'column', gap: 4 }}>
        {toasts.map(t => (
          <div key={t.id} style={{
            padding: '6px 14px', background: 'rgba(0,230,118,0.12)', border: '1px solid rgba(0,230,118,0.25)',
            borderRadius: 6, color: '#00e676', fontSize: 11, animation: 'fadeIn 0.2s ease',
            backdropFilter: 'blur(8px)',
          }}>✓ {t.msg}</div>
        ))}
      </div>
      <style>{`@keyframes fadeIn { from { opacity:0; transform:translateY(-8px) } to { opacity:1; transform:translateY(0) } }`}</style>

      {/* Header */}
      <div style={{ maxWidth: 900, margin: '0 auto 12px', display: 'flex', alignItems: 'center', gap: 10 }}>
        <span style={{ fontSize: 22 }}>🛡️</span>
        <h1 style={{ fontSize: 16, fontWeight: 'bold', background: 'linear-gradient(135deg,#00e676,#22d3ee)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Admin Console</h1>
        <span style={{ fontSize: 10, color: '#4a5568' }}>system administration</span>
      </div>

      {/* Tabs */}
      <div style={{ maxWidth: 900, margin: '0 auto 12px', display: 'flex', gap: 2, borderBottom: '1px solid rgba(42,42,64,0.4)', overflowX: 'auto' }}>
        {TABS.map(t => (
          <button key={t.key} onClick={() => setActiveTab(t.key)} style={{
            padding: '6px 12px', border: 'none', cursor: 'pointer', fontSize: 10, whiteSpace: 'nowrap',
            borderRadius: '6px 6px 0 0', background: activeTab === t.key ? 'rgba(0,230,118,0.1)' : 'transparent',
            color: activeTab === t.key ? '#00e676' : '#4a5568',
            fontWeight: activeTab === t.key ? 600 : 400,
            borderBottom: activeTab === t.key ? '2px solid #00e676' : '2px solid transparent',
            transition: 'all 0.15s',
          }}>{t.icon} {t.label}</button>
        ))}
      </div>

      {/* Content */}
      <div style={{ maxWidth: 900, margin: '0 auto' }}>

        {/* ─── HEALTH ─── */}
        {activeTab === 'health' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>❤️ System Health</span>
              <button onClick={withLoading('health', fetchHealth)} style={s.btn(false, true)}>↻ Refresh</button>
              {loading.health && <span style={{ color: '#4a5568', fontSize: 10 }}>refreshing...</span>}
            </div>
            {health ? (
              <>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 8 }}>
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0' }}>Status</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: health.status === 'healthy' ? '#00e676' : '#ef4444', marginTop: 4 }}>
                      {health.status === 'healthy' ? '● Healthy' : '● Unhealthy'}
                    </div>
                    <div style={{ fontSize: 9, color: '#4a5568', marginTop: 2 }}>v{health.version || '—'}</div>
                  </div>
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0' }}>Uptime</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#22d3ee', marginTop: 4 }}>{fmtTime(health.uptime_seconds || 0)}</div>
                    <div style={{ fontSize: 9, color: '#4a5568', marginTop: 2 }}>{(health.uptime_seconds || 0).toLocaleString()} seconds</div>
                  </div>
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0' }}>Services</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#a855f7', marginTop: 4 }}>
                      {health.services ? Object.keys(health.services).length : '—'}
                    </div>
                    <div style={{ fontSize: 9, color: '#4a5568', marginTop: 2 }}>endpoints</div>
                  </div>
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0' }}>Data Providers</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#facc15', marginTop: 4 }}>{health.data_providers || '—'}</div>
                    <div style={{ fontSize: 9, color: '#4a5568', marginTop: 2 }}>registered</div>
                  </div>
                </div>
                {health.provider_health && Object.keys(health.provider_health).length > 0 && (
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0', marginBottom: 8 }}>📡 Provider Health</div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: 4 }}>
                      {Object.entries(health.provider_health).map(([name, ok]) => (
                        <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '3px 6px', background: 'rgba(0,0,0,0.2)', borderRadius: 4 }}>
                          <span style={{ width: 6, height: 6, borderRadius: '50%', background: ok ? '#00e676' : '#ef4444', flexShrink: 0 }} />
                          <span style={{ fontSize: 10, color: ok ? '#c0c0c0' : '#8899b0' }}>{name}</span>
                          <span style={{ fontSize: 8, color: '#4a5568', marginLeft: 'auto' }}>{ok ? 'up' : 'down'}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {health.services && Object.keys(health.services).length > 0 && (
                  <div style={s.card()}>
                    <div style={{ fontSize: 10, color: '#8899b0', marginBottom: 8 }}>⚙️ Service Status</div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                      {Object.entries(health.services).map(([name, ok]) => (
                        <span key={name} style={{
                          display: 'flex', alignItems: 'center', gap: 4, padding: '2px 8px', borderRadius: 10,
                          background: ok ? 'rgba(0,230,118,0.08)' : 'rgba(239,68,68,0.08)',
                          border: `1px solid ${ok ? 'rgba(0,230,118,0.2)' : 'rgba(239,68,68,0.2)'}`,
                          fontSize: 9, color: ok ? '#00e676' : '#ef4444',
                        }}>
                          <span style={{ width: 4, height: 4, borderRadius: '50%', background: ok ? '#00e676' : '#ef4444' }} />
                          {name}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div style={{ textAlign: 'center', padding: 40, color: '#4a5568', fontSize: 11 }}>
                {loading.health ? '⏳ loading...' : 'No health data available'}
              </div>
            )}
          </div>
        )}

        {/* ─── MEMBERS ─── */}
        {activeTab === 'members' && (
          <div>
            {teams.length === 0 ? (
              <div style={{ textAlign: 'center', padding: 40, color: '#4a5568', fontSize: 11 }}>
                <div style={{ fontSize: 24, marginBottom: 8 }}>👥</div>
                No teams found — create one: <code style={{ color: '#00e676' }}>team create &lt;name&gt;</code>
              </div>
            ) : (
              <>
                {teams.length > 1 && (
                  <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
                    {teams.map(t => (
                      <button key={t.id} onClick={() => fetchTeam(t.id)} style={{
                        ...s.btn(selectedTeam?.id === t.id),
                        background: selectedTeam?.id === t.id ? 'rgba(0,230,118,0.12)' : 'rgba(19,19,26,0.85)',
                        borderColor: selectedTeam?.id === t.id ? 'rgba(0,230,118,0.3)' : 'rgba(42,42,64,0.4)',
                      }}>{t.name}</button>
                    ))}
                  </div>
                )}
                {selectedTeam && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontSize: 11, color: '#8899b0' }}>Team:</span>
                      <span style={{ fontSize: 12, color: '#00e676', fontWeight: 600 }}>{selectedTeam.name}</span>
                      <span style={{ fontSize: 10, color: '#4a5568' }}>Owner: {selectedTeam.owner_username || '—'}</span>
                    </div>
                    <div style={{ display: 'flex', gap: 6 }}>
                      <input style={s.input()} placeholder="Username to invite..." value={newMemberUsername}
                        onChange={e => setNewMemberUsername(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleAddMember()} />
                      <button onClick={handleAddMember} style={s.btn(true)}>➕ Add</button>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                      {selectedTeam.members?.map(m => (
                        <div key={m.id} style={{ ...s.card(), padding: '8px 12px', display: 'flex', alignItems: 'center', gap: 8 }}>
                          <span style={{ fontSize: 14 }}>🐱</span>
                          <span style={{ fontSize: 11, color: '#e0e0e0', flex: 1 }}>{m.username}</span>
                          <span style={{
                            padding: '1px 6px', borderRadius: 8, fontSize: 9, fontWeight: 600,
                            background: m.role === 'admin' ? 'rgba(168,85,247,0.15)' : 'rgba(42,42,64,0.5)',
                            color: m.role === 'admin' ? '#a855f7' : '#8899b0',
                          }}>{m.role}</span>
                          <button onClick={() => handleRemoveMember(m.user_id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: '#ef4444', fontSize: 10, padding: '2px 4px' }}>✕</button>
                        </div>
                      ))}
                      {(!selectedTeam.members || selectedTeam.members.length === 0) && (
                        <div style={{ color: '#4a5568', fontSize: 10, padding: 8 }}>No members yet — invite someone above</div>
                      )}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* ─── SETTINGS ─── */}
        {activeTab === 'settings' && selectedTeam && (
          <div style={{ maxWidth: 500, display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div>
              <label style={s.label()}>Team Name</label>
              <input style={s.input()} value={teamName} onChange={e => setTeamName(e.target.value)} />
            </div>
            <div>
              <label style={s.label()}>Description</label>
              <textarea style={{ ...s.input(), resize: 'vertical', minHeight: 60 }} value={teamDesc} onChange={e => setTeamDesc(e.target.value)} />
            </div>
            <div>
              <button onClick={handleUpdateTeam} style={s.btn(true)}>💾 Save Changes</button>
            </div>
          </div>
        )}

        {/* ─── BILLING ─── */}
        {activeTab === 'billing' && (
          <div style={s.card()}>
            <div style={{ fontSize: 11, color: '#8899b0', marginBottom: 8 }}>💰 Subscription</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>Plan:</span>
              <span style={{ fontSize: 14, fontWeight: 'bold', color: TIER_COLORS[subscription?.tier || 'free'] || '#4a5568' }}>
                {(subscription?.tier || 'free').toUpperCase()}
              </span>
              <span style={{
                padding: '1px 8px', borderRadius: 8, fontSize: 9,
                background: subscription?.status === 'active' ? 'rgba(0,230,118,0.12)' : 'rgba(250,204,21,0.12)',
                color: subscription?.status === 'active' ? '#00e676' : '#facc15',
              }}>{subscription?.status || '—'}</span>
            </div>
            {subscription?.current_period_end && (
              <div style={{ fontSize: 10, color: '#4a5568', marginBottom: 10 }}>
                Period ends: {new Date(subscription.current_period_end).toLocaleDateString()}
              </div>
            )}
            <div style={{ display: 'flex', gap: 6 }}>
              <a href="/billing" style={s.btn(true)}>⚡ Manage Billing</a>
              <button onClick={withLoading('billing', fetchSubscription)} style={s.btn(false, true)}>↻</button>
            </div>
          </div>
        )}

        {/* ─── API USAGE ─── */}
        {activeTab === 'usage' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>📊 API Usage</span>
              <button onClick={withLoading('usage', fetchUsage)} style={s.btn(false, true)}>↻ Refresh</button>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))', gap: 8 }}>
              {[
                { label: 'Requests Today', value: (usage?.requests_today || 0).toLocaleString(), color: '#22d3ee', sub: 'requests' },
                { label: 'This Month', value: (usage?.requests_this_month || 0).toLocaleString(), color: '#00e676', sub: 'requests' },
                { label: 'API Keys', value: String(usage?.total_api_keys || 0), color: '#facc15', sub: 'active' },
                { label: 'Webhooks', value: String(usage?.active_webhooks || 0), color: '#a855f7', sub: 'active' },
              ].map(c => (
                <div key={c.label} style={s.card()}>
                  <div style={{ fontSize: 10, color: '#8899b0' }}>{c.label}</div>
                  <div style={{ fontSize: 22, fontWeight: 'bold', color: c.color, marginTop: 4 }}>{c.value}</div>
                  <div style={{ fontSize: 9, color: '#4a5568', marginTop: 2 }}>{c.sub}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ─── LOGS ─── */}
        {activeTab === 'logs' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>📋 Log Files</span>
              <button onClick={withLoading('logs', fetchLogs)} style={s.btn(false, true)}>↻ Refresh</button>
              {loading.logs && <span style={{ color: '#4a5568', fontSize: 10 }}>loading...</span>}
            </div>
            {logs.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                {logs.map((f, i) => (
                  <div key={i} style={{ ...s.card(), padding: '8px 12px', display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 14 }}>📄</span>
                    <span style={{ fontSize: 11, color: '#e0e0e0', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {f.path || f.name || `log-${i}`}
                    </span>
                    <span style={{ fontSize: 10, color: '#8899b0' }}>{fmtBytes(f.size_bytes || 0)}</span>
                    <span style={{ fontSize: 9, color: '#4a5568' }}>{f.modified?.slice(0, 10) || ''}</span>
                    <a href={`/logs-viewer`} style={{ ...s.btn(false, true), textDecoration: 'none', fontSize: 9 }}>View</a>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: 40, color: '#4a5568', fontSize: 11 }}>
                {loading.logs ? '⏳ loading...' : 'No log files available'}
              </div>
            )}
            <div style={{ fontSize: 9, color: '#4a5568', textAlign: 'center' }}>
              Full log viewer at <a href="/logs-viewer" style={{ color: '#00e676', textDecoration: 'none' }}>/logs-viewer</a>
            </div>
          </div>
        )}

        {/* ─── AUDIT ─── */}
        {activeTab === 'audit' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 11, color: '#8899b0' }}>🔍 Audit Logs</span>
              <button onClick={withLoading('audit', fetchAudit)} style={s.btn(false, true)}>↻ Refresh</button>
            </div>
            {auditLogs.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                {auditLogs.map((e, i) => (
                  <div key={e.id || i} style={{ ...s.card(), padding: '6px 10px', display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{ fontSize: 10, color: '#4a5568', width: 80, flexShrink: 0 }}>{e.timestamp?.slice(0, 16) || e.created_at?.slice(0, 16) || ''}</span>
                    <span style={{ fontSize: 10, color: '#22d3ee', fontWeight: 600, width: 60, flexShrink: 0 }}>{e.user || e.username || '—'}</span>
                    <span style={{
                      padding: '1px 5px', borderRadius: 4, fontSize: 9, fontWeight: 600, width: 60, textAlign: 'center', flexShrink: 0,
                      background: e.action?.includes('CREATE') ? 'rgba(0,230,118,0.12)' : e.action?.includes('DELETE') ? 'rgba(239,68,68,0.12)' : 'rgba(42,42,64,0.3)',
                      color: e.action?.includes('CREATE') ? '#00e676' : e.action?.includes('DELETE') ? '#ef4444' : '#8899b0',
                    }}>{e.action || '—'}</span>
                    <span style={{ fontSize: 10, color: '#8899b0', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {e.resource || e.details || e.message || ''}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: 40, color: '#4a5568', fontSize: 11 }}>No audit logs available</div>
            )}
          </div>
        )}

      </div>
    </div>
  )
}
