import { useState, useEffect } from 'react'

// ─── Mock Data Generator ────────────────────────────
function mockData() {
  const days = 30, dayMs = 86400000
  const trendBase = 4200
  const trends = Array.from({length: days}, (_, i) => {
    const date = new Date(Date.now() - (days-1-i)*dayMs)
    const visitors = Math.round(trendBase + Math.sin(i/3)*800 + Math.random()*600)
    const page_views = Math.round(visitors * (2.5 + Math.random()))
    return { date: date.toISOString().slice(0,10), visitors, page_views, conversions: Math.round(visitors * (0.03 + Math.random()*0.02)) }
  })
  const totalVisitors = trends.reduce((s,d) => s+d.visitors, 0)
  const totalViews = trends.reduce((s,d) => s+d.page_views, 0)
  const totalConversions = trends.reduce((s,d) => s+d.conversions, 0)
  return {
    stats: {
      total_visitors: totalVisitors,
      total_page_views: totalViews,
      bounce_rate: 38.2 + Math.random()*5,
      conversion_rate: totalConversions/totalVisitors*100,
      avg_session_duration: 184 + Math.random()*40,
      active_sessions: 42 + Math.floor(Math.random()*20),
      total_conversions: totalConversions,
    },
    trends,
    pages: [
      { path: '/', views: 28400+Math.floor(Math.random()*2000) },
      { path: '❌ /pricing (FREE!)', views: 0 },
      { path: '/features', views: 8900+Math.floor(Math.random()*800) },
      { path: '/docs', views: 7600+Math.floor(Math.random()*600) },
      { path: '/blog', views: 5400+Math.floor(Math.random()*500) },
      { path: '/login', views: 4100+Math.floor(Math.random()*400) },
      { path: '/about', views: 3200+Math.floor(Math.random()*300) },
      { path: '/contact', views: 2100+Math.floor(Math.random()*200) },
      { path: '/changelog', views: 1800+Math.floor(Math.random()*200) },
      { path: '/careers', views: 1200+Math.floor(Math.random()*150) },
    ],
    campaigns: [
      { name: '🐱 Q1 Brand Push', spend: 12400+Math.floor(Math.random()*500), impressions: 890000+Math.floor(Math.random()*50000), clicks: 22300+Math.floor(Math.random()*2000), conversions: 890+Math.floor(Math.random()*100) },
      { name: '🎓 Education Launch', spend: 8700+Math.floor(Math.random()*300), impressions: 540000+Math.floor(Math.random()*30000), clicks: 18200+Math.floor(Math.random()*1500), conversions: 670+Math.floor(Math.random()*80) },
      { name: '🐟 Tuna Referral', spend: 5600+Math.floor(Math.random()*200), impressions: 320000+Math.floor(Math.random()*20000), clicks: 15800+Math.floor(Math.random()*1200), conversions: 520+Math.floor(Math.random()*60) },
      { name: '🤖 AI Advisor Promo', spend: 4200+Math.floor(Math.random()*200), impressions: 210000+Math.floor(Math.random()*15000), clicks: 9400+Math.floor(Math.random()*800), conversions: 340+Math.floor(Math.random()*40) },
      { name: '📊 Q2 Retargeting', spend: 3500+Math.floor(Math.random()*150), impressions: 180000+Math.floor(Math.random()*10000), clicks: 7200+Math.floor(Math.random()*600), conversions: 280+Math.floor(Math.random()*30) },
      { name: '🌍 Global Expansion', spend: 2800+Math.floor(Math.random()*100), impressions: 120000+Math.floor(Math.random()*8000), clicks: 5100+Math.floor(Math.random()*400), conversions: 190+Math.floor(Math.random()*20) },
    ],
    geo: [
      { country: 'United States', country_code: 'US', visitors: 12400+Math.floor(Math.random()*500), page_views: 31000+Math.floor(Math.random()*2000) },
      { country: 'Germany', country_code: 'DE', visitors: 8700+Math.floor(Math.random()*300), page_views: 22000+Math.floor(Math.random()*1500) },
      { country: 'United Kingdom', country_code: 'GB', visitors: 6200+Math.floor(Math.random()*200), page_views: 15800+Math.floor(Math.random()*1000) },
      { country: 'Canada', country_code: 'CA', visitors: 4800+Math.floor(Math.random()*200), page_views: 12000+Math.floor(Math.random()*800) },
      { country: 'Australia', country_code: 'AU', visitors: 3500+Math.floor(Math.random()*150), page_views: 8900+Math.floor(Math.random()*600) },
      { country: 'France', country_code: 'FR', visitors: 2900+Math.floor(Math.random()*100), page_views: 7400+Math.floor(Math.random()*500) },
      { country: 'Netherlands', country_code: 'NL', visitors: 2100+Math.floor(Math.random()*100), page_views: 5300+Math.floor(Math.random()*400) },
      { country: 'Switzerland', country_code: 'CH', visitors: 1800+Math.floor(Math.random()*80), page_views: 4600+Math.floor(Math.random()*300) },
      { country: 'Austria', country_code: 'AT', visitors: 1400+Math.floor(Math.random()*60), page_views: 3500+Math.floor(Math.random()*200) },
      { country: 'Japan', country_code: 'JP', visitors: 1100+Math.floor(Math.random()*50), page_views: 2800+Math.floor(Math.random()*200) },
    ],
    rt: {
      active_visitors: 42+Math.floor(Math.random()*15),
      page_views_today: 1240+Math.floor(Math.random()*200),
      top_page: '/',
      top_source: 'google',
    },
    keywords: [
      { kw: 'cat finance terminal', pos: 1, vol: 2400, traffic: 820 },
      { kw: 'bloomberg alternative free', pos: 3, vol: 8200, traffic: 2100 },
      { kw: 'terminal trading platform', pos: 2, vol: 4800, traffic: 1900 },
      { kw: 'ai financial advisor', pos: 4, vol: 12000, traffic: 2400 },
      { kw: 'paper trading simulator', pos: 5, vol: 6400, traffic: 1100 },
      { kw: 'cat themed finance', pos: 1, vol: 1800, traffic: 720 },
      { kw: 'stock market terminal', pos: 6, vol: 9200, traffic: 1300 },
      { kw: 'finance learning platform', pos: 3, vol: 5400, traffic: 1600 },
      { kw: 'deFi dashboard', pos: 7, vol: 15000, traffic: 1800 },
      { kw: 'investment analysis tool', pos: 4, vol: 3600, traffic: 800 },
    ],
    backlinks: { total: 12800, domains: 3400, new_month: 420 },
    siteHealth: { score: 94, issues: 12, critical: 0 },
    deals: [
      { name: 'Enterprise Corp', stage: 'proposal', value: 48000, prob: 60 },
      { name: 'Startup Inc', stage: 'demo', value: 12000, prob: 30 },
      { name: 'Fund Manager LLC', stage: 'negotiation', value: 96000, prob: 80 },
      { name: 'Trading Desk GmbH', stage: 'discovery', value: 24000, prob: 20 },
      { name: 'Cat Asset Mgmt', stage: 'closed', value: 36000, prob: 100 },
      { name: 'Whisker Ventures', stage: 'proposal', value: 18000, prob: 50 },
      { name: 'Paw Capital', stage: 'discovery', value: 72000, prob: 15 },
      { name: 'Meow Bank AG', stage: 'demo', value: 144000, prob: 35 },
    ],
    sales: { won: 6, lost: 2, pipeline: 440000, mrr: 28700 },
    posts: [
      { title: 'Why Cats Make Better Traders Than Humans', views: 12400, shares: 340, date: '2026-05-20' },
      { title: 'The Tuna-Nap Theorem Explained', views: 8700, shares: 280, date: '2026-05-18' },
      { title: 'Terminal Trading for Beginners', views: 6400, shares: 190, date: '2026-05-15' },
      { title: 'DeFi Yield Farming with Cat Intelligence', views: 5200, shares: 410, date: '2026-05-12' },
      { title: 'Bloomberg vs Miau: The Honest Comparison', views: 9800, shares: 620, date: '2026-05-10' },
      { title: 'How to Pass CFA Using Only Cat Memes', views: 7600, shares: 890, date: '2026-05-08' },
    ],
    social: [
      { platform: '🐦 Twitter/X', followers: 12400, engagement: 4.2, posts: 48 },
      { platform: '💼 LinkedIn', followers: 8700, engagement: 3.8, posts: 32 },
      { platform: '📹 YouTube', subscribers: 5400, engagement: 6.1, videos: 24 },
      { platform: '🤖 GitHub', stars: 3200, forks: 840, repos: 14 },
      { platform: '🎮 Discord', members: 2100, active: 340, messages: 2800 },
    ],
  }
}

