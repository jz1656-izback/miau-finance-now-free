import { useState, useRef, useCallback } from 'react'

const PULL_THRESHOLD = 80
const MAX_PULL = 150

interface PullRefreshProps {
  onRefresh: () => Promise<void>
  children: React.ReactNode
}

export default function MobilePullRefresh({ onRefresh, children }: PullRefreshProps) {
  const [pulling, setPulling] = useState(false)
  const [pullDist, setPullDist] = useState(0)
  const [refreshing, setRefreshing] = useState(false)
  const startY = useRef(0)

  const onTouchStart = useCallback((e: React.TouchEvent) => {
    if (window.scrollY <= 0 && e.touches[0]) {
      startY.current = e.touches[0].clientY
      setPulling(true)
    }
  }, [])

  const onTouchMove = useCallback((e: React.TouchEvent) => {
    if (!pulling || refreshing) return
    const dist = Math.min(e.touches[0].clientY - startY.current, MAX_PULL)
    if (dist > 0) setPullDist(dist)
  }, [pulling, refreshing])

  const onTouchEnd = useCallback(async () => {
    if (!pulling) return
    setPulling(false)
    if (pullDist >= PULL_THRESHOLD && !refreshing) {
      setRefreshing(true)
      try { await onRefresh() }
      finally { setRefreshing(false) }
    }
    setPullDist(0)
  }, [pulling, pullDist, refreshing, onRefresh])

  return (
    <div onTouchStart={onTouchStart} onTouchMove={onTouchMove} onTouchEnd={onTouchEnd}>
      {pulling && pullDist > 0 && (
        <div
          className="flex items-center justify-center text-green-400 text-sm font-mono transition-opacity"
          style={{
            height: Math.min(pullDist, PULL_THRESHOLD),
            opacity: Math.min(pullDist / PULL_THRESHOLD, 1),
          }}
        >
          {refreshing ? '🐱 refreshing...' : pullDist >= PULL_THRESHOLD ? '🐱 release to refresh' : '🐱 pull to refresh'}
        </div>
      )}
      {refreshing && (
        <div className="flex items-center justify-center py-2 text-green-400 text-sm font-mono">
          🐱 refreshing...
        </div>
      )}
      {children}
    </div>
  )
}
