function openDB(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('miau-offline-client', 1)
    req.onupgradeneeded = () => {
      const db = req.result
      if (!db.objectStoreNames.contains('commandQueue')) {
        db.createObjectStore('commandQueue', { keyPath: 'id', autoIncrement: true })
      }
    }
    req.onsuccess = () => resolve(req.result)
    req.onerror = () => reject(req.error)
  })
}

export async function queueCommand(command: string, args: any) {
  const db = await openDB()
  const tx = db.transaction('commandQueue', 'readwrite')
  tx.objectStore('commandQueue').add({ command, args, timestamp: Date.now() })
  await new Promise<void>((resolve, reject) => {
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

export async function getQueuedCommands(): Promise<any[]> {
  const db = await openDB()
  return new Promise((resolve, reject) => {
    const tx = db.transaction('commandQueue', 'readonly')
    const all = tx.objectStore('commandQueue').getAll()
    tx.oncomplete = () => resolve(all.result || [])
    tx.onerror = () => reject(tx.error)
  })
}

export async function clearCommandQueue() {
  const db = await openDB()
  const tx = db.transaction('commandQueue', 'readwrite')
  tx.objectStore('commandQueue').clear()
  await new Promise<void>((resolve, reject) => {
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

export async function registerSync(tag: string) {
  if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
    try {
      const reg = await navigator.serviceWorker.ready
      await (reg as any).sync.register(tag)
    } catch {
      // Background sync not supported
    }
  }
}

export async function checkStorageQuota(): Promise<{ usage: number; quota: number; pct: number }> {
  if ('storage' in navigator && 'estimate' in navigator.storage) {
    const estimate = await navigator.storage.estimate()
    const usage = estimate.usage || 0
    const quota = estimate.quota || 0
    return { usage, quota, pct: quota > 0 ? (usage / quota) * 100 : 0 }
  }
  return { usage: 0, quota: 0, pct: 0 }
}