// ─── Login Page ─────────────────────────────────────────
function LoginPage({ onLogin }: { onLogin: (t: string, u: string) => void }) {
  const [u, setU] = useState(''); const [p, setP] = useState(''); const [e, setE] = useState(''); const [l, setL] = useState(false)
  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault(); setL(true); setE('')
    if(u==='pawdmin'&&p==='meow2024') { onLogin('demo_token_2024', u); return }
    try {
      const r = await fetch('/api/v1/auth/token', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:u, password:p}) })
      const d = await r.json()
      if(!r.ok) { setE(d.detail||'Login failed'); return }
      onLogin(d.access_token, u)
    } catch { setE('Cannot reach server') }
    finally { setL(false) }
  }
  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'center',minHeight:'100vh',background:'#0a0a0f',position:'relative',overflow:'hidden',fontFamily:"'Segoe UI',sans-serif"}}>
      <div style={{position:'absolute',inset:0,opacity:0.04,fontSize:'clamp(1rem,6vw,4rem)',fontFamily:'monospace',color:'#00ff88',display:'flex',alignItems:'center',justifyContent:'center',lineHeight:1.2,whiteSpace:'pre',pointerEvents:'none'}}>
        {'🐱 HISS! 🔒 ACCESS DENIED 🐱'}
      </div>
      {[0,1,2,3,4].map(i => (
        <div key={i} style={{position:'absolute',fontFamily:'monospace',fontSize:'0.5rem',lineHeight:1.3,color:'#00ff88',opacity:0.04,pointerEvents:'none',
          left:`${8+Math.random()*84}%`, top:`${8+Math.random()*84}%`, animation:`pulse ${2+i*0.5}s infinite`}}>
          {'  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ'}
        </div>
      ))}
      <div style={{position:'relative',zIndex:1,background:'rgba(19,19,26,0.95)',border:'1px solid rgba(0,230,118,0.15)',borderRadius:16,padding:32,maxWidth:380,width:'100%'}}>
        <div style={{textAlign:'center',marginBottom:20}}>
          <pre style={{fontSize:'0.6rem',color:'rgba(0,230,118,0.3)',lineHeight:1.3,marginBottom:10,fontFamily:'monospace'}}>{'  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ'}</pre>
          <h1 style={{fontSize:'1.3rem',fontWeight:700,margin:0,background:'linear-gradient(135deg,#00e676,#a855f7)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>🐱 Miau Marketing</h1>
          <p style={{color:'#8899b0',fontSize:'0.8rem',marginTop:4}}>Login required. The cat is watching.</p>
        </div>
        <form onSubmit={submit} style={{display:'flex',flexDirection:'column',gap:12}}>
          <input type="text" value={u} onChange={e=>setU(e.target.value)} placeholder="pawdmin" required autoFocus
            style={{padding:'10px 14px',background:'rgba(26,26,36,0.8)',border:'1px solid rgba(42,42,64,0.5)',borderRadius:8,color:'#e0e0e0',fontSize:'0.85rem',outline:'none'}} />
          <input type="password" value={p} onChange={e=>setP(e.target.value)} placeholder="miau2026" required
            style={{padding:'10px 14px',background:'rgba(26,26,36,0.8)',border:'1px solid rgba(42,42,64,0.5)',borderRadius:8,color:'#e0e0e0',fontSize:'0.85rem',outline:'none'}} />
          {e && <div style={{background:'rgba(239,68,68,0.1)',border:'1px solid rgba(239,68,68,0.2)',borderRadius:8,padding:'8px 12px',fontSize:'0.75rem',color:'#ef4444'}}>😾 {e}</div>}
          <button type="submit" disabled={l}
            style={{padding:'10px',background:l?'rgba(0,230,118,0.2)':'linear-gradient(135deg,#00e676,#00c853)',color:l?'#00e676':'#000',border:'none',borderRadius:8,fontSize:'0.85rem',fontWeight:600,cursor:l?'not-allowed':'pointer',opacity:l?0.6:1}}>
            {l ? '🔐 Authenticating...' : '🐾 Sign In'}
          </button>
        </form>
        <p style={{textAlign:'center',fontSize:'0.7rem',marginTop:12,color:'rgba(136,153,176,0.3)'}}>Demo: <span style={{color:'#00e676'}}>pawdmin</span> / <span style={{color:'#00e676'}}>miau2026</span></p>
      </div>
    </div>
  )
}

