import { useEffect, useState } from 'react'

export default function PushPermission() {
  const [show, setShow] = useState(false)

  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      setShow(true)
    }
  }, [])

  const request = async () => {
    const result = await Notification.requestPermission()
    if (result === 'granted') {
      setShow(false)
    }
  }

  if (!show) return null

  return (
    <div className="fixed bottom-36 right-4 z-[9999] glass-panel rounded-lg p-3 shadow-lg border border-green/30 max-w-xs">
      <div className="text-xs text-green font-semibold mb-1">Enable Notifications</div>
      <div className="text-xs text-dim mb-2">Get real-time alerts on price moves and trades.</div>
      <div className="flex gap-2">
        <button onClick={request} className="px-3 py-1 text-xs rounded border border-green text-green hover:bg-green/10 transition-colors">Enable</button>
        <button onClick={() => setShow(false)} className="px-3 py-1 text-xs rounded border border-[#1a3a2a] text-dim hover:text-green transition-colors">Later</button>
      </div>
    </div>
  )
}
