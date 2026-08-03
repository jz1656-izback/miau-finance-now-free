import { useEffect, useRef, useState, useCallback } from 'react'

const CAT_ART = ['  ╱|、', ' (˚ˎ 。7', '  |、˜〵', '  じしˍ,)ノ']

type Panel = 'wei' | 'n' | 'top' | 'read' | 'wcv' | 'wb' | 'im' | 'ecst' | 'weco' | 'acdr' |
  'gpo' | 'gip' | 'des' | 'cn' | 'mcn' | 'mgmt' | 'phdc' | 'anr' | 'em' | 'rv' | 'fa' |
  'cbq' | 'nrg' | 'hym' | 'ma' | 'fund' | 'emkt' | 'et' | 'irsm' |
  'yas' | 'ws' | 'back' | 'pdfq' | 'easy' | 'blp' | 'train' | 'docs' | 'print' | 'help'

const PANEL_LABELS: Record<string, string> = {
  wei:'World Equity Index', n:'News', top:'Top Headlines', read:'Most Read', wcv:'Currency Values',
  wb:'World Bonds', im:'Money Market', ecst:'Economy Stats', weco:'Eco Calendar', acdr:'Earnings',
  gpo:'Price Chart', gip:'Intraday', des:'Company', cn:'Company News', mcn:'Popular News',
  mgmt:'Management', phdc:'Holders', anr:'Analyst Ratings', em:'Earnings Matrix', rv:'Relative Value', fa:'Financial Analysis',
  cbq:'Country Overview', nrg:'Energy', hym:'High Yield', ma:'M&A', fund:'Funds', emkt:'Emerging Mkts', et:'E-Trading', irsm:'Rate Swaps',
  yas:'Yield Spread', ws:'Swap Rates', back:'Back', pdfq:'Quick Defaults', easy:'Tips', blp:'Launchpad', train:'Training', docs:'Docs', print:'Print', help:'Help',
}