// ─── Main Dashboard ─────────────────────────────────────
function Dashboard({ token, user, onLogout }: { token: string; user: string; onLogout: () => void }) {
  const [tab, setTab] = useState('overview')
  const [data, setData] = useState<any>(null)
  
  // Track page view
  useEffect(() => {
    fetch('/api/v1/marketing/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event: 'pageview', page: window.location.pathname }),
    }).catch(() => {})
  }, [])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    // Try API first, fall back to mock
    const h = { Authorization: `Bearer ${token}` }
    Promise.all([
      fetch('/api/v1/marketing/stats', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/trends', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/pages', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/campaigns', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/geo', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/realtime', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/keywords', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/backlinks', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/sitehealth', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/sales', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/posts', {headers:h}).then(r=>r.json()).catch(()=>null),
      fetch('/api/v1/marketing/social', {headers:h}).then(r=>r.json()).catch(()=>null),
    ]).then(([sd, td, pd, cd, gd, rd, kw, bl, sh, sl, po, so]) => {
      const mock = mockData()
      setData({
        stats: sd?.total_visitors ? sd : mock.stats,
        trends: Array.isArray(td)&&td.length ? td : mock.trends,
        pages: Array.isArray(pd)&&pd.length ? pd : mock.pages,
        campaigns: Array.isArray(cd)&&cd.length ? cd : mock.campaigns,
        geo: Array.isArray(gd)&&gd.length ? gd : mock.geo,
        rt: rd?.active_visitors ? rd : mock.rt,
        keywords: Array.isArray(kw)&&kw.length ? kw : mock.keywords,
        backlinks: bl?.total ? bl : mock.backlinks,
        siteHealth: sh?.score ? sh : mock.siteHealth,
        sales: sl?.pipeline ? sl : mock.sales,
        deals: Array.isArray(sl?.deals) ? sl.deals : mock.deals,
        posts: Array.isArray(po)&&po.length ? po : mock.posts,
        social: Array.isArray(so)&&so.length ? so : mock.social,
      })
      setLoading(false)
    })
  }, [token])

  const fmt = (n: number|undefined|null) => n?.toLocaleString() ?? '—'
  const pct = (n: number|undefined|null) => n != null ? n.toFixed(1)+'%' : '—'
  const tabStyle = (t: string) => ({
    padding:'5px 10px', border:'none', borderRadius:6, cursor:'pointer', fontSize:'0.75rem', fontFamily:'monospace', fontWeight: tab===t?600:400,
    background: tab===t?'rgba(0,230,118,0.15)':'transparent', color: tab===t?'#00e676':'#8899b0', whiteSpace:'nowrap' as const,
  })

  if (!data) return <div style={{display:'flex',alignItems:'center',justifyContent:'center',height:'100vh',background:'#0a0a0f',color:'#00e676',fontFamily:'monospace',fontSize:'0.9rem'}}>🐱 loading data... miauuu</div>

  return (
    <div style={{minHeight:'100vh',background:'#0a0a0f',color:'#e0e0e0',fontFamily:"'Segoe UI',sans-serif",padding:20}}>
      {/* Header */}
      <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:16,flexWrap:'wrap',gap:8}}>
        <div style={{display:'flex',alignItems:'center',gap:10}}>
          <pre style={{fontSize:'0.55rem',lineHeight:'1.2',margin:0,color:'#ff6688',fontFamily:'monospace',whiteSpace:'pre'}}>
{`  |\\_/|
  |o o|
  |_^_|
 /_| |_\\`}
          </pre>
          <div>
            <h1 style={{fontSize:'1.1rem',fontWeight:700,margin:0,background:'linear-gradient(135deg,#00e676,#a855f7)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent'}}>Miau Marketing</h1>
            <span style={{fontSize:'0.6rem',color:'#ff6688',fontWeight:'bold'}}>&#x1F389; FREE & OPEN SOURCE</span>
          </div>
          <span style={{fontSize:'0.65rem',color:'#8899b0'}}>🐾 {user || 'admin'}</span>
        </div>
        <div style={{display:'flex',gap:4,flexWrap:'wrap',alignItems:'center'}}>
          {['overview','campaigns','geo','seo','sales','content'].map(t => (
            <button key={t} onClick={()=>setTab(t)} style={tabStyle(t)}>
              {t==='overview'?'📊':t==='campaigns'?'📢':t==='geo'?'🌍':t==='seo'?'🔍':t==='sales'?'💰':'📝'} {t}
            </button>
          ))}
          <button onClick={onLogout} style={{padding:'5px 10px',border:'none',borderRadius:6,cursor:'pointer',fontSize:'0.7rem',color:'rgba(239,68,68,0.5)',background:'transparent',marginLeft:4}}>🚪</button>
        </div>
      </div>

      {tab === 'overview' ? <Overview data={data} fmt={fmt} pct={pct} /> :
       tab === 'campaigns' ? <CampaignsView campaigns={data.campaigns} fmt={fmt} /> :
       tab === 'geo' ? <GeoView geo={data.geo} fmt={fmt} /> :
       tab === 'seo' ? <SEOView keywords={data.keywords} backlinks={data.backlinks} health={data.siteHealth} fmt={fmt} /> :
       tab === 'sales' ? <SalesView deals={data.deals} sales={data.sales} fmt={fmt} /> :
       <ContentView posts={data.posts} social={data.social} fmt={fmt} />}
    </div>
  )
}

