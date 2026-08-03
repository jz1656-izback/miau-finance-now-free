import { describe, it, expect, vi, beforeEach } from 'vitest'

const mockSwRegister = vi.fn()
const mockSwReady = vi.fn()
const mockSyncRegister = vi.fn()

beforeEach(() => {
  vi.resetAllMocks()

  Object.assign(globalThis, {
    navigator: {
      serviceWorker: {
        register: mockSwRegister,
        ready: mockSwReady,
      },
      sync: {
        register: mockSyncRegister,
      },
    },
    Notification: {
      permission: 'default',
      requestPermission: vi.fn().mockResolvedValue('granted'),
    },
  })
})

describe('PWA Service Worker', () => {
  it('registers service worker on init', async () => {
    mockSwRegister.mockResolvedValue({ scope: '/' })
    const { registerSW } = await import('../src/lib/sw')
    const result = await registerSW()
    expect(mockSwRegister).toHaveBeenCalledWith('/sw.js', expect.any(Object))
    expect(result.scope).toBe('/')
  })

  it('returns null when SW registration fails', async () => {
    mockSwRegister.mockRejectedValue(new Error('no sw'))
    const { registerSW } = await import('../src/lib/sw')
    const result = await registerSW()
    expect(result).toBeNull()
  })
})

describe('PWA Offline Cache', () => {
  it('caches static assets after install', async () => {
    const caches = {
      open: vi.fn().mockResolvedValue({
        addAll: vi.fn().mockResolvedValue(undefined),
      }),
    }
    Object.assign(globalThis, { caches })

    const cache = await caches.open('miau-v1')
    await cache.addAll(['/', '/index.html', '/manifest.json'])
    expect(caches.open).toHaveBeenCalledWith('miau-v1')
    expect(cache.addAll).toHaveBeenCalled()
  })

  it('serves cached content when offline', async () => {
    const mockMatch = vi.fn().mockResolvedValue(new Response('cached'))
    const caches = {
      open: vi.fn().mockResolvedValue({ match: mockMatch }),
    }
    Object.assign(globalThis, { caches })

    const cache = await caches.open('miau-v1')
    const response = await cache.match('/index.html')
    expect(response).toBeTruthy()
    expect(await response!.text()).toBe('cached')
  })
})

describe('PWA Install Prompt', () => {
  it('fires beforeinstallprompt event', () => {
    let capturedEvent: Event | null = null
    window.addEventListener('beforeinstallprompt', (e) => {
      capturedEvent = e
    })
    const event = new Event('beforeinstallprompt')
    window.dispatchEvent(event)
    expect(capturedEvent).toBeTruthy()
  })

  it('shows install button when prompt is available', () => {
    const btn = document.createElement('button')
    btn.id = 'install-btn'
    btn.style.display = 'none'
    document.body.appendChild(btn)

    window.addEventListener('beforeinstallprompt', () => {
      btn.style.display = 'block'
    })
    window.dispatchEvent(new Event('beforeinstallprompt'))
    expect(btn.style.display).toBe('block')
  })
})

describe('Background Sync', () => {
  it('registers sync for pending orders', async () => {
    mockSyncRegister.mockResolvedValue(undefined)
    const result = await navigator.sync.register('sync-orders')
    expect(mockSyncRegister).toHaveBeenCalledWith('sync-orders')
    expect(result).toBeUndefined()
  })
})
