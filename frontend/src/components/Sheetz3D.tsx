import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import * as THREE from 'three'
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

interface Props { ticker: string; onClose: () => void }

export default function Sheetz3D({ ticker, onClose }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [data, setData] = useState<any>({ dcf: null, wacc: null, comps: null, lbo: null })
  const [loading, setLoading] = useState(true)
  const [autoSpin, setAutoSpin] = useState(false)
  const sheetzSceneRef = useRef<any>(null)
  const controlsRef = useRef<OrbitControls | null>(null)
  const barTargets = useRef<{ mesh: THREE.Mesh; targetY: number; currentH: number }[]>([])

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 's' || e.key === 'S') {
        const canvas = document.querySelector('canvas')
        if (canvas) {
          const link = document.createElement('a')
          link.download = `${ticker}_sheetz3d.png`
          link.href = canvas.toDataURL('image/png')
          link.click()
        }
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose, ticker])

  useEffect(() => {
    if (!ticker) return
    setLoading(true)
    const headers: Record<string, string> = localStorage.getItem('miau_token')
      ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
    Promise.all([
      fetch(`/api/v1/analytics/valuation/dcf/${ticker}?growth=0.05&terminal_growth=0.025&years=5`, { headers }).then(r => r.ok ? r.json() : null),
      fetch(`/api/v1/analytics/valuation/wacc/${ticker}`, { headers }).then(r => r.ok ? r.json() : null),
      fetch(`/api/v1/analytics/valuation/comps/${ticker}`, { headers }).then(r => r.ok ? r.json() : null),
      fetch(`/api/v1/analytics/valuation/lbo/${ticker}`, { headers }).then(r => r.ok ? r.json() : null),
    ]).then(([dcf, wacc, comps, lbo]) => {
      setData({ dcf, wacc, comps, lbo })
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [ticker])

  useEffect(() => {
    if (!containerRef.current || loading) return
    const container = containerRef.current
    if (sheetzSceneRef.current) {
      try { if (sheetzSceneRef.current.renderer.domElement.parentNode) sheetzSceneRef.current.renderer.domElement.parentNode.removeChild(sheetzSceneRef.current.renderer.domElement) } catch {}
      sheetzSceneRef.current.renderer.dispose()
    }

    const w = window.innerWidth, h = window.innerHeight
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0a1a14)

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100)
    camera.position.set(12, 8, 14)
    camera.lookAt(0, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(w, h)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.08
    controls.target.set(0, 1, 0)
    controls.minDistance = 5
    controls.maxDistance = 40
    controls.autoRotate = autoSpin
    controls.autoRotateSpeed = 1.5
    controlsRef.current = controls

    // ── Lights ──
    const ambient = new THREE.AmbientLight(0x404060, 0.6)
    scene.add(ambient)
    const dir = new THREE.DirectionalLight(0xffffff, 0.8)
    dir.position.set(5, 10, 7)
    scene.add(dir)
    const back = new THREE.DirectionalLight(0x4488ff, 0.3)
    back.position.set(-5, 0, -7)
    scene.add(back)

    // ── Particles ──
    const particleCount = 200
    const particleGeo = new THREE.BufferGeometry()
    const positions = new Float32Array(particleCount * 3)
    for (let i = 0; i < particleCount * 3; i++) positions[i] = (Math.random() - 0.5) * 30
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    const particleMat = new THREE.PointsMaterial({ color: 0x00ff88, size: 0.05, transparent: true, opacity: 0.3 })
    const particles = new THREE.Points(particleGeo, particleMat)
    scene.add(particles)

    // ── Grid ──
    const grid = new THREE.GridHelper(20, 10, 0x00ff88, 0x002211)
    scene.add(grid)

    // ── Label helper ──
    const makeLabel = (text: string, x: number, z: number, color = '#00ff88', scale = 4) => {
      const c = document.createElement('canvas')
      c.width = 256; c.height = 48
      const cx = c.getContext('2d')!
      cx.fillStyle = color
      cx.font = '28px monospace'
      cx.textAlign = 'center'
      cx.fillText(text, 128, 32)
      const tex = new THREE.CanvasTexture(c)
      const mat = new THREE.SpriteMaterial({ map: tex, transparent: true })
      const s = new THREE.Sprite(mat)
      s.position.set(x, 4.5, z)
      s.scale.set(scale, 0.75, 1)
      scene.add(s)
    }

    // ── Animated bar ──
    barTargets.current = []
    const createBar = (val: number, x: number, z: number, color: number, scale: number): THREE.Mesh => {
      const h = Math.max(val * scale, 0.05)
      const m = new THREE.Mesh(
        new THREE.BoxGeometry(0.4, 0.05, 0.4),
        new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.1 })
      )
      m.position.set(x, 0.025, z)
      scene.add(m)
      barTargets.current.push({ mesh: m, targetY: h, currentH: 0.05 })
      return m
    }

    // ════════════════════════════════════════════
    // DCF Panel (x: -4, z: -2)
    // ════════════════════════════════════════════
    makeLabel('📈 DCF', -4, -2)
    if (data.dcf?.projections && Array.isArray(data.dcf.projections)) {
      data.dcf.projections.forEach((p: any, idx: number) => {
        createBar(p.fcf || 0, -4 + idx * 1.5, -2, 0x00ff88, 0.5 / 1e8)
      })
      const fp = data.dcf.fair_price || 0
      const cp = data.dcf.current_price || 1
      createBar(fp, -4, -3.5, 0x00ff88, 0.5)
      createBar(cp, -2.5, -3.5, 0xffcc00, 0.5)
      makeLabel(`FP:$${fp.toFixed(0)}`, -4, -4.5, '#00ff88', 3)
      makeLabel(`CP:$${cp.toFixed(0)}`, -2.5, -4.5, '#ffcc00', 3)
    }

    // ════════════════════════════════════════════
    // WACC Panel (x: 4, z: -2)
    // ════════════════════════════════════════════
    makeLabel('⚖️ WACC', 4, -2)
    if (data.wacc) {
      const wv = data.wacc
      createBar((wv.cost_of_equity || 0) * 100, 2.5, -2, 0x00ff88, 30)
      createBar((wv.cost_of_debt || 0) * 100, 4, -2, 0xff6644, 30)
      createBar((wv.wacc || 0) * 100, 5.5, -2, 0xffcc00, 30)
      makeLabel(`CoE:${((wv.cost_of_equity||0)*100).toFixed(1)}%`, 2.5, -3.5, '#00ff88', 2.5)
      makeLabel(`CoD:${((wv.cost_of_debt||0)*100).toFixed(1)}%`, 4, -3.5, '#ff6644', 2.5)
      makeLabel(`WACC:${((wv.wacc||0)*100).toFixed(1)}%`, 5.5, -3.5, '#ffcc00', 2.5)
    }

    // ════════════════════════════════════════════
    // Comps Panel (x: -4, z: 2)
    // ════════════════════════════════════════════
    makeLabel('📊 Comps', -4, 2)
    if (data.comps) {
      const co = data.comps
      createBar(co.pe_ratio || 0, -5.5, 2, 0x00ff88, 0.1)
      createBar(co.ev_ebitda || 0, -4, 2, 0x00ccff, 0.1)
      createBar(co.price_to_book || 0, -2.5, 2, 0xffcc00, 0.1)
      createBar(co.price_to_sales || 0, -1, 2, 0xff6644, 0.1)
      makeLabel(`P/E:${(co.pe_ratio||0).toFixed(1)}`, -5.5, 0.5, '#00ff88', 2.5)
      makeLabel(`EV/EBITDA:${(co.ev_ebitda||0).toFixed(1)}`, -4, 0.5, '#00ccff', 2.5)
      makeLabel(`P/B:${(co.price_to_book||0).toFixed(2)}`, -2.5, 0.5, '#ffcc00', 2.5)
      makeLabel(`P/S:${(co.price_to_sales||0).toFixed(2)}`, -1, 0.5, '#ff6644', 2.5)
    }

    // ════════════════════════════════════════════
    // LBO Panel (x: 4, z: 2)
    // ════════════════════════════════════════════
    makeLabel('💼 LBO', 4, 2)
    if (data.lbo) {
      const lb = data.lbo
      createBar(lb.entry_ev || 0, 3, 2, 0x00ff88, 0.5 / 1e9)
      createBar(lb.exit_ev || 0, 4.5, 2, 0xffcc00, 0.5 / 1e9)
      createBar(lb.exit_equity || 0, 6, 2, 0x00ccff, 0.5 / 1e9)
      makeLabel(`MOIC:${(lb.moic||0).toFixed(2)}x`, 3, 0.5, '#00ff88', 2.5)
      makeLabel(`IRR:${(lb.irr_pct||0).toFixed(1)}%`, 4.5, 0.5, '#ffcc00', 2.5)
      makeLabel(`V:${lb.verdict||''}`, 6, 0.5, '#00ccff', 2.5)
    }

    // ── Connection lines between panels ──
    const connections = [
      { from: [-4, 2], to: [4, -2], color: 0x00ff8844 },  // Comps to WACC
      { from: [-4, -2], to: [4, -2], color: 0x00ff8844 },  // DCF to WACC
      { from: [4, -2], to: [4, 2], color: 0xffcc0044 },    // WACC to LBO
    ]
    connections.forEach(c => {
      const pts = [
        new THREE.Vector3(c.from[0], 0.1, c.from[1]),
        new THREE.Vector3(c.to[0], 0.1, c.to[1])
      ]
      const g = new THREE.BufferGeometry().setFromPoints(pts)
      const m = new THREE.LineDashedMaterial({ color: c.color, dashSize: 0.1, gapSize: 0.1, transparent: true, opacity: 0.3 })
      const line = new THREE.Line(g, m)
      line.computeLineDistances()
      scene.add(line)
    })

    // ── Recommendation orb ──
    const dcfRec = data.dcf?.recommendation || ''
    const lboVerdict = data.lbo?.verdict || ''
    const isBullish = dcfRec === 'BUY' || lboVerdict === 'GOOD'
    const isBearish = dcfRec === 'SELL' || lboVerdict === 'BAD'
    const orbColor = isBullish ? 0x00ff88 : isBearish ? 0xff4444 : 0xffcc00
    const orb = new THREE.Mesh(
      new THREE.SphereGeometry(0.4, 16, 16),
      new THREE.MeshStandardMaterial({ color: orbColor, emissive: orbColor, emissiveIntensity: 0.3 })
    )
    orb.position.set(0, 3, 0)
    scene.add(orb)
    // Orb glow ring
    const glowRing = new THREE.Mesh(
      new THREE.RingGeometry(0.5, 0.7, 32),
      new THREE.MeshBasicMaterial({ color: orbColor, transparent: true, opacity: 0.2, side: THREE.DoubleSide })
    )
    glowRing.position.set(0, 3, 0)
    scene.add(glowRing)
    makeLabel(isBullish ? '✅ BUY' : isBearish ? '❌ SELL' : '⚠️ HOLD', 0, 1.5, isBullish ? '#00ff88' : isBearish ? '#ff4444' : '#ffcc00', 3)

    // ── Cat roams to best panel ──
    let catX = 0, catZ = 0
    if (isBullish) { catX = -4; catZ = 2 }      // sits on Comps
    else if (isBearish) { catX = 4; catZ = 2 }   // sits on LBO
    else { catX = -4; catZ = -2 }                  // sits on DCF

    const cv = document.createElement('canvas')
    cv.width = 128; cv.height = 128
    const cctx = cv.getContext('2d')!
    cctx.font = '80px serif'
    cctx.textAlign = 'center'
    cctx.textBaseline = 'middle'
    cctx.fillText(isBearish ? '😿' : isBullish ? '😸' : '😐', 64, 64)
    const ctex = new THREE.CanvasTexture(cv)
    const cmat = new THREE.SpriteMaterial({ map: ctex, transparent: true, opacity: 0.5 })
    const cat = new THREE.Sprite(cmat)
    cat.position.set(catX, 2.5, catZ)
    cat.scale.set(2, 2, 1)
    scene.add(cat)

    // ── Animation ──
    let animTime = 0
    const animate = () => {
      animTime += 0.02
      controls.update()

      // Animate bars growing
      barTargets.current.forEach(bt => {
        const step = (bt.targetY - bt.currentH) * 0.05
        if (Math.abs(step) > 0.001) {
          bt.currentH += step
          bt.mesh.geometry.dispose()
          bt.mesh.geometry = new THREE.BoxGeometry(0.4, bt.currentH, 0.4)
          bt.mesh.position.y = bt.currentH / 2
        }
      })

      // Animate particles
      const pos = particles.geometry.attributes.position.array as Float32Array
      for (let i = 0; i < pos.length; i += 3) {
        pos[i + 1] += Math.sin(animTime + i) * 0.002
        if (pos[i + 1] > 5) pos[i + 1] = -5
      }
      particles.geometry.attributes.position.needsUpdate = true

      // Pulse glow ring
      const pulse = Math.sin(animTime * 2) * 0.1 + 0.2
      glowRing.material.opacity = pulse

      renderer.render(scene, camera)
      aid.current = requestAnimationFrame(animate)
    }
    const aid: { current: number } = { current: 0 }
    aid.current = requestAnimationFrame(animate)

    sheetzSceneRef.current = { renderer, scene, camera, controls }
    const resize = () => {
      const w2 = window.innerWidth, h2 = window.innerHeight
      camera.aspect = w2 / h2; camera.updateProjectionMatrix()
      renderer.setSize(w2, h2)
    }
    window.addEventListener('resize', resize)
    return () => {
      cancelAnimationFrame(aid.current)
      window.removeEventListener('resize', resize)
      controls.dispose(); renderer.dispose()
      try { if (renderer.domElement.parentNode) renderer.domElement.parentNode.removeChild(renderer.domElement) } catch {}
    }
  }, [data, loading, autoSpin])

  return createPortal(
    <>
      <div ref={containerRef} style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, background: '#0a1a14' }} />
      <div style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100000, display: 'flex', alignItems: 'center', gap: 12, padding: '8px 16px', background: 'rgba(0,0,0,0.8)', borderBottom: '1px solid rgba(0,255,136,0.3)' }}>
        <button onClick={onClose} style={{ padding: '4px 12px', fontSize: 13, color: '#fff', background: '#1a1a1a', border: '1px solid #444', borderRadius: 4, cursor: 'pointer', fontFamily: 'monospace' }}>← Back</button>
        <span style={{ color: '#00ff88', fontSize: 13, fontFamily: 'monospace', fontWeight: 'bold' }}>🏦 {ticker} — IB 3D</span>
        <span style={{ color: '#557755', fontSize: 11, fontFamily: 'monospace' }}>📈 DCF · ⚖️ WACC · 📊 Comps · 💼 LBO</span>
        <button onClick={() => setAutoSpin(!autoSpin)}
          style={{ padding: '2px 8px', fontSize: 11, fontFamily: 'monospace', color: autoSpin ? '#00ff88' : '#557755', background: autoSpin ? '#003322' : 'transparent', border: `1px solid ${autoSpin ? '#00ff88' : '#333'}`, borderRadius: 3, cursor: 'pointer' }}>⟳ {autoSpin ? 'ON' : 'OFF'}</button>
        {loading && <span style={{ color: '#ffcc00', fontSize: 11, fontFamily: 'monospace' }}>loading...</span>}
      </div>
      <div style={{ position: 'fixed', bottom: 8, right: 12, zIndex: 100000, fontSize: 11, fontFamily: 'monospace', color: '#557755', opacity: 0.6 }}>
        🐱 3D IB dashboard · {ticker}
      </div>
    </>,
    document.body
  )
}
