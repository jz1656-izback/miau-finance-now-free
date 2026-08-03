import { authHeaders, clearToken, getToken } from '../auth'
// import { getLogger } from '../logger'
// const log = getLogger('commands')

export type AddLine = (line: { text: string; html?: boolean; className?: string }) => void

export function escapeHtml(s: string): string {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;')
}

// 🔐 pawdentity: `miau_user` is stored as JSON {username, role}. Resolve the
// plain username for display (falling back to legacy plain-string values).
export function miauUsername(): string {
  const raw = localStorage.getItem('miau_user')
  if (!raw) return 'trader'
  try {
    const parsed = JSON.parse(raw)
    if (parsed && typeof parsed === 'object' && typeof parsed.username === 'string') return parsed.username
  } catch {}
  return raw
}

export async function authFetch(url: string, init?: RequestInit): Promise<Response> {
  const headers = authHeaders(init?.headers as Record<string, string> | undefined)
  const method = (init?.method || 'GET').toUpperCase()
  if (method !== 'GET' && method !== 'HEAD' && method !== 'OPTIONS') {
    const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]*)/)
    if (match) {
      headers['X-CSRF-Token'] = decodeURIComponent(match[1])
    }
  }
  const res = await fetch(url, { ...init, headers, credentials: 'include' })
  if (res.status === 401) {
    clearToken()
  }
  return res
}

export const CAT_ERROR: Record<number, string> = {
  400: '😾 bad request — the cat disapproves',
  401: '🐱 not authenticated — type: login <username>',
  403: '😿 forbidden — the cat says no',
  404: '😹 not found — the cat hid it',
  409: '🙀 conflict — even the cat is confused',
  422: '😼 invalid input — the cat judges you',
  429: '🐈 rate limited — the cat needs a nap',
  500: '💀 server error — the cat broke it',
}

export async function safeJson(res: Response, addLine: AddLine): Promise<any | null> {
  if (res.status === 401) {
    if (!getToken()) {
      addLine({ text: CAT_ERROR[401] || '🔒 not authenticated', className: 'text-red' })
    }
    return null
  }
  if (!res.ok) {
    const err = await res.text().catch(() => 'unknown error')
    const catMsg = CAT_ERROR[res.status]
    const prefix = catMsg ? `${catMsg}` : `❌ API error ${res.status}`
    addLine({ text: `${prefix}: ${err.slice(0, 200)}`, className: 'text-red' })
    return null
  }
  return res.json()
}

export function fmt(n: number | null | undefined, decimals = 2): string {
  if (n == null) return '-'
  if (Math.abs(n) >= 1_000_000_000) return `$${(n / 1_000_000_000).toFixed(2)}B`
  if (Math.abs(n) >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
  if (Math.abs(n) >= 1_000) return `$${(n / 1_000).toFixed(1)}K`
  return `$${n.toFixed(decimals)}`
}

export function pct(n: number | null | undefined): string {
  if (n == null) return '-'
  const s = n >= 0 ? '+' : ''
  return `${s}${n.toFixed(2)}%`
}

export function table(headers: string[], rows: string[][]): string {
  const colW = headers.map((h, i) =>
    Math.max(h.length, ...rows.map(r => (r[i] || '').length))
  )
  const sep = '─'.repeat(colW.reduce((a, b) => a + b + 3, 0))
  let out = ''
  out += headers.map((h, i) => h.padEnd(colW[i])).join(' ─ ') + '\n'
  out += sep + '\n'
  for (const row of rows) {
    out += row.map((v, i) => (v || '').padEnd(colW[i])).join('   ') + '\n'
  }
  return out
}

export const SPARKLINE_CHARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

export function sparkline(data: number[], width: number = 10): string {
  if (!data.length) return ''
  const step = Math.max(1, Math.floor(data.length / width))
  const sampled: number[] = []
  for (let i = 0; i < data.length; i += step) sampled.push(data[i])
  if (sampled.length < 2) return '~'.repeat(width)
  const min = Math.min(...sampled)
  const max = Math.max(...sampled)
  const range = max - min || 1
  return sampled.map(v => SPARKLINE_CHARS[Math.min(7, Math.floor(((v - min) / range) * 7))]).join('')
}