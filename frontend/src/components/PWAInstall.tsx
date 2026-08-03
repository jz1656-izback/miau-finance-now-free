import { useState } from 'react'

export default function PWAInstall() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null)
  const [show, setShow] = useState(false)

  useState(() => {
    const handler = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e)
      setShow(true)
    }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  })

  const install = () => {
    if (deferredPrompt) {
      deferredPrompt.prompt()
      deferredPrompt.userChoice.then(() => {
        setDeferredPrompt(null)
        setShow(false)
      })
    }
  }

  if (!show) return null

  return (
    <div className="fixed bottom-20 right-4 z-[9999] glass-panel rounded-lg p-3 shadow-lg border border-green/30 max-w-xs">
      <div className="text-xs text-green font-semibold mb-1">Install Miau Finance</div>
      <div className="text-xs text-dim mb-2">Add to your home screen for the best experience.</div>
      <div className="flex gap-2">
        <button onClick={install} className="px-3 py-1 text-xs rounded border border-green text-green hover:bg-green/10 transition-colors">Install</button>
        <button onClick={() => setShow(false)} className="px-3 py-1 text-xs rounded border border-[#1a3a2a] text-dim hover:text-green transition-colors">Not now</button>
      </div>
    </div>
  )
}
