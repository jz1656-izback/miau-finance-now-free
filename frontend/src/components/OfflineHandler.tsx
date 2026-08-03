import { useState, useEffect, ReactNode } from 'react'

interface Props {
  children: ReactNode
}

export default function OfflineHandler({ children }: Props) {
  const [online, setOnline] = useState(navigator.onLine)

  useEffect(() => {
    const go = () => setOnline(true)
    const gone = () => setOnline(false)
    window.addEventListener('online', go)
    window.addEventListener('offline', gone)
    return () => {
      window.removeEventListener('online', go)
      window.removeEventListener('offline', gone)
    }
  }, [])

  return (
    <>
      {!online && (
        <div
          className="fixed top-0 left-0 right-0 z-[9999] text-center py-1 text-xs font-mono"
          style={{ background: '#ff4444', color: '#fff' }}
        >
          📡 offline — some features unavailable
        </div>
      )}
      {children}
    </>
  )
}