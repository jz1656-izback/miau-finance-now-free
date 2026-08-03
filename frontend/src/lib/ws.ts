type WsCallback = (data: any) => void

let ws: WebSocket | null = null
let reconnectTimer: ReturnType<typeof setTimeout> | null = null
let listeners: Map<string, Set<WsCallback>> = new Map()
let shouldReconnect = true

export function connectWs(url: string) {
  if (ws && ws.readyState === WebSocket.OPEN) return

  ws = new WebSocket(url)

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      const type = msg.type || 'message'
      const cbs = listeners.get(type)
      if (cbs) cbs.forEach(cb => cb(msg.data || msg))
    } catch { /* ignore */ }
  }

  ws.onclose = () => {
    ws = null
    if (shouldReconnect) {
      reconnectTimer = setTimeout(() => connectWs(url), 3000)
    }
  }

  ws.onerror = () => {
    ws?.close()
  }
}

export function disconnectWs() {
  shouldReconnect = false
  if (reconnectTimer) clearTimeout(reconnectTimer)
  ws?.close()
  ws = null
}

export function subscribeWs(type: string, cb: WsCallback) {
  if (!listeners.has(type)) listeners.set(type, new Set())
  listeners.get(type)!.add(cb)
  return () => listeners.get(type)?.delete(cb)
}

export function sendWs(data: any) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(data))
  }
}
