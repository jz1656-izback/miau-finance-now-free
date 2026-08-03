// market.ts — Market data command handlers
import { AddLine, authFetch, safeJson, fmt, pct } from './shared'

type Handler = (args: string[], addLine: AddLine) => Promise<void>

export const marketHandlers: Record<string, Handler> = {
  price: async (args, addLine) => {
    const ticker = args[0]?.toUpperCase()
    if (!ticker) { addLine({ text: 'Usage: price <ticker>', className: 'text-yellow' }); return }
    addLine({ text: `🔍 fetching ${ticker}...`, className: 'text-dim' })
    const res = await authFetch(`/api/v1/market/live?tickers=${ticker}`)
    const data = await safeJson(res, addLine)
    if (!data) return
    const d = data.data?.[ticker] || data?.[ticker]
    if (!d) { addLine({ text: `No data for ${ticker}`, className: 'text-red' }); return }
    const cat = (d.change_pct ?? 0) >= 0 ? '😸' : '😿'
    const src = data.source === 'chonk' ? '📦 chonk' : '🌐 live'
    addLine({
      text: `${cat} ${ticker}  ${d.name || ''}  ${src}
price:   ${fmt(d.price)}
change:  ${pct(d.change_pct)}
high:    ${fmt(d.high)}
low:     ${fmt(d.low)}
volume:  ${((d.volume ?? 0)).toLocaleString()}`,
      className: (d.change_pct ?? 0) >= 0 ? 'text-green' : 'text-red'
    })
  },
}
