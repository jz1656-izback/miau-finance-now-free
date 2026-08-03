import { useState, useEffect } from 'react'

export default function OfflineIndicator() {
  const [offline, setOffline] = useState(!navigator.onLine)

  useEffect(() => {
    const onOffline = () => setOffline(true)
    const onOnline = () => setOffline(false)
    window.addEventListener('offline', onOffline)
    window.addEventListener('online', onOnline)
    return () => {
      window.removeEventListener('offline', onOffline)
      window.removeEventListener('online', onOnline)
    }
  }, [])

  if (!offline) return null

  return (
    <div className="fixed top-0 left-0 right-0 bg-yellow-900/80 text-yellow-300 text-center py-1 text-xs font-mono z-50">
      🐱 Offline — some features may be unavailable
    </div>
  )
}
