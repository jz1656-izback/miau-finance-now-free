function send(data: Record<string, any>) {
  try {
    const payload = { ...data, ts: Date.now(), url: window.location.href }
    navigator.sendBeacon?.('/api/v1/analytics/events', JSON.stringify(payload))
  } catch { /* beacon not supported */ }
}

export function trackPageView(path: string, referrer?: string) {
  send({ event: 'page_view', path, referrer })
}

export function trackEvent(category: string, action: string, label?: string, value?: number) {
  send({ event: 'custom', category, action, label, value })
}

export function trackTiming(category: string, variable: string, durationMs: number) {
  send({ event: 'timing', category, variable, duration_ms: durationMs })
}
