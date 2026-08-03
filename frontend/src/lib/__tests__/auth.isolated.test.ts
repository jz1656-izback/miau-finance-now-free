/**
 * ISOLATED Unit Test for auth.ts (pawdentity login)
 * Target: frontend/src/lib/auth.ts
 * Session: ses_login_pawdentity
 *
 * **WARNING**: THIS FILE WILL BE DELETED AFTER TEST PASSES
 * Test code preserved in: .opencode/unit-tests/
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

// Mock localStorage with a clean in-memory store
class MemoryStorage {
  private store = new Map<string, string>()
  getItem(k: string): string | null { return this.store.has(k) ? this.store.get(k)! : null }
  setItem(k: string, v: string): void { this.store.set(k, v) }
  removeItem(k: string): void { this.store.delete(k) }
  clear(): void { this.store.clear() }
  key(i: number): string | null { return Array.from(this.store.keys())[i] ?? null }
  get length(): number { return this.store.size }
}

let storage: MemoryStorage
const fetchMock = vi.fn()

beforeEach(() => {
  storage = new MemoryStorage()
  vi.stubGlobal('localStorage', storage)
  fetchMock.mockReset()
  vi.stubGlobal('fetch', fetchMock)
})

afterEach(() => {
  vi.unstubAllGlobals()
})

// Import AFTER globals are stubbed (module only touches localStorage inside functions)
import { login, getSession, logout, clearToken, isAuthenticated, getUser, setToken } from '../auth'

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('auth.ts — pawdentity login', () => {
  it('calls pawdentity/login with credentials:include and stores user metadata as JSON', async () => {
    fetchMock.mockResolvedValue(jsonResponse({
      authenticated: true, username: 'kitty', role: 'admin', expires_in: 3600, access_token: 'jwt-abc',
    }))

    const data = await login('kitty', 'secret-123')

    // The password is sent ONLY in the request body — never persisted
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('/api/v1/pawdentity/login')
    expect(init.method).toBe('POST')
    expect(init.credentials).toBe('include')
    expect(JSON.parse(init.body)).toEqual({ username: 'kitty', password: 'secret-123' })

    // miau_user is JSON display metadata
    const user = JSON.parse(storage.getItem('miau_user')!)
    expect(user).toEqual({ username: 'kitty', role: 'admin' })
    // access_token still stored for SDK/header compat
    expect(storage.getItem('miau_token')).toBe('jwt-abc')
    expect(data.authenticated).toBe(true)
  })

  it('never writes the password anywhere in localStorage', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ authenticated: true, username: 'kitty', role: 'user' }))
    await login('kitty', 'hunter2-secret')
    const allValues = Array.from(new Set([...Array(storage.length)].map((_, i) => storage.key(i)!).map(k => storage.getItem(k))))
    expect(allValues.some(v => v && v.includes('hunter2-secret'))).toBe(false)
  })

  it('throws Error(detail) on 401', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ authenticated: false, detail: 'Incorrect username or password' }, 401))
    await expect(login('kitty', 'wrong')).rejects.toThrow('Incorrect username or password')
    // failed login must NOT leave any session state
    expect(storage.getItem('miau_token')).toBeNull()
    expect(storage.getItem('miau_user')).toBeNull()
  })

  it('getSession returns authenticated payload from pawdentity/session', async () => {
    fetchMock.mockResolvedValue(jsonResponse({ authenticated: true, username: 'kitty', role: 'user' }))
    const s = await getSession()
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/pawdentity/session')
    expect(fetchMock.mock.calls[0][1].credentials).toBe('include')
    expect(s).toEqual({ authenticated: true, username: 'kitty', role: 'user' })
  })

  it('getSession returns {authenticated:false} on network error', async () => {
    fetchMock.mockRejectedValue(new TypeError('NetworkError'))
    const s = await getSession()
    expect(s).toEqual({ authenticated: false })
  })

  it('logout calls pawdentity/logout and clears local session state', async () => {
    setToken('jwt-abc')
    storage.setItem('miau_user', JSON.stringify({ username: 'kitty', role: 'admin' }))
    fetchMock.mockResolvedValue(jsonResponse({ authenticated: false }))

    const res = await logout()
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/pawdentity/logout')
    expect(fetchMock.mock.calls[0][1].credentials).toBe('include')
    expect(res).toEqual({ authenticated: false })
    expect(storage.getItem('miau_token')).toBeNull()
    expect(storage.getItem('miau_user')).toBeNull()
  })

  it('isAuthenticated is true when miau_user exists even without a token', () => {
    expect(isAuthenticated()).toBe(false)
    storage.setItem('miau_user', JSON.stringify({ username: 'kitty', role: 'user' }))
    expect(isAuthenticated()).toBe(true)
  })

  it('clearToken removes token and user metadata', () => {
    setToken('jwt-abc')
    storage.setItem('miau_user', JSON.stringify({ username: 'kitty' }))
    clearToken()
    expect(getUser()).toBeNull()
    expect(isAuthenticated()).toBe(false)
  })
})
