import { useState, useEffect } from 'react'

// ─── Miau Marketing — NOW FREE & OPEN SOURCE 🎉 ───────

function fmt(n: number | null | undefined): string {
  if (n == null) return '-'
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M'
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K'
  return n.toFixed(0)
}

export default function App() {
  const [health, setHealth] = useState<any>(null)
  const [fundCount, setFundCount] = useState<number>(0)

  useEffect(() => {
    fetch('/api/v1/health').then(r => r.json()).then(setHealth).catch(() => {})
    fetch('/api/v1/datavore/map/companies?continent=all&limit=1').then(r => r.json()).then(d => {
      if (Array.isArray(d)) setFundCount(d.length)
      else if (d?.total) setFundCount(d.total)
    }).catch(() => {})
  }, [])

  const cat = `  |\\_/|
  |o o|
  |_^_|
 /_| |_\\`

  return (
    <div style={{minHeight:'100vh',background:'#0a0a0a',color:'#e0e0e0',fontFamily:'monospace',padding:20}}>
      {/* Header */}
      <div style={{textAlign:'center',padding:'40px 20px 20px'}}>
        <pre style={{fontSize:'1.3rem',lineHeight:'1.3',color:'#ff6688',margin:'0 auto',width:'fit-content',textAlign:'left'}}>
{cat}
        </pre>
        <div style={{fontSize:'2rem',marginTop:4}}>😿</div>
        <h1 style={{fontSize:'1.5rem',color:'#ff6688',margin:'8px 0 4px'}}>MIAU IS FREE! 🥳</h1>
        <p style={{fontSize:'0.85rem',color:'rgba(200,214,208,0.5)',margin:0}}>
          No pawborghinis · No billionaires eating kittens · Just cats and charts
        </p>
        <p style={{fontSize:'1rem',color:'#00ff88',margin:'10px 0 0',fontWeight:'bold'}}>
          FREE & OPEN SOURCE 🎉
        </p>
      </div>

      {/* Real stats from backend */}
      <div style={{maxWidth:600,margin:'30px auto',display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:10}}>
        <div style={{background:'rgba(0,255,136,0.03)',border:'1px solid rgba(0,255,136,0.08)',borderRadius:10,padding:'14px 16px',textAlign:'center'}}>
          <div style={{fontSize:'0.6rem',color:'rgba(200,214,208,0.4)',textTransform:'uppercase',letterSpacing:1}}>Real Companies</div>
          <div style={{fontSize:'1.8rem',fontWeight:'bold',color:'#00ff88',marginTop:4}}>{fundCount ? fmt(fundCount) : '...'}</div>
        </div>
        <div style={{background:'rgba(0,255,136,0.03)',border:'1px solid rgba(0,255,136,0.08)',borderRadius:10,padding:'14px 16px',textAlign:'center'}}>
          <div style={{fontSize:'0.6rem',color:'rgba(200,214,208,0.4)',textTransform:'uppercase',letterSpacing:1}}>Backend Status</div>
          <div style={{fontSize:'1.8rem',fontWeight:'bold',color: health?.status === 'healthy' ? '#00ff88' : '#ff6688',marginTop:4}}>
            {health ? (health.status === 'healthy' ? '✅ LIVE' : '⚠️ ISSUE') : '...'}
          </div>
        </div>
      </div>

      {/* Links to real tools */}
      <div style={{maxWidth:500,margin:'30px auto',display:'flex',flexDirection:'column',gap:8}}>
        <a href="http://localhost:5173" target="_blank" style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',background:'rgba(0,255,136,0.04)',border:'1px solid rgba(0,255,136,0.12)',borderRadius:10,color:'#00ff88',textDecoration:'none',fontSize:'0.85rem'}}>
          <span>💻 Terminal</span>
          <span style={{color:'rgba(200,214,208,0.3)',fontSize:'0.7rem'}}>:5173 →</span>
        </a>
        <a href="http://localhost:5174" target="_blank" style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',background:'rgba(0,255,136,0.04)',border:'1px solid rgba(0,255,136,0.12)',borderRadius:10,color:'#00ff88',textDecoration:'none',fontSize:'0.85rem'}}>
          <span>📚 Education</span>
          <span style={{color:'rgba(200,214,208,0.3)',fontSize:'0.7rem'}}>:5174 →</span>
        </a>
        <a href="http://localhost:5175" target="_blank" style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',background:'rgba(0,255,136,0.04)',border:'1px solid rgba(0,255,136,0.12)',borderRadius:10,color:'#00ff88',textDecoration:'none',fontSize:'0.85rem'}}>
          <span>🏢 Ecosystem</span>
          <span style={{color:'rgba(200,214,208,0.3)',fontSize:'0.7rem'}}>:5175 →</span>
        </a>
        <a href="https://github.com/jz1656-izback/miau-finance-now-free" target="_blank" style={{display:'flex',justifyContent:'space-between',padding:'12px 16px',background:'rgba(0,255,136,0.04)',border:'1px solid rgba(0,255,136,0.12)',borderRadius:10,color:'#00ff88',textDecoration:'none',fontSize:'0.85rem'}}>
          <span>🐙 GitHub</span>
          <span style={{color:'rgba(200,214,208,0.3)',fontSize:'0.7rem'}}>→</span>
        </a>
      </div>

      {/* Crossed-out old marketing stuff */}
      <div style={{maxWidth:500,margin:'30px auto',textAlign:'center',fontSize:'0.7rem',color:'rgba(200,214,208,0.2)'}}>
        <p style={{textDecoration:'line-through',textDecorationColor:'#ff3344',margin:'4px 0'}}>
          Q1 Brand Push: €12.4K · Education Launch: €8.7K · Tuna Referral: €5.6K
        </p>
        <p style={{textDecoration:'line-through',textDecorationColor:'#ff3344',margin:'4px 0'}}>
          Pricing page views: 12,300 · Conversion rate: 3.2% · Bounce: 38%
        </p>
        <p style={{marginTop:16,color:'rgba(200,214,208,0.4)'}}>
          🐱 Made in Germany 🇩🇪
        </p>
      </div>
    </div>
  )
}
