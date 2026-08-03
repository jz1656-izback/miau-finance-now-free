import { useState, useEffect } from 'react'

export default function PwaUpdate() {
  const [waitingWorker, setWaitingWorker] = useState<ServiceWorker | null>(null)
  const [show, setShow] = useState(false)

  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').then((reg) => {
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

  const update = () => {
    if (waitingWorker) {
      waitingWorker.postMessage({ type: 'SKIP_WAITING' })
      window.location.reload()
    }
  }

  const dismiss = () => setShow(false)

  if (!show) return null

  return (
    <div className="fixed bottom-4 right-4 z-[9999] glass-panel rounded-lg p-3 shadow-lg border border-green/30 max-w-xs">
      <div className="text-xs text-green font-semibold mb-1">Update Available</div>
      <div className="text-xs text-dim mb-2">A new version of Miau Finance is ready.</div>
      <div className="flex gap-2">
        <button
          onClick={update}
          className="px-3 py-1 text-xs rounded border border-green text-green hover:bg-green/10 transition-colors"
        >
          Update
        </button>
        <button
          onClick={dismiss}
          className="px-3 py-1 text-xs rounded border border-[#1a3a2a] text-dim hover:text-green hover:border-green/30 transition-colors"
        >
          Later
        </button>
      </div>
    </div>
  )
}