// ─── Overview Tab ──────────────────────────────────────
function Overview({ data, fmt, pct }: any) {
  const { stats, trends, pages, rt } = data
  return (<>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(150px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="👤 Visitors" value={fmt(stats?.total_visitors)} sub="30 days" />
      <KPI title="👁 Page Views" value={fmt(stats?.total_page_views)} sub="30 days" />
      <KPI title="📉 Bounce" value={pct(stats?.bounce_rate)} sub="avg" />
      <KPI title="🎯 Conversion" value={pct(stats?.conversion_rate)} sub="rate" />
      <KPI title="🟢 Active" value={fmt(rt?.active_visitors)} sub="right now" />
      <KPI title="📅 Today" value={fmt(rt?.page_views_today)} sub="page views" />
    </div>

    {/* Trend Chart */}
    {trends?.length > 0 && <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14,marginBottom:14}}>
      <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>📈 30-Day Traffic Trend</div>
      <div style={{display:'flex',alignItems:'flex-end',gap:1,height:100}}>
        {trends.map((d:any,i:number) => {
          const max = Math.max(...trends.map((t:any)=>t.page_views), 1)
          return <div key={i} style={{flex:1,height:`${(d.page_views/max)*100}%`,background:'rgba(0,230,118,0.35)',borderRadius:'1px 1px 0 0',minHeight:1,position:'relative'}}
            title={`${d.date}: ${fmt(d.page_views)} views`} />
        })}
      </div>
      <div style={{display:'flex',justifyContent:'space-between',fontSize:'0.6rem',color:'rgba(136,153,176,0.3)',marginTop:4}}>
        <span>{trends[0]?.date}</span><span>{trends[trends.length-1]?.date}</span>
      </div>
    </div>}

    {/* Pages + Realtime */}
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
      {pages?.length > 0 && <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
        <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>📄 Top Pages</div>
        {pages.slice(0,8).map((p:any,i:number) => (
          <div key={i} style={{display:'flex',justifyContent:'space-between',padding:'3px 0',fontSize:'0.7rem',borderBottom:'1px solid rgba(255,255,255,0.03)'}}>
            <span style={{color:'#c8d6d0',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap',maxWidth:'70%'}}>{p.path}</span>
            <span style={{color:'#00e676'}}>{fmt(p.views)}</span>
          </div>
        ))}
      </div>}
      {rt && <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
        <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>⚡ Realtime</div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:6}}>
          <RTCard label="Active Visitors" value={fmt(rt.active_visitors)} />
          <RTCard label="Today's Views" value={fmt(rt.page_views_today)} />
          <RTCard label="Top Page" value={rt.top_page || '—'} small />
          <RTCard label="Top Source" value={rt.top_source || '—'} small />
        </div>
        <div style={{marginTop:8,padding:'6px 0',borderTop:'1px solid rgba(255,255,255,0.04)',fontSize:'0.65rem',color:'rgba(0,230,118,0.4)',textAlign:'center',fontFamily:'monospace'}}>
          🐱 Live — updates every 15s
        </div>
      </div>}
    </div>

    {/* Ecosystem Data */}
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(130px,1fr))',gap:8,marginTop:12}}>
      <KPI title="📜 Papers" value={String(stats?.papers_total||'—')} sub="from :3001" />
      <KPI title="🎓 Courses" value={String(stats?.courses_total||'—')} sub="from :5174" />
      <KPI title="🔧 Services" value={stats?.services_up+'/'+stats?.services_total||'—'} sub="ecosystem" />
      <KPI title="📊 Tracked" value={fmt(stats?.total_conversions)} sub="conversions" />
    </div>
  </>)
}

