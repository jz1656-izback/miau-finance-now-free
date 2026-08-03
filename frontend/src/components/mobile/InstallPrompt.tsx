import { useState, useEffect } from 'react'

export default function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null)
  const [show, setShow] = useState(false)

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e)
      setShow(true)
    }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  const onInstall = async () => {
    if (!deferredPrompt) return
    deferredPrompt.prompt()
    const result = await deferredPrompt.userChoice
    if (result.outcome === 'accepted') {
      localStorage.setItem('miau:installed', 'true')
    }
    setDeferredPrompt(null)
    setShow(false)
  }

  if (!show) return null

  return (
    <div className="fixed bottom-20 left-4 right-4 md:left-auto md:right-4 md:w-80 bg-[#0a1a14] border border-green-700/50 rounded-lg p-4 shadow-xl z-50">
      <div className="flex items-start gap-3">
        <span className="text-2xl">🐱</span>
        <div className="flex-1">
          <div className="text-green-400 font-mono text-sm font-bold">Install Miau Finance</div>
          <div className="text-green-600 font-mono text-xs mt-1">Add to your home screen for the best cat-trading experience.</div>
        </div>
      </div>
      <div className="flex gap-2 mt-3 justify-end">
        <button onClick={() => setShow(false)} className="px-3 py-1.5 text-green-600 font-mono text-xs hover:text-green-400 transition-colors">Later</button>
        <button onClick={onInstall} className="px-3 py-1.5 bg-green-700 text-green-200 font-mono text-xs rounded hover:bg-green-600 transition-colors">Install</button>
      </div>
    </div>
  )
}
