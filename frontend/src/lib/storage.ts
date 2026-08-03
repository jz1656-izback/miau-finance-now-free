export async function checkStorage(): Promise<{ usage: number; quota: number; pct: number }> {
  if ('storage' in navigator && 'estimate' in navigator.storage) {
    const est = await navigator.storage.estimate()
    const usage = est.usage || 0
    const quota = est.quota || 0
    return { usage, quota, pct: quota > 0 ? (usage / quota) * 100 : 0 }
  }
  return { usage: 0, quota: 0, pct: 0 }
}

export function isStorageLow(pct: number): boolean {
  return pct > 80
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1048576).toFixed(1)} MB`
}