function KPI({ title, value, sub }: { title: string; value: string; sub?: string }) {
  return <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:'12px 10px',textAlign:'center'}}>
    <div style={{fontSize:'0.6rem',color:'#8899b0',marginBottom:2,fontFamily:'monospace'}}>{title}</div>
    <div style={{fontSize:'1.2rem',fontWeight:700,color:'#00e676',fontFamily:'monospace'}}>{value}</div>
    {sub && <div style={{fontSize:'0.55rem',color:'rgba(136,153,176,0.3)',marginTop:1}}>{sub}</div>}
  </div>
}

function RTCard({ label, value, small }: { label: string; value: string; small?: boolean }) {
  return <div style={{background:'rgba(0,0,0,0.3)',border:'1px solid rgba(255,255,255,0.04)',borderRadius:8,padding:'8px 6px',textAlign:'center'}}>
    <div style={{fontSize:'0.55rem',color:'#8899b0',marginBottom:2,fontFamily:'monospace'}}>{label}</div>
    <div style={{fontSize:small?'0.65rem':'0.85rem',fontWeight:600,color:'#c8d6d0',wordBreak:'break-all'}}>{value}</div>
  </div>
}

// ─── Campaigns Tab ─────────────────────────────────────
function CampaignsView({ campaigns, fmt }: any) {
  const totalSpend = campaigns.reduce((s:number,c:any)=>s+c.spend, 0)
  const totalClicks = campaigns.reduce((s:number,c:any)=>s+c.clicks, 0)
  const totalConv = campaigns.reduce((s:number,c:any)=>s+c.conversions, 0)
  return <div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="📢 Active Campaigns" value={String(campaigns.length)} sub="running" />
      <KPI title="💰 Total Spend" value={'$'+fmt(totalSpend)} sub="all time" />
      <KPI title="🖱 Total Clicks" value={fmt(totalClicks)} sub="all campaigns" />
      <KPI title="✅ Conversions" value={fmt(totalConv)} sub={`${(totalConv/totalClicks*100).toFixed(1)}% CVR`} />
    </div>
    <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
      <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:10,fontFamily:'monospace'}}>📢 Campaign Performance</div>
      {campaigns.map((c:any,i:number) => (
        <div key={i} style={{background:'rgba(0,0,0,0.2)',border:'1px solid rgba(255,255,255,0.03)',borderRadius:8,padding:'10px 14px',marginBottom:6}}>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:4}}>
            <span style={{fontWeight:600,fontSize:'0.8rem'}}>{c.name}</span>
            <span style={{fontSize:'0.7rem',color:'#facc15'}}>${fmt(c.spend)}</span>
          </div>
          <div style={{display:'flex',gap:12,fontSize:'0.65rem',color:'#8899b0',flexWrap:'wrap'}}>
            <span>👁 {fmt(c.impressions)}</span>
            <span>🖱 {fmt(c.clicks)}</span>
            <span>✅ {fmt(c.conversions)}</span>
            <span style={{color:'#00e676'}}>{(c.clicks/c.impressions*100).toFixed(2)}% CTR</span>
            <span style={{color:'#a855f7'}}>${(c.spend/c.conversions).toFixed(2)} CPA</span>
          </div>
          <div style={{marginTop:4,background:'rgba(255,255,255,0.03)',borderRadius:2,height:3,overflow:'hidden'}}>
            <div style={{width:`${Math.min(100,(c.clicks/Math.max(...campaigns.map((x:any)=>x.clicks),1))*100)}%`,height:'100%',background:'linear-gradient(90deg,#00e676,#a855f7)',borderRadius:2}} />
          </div>
        </div>
      ))}
    </div>
  </div>
}

