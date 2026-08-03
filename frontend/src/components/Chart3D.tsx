import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import * as THREE from 'three'
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

interface Props { ticker: string; onClose: () => void }

export default function Chart3D({ ticker, onClose }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [data, setData] = useState<any[]>([])
  const [period, setPeriod] = useState('1y')
  const [loading, setLoading] = useState(true)
  const [autoRotate, setAutoRotate] = useState(false)
  const [hoveredCandle, setHoveredCandle] = useState<any>(null)
  const sceneRef = useRef<any>(null)
  const controlsRef = useRef<OrbitControls | null>(null)
  const raycaster = useRef(new THREE.Raycaster())
  const mouse = useRef(new THREE.Vector2())

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
      if (e.key === 's' || e.key === 'S') {
        const canvas = document.querySelector('canvas')
        if (canvas) {
          const link = document.createElement('a')
          link.download = `${ticker}_3d.png`
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
    fetch(`/api/v1/market/historical/${ticker}?period=${period}`, { headers })
      .then(r => r.ok ? r.json() : null)
      .then(d => {
        const records = d?.records || []
        if (records.length > 1) { setData(records); setLoading(false); return }
        const syn = []
        let p = 100 + Math.random() * 200
        for (let i = 0; i < 100; i++) {
          const hi = p * (1 + Math.random() * 0.03)
          const lo = p * (1 - Math.random() * 0.03)
          const op = lo + Math.random() * (hi - lo)
          const cl = lo + Math.random() * (hi - lo)
          syn.push({ date: '', open: op, high: hi, low: lo, close: cl, volume: Math.round(1000000 + Math.random() * 5000000) })
          p += (Math.random() - 0.48) * p * 0.02
        }
        setData(syn)
        setLoading(false)
      })
      .catch(() => { setLoading(false) })
  }, [ticker, period])

  // ── Compute moving averages ──
  const ma = (arr: number[], period: number) => {
    const result: (number | null)[] = []
    for (let i = 0; i < arr.length; i++) {
      if (i < period - 1) { result.push(null); continue }
      let s = 0
      for (let j = i - period + 1; j <= i; j++) s += arr[j]
      result.push(s / period)
    }
    return result
  }

  useEffect(() => {
    if (!containerRef.current || data.length === 0) return
    const container = containerRef.current
    if (sceneRef.current) {
      try { if (sceneRef.current.renderer.domElement.parentNode) sceneRef.current.renderer.domElement.parentNode.removeChild(sceneRef.current.renderer.domElement) } catch {}
      sceneRef.current.renderer.dispose()
    }

    const w = window.innerWidth, h = window.innerHeight
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0a1a14)

    const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100)
    camera.position.set(data.length * 0.4, data.length * 0.3, data.length * 0.5)
    camera.lookAt(data.length / 2, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(w, h)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.08
    controls.target.set(data.length / 2, 0, 0)
    controls.minDistance = 5
    controls.maxDistance = data.length * 2
    controls.autoRotate = autoRotate
    controls.autoRotateSpeed = 2
    controlsRef.current = controls

    const ambient = new THREE.AmbientLight(0x404060, 0.6)
    scene.add(ambient)
    const dir = new THREE.DirectionalLight(0xffffff, 0.8)
    dir.position.set(5, 10, 7)
    scene.add(dir)

    const grid = new THREE.GridHelper(data.length * 1.5, 10, 0x00ff88, 0x003322)
    grid.position.x = data.length / 2
    scene.add(grid)

    const prices = data.map(r => r.close)
    const minP = Math.min(...prices)
    const maxP = Math.max(...prices)
    const range = maxP - minP || 1
    const candleW = 0.6
    const volAvg = data.reduce((s, r) => s + r.volume, 0) / data.length

    // Y-axis labels
    const makeLabel = (text: string, x: number, y: number, z: number, color = '#00ff88', size = 2) => {
      const canvas = document.createElement('canvas')
      canvas.width = 128; canvas.height = 48
      const ctx = canvas.getContext('2d')!
      ctx.fillStyle = color
      ctx.font = '24px monospace'
      ctx.textAlign = 'center'
      ctx.fillText(text, 64, 32)
      const tex = new THREE.CanvasTexture(canvas)
      const mat = new THREE.SpriteMaterial({ map: tex, transparent: true })
      const sprite = new THREE.Sprite(mat)
      sprite.position.set(x, y, z)
      sprite.scale.set(size, size * 0.4, 1)
      scene.add(sprite)
    }
    makeLabel(ticker, data.length / 2, range * 0.7, 0, '#00ff88')

    // Store candle meshes for raycasting
    const candleMeshes: THREE.Mesh[] = []
    const candleData: any[] = []

    // Candles
    for (let i = 0; i < data.length; i++) {
      const d = data[i]
      const up = d.close >= d.open
      const bodyH = Math.abs(d.close - d.open) / range * 5
      const bodyY = (Math.min(d.close, d.open) - minP) / range * 5 + bodyH / 2
      const wickH = (d.high - d.low) / range * 5
      const wickY = (d.low - minP) / range * 5 + wickH / 2
      const changePct = ((d.close - d.open) / d.open) * 100
      const intensity = Math.min(Math.abs(changePct) / 5, 1)
      const g = up ? Math.round(0x88 + (0xff - 0x88) * intensity) : 0x44
      const r = up ? 0x00 : Math.round(0xff - (0xff - 0x44) * intensity)
      const color = (r << 16) | (g << 8) | 0x00
      const volScale = d.volume / volAvg * 0.8

      const box = new THREE.Mesh(
        new THREE.BoxGeometry(candleW, Math.max(bodyH, 0.01), candleW),
        new THREE.MeshStandardMaterial({ color, emissive: color, emissiveIntensity: 0.15 })
      )
      box.position.set(i, bodyY, 0)
      box.userData = { index: i, ...d }
      scene.add(box)
      candleMeshes.push(box)
      candleData.push(d)

      if (wickH > bodyH + 0.01) {
        const wickMat = new THREE.MeshBasicMaterial({ color })
        const wick = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, wickH, 4), wickMat)
        wick.position.set(i, wickY, 0)
        scene.add(wick)
      }

      // Volume bar
      const volBox = new THREE.Mesh(
        new THREE.BoxGeometry(candleW * 0.8, Math.max(volScale, 0.02), candleW * 0.8),
        new THREE.MeshBasicMaterial({ color: up ? 0x224433 : 0x442222, transparent: true, opacity: 0.4 })
      )
      volBox.position.set(i, -volScale / 2 - 0.3, 0)
      scene.add(volBox)

      // Volume spark particles on high volume
      if (d.volume > volAvg * 1.5) {
        const sparkCount = Math.min(Math.floor(d.volume / volAvg), 8)
        for (let s = 0; s < sparkCount; s++) {
          const spark = new THREE.Mesh(
            new THREE.SphereGeometry(0.04, 4, 4),
            new THREE.MeshBasicMaterial({ color: up ? 0x00ff88 : 0xff4444, transparent: true, opacity: 0.6 })
          )
          spark.position.set(i + (Math.random() - 0.5) * 0.5, bodyY + Math.random() * 0.5, (Math.random() - 0.5) * 0.5)
          scene.add(spark)
        }
      }
    }

    // ── Smooth price line ──
    const linePoints: THREE.Vector3[] = []
    for (let i = 0; i < data.length; i++) {
      const y = (data[i].close - minP) / range * 5
      linePoints.push(new THREE.Vector3(i, y, 0.35))
    }
    const lineGeo = new THREE.BufferGeometry().setFromPoints(linePoints)
    const lineMat = new THREE.LineBasicMaterial({ color: 0x44ffaa, transparent: true, opacity: 0.6 })
    const line = new THREE.Line(lineGeo, lineMat)
    scene.add(line)

    // ── Moving Averages ──
    const ma20 = ma(prices, 20)
    const ma50 = ma(prices, 50)

    ;[[ma20, 0xffcc00, 0.4], [ma50, 0xff8844, 0.3]].forEach(([maArr, maColor, maOpacity]) => {
      const pts: THREE.Vector3[] = []
      ;(maArr as (number | null)[]).forEach((v, i) => {
        if (v !== null) pts.push(new THREE.Vector3(i, (v - minP) / range * 5, 0.3))
      })
      if (pts.length > 1) {
        const g = new THREE.BufferGeometry().setFromPoints(pts)
        const m = new THREE.LineBasicMaterial({ color: maColor as number, transparent: true, opacity: maOpacity as number })
        scene.add(new THREE.Line(g, m))
      }
    })

    // ── Hover crosshair ──
    const hoverGroup = new THREE.Group()
    hoverGroup.visible = false
    scene.add(hoverGroup)

    // Crosshair lines
    const hLineMat = new THREE.LineBasicMaterial({ color: 0x00ff88, transparent: true, opacity: 0.3 })
    const vLineMat = new THREE.LineBasicMaterial({ color: 0x00ff88, transparent: true, opacity: 0.3 })

    const mouseMove = (e: MouseEvent) => {
      mouse.current.x = (e.clientX / window.innerWidth) * 2 - 1
      mouse.current.y = -(e.clientY / window.innerHeight) * 2 + 1

      raycaster.current.setFromCamera(mouse.current, camera)
      const intersects = raycaster.current.intersectObjects(candleMeshes)
      if (intersects.length > 0) {
        const hit = intersects[0].object
        const idx = hit.userData.index
        if (idx !== undefined && candleData[idx]) {
          setHoveredCandle(candleData[idx])
          hoverGroup.visible = true
          // Update crosshair
          while (hoverGroup.children.length) hoverGroup.remove(hoverGroup.children[0])
          const y = (candleData[idx].close - minP) / range * 5
          const hGeo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(-1, y, 0), new THREE.Vector3(data.length + 1, y, 0)
          ])
          const hLine = new THREE.Line(hGeo, hLineMat)
          hoverGroup.add(hLine)
          const vGeo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(idx, -1, 0), new THREE.Vector3(idx, range / 5 + 0.5, 0)
          ])
          const vLine = new THREE.Line(vGeo, vLineMat)
          hoverGroup.add(vLine)
          return
        }
      }
      setHoveredCandle(null)
      hoverGroup.visible = false
    }
    renderer.domElement.addEventListener('mousemove', mouseMove)

    // ── Cat reacts to trend ──
    const firstPrice = prices[0]
    const lastPrice = prices[prices.length - 1]
    const trend = ((lastPrice - firstPrice) / firstPrice) * 100
    const catEmoji = trend > 5 ? '😸' : trend > 2 ? '😺' : trend > -2 ? '😐' : trend > -5 ? '😾' : '😿'

    const catCanvas = document.createElement('canvas')
    catCanvas.width = 128; catCanvas.height = 128
    const ctx2 = catCanvas.getContext('2d')!
    ctx2.font = '80px serif'
    ctx2.textAlign = 'center'
    ctx2.textBaseline = 'middle'
    ctx2.fillText(catEmoji, 64, 64)
    const catTex = new THREE.CanvasTexture(catCanvas)
    const catMat = new THREE.SpriteMaterial({ map: catTex, transparent: true, opacity: 0.5 })
    const catSprite = new THREE.Sprite(catMat)
    catSprite.position.set(data.length + 1, range * 0.3, 0)
    catSprite.scale.set(2, 2, 1)
    scene.add(catSprite)

    // Trend label
    const trendStr = `${trend > 0 ? '+' : ''}${trend.toFixed(1)}%`
    makeLabel(trendStr, data.length + 1, range * 0.3 - 1, 0, trend > 0 ? '#00ff88' : '#ff4444', 1.5)

    // ── Animation loop ──
    const animate = () => {
      controls.update()
      renderer.render(scene, camera)
      aid.current = requestAnimationFrame(animate)
    }
    const aid: { current: number } = { current: 0 }
    aid.current = requestAnimationFrame(animate)

    sceneRef.current = { renderer, scene, camera, controls }

    const resize = () => {
      const w2 = window.innerWidth, h2 = window.innerHeight
      camera.aspect = w2 / h2
      camera.updateProjectionMatrix()
      renderer.setSize(w2, h2)
    }
    window.addEventListener('resize', resize)

    return () => {
      cancelAnimationFrame(aid.current)
      window.removeEventListener('resize', resize)
      renderer.domElement.removeEventListener('mousemove', mouseMove)
      controls.dispose()
      renderer.dispose()
      try { if (renderer.domElement.parentNode) renderer.domElement.parentNode.removeChild(renderer.domElement) } catch {}
    }
  }, [data, autoRotate])

  return createPortal(
    <>
      <div ref={containerRef} style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, background: '#0a1a14' }} />
      <div style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100000, display: 'flex', alignItems: 'center', gap: 12, padding: '8px 16px', background: 'rgba(0,0,0,0.8)', borderBottom: '1px solid rgba(0,255,136,0.3)' }}>
        <button onClick={onClose} style={{ padding: '4px 12px', fontSize: 13, color: '#fff', background: '#1a1a1a', border: '1px solid #444', borderRadius: 4, cursor: 'pointer', fontFamily: 'monospace' }}>← Back</button>
        <span style={{ color: '#00ff88', fontSize: 13, fontFamily: 'monospace', fontWeight: 'bold' }}>📈 {ticker} 3D</span>
        <span style={{ color: '#557755', fontSize: 11, fontFamily: 'monospace' }}>hover candle · drag orbit · scroll zoom</span>
        {['1m','3m','6m','1y','5y'].map(p => (
          <button key={p} onClick={() => setPeriod(p)}
            style={{ padding: '2px 8px', fontSize: 11, fontFamily: 'monospace', color: period === p ? '#00ff88' : '#557755', background: period === p ? '#003322' : 'transparent', border: `1px solid ${period === p ? '#00ff88' : '#333'}`, borderRadius: 3, cursor: 'pointer' }}>{p.toUpperCase()}</button>
        ))}
        <button onClick={() => setAutoRotate(!autoRotate)}
          style={{ padding: '2px 8px', fontSize: 11, fontFamily: 'monospace', color: autoRotate ? '#00ff88' : '#557755', background: autoRotate ? '#003322' : 'transparent', border: `1px solid ${autoRotate ? '#00ff88' : '#333'}`, borderRadius: 3, cursor: 'pointer' }}>⟳ {autoRotate ? 'ON' : 'OFF'}</button>
        {loading && <span style={{ color: '#ffcc00', fontSize: 11, fontFamily: 'monospace' }}>loading...</span>}
      </div>
      {/* Hover tooltip */}
      {hoveredCandle && (
        <div style={{ position: 'fixed', bottom: 40, left: '50%', transform: 'translateX(-50%)', zIndex: 100000, background: 'rgba(0,0,0,0.9)', border: '1px solid #00ff8844', borderRadius: 8, padding: '8px 16px', fontFamily: 'monospace', fontSize: 12, color: '#ccc', display: 'flex', gap: 16, pointerEvents: 'none' }}>
          <span style={{ color: '#00ff88' }}>O: ${hoveredCandle.open?.toFixed(2)}</span>
          <span style={{ color: '#00ff88' }}>H: ${hoveredCandle.high?.toFixed(2)}</span>
          <span style={{ color: '#ff4444' }}>L: ${hoveredCandle.low?.toFixed(2)}</span>
          <span style={{ color: hoveredCandle.close >= hoveredCandle.open ? '#00ff88' : '#ff4444' }}>C: ${hoveredCandle.close?.toFixed(2)}</span>
          <span style={{ color: '#888' }}>Vol: {(hoveredCandle.volume / 1e6).toFixed(1)}M</span>
        </div>
      )}
      <div style={{ position: 'fixed', bottom: 8, right: 12, zIndex: 100000, fontSize: 11, fontFamily: 'monospace', color: '#557755', opacity: 0.6 }}>
        🐱 3D chart · {data.length} candles
      </div>
    </>,
    document.body
  )
}
