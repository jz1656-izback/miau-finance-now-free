import { useState, useEffect } from 'react'

export default function PWAUpdateNotifier() {
  const [waitingWorker, setWaitingWorker] = useState<ServiceWorker | null>(null)
  const [show, setShow] = useState(false)

  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.ready.then(reg => {
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                setWaitingWorker(newWorker)
                setShow(true)
              }
            })
          }
        })
      }).catch(() => {})
    }
  }, [])

  const onUpdate = () => {
    if (waitingWorker) {
      waitingWorker.postMessage({ type: 'SKIP_WAITING' })
      window.location.reload()
    }
  }

  if (!show) return null

  return (
    <div className="fixed bottom-20 left-4 right-4 md:left-auto md:right-4 md:w-80 bg-[#0a1a14] border border-green-700/50 rounded-lg p-4 shadow-xl z-50">
      <div className="flex items-start gap-3">
        <span className="text-2xl">🐱</span>
        <div className="flex-1">
          <div className="text-green-400 font-mono text-sm font-bold">Update Available</div>
          <div className="text-green-600 font-mono text-xs mt-1">A new version of Miau Finance is ready. Refresh to get the latest.</div>
        </div>
      </div>
      <div className="flex gap-2 mt-3 justify-end">
        <button onClick={() => setShow(false)} className="px-3 py-1.5 text-green-600 font-mono text-xs hover:text-green-400 transition-colors">Dismiss</button>
        <button onClick={onUpdate} className="px-3 py-1.5 bg-green-700 text-green-200 font-mono text-xs rounded hover:bg-green-600 transition-colors">Refresh</button>
      </div>
    </div>
  )
}