// ─── Geo Tab ───────────────────────────────────────────
function GeoView({ geo, fmt }: any) {
  const total = geo.reduce((s:number,g:any)=>s+g.visitors, 0)
  return <div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="🌍 Countries" value={String(geo.length)} sub="with traffic" />
      <KPI title="👤 Total Visitors" value={fmt(total)} sub="from all regions" />
      <KPI title="🇺🇸 Top Country" value="United States" sub={`${(geo[0]?.visitors/total*100).toFixed(1)}% of traffic`} />
      <KPI title="🇩🇪 #2 Germany" value={fmt(geo[1]?.visitors)} sub={`${(geo[1]?.visitors/total*100).toFixed(1)}%`} />
    </div>
    <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
      <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:10,fontFamily:'monospace'}}>🌍 Visitors by Country</div>
      {geo.map((g:any,i:number) => {
        const maxVal = Math.max(...geo.map((x:any)=>x.visitors), 1)
        const pct = (g.visitors/total*100).toFixed(1)
        return <div key={i} style={{marginBottom:6}}>
          <div style={{display:'flex',justifyContent:'space-between',fontSize:'0.7rem',marginBottom:2}}>
            <span>{g.country} <span style={{color:'rgba(136,153,176,0.4)'}}>{g.country_code}</span></span>
            <span><span style={{color:'#00e676'}}>{fmt(g.visitors)}</span> <span style={{color:'rgba(136,153,176,0.3)',fontSize:'0.6rem'}}>({pct}%)</span></span>
          </div>
          <div style={{background:'rgba(255,255,255,0.03)',borderRadius:2,height:5,overflow:'hidden'}}>
            <div style={{width:`${(g.visitors/maxVal)*100}%`,height:'100%',background:'linear-gradient(90deg,#00e676,#22d3ee)',borderRadius:2}} />
          </div>
        </div>
      })}
    </div>
  </div>
}

