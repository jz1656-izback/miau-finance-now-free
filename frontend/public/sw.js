const CACHE_NAME = 'miau-finance-v3'
const API_CACHE = 'miau-api-v3'
const STATIC_CACHE = 'miau-static-v3'
const COMMANDS_CACHE = 'miau-commands-v3'

const APP_SHELL = [
  '/',
  '/index.html',
  '/manifest.json',
  '/offline.html',
]

const API_CACHE_REGEX = /^\/api\//
const COMMANDS_CACHE_REGEX = /^\/api\/v1\/commands\//

async function createOfflinePage() {
  const cache = await caches.open(CACHE_NAME)
  const offlineHtml = '<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Miau Finance — Offline</title><style>body{background:#05080a;color:#00ff88;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}.offline-box{padding:2rem}.cat{font-size:2rem;margin-bottom:1rem}h1{font-size:1.2rem;margin-bottom:0.5rem}p{color:#4a5568;font-size:0.9rem}</style></head><body><div class="offline-box"><div class="cat">🐱</div><h1>You\'re offline</h1><p>Commands typed while offline will sync when you\'re back.</p></div></body></html>'
  await cache.put('/offline.html', new Response(offlineHtml, { headers: { 'Content-Type': 'text/html' } }))
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL).then(() => createOfflinePage()))
  )
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME && k !== API_CACHE && k !== STATIC_CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  if (request.method === 'GET') {
    if (COMMANDS_CACHE_REGEX.test(url.pathname)) {
      event.respondWith(networkFirst(request, COMMANDS_CACHE))
      return
    }
    if (API_CACHE_REGEX.test(url.pathname)) {
      event.respondWith(networkFirst(request, API_CACHE))
      return
    }
  }

  if (['style', 'script', 'font', 'image'].includes(request.destination)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE))
    return
  }

  if (request.destination === 'document') {
    event.respondWith(networkFirst(request, CACHE_NAME))
    return
  }

  event.respondWith(cacheFirst(request, CACHE_NAME))
})

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-orders') {
    event.waitUntil(syncOrders())
  }
  if (event.tag === 'sync-activity') {
    event.waitUntil(syncActivity())
  }
})

self.addEventListener('push', (event) => {
  if (!event.data) return
  try {
    const data = event.data.json()
    const title = data.title || '🐱 Miau Finance'
    const options = {
      body: data.body || '',
      icon: data.icon || '/favicon.ico',
      badge: data.badge || '/favicon.ico',
      tag: data.tag || 'miau-default',
      data: data.data || {},
      vibrate: data.vibrate || [200, 100, 200],
      requireInteraction: data.requireInteraction || false,
      actions: data.actions || [
        { action: 'open', title: 'Open Terminal' },
        { action: 'dismiss', title: 'Dismiss' },
      ],
    }
    event.waitUntil(self.registration.showNotification(title, options))
  } catch (e) {
    // Non-JSON push — show raw text
    event.waitUntil(
      self.registration.showNotification('🐱 Miau Finance', { body: event.data.text() })
    )
  }
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  if (event.action === 'dismiss') return
  const data = event.notification.data || {}
  const url = data.url || '/'
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          return client.focus()
        }
      }
      if (clients.openWindow) return clients.openWindow(url)
    })
  )
})

async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request)
  if (cached) return cached
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(cacheName)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    return cached || new Response('Offline', { status: 503 })
  }
}

async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(cacheName)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    const cached = await caches.match(request)
    if (cached) return cached
    return new Response(JSON.stringify({ error: 'offline', cached: false }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

async function syncOrders() {
  const db = await openDB()
  const pending = await db.getAll('pendingOrders')
  for (const order of pending) {
    try {
      const resp = await fetch('/api/v1/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(order),
      })
      if (resp.ok) {
        await db.delete('pendingOrders', order.id)
      }
    } catch {}
  }
}

async function syncActivity() {
  const db = await openDB()
  const pending = await db.getAll('pendingActivity')
  for (const activity of pending) {
    try {
      const resp = await fetch('/api/v1/social/activity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(activity),
      })
      if (resp.ok) {
        await db.delete('pendingActivity', activity.id)
      }
    } catch {}
  }
}

async function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('miau-offline', 1)
    req.onupgradeneeded = () => {
      const db = req.result
      if (!db.objectStoreNames.contains('pendingOrders')) db.createObjectStore('pendingOrders', { keyPath: 'id' })
      if (!db.objectStoreNames.contains('pendingActivity')) db.createObjectStore('pendingActivity', { keyPath: 'id' })
    }
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
}