export default function Catberg() {
  const [tickerBar, setTickerBar] = useState<any[]>([])
  const [panel, setPanel] = useState<Panel>('wei')
  const [panelData, setPanelData] = useState<any>(null)
  const [rightPanel, setRightPanel] = useState<'news' | 'chart'>('news')
  const [newsData, setNewsData] = useState<any>(null)
  const [catWalk, setCatWalk] = useState(false)
  const [catPhrase, setCatPhrase] = useState('🐱 The cat is watching.')
  const [time, setTime] = useState('')
  const [inputFn, setInputFn] = useState('')
  const [inputTicker, setInputTicker] = useState('')
  const containerRef = useRef<HTMLDivElement>(null)

  const authHeaders = useCallback((): Record<string, string> => {
    const token = localStorage.getItem('miau_token')
    return token ? { Authorization: `Bearer ${token}` } : {}
  }, [])

  const fetchData = useCallback(async () => {
    try {
      const headers = authHeaders()
      const opts = { headers, credentials: 'include' as RequestCredentials }
      const [tickerRes, newsRes] = await Promise.allSettled([
        fetch('/api/v1/market/live?tickers=SPY,AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA,BTC', opts),
        fetch('/api/v1/catberg/n', opts),
      ])
      if (tickerRes.status === 'fulfilled' && tickerRes.value.ok) { const d = await tickerRes.value.json(); if (d?.data) setTickerBar(Object.values(d.data)) }
      if (newsRes.status === 'fulfilled' && newsRes.value.ok) { const d = await newsRes.value.json(); if (d?.data) setNewsData(d.data) }
    } catch {}
  }, [authHeaders])

  const fetchPanel = useCallback(async (p: string) => {
    try {
      const headers = authHeaders()
      const opts = { headers, credentials: 'include' as RequestCredentials }
      const ticker = p === 'cbq' ? inputTicker || 'US' : inputTicker
      const qs = ticker ? `?ticker=${ticker}` : ''
      const res = await fetch(`/api/v1/catberg/${p}${qs}`, opts)
      if (!res.ok) { setPanelData(null); return }
      const d = await res.json()
      if (d) setPanelData(d)
      if (d?.cat_commentary?.length) setCatPhrase(d.cat_commentary[0])
    } catch {}
  }, [authHeaders, inputTicker])

  useEffect(() => { fetchData(); fetchPanel('wei'); const t = setInterval(() => { fetchData(); setTime(new Date().toLocaleTimeString('de-DE', { hour:'2-digit', minute:'2-digit' })) }, 30000); return () => clearInterval(t) }, [fetchData, fetchPanel])

  const switchPanel = useCallback((p: Panel) => { setPanel(p); fetchPanel(p) }, [fetchPanel])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { switchPanel('wei'); return }
      if (e.key === 'Enter' && inputFn) { switchPanel(inputFn as Panel); setInputFn(''); return }
      if (e.key === 'Backspace' && inputFn) { setInputFn(prev => prev.slice(0, -1)); return }
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey && !(e.target as HTMLElement)?.closest('input,textarea,select')) {
        setInputFn(prev => prev + e.key.toUpperCase())
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [inputFn, switchPanel])

  useEffect(() => { const walk = setInterval(() => { if (Math.random() < 0.07) { setCatWalk(true); setTimeout(() => setCatWalk(false), 1200) } }, 8000); return () => clearInterval(walk) }, [])
  useEffect(() => { const phrase = setInterval(() => { const p = ['🐱 The cat is watching the ticker.','🐱 The cat predicts a bullish afternoon.','🐱 The cat saw this rally coming.','🐱 Treat jar status: half full.','🐱 The cat approves of this session.','🐱 Whisker analysis: BUY.']; setCatPhrase(p[Math.floor(Math.random()*p.length)]) }, 15000); return () => clearInterval(phrase) }, [])

  const panelLabel = PANEL_LABELS[panel] || '---'
  const score = panelData?.miau_score

  const renderGenericTable = (rows: any[], keyMap: string[], title?: string) => (
    <div className="space-y-1">
      {title && <div className="text-dim mb-1">{title}</div>}
      {rows.map((r: any, i: number) => (
        <div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5">
          {keyMap.map((k, j) => <span key={j} className={j === 0 ? 'text-dim' : k.includes('change') || k.includes('pct') ? (parseFloat(r[k]) >= 0 ? 'text-green' : 'text-red') : 'text-dim'}>{typeof r[k] === 'number' ? (k.includes('pct') || k.includes('change') ? (r[k] >= 0 ? '+' : '') + r[k].toFixed(2) + '%' : r[k].toFixed(2)) : r[k]}</span>)}
        </div>
      ))}
    </div>
  )

  return (
    <div ref={containerRef} className="h-full w-full flex flex-col bg-black text-green font-mono text-[11px] relative overflow-hidden" style={{ fontFamily: '"JetBrains Mono", "Fira Code", monospace' }}>
      {/* Ticker Bar */}
      <div className="flex items-center h-5 px-2 bg-[#0a0a0a] border-b border-green/10 overflow-hidden select-none" style={{ fontSize: '10px' }}>
        {tickerBar.slice(0, 8).map((t: any, i: number) => {
          const pct = t?.change_pct || 0
          return (<span key={i} className="flex items-center gap-1 mr-4 whitespace-nowrap"><span className="font-bold">{t?.ticker || t?.symbol || '---'}</span><span className={pct >= 0 ? 'text-green' : 'text-red'}>{typeof pct === 'number' ? `${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%` : '---'}</span><span>{pct >= 2 ? '🐱' : pct >= 0 ? '📈' : '😿'}</span></span>)
        })}
        <span className="ml-auto text-dim">{time}</span><span className="ml-4 text-yellow">🐟</span>
      </div>

      {/* Split Screen */}
      <div className="flex flex-1 overflow-hidden">
        {/* LEFT Panel */}
        <div className="w-[55%] border-r border-green/10 p-2 overflow-y-auto">
          <div className="font-bold text-green mb-2 flex justify-between">
            <span>CATBERG  {panel.toUpperCase()}  — {panelLabel}</span>
            <span className="text-dim text-[10px]">{score ? `🐱 ${score}/10` : ''}</span>
          </div>

          {/* ── Render ALL panel types ── */}
          {panel === 'wei' && panelData?.data && ['americas','europe','asia'].map(reg => {
            const items = panelData.data[reg]
            if (!items?.length) return null
            return (
              <div key={reg} className="mb-2">
                <div className="text-cyan mb-1 text-[10px]">
                  {reg === 'americas' ? '🐱 AMERICAS' : reg === 'europe' ? '🐱 EUROPE' : '🐱 ASIA PAC'}
                </div>
                {items.map((item: any, i: number) => (
                  <div key={i} className="flex justify-between ml-2">
                    <span className="text-dim">{item.name}</span>
                    <span className={item.change >= 0 ? 'text-green' : 'text-red'}>
                      {item.change >= 0 ? '▲' : '▼'} {Math.abs(item.change).toFixed(2)}% {item.cat || ''}
                    </span>
                  </div>
                ))}
              </div>
            )
          })}

          {panel === 'n' && panelData?.data?.headlines && panelData.data.headlines.map((h:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-1 mb-1"><div className="text-green text-[10px]">{h.headline}</div><div className="text-dim text-[8px]">{h.source} · {h.time}</div></div>))}

          {panel === 'top' && panelData?.data?.headlines && panelData.data.headlines.map((h:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-1 mb-1"><div className="text-green text-[10px]">🔥 {h.headline}</div><div className="text-dim text-[8px]">{h.source} · {h.time}</div></div>))}

          {panel === 'read' && panelData?.data?.stories && renderGenericTable(panelData.data.stories.map((s:any)=>({name:s.title,reads:s.reads})), ['name','reads'], 'Most Read Stories')}

          {panel === 'wcv' && panelData?.data?.currencies && renderGenericTable(panelData.data.currencies, ['pair','rate','change'], 'Major Currency Pairs vs USD')}

          {panel === 'wb' && panelData?.data?.bonds && renderGenericTable(panelData.data.bonds, ['name','yield','change'], 'Global Government Bonds')}

          {panel === 'im' && panelData?.data?.rates && renderGenericTable(panelData.data.rates, ['name','rate'], 'Treasury & Money Market Rates')}

          {panel === 'ecst' && panelData?.data?.indicators && panelData.data.indicators.map((i:any,j:number)=>(<div key={j} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-dim">{i.name}</span><span><span className="text-green">{i.value}</span><span className="text-dim ml-2">est: {i.forecast}</span></span></div>))}

          {panel === 'weco' && panelData?.data?.events && panelData.data.events.map((e:any,i:number)=>(<div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-dim">{e.date}</span><span className="text-green">{e.event}</span><span className="text-dim">{e.country}</span></div>))}

          {panel === 'acdr' && panelData?.data?.earnings && panelData.data.earnings.map((e:any,i:number)=>(<div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-dim">{e.date}</span><span className="text-green">{e.ticker}</span><span className="text-dim">${e.estimate} {e.when}</span></div>))}

          {panel === 'gpo' && panelData?.data && (<div><div className="text-cyan">{panelData.data.ticker} — OHLC</div><div className="text-dim">High: {panelData.data.high} | Low: {panelData.data.low}</div><div className="text-dim">Open: {panelData.data.open} | Close: {panelData.data.close}</div><div className="text-dim">Vol: {panelData.data.volume?.toLocaleString()}</div></div>)}

          {panel === 'gip' && panelData?.data && (<div><div className="text-cyan">{panelData.data.ticker} — {panelData.data.timeframe}</div><div className="text-green">${panelData.data.current} ({panelData.data.change >= 0 ? '+' : ''}{panelData.data.change}%)</div><div className="text-dim">Intraday: {panelData.data.intraday?.join(' → ')}</div></div>)}

          {panel === 'des' && panelData?.data && (<div className="space-y-1"><div className="text-cyan">{panelData.data.name} ({panelData.data.ticker})</div><div className="text-dim">Sector: {panelData.data.sector} | Industry: {panelData.data.industry}</div><div className="text-dim">Employees: {panelData.data.employees?.toLocaleString()} | Market Cap: {panelData.data.market_cap}</div><div className="text-dim mt-1">{panelData.data.description}</div></div>)}

          {panel === 'cn' && panelData?.data?.news && panelData.data.news.map((n:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-1 mb-1"><div className="text-green text-[10px]">{n.headline}</div><div className="text-dim text-[8px]">{n.source} · {n.time}</div></div>))}

          {panel === 'mcn' && panelData?.data?.news && <div><div className="text-dim mb-1">Most Popular — {panelData.data.ticker}</div>{panelData.data.news.map((n:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-1 mb-1"><div className="text-green text-[10px]">⭐ {n.headline}</div></div>))}</div>}

          {panel === 'mgmt' && panelData?.data?.executives && panelData.data.executives.map((e:any,i:number)=>(<div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-dim">{e.title}</span><span className="text-green">{e.name}</span><span className="text-dim">since {e.since}</span></div>))}

          {panel === 'phdc' && panelData?.data?.top_holders && (<div><div className="text-dim mb-1">Institutional: {panelData.data.institutional_pct}%</div>{panelData.data.top_holders.map((h:any,i:number)=>(<div key={i} className="flex justify-between text-[10px]"><span className="text-dim">{h.name}</span><span className="text-green">{h.pct}%</span></div>))}</div>)}

          {panel === 'anr' && panelData?.data?.analysts && renderGenericTable(panelData.data.analysts, ['firm','rating','target'], `Analyst Ratings — ${panelData.data.ticker}`)}

          {panel === 'em' && panelData?.data?.quarters && panelData.data.quarters.map((q:any,i:number)=>(<div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-dim">{q.q}</span><span className="text-dim">est: ${q.eps_est}</span><span className="text-green">act: ${q.eps_act}</span><span className={q.surprise.startsWith('+')?'text-green':'text-red'}>{q.surprise}</span></div>))}

          {panel === 'rv' && panelData?.data?.peers && renderGenericTable(panelData.data.peers, ['ticker','pe','ev_ebitda'], `Relative Value — ${panelData.data.ticker}`)}

          {panel === 'fa' && panelData?.data && (<div><div className="text-cyan">{panelData.data.ticker} Analysis</div><div className="text-dim">DCF: ${panelData.data.dcf_fair} | Current: ${panelData.data.current}</div><div className={panelData.data.upside >= 0 ? 'text-green' : 'text-red'}>Upside: {panelData.data.upside}% | Rec: {panelData.data.recommendation}</div><div className="text-dim">WACC: {panelData.data.wacc}% | P/E: {panelData.data.pe} | EV/EBITDA: {panelData.data.ev_ebitda}</div></div>)}

          {panel === 'cbq' && panelData?.data && (<div><div className="text-cyan">{panelData.data.country} Overview</div><div className="text-dim">GDP Growth: {panelData.data.gdp_growth}%</div><div className="text-dim">Inflation: {panelData.data.inflation}%</div><div className="text-dim">Unemployment: {panelData.data.unemployment}%</div><div className="text-dim">Central Bank Rate: {panelData.data.central_bank_rate}%</div></div>)}

          {panel === 'yas' && panelData?.data?.yields && renderGenericTable(panelData.data.yields, ['bond','ytm','spread'], 'Yield & Spread Analysis')}

          {panel === 'ws' && panelData?.data?.swaps && renderGenericTable(panelData.data.swaps, ['tenor','rate'], 'Swap Rates')}

          {panel === 'help' && panelData?.data?.shortcuts && panelData.data.shortcuts.map((s:any,i:number)=>(<div key={i} className="flex gap-3"><span className="text-green font-bold">{s.key}</span><span className="text-dim">{s.action}</span></div>))}

          {['nrg','hym','ma','fund','emkt','et','irsm'].includes(panel) && panelData?.data && (<div><div className="text-cyan">{panelData.data.sector}</div><div className="text-dim mt-1">{panelData.data.items?.[0]}</div></div>)}

          {panel === 'pdfq' && panelData?.data && (<div><div className="text-cyan">Quick Defaults</div>{panelData.data.watchlist && <div className="text-dim">Watchlist: {panelData.data.watchlist.join(', ')}</div>}<div className="text-dim">Theme: {panelData.data.theme} | Refresh: {panelData.data.refresh}s</div></div>)}

          {panel === 'easy' && panelData?.data?.tips && panelData.data.tips.map((t:string,i:number)=>(<div key={i} className="text-dim text-[10px] mb-0.5">• {t}</div>))}

          {panel === 'blp' && panelData?.data?.launchpad && (<div>{Object.entries(panelData.data.launchpad).map(([k,v])=>(<div key={k} className="text-[10px]"><span className="text-dim">{k}: </span><span className="text-green">{v as string}</span></div>))}</div>)}

          {panel === 'train' && panelData?.data?.materials && panelData.data.materials.map((m:any,i:number)=>(<div key={i} className="flex justify-between text-[10px] border-b border-green/5 pb-0.5"><span className="text-green">{m.title}</span><span className="text-dim">{m.lessons} lessons</span></div>))}

          {panel === 'docs' && panelData?.data?.docs && panelData.data.docs.map((d:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-0.5 mb-0.5"><a href={d.url} target="_blank" className="text-green text-[10px] hover:underline">{d.title}</a></div>))}

          {panel === 'print' && <div className="text-green text-[10px]">🐱 Printing. The cat does not approve of paper.</div>}

          {panel === 'back' && <div className="text-green text-[10px]">🐱 Type 'back' in terminal to return. The cat will miss you.</div>}

          <div className="mt-2 text-dim italic border-t border-green/5 pt-1 text-[9px]">{panelData?.cat_commentary?.[1] || panelData?.cat_commentary?.[0] || catPhrase}</div>
        </div>

        {/* RIGHT Panel */}
        <div className="flex-1 p-2 overflow-y-auto">
          <div className="flex gap-2 mb-2 text-[10px]">
            <button className={`px-2 py-0.5 rounded ${rightPanel==='news'?'bg-green/20 text-green':'text-dim'}`} onClick={()=>setRightPanel('news')}>📰 Cat News</button>
            <button className={`px-2 py-0.5 rounded ${rightPanel==='chart'?'bg-green/20 text-green':'text-dim'}`} onClick={()=>setRightPanel('chart')}>📊 Chart</button>
          </div>
          {rightPanel==='news' && (<div className="space-y-2"><div className="text-cyan text-[10px]">🐟 CAT NEWS DESK — The Cat, CFA</div>{(newsData?.headlines || [{headline:'🐟 The cat is monitoring global markets.','source':'The Cat, CFA','time':time},{headline:'🐟 Treat jar at 47%. Markets respond favorably.','source':'The Cat, CFA','time':time},{headline:'🐟 The cat predicts a bullish afternoon.','source':'The Cat, CFA','time':time}]).map((h:any,i:number)=>(<div key={i} className="border-b border-green/5 pb-1"><div className="text-green text-[10px]">{h.headline}</div><div className="text-dim text-[8px]">{h.source||'Miau News'} · {h.time||'---'}</div></div>))}</div>)}
          {rightPanel==='chart' && (<div className="space-y-2"><div className="text-cyan text-[10px]">📈 AAPL — Last 7 Days</div><div className="text-green text-lg tracking-wider mono">▁▂▃▄▅▆▇█▇▆</div><div className="text-dim text-[10px]">1D ▲1.2% | 5D ▲3.5% | 1M ▲8.2%</div><div className="text-dim text-[10px] mt-2">Cat Analysis: "The whiskers are twitching right. BUY."</div></div>)}
          <div className="mt-4 text-green/50 text-[10px] leading-none select-none">{CAT_ART.map((line,i)=><div key={i}>{line}</div>)}<div className="text-dim mt-1 text-[8px]">The Cat, CFA</div></div>
        </div>
      </div>

      {/* Footer — Function Input Bar */}
      <div className="flex items-center h-5 px-2 bg-[#0a0a0a] border-t border-green/10 text-[10px] select-none">
        <span className="text-green font-bold mr-2">FUNC:</span>
        <input className="bg-transparent border-none outline-none text-green font-mono text-[10px] w-20" value={inputFn} onChange={e => setInputFn(e.target.value.toUpperCase())} onKeyDown={e => { if (e.key === 'Enter' && inputFn) { switchPanel(inputFn as Panel); setInputFn('') } }} placeholder="e.g. WEI" spellCheck={false} />
        <span className="text-dim ml-2">Ticker:</span>
        <input className="bg-transparent border-none outline-none text-green font-mono text-[10px] w-16" value={inputTicker} onChange={e => setInputTicker(e.target.value.toUpperCase())} placeholder="e.g. AAPL" spellCheck={false} />
        <span className="ml-auto text-dim">{PANEL_LABELS[panel] || panel}</span>
        <span className="ml-4 text-yellow">🐟 treats</span>
      </div>

      {catWalk && <div className="absolute top-8 left-0 right-0 animate-pulse text-green text-center text-xl pointer-events-none select-none z-50">🐱 walking across... 🐾 🐾 🐾</div>}
    </div>
  )
}