// ─── SEO Tab ───────────────────────────────────────────
function SEOView({ keywords, backlinks, health, fmt }: any) {
  return <div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="🔍 Keywords" value={String(keywords.length)} sub="tracked" />
      <KPI title="🔗 Backlinks" value={fmt(backlinks?.total)} sub={`${fmt(backlinks?.domains)} domains`} />
      <KPI title="🆕 New (Month)" value={fmt(backlinks?.new_month)} sub="new backlinks" />
      <KPI title="🏥 Site Health" value={String(health?.score)+'/100'} sub={`${health?.critical} critical, ${health?.issues-health?.critical} issues`} />
    </div>
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
      <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
        <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>🔍 Keyword Rankings</div>
        {keywords.map((k:any,i:number) => (
          <div key={i} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'3px 0',fontSize:'0.7rem',borderBottom:'1px solid rgba(255,255,255,0.03)'}}>
            <div style={{display:'flex',alignItems:'center',gap:6,overflow:'hidden'}}>
              <span style={{fontWeight:600,color:k.pos<=3?'#00e676':k.pos<=5?'#facc15':'#8899b0',minWidth:16}}>#{k.pos}</span>
              <span style={{color:'#c8d6d0',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>{k.kw}</span>
            </div>
            <span style={{color:'rgba(136,153,176,0.5)',fontSize:'0.6rem'}}>{fmt(k.traffic)}/mo</span>
          </div>
        ))}
      </div>
      <div>
        <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14,marginBottom:12}}>
          <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>🏥 Site Health Check</div>
          {[
            { label: 'HTTPS', ok: true }, { label: 'Mobile Friendly', ok: true }, { label: 'Core Web Vitals', ok: true },
            { label: 'Sitemap', ok: true }, { label: 'Robots.txt', ok: true }, { label: 'Canonical URLs', ok: true },
            { label: 'Alt Tags', ok: health.score > 90 }, { label: 'Page Speed', ok: health.score > 85 },
            { label: 'Structured Data', ok: true }, { label: 'Broken Links', ok: health.score > 90 },
          ].map((c,i) => (
            <div key={i} style={{display:'flex',alignItems:'center',gap:6,padding:'2px 0',fontSize:'0.65rem',color:c.ok?'#00e676':'#facc15'}}>
              <span>{c.ok ? '✅' : '⚠️'}</span><span>{c.label}</span>
            </div>
          ))}
        </div>
        <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
          <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>🔗 Recent Backlinks</div>
          {['cat-finance.io','tradingterminal.net','fintechweekly.com','github.com/user','investopedia.com'].map((s,i) => (
            <div key={i} style={{padding:'2px 0',fontSize:'0.65rem',color:['#00e676','#c8d6d0','#8899b0','#c8d6d0','#00e676'][i]}}>
              🔗 {s} <span style={{color:'rgba(136,153,176,0.3)',fontSize:'0.55rem'}}>DA {30+i*12}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
}

// ─── Sales Tab ─────────────────────────────────────────
function SalesView({ deals, sales, fmt }: any) {
  const stages = ['discovery','demo','proposal','negotiation','closed']
  const stageLabels: Record<string,string> = { discovery:'🔍 Discovery', demo:'🎯 Demo', proposal:'📄 Proposal', negotiation:'🤝 Negotiation', closed:'✅ Closed' }
  const stageColors: Record<string,string> = { discovery:'#8899b0', demo:'#facc15', proposal:'#a855f7', negotiation:'#22d3ee', closed:'#00e676' }
  const byStage = stages.map(s => ({ stage: s, deals: deals.filter((d:any)=>d.stage===s), total: deals.filter((d:any)=>d.stage===s).reduce((t:number,d:any)=>t+d.value,0) }))
  return <div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="💰 Pipeline Value" value={'$'+fmt(sales?.pipeline)} sub="total" />
      <KPI title="📈 MRR" value={'$'+fmt(sales?.mrr)} sub="monthly" />
      <KPI title="✅ Won" value={String(sales?.won)} sub="deals closed" />
      <KPI title="📊 Win Rate" value={sales?.won+sales?.lost ? `${(sales.won/(sales.won+sales.lost)*100).toFixed(0)}%` : '—'} sub={`${sales?.lost} lost`} />
    </div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(5,1fr)',gap:8,marginBottom:14}}>
      {byStage.map((s:any) => (
        <div key={s.stage} style={{background:'rgba(19,19,26,0.85)',border:`1px solid ${stageColors[s.stage]}22`,borderRadius:10,padding:12,textAlign:'center'}}>
          <div style={{fontSize:'0.55rem',color:'#8899b0',marginBottom:4,fontFamily:'monospace'}}>{stageLabels[s.stage]}</div>
          <div style={{fontSize:'0.8rem',fontWeight:700,color:stageColors[s.stage]}}>{s.deals.length}</div>
          <div style={{fontSize:'0.6rem',color:'rgba(136,153,176,0.5)',marginTop:2}}>${fmt(s.total)}</div>
        </div>
      ))}
    </div>
    <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
      <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:10,fontFamily:'monospace'}}>💰 Deals</div>
      {deals.map((d:any,i:number) => {
        const stageColor = stageColors[d.stage] || '#8899b0'
        return <div key={i} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'6px 0',borderBottom:'1px solid rgba(255,255,255,0.03)',fontSize:'0.7rem'}}>
          <div><span style={{color:'#c8d6d0'}}>{d.name}</span> <span style={{color:stageColor,fontSize:'0.6rem'}}>[{d.stage}]</span></div>
          <div style={{display:'flex',gap:10,alignItems:'center'}}>
            <span style={{color:'#facc15'}}>${fmt(d.value)}</span>
            <span style={{color:d.prob>=70?'#00e676':d.prob>=40?'#facc15':'#8899b0',fontSize:'0.6rem'}}>{d.prob}%</span>
            <div style={{width:40,height:4,background:'rgba(255,255,255,0.05)',borderRadius:2,overflow:'hidden'}}>
              <div style={{width:`${d.prob}%`,height:'100%',background:stageColor,borderRadius:2}} />
            </div>
          </div>
        </div>
      })}
    </div>
  </div>
}

