import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import * as THREE from 'three'
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

interface Props { tickers: string[]; onClose: () => void }

export default function Compare3D({ tickers, onClose }: Props) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [data, setData] = useState<Record<string, any[]>>({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [onClose])

  useEffect(() => {
    if (tickers.length === 0) return
    setLoading(true)
    const headers: Record<string, string> = localStorage.getItem('miau_token')
      ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
    Promise.all(tickers.map(t =>
      fetch(`/api/v1/market/historical/${t}?period=1y`, { headers }).then(r => r.ok ? r.json() : null)
    )).then(results => {
      const map: Record<string, any[]> = {}
      for (let i = 0; i < tickers.length; i++) {
        const records = results[i]?.records || []
        if (records.length > 1) map[tickers[i]] = records
      }
      setData(map)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [tickers])

  useEffect(() => {
    if (!containerRef.current || Object.keys(data).length === 0) return
    const container = containerRef.current
    const w = window.innerWidth, h = window.innerHeight

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x0a1a14)

    const camera = new THREE.PerspectiveCamera(45, w / h, 0.1, 100)
    camera.position.set(0, 3, 8)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(w, h)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.08
    controls.target.set(0, 0, 0)
    controls.minDistance = 3
    controls.maxDistance = 20

    const ambient = new THREE.AmbientLight(0x404060, 0.6)
    scene.add(ambient)
    const dir = new THREE.DirectionalLight(0xffffff, 0.8)
    dir.position.set(5, 10, 7)
    scene.add(dir)

    const colors = [0x00ff88, 0x00ccff, 0xffcc00, 0xff6644, 0xcc88ff]
    const entries = Object.entries(data)
    const spacing = Math.max(3, entries.length * 1.5)

    entries.forEach(([ticker, records], idx) => {
      const prices = records.map(r => r.close)
      const minP = Math.min(...prices)
      const maxP = Math.max(...prices)
      const range = maxP - minP || 1
      const color = colors[idx % colors.length]
      const xOffset = (idx - (entries.length - 1) / 2) * spacing
      const points: THREE.Vector3[] = []

      for (let i = 0; i < prices.length; i++) {
        const y = ((prices[i] - minP) / range) * 3
        points.push(new THREE.Vector3(xOffset + (i / prices.length) * 2 - 1, y, 0))
      }

      // Line
      const geo = new THREE.BufferGeometry().setFromPoints(points)
      const mat = new THREE.LineBasicMaterial({ color, linewidth: 2 })
      const line = new THREE.Line(geo, mat)
      scene.add(line)

      // Dots on line
      const dotPositions = new Float32Array(points.length * 3)
      for (let i = 0; i < points.length; i++) {
        dotPositions[i * 3] = points[i].x
        dotPositions[i * 3 + 1] = points[i].y
        dotPositions[i * 3 + 2] = points[i].z
      }
      const dotGeo = new THREE.BufferGeometry()
      dotGeo.setAttribute('position', new THREE.BufferAttribute(dotPositions, 3))
      const dotMat = new THREE.PointsMaterial({ size: 0.06, color, transparent: true, opacity: 0.5 })
      const dots = new THREE.Points(dotGeo, dotMat)
      scene.add(dots)

      // Label
      const cv = document.createElement('canvas')
      cv.width = 128; cv.height = 48
      const cx = cv.getContext('2d')!
      cx.fillStyle = '#' + color.toString(16).padStart(6, '0')
      cx.font = 'bold 28px monospace'
      cx.textAlign = 'center'
      cx.fillText(ticker, 64, 32)
      const tex = new THREE.CanvasTexture(cv)
      const sMat = new THREE.SpriteMaterial({ map: tex, transparent: true })
      const sprite = new THREE.Sprite(sMat)
      sprite.position.set(xOffset, 3.5, 0)
      sprite.scale.set(2, 0.75, 1)
      scene.add(sprite)
    })

    // Grid
    const grid = new THREE.GridHelper(10 + entries.length * 3, 10, 0x00ff88, 0x002211)
    scene.add(grid)

    // Cat
    const cv = document.createElement('canvas')
    cv.width = 128; cv.height = 128
    const ctx = cv.getContext('2d')!
    ctx.font = '80px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'
    ctx.fillText('🐱', 64, 64)
    const cTex = new THREE.CanvasTexture(cv)
    const cMat = new THREE.SpriteMaterial({ map: cTex, transparent: true, opacity: 0.3 })
    const cat = new THREE.Sprite(cMat)
    cat.position.set(0, -1, 3)
    cat.scale.set(2, 2, 1)
    scene.add(cat)

    const animRef = { current: 0 }
    const animate = () => { controls.update(); renderer.render(scene, camera); animRef.current = requestAnimationFrame(animate) }
    animRef.current = requestAnimationFrame(animate)

    const resize = () => {
      const w2 = window.innerWidth, h2 = window.innerHeight
      camera.aspect = w2 / h2; camera.updateProjectionMatrix()
      renderer.setSize(w2, h2)
    }
    window.addEventListener('resize', resize)

    return () => {
      cancelAnimationFrame(animRef.current)
      window.removeEventListener('resize', resize)
      controls.dispose(); renderer.dispose()
      try { if (renderer.domElement.parentNode) renderer.domElement.parentNode.removeChild(renderer.domElement) } catch {}
    }
  }, [data])

  return createPortal(
    <>
      <div ref={containerRef} style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 99999, background: '#0a1a14' }} />
      <div style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100000, display: 'flex', alignItems: 'center', gap: 12, padding: '8px 16px', background: 'rgba(0,0,0,0.8)', borderBottom: '1px solid rgba(0,255,136,0.3)' }}>
        <button onClick={onClose} style={{ padding: '4px 12px', fontSize: 13, color: '#fff', background: '#1a1a1a', border: '1px solid #444', borderRadius: 4, cursor: 'pointer', fontFamily: 'monospace' }}>← Back</button>
        <span style={{ color: '#00ff88', fontSize: 13, fontFamily: 'monospace', fontWeight: 'bold' }}>📊 {tickers.join(' vs ')}</span>
        <span style={{ color: '#557755', fontSize: 11, fontFamily: 'monospace' }}>3D comparison · drag to orbit</span>
        {loading && <span style={{ color: '#ffcc00', fontSize: 11, fontFamily: 'monospace' }}>loading...</span>}
      </div>
    </>,
    document.body
  )
}
