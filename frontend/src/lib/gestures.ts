const SWIPE_THRESHOLD = 50

interface SwipeHandlers {
  onSwipeLeft?: () => void
  onSwipeRight?: () => void
  onSwipeUp?: () => void
  onSwipeDown?: () => void
}

interface TouchState {
  startX: number
  startY: number
  startTime: number
}

export function createSwipeHandler(handlers: SwipeHandlers) {
  let state: TouchState | null = null

  return {
    onTouchStart(e: TouchEvent) {
      const t = e.touches[0]
      state = { startX: t.clientX, startY: t.clientY, startTime: Date.now() }
    },

    onTouchEnd(e: TouchEvent) {
      if (!state) return
      const t = e.changedTouches[0]
      const dx = t.clientX - state.startX
      const dy = t.clientY - state.startY
      const elapsed = Date.now() - state.startTime

      if (elapsed > 500) { state = null; return }

      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > SWIPE_THRESHOLD) {
        if (dx > 0) handlers.onSwipeRight?.()
        else handlers.onSwipeLeft?.()
      } else if (Math.abs(dy) > SWIPE_THRESHOLD) {
        if (dy > 0) handlers.onSwipeDown?.()
        else handlers.onSwipeUp?.()
      }
      state = null
    },
  }
}

export function isMobileDevice(): boolean {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

export function preventZoomOnInput(node: HTMLInputElement) {
  node.style.fontSize = '16px'
}

export function createPinchZoomHandler(onZoom: (scale: number, centerX: number, centerY: number) => void) {
  let initialDist = 0

  return {
    onTouchStart(e: TouchEvent) {
      if (e.touches.length === 2) {
        const dx = e.touches[0].clientX - e.touches[1].clientX
        const dy = e.touches[0].clientY - e.touches[1].clientY
        initialDist = Math.sqrt(dx * dx + dy * dy)
      }
    },
    onTouchMove(e: TouchEvent) {
      if (e.touches.length === 2) {
        e.preventDefault()
        const dx = e.touches[0].clientX - e.touches[1].clientX
        const dy = e.touches[0].clientY - e.touches[1].clientY
        const dist = Math.sqrt(dx * dx + dy * dy)
        const scale = initialDist > 0 ? dist / initialDist : 1
        const cx = (e.touches[0].clientX + e.touches[1].clientX) / 2
        const cy = (e.touches[0].clientY + e.touches[1].clientY) / 2
        onZoom(scale, cx, cy)
      }
    },
    onTouchEnd() {
      initialDist = 0
    },
  }
}

export function createTapHandler(onTap: (x: number, y: number) => void, onDoubleTap?: () => void) {
  let lastTap = 0
  let tapX = 0
  let tapY = 0

  return {
    onTouchStart(_e: TouchEvent) {},
    onTouchEnd(e: TouchEvent) {
      const now = Date.now()
      const t = e.changedTouches[0]
      const elapsed = now - lastTap
      if (elapsed < 300 && Math.abs(t.clientX - tapX) < 30 && Math.abs(t.clientY - tapY) < 30) {
        onDoubleTap?.()
        lastTap = 0
      } else {
        onTap(t.clientX, t.clientY)
        tapX = t.clientX
        tapY = t.clientY
        lastTap = now
      }
    },
  }
}