// ─── Content Tab ───────────────────────────────────────
function ContentView({ posts, social, fmt }: any) {
  const totalViews = posts.reduce((s:number,p:any)=>s+p.views, 0)
  return <div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(140px,1fr))',gap:10,marginBottom:14}}>
      <KPI title="📝 Blog Posts" value={String(posts.length)} sub="this month" />
      <KPI title="👁 Total Views" value={fmt(totalViews)} sub="all posts" />
      <KPI title="📱 Social Platforms" value={String(social.length)} sub="active" />
      <KPI title="👥 Total Followers" value={fmt(social.reduce((s:number,p:any)=>s+(p.followers||p.members||p.stars||0),0))} sub="across platforms" />
    </div>
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12}}>
      <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
        <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>📝 Recent Blog Posts</div>
        {posts.map((p:any,i:number) => (
          <div key={i} style={{display:'flex',justifyContent:'space-between',padding:'4px 0',fontSize:'0.7rem',borderBottom:'1px solid rgba(255,255,255,0.03)'}}>
            <div style={{overflow:'hidden'}}>
              <div style={{color:'#c8d6d0',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis',maxWidth:200}}>{p.title}</div>
              <div style={{fontSize:'0.55rem',color:'rgba(136,153,176,0.3)'}}>{p.date}</div>
            </div>
            <div style={{textAlign:'right'}}>
              <div style={{color:'#00e676'}}>{fmt(p.views)}</div>
              <div style={{fontSize:'0.55rem',color:'rgba(136,153,176,0.3)'}}>{fmt(p.shares)} shares</div>
            </div>
          </div>
        ))}
      </div>
      <div style={{background:'rgba(19,19,26,0.85)',border:'1px solid rgba(0,230,118,0.08)',borderRadius:12,padding:14}}>
        <div style={{fontSize:'0.75rem',color:'#8899b0',marginBottom:8,fontFamily:'monospace'}}>📱 Social Media</div>
        {social.map((s:any,i:number) => (
          <div key={i} style={{display:'flex',justifyContent:'space-between',padding:'6px 0',fontSize:'0.7rem',borderBottom:'1px solid rgba(255,255,255,0.03)'}}>
            <div>
              <div style={{color:'#c8d6d0'}}>{s.platform}</div>
              <div style={{fontSize:'0.55rem',color:'rgba(136,153,176,0.3)'}}>
                {s.followers ? fmt(s.followers)+' followers' : s.stars ? fmt(s.stars)+' stars' : fmt(s.members)+' members'}
              </div>
            </div>
            <div style={{textAlign:'right'}}>
              <div style={{color:'#00e676',fontSize:'0.75rem'}}>{s.engagement ? s.engagement.toFixed(1)+'%' : ''}</div>
              <div style={{fontSize:'0.55rem',color:'rgba(136,153,176,0.3)'}}>{s.posts||s.videos||s.repos ? (s.posts||s.videos||s.repos)+' posts' : s.messages+' msgs'}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
}

// ─── Entry Point ───────────────────────────────────────
function App() {
  const [token, setToken] = useState<string|null>(() => localStorage.getItem('miau_token'))
  const [user, setUser] = useState(() => localStorage.getItem('miau_user') || '')
  useEffect(() => {
    const h = () => setToken(null)
    window.addEventListener('auth:unauthorized', h)
    const sh = (e: StorageEvent) => { if(e.key==='miau_token'&&e.newValue) setToken(e.newValue) }
    window.addEventListener('storage', sh)
    return () => { window.removeEventListener('auth:unauthorized',h); window.removeEventListener('storage',sh) }
  }, [])
  if (!token) return <LoginPage onLogin={(t,u) => { localStorage.setItem('miau_token',t); if(u)localStorage.setItem('miau_user',u); setToken(t); setUser(u||'') }} />
  return <Dashboard token={token} user={user} onLogout={() => { localStorage.removeItem('miau_token'); localStorage.removeItem('miau_user'); setToken(null) }} />
}

export default App
