const TOKEN_KEY = 'miau_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function authHeaders(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

// Read the HttpOnly-eligible CSRF token cookie (set by the backend CSRF middleware).
// Mirrors the pattern used by the main frontend (frontend/src/lib/api.ts).
export function getCSRFToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]*)/)
  return match ? decodeURIComponent(match[1]) : null
}

export async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const method = (options?.method || 'GET').toUpperCase()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...(options?.headers as Record<string, string> | undefined),
  }
  if (method !== 'GET' && method !== 'HEAD' && method !== 'OPTIONS') {
    const csrf = getCSRFToken()
    if (csrf) headers['X-CSRF-Token'] = csrf
  }
  const res = await fetch(url, {
    ...options,
    credentials: 'include',
    headers,
  })
  if (!res.ok) throw new Error(`API ${res.status}`)
  return res.json()
}

export async function apiFetchNoAuth<T>(url: string, options?: RequestInit): Promise<T> {
  const method = (options?.method || 'GET').toUpperCase()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string> | undefined),
  }
  if (method !== 'GET' && method !== 'HEAD' && method !== 'OPTIONS') {
    const csrf = getCSRFToken()
    if (csrf) headers['X-CSRF-Token'] = csrf
  }
  const res = await fetch(url, {
    ...options,
    credentials: 'include',
    headers,
  })
  if (!res.ok) throw new Error(`API ${res.status}`)
  return res.json()
}

export async function executeTerminalCommand(command: string, args?: string): Promise<{ output: string; status: string }> {
  try {
    const token = getToken()
    const headers: Record<string, string> = { 'Content-Type': 'application/json' }
    const csrf = getCSRFToken()
    if (csrf) headers['X-CSRF-Token'] = csrf
    const res = await fetch('/api/v1/education/terminal/execute', {
      method: 'POST',
      credentials: 'include',
      headers,
      body: JSON.stringify({ command, args: args || '', token: token || '' }),
    })
    if (!res.ok) return { output: `API error: ${res.status}`, status: 'error' }
    return await res.json()
  } catch {
    return { output: 'Backend unavailable. The cat is napping.', status: 'error' }
  }
}

// Pawdentity single sign-on: cookie-based session check shared across ALL apps.
// Same-origin via the vite `/api` proxy → host-only cookie on `localhost` = one login everywhere.
export async function getPawdentitySession(): Promise<{ authenticated: boolean; username?: string; role?: string }> {
  try {
    const res = await fetch('/api/v1/pawdentity/session', {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
    })
    if (!res.ok) return { authenticated: false }
    const data = await res.json()
    return {
      authenticated: !!data.authenticated,
      username: typeof data.username === 'string' ? data.username : undefined,
      role: typeof data.role === 'string' ? data.role : undefined,
    }
  } catch {
    return { authenticated: false }
  }
}
