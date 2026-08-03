const TOKEN_KEY = 'miau_token'
const REFRESH_KEY = 'miau_refresh_token'
const USER_KEY = 'miau_user'
const API_BASE = '/api/v1'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}

export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_KEY, token)
}

// 🔐 pawdentity: display metadata for the session (username/role). The REAL
// session lives in the HttpOnly `pawd_session` cookie — this key is cosmetic
// only and is always cleared together with the token on logout/401.
export function getUser(): { username?: string; role?: string } | null {
  try {
    const raw = localStorage.getItem(USER_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    return typeof parsed === 'object' && parsed !== null ? parsed : null
  } catch {
    return null
  }
}

export function setUser(user: { username: string; role?: string }): void {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify({ username: user.username, role: user.role || 'user' }))
  } catch {}
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_KEY)
  localStorage.removeItem(USER_KEY)
}

export function isAuthenticated(): boolean {
  return !!getToken() || !!getUser()
}

export function getUserRole(): string {
  const user = getUser()
  if (user?.role) return user.role
  try {
    const token = getToken()
    if (!token) return 'readonly'
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.role || 'readonly'
  } catch {
    return 'readonly'
  }
}

export function hasRole(...roles: string[]): boolean {
  const userRole = getUserRole()
  const hierarchy: Record<string, string[]> = {
    admin: ['admin', 'user', 'readonly'],
    user: ['user', 'readonly'],
    readonly: ['readonly'],
  }
  const allowed = hierarchy[userRole] || ['readonly']
  return roles.some(r => allowed.includes(r))
}

export function authHeaders(extra?: Record<string, string>): Record<string, string> {
  const headers: Record<string, string> = {}
  const token = getToken()
  if (token) headers['Authorization'] = `Bearer ${token}`
  if (extra) Object.assign(headers, extra)
  return headers
}

export interface PawdentityLoginResult {
  authenticated?: boolean
  username?: string
  role?: string
  expires_in?: number
  access_token?: string
  refresh_token?: string
  detail?: string
}

// 🔐 pawdentity login — the password is sent only in the request body, never
// echoed or stored. The real session is an HttpOnly cookie; `miau_user` and
// `miau_token` are kept purely for display + SDK/header compatibility.
export async function login(username: string, password: string): Promise<PawdentityLoginResult> {
  const res = await fetch(`${API_BASE}/pawdentity/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  })
  const data: PawdentityLoginResult = await res.json().catch(() => ({}))
  if (!res.ok) {
    const detail = (data && typeof data.detail === 'string' && data.detail) || `Login failed (HTTP ${res.status})`
    throw new Error(detail)
  }
  if (data.authenticated === false) {
    const detail = (data && typeof data.detail === 'string' && data.detail) || 'Login failed'
    throw new Error(detail)
  }
  setUser({ username: data.username || username, role: data.role })
  if (data.access_token) setToken(data.access_token)
  if (data.refresh_token) setRefreshToken(data.refresh_token)
  return data
}

export async function getSession(): Promise<{ authenticated: boolean; username?: string; role?: string }> {
  try {
    const res = await fetch(`${API_BASE}/pawdentity/session`, {
      method: 'GET',
      credentials: 'include',
    })
    if (!res.ok) return { authenticated: false }
    const data = await res.json()
    return {
      authenticated: !!data.authenticated,
      username: data.username,
      role: data.role,
    }
  } catch {
    return { authenticated: false }
  }
}

export async function logout(): Promise<{ authenticated: boolean }> {
  try {
    await fetch(`${API_BASE}/pawdentity/logout`, {
      method: 'POST',
      credentials: 'include',
    })
  } catch {
    // best-effort — always clear the local session state
  }
  clearToken()
  return { authenticated: false }
}

export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = getRefreshToken()
  if (!refreshToken) {
    clearToken()
    return null
  }
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ refresh_token: refreshToken }),
    })
    if (!res.ok) {
      clearToken()
      return null
    }
    const data = await res.json()
    setToken(data.access_token)
    if (data.refresh_token) setRefreshToken(data.refresh_token)
    return data.access_token
  } catch {
    clearToken()
    return null
  }
}

export async function authFetch(url: string, init?: RequestInit): Promise<Response> {
  const headers = authHeaders(init?.headers as Record<string, string> | undefined)
  const res = await fetch(`${API_BASE}${url}`, { ...init, headers, credentials: 'include' })

  if (res.status === 401) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      const retryHeaders = authHeaders(init?.headers as Record<string, string> | undefined)
      return fetch(`${API_BASE}${url}`, { ...init, headers: retryHeaders, credentials: 'include' })
    }
    clearToken()
  }
  return res
}
