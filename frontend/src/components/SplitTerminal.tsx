import { useState, useRef, useEffect, useCallback, Fragment } from 'react'
import Terminal from './Terminal'

interface LeafPane {
  id: string
  type: 'leaf'
}

interface SplitPane {
  id: string
  type: 'split'
  direction: 'horizontal' | 'vertical'
  children: PaneNode[]
  sizes: number[]
}

type PaneNode = LeafPane | SplitPane

let idCounter = 0
function genId(): string {
  return `pane-${++idCounter}`
}

function createLeaf(): LeafPane {
  return { id: genId(), type: 'leaf' }
}

function cloneTree(node: PaneNode): PaneNode {
  if (node.type === 'leaf') return { id: node.id, type: 'leaf' }
  return {
    id: node.id,
    type: 'split',
    direction: node.direction,
    children: node.children.map(cloneTree),
    sizes: [...node.sizes],
  }
}

function findParent(tree: PaneNode, targetId: string): { parent: SplitPane; index: number } | null {
  if (tree.type === 'split') {
    for (let i = 0; i < tree.children.length; i++) {
      if (tree.children[i].id === targetId) return { parent: tree, index: i }
      const found = findParent(tree.children[i], targetId)
      if (found) return found
    }
  }
  return null
}

function replaceNode(tree: PaneNode, targetId: string, replacement: PaneNode): PaneNode {
  if (tree.id === targetId) return replacement
  if (tree.type === 'split') {
    return {
      ...tree,
      children: tree.children.map(c => replaceNode(c, targetId, replacement)),
    }
  }
  return tree
}

function findNode(tree: PaneNode, targetId: string): PaneNode | null {
  if (tree.id === targetId) return tree
  if (tree.type === 'split') {
    for (const child of tree.children) {
      const found = findNode(child, targetId)
      if (found) return found
    }
  }
  return null
}

export default function SplitTerminal() {
  const [layout, setLayout] = useState<PaneNode>(createLeaf())
  const [focusedPane, setFocusedPane] = useState<string>('')
  const [chordActive, setChordActive] = useState(false)
  const chordTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const layoutRef = useRef(layout)
  const focusedRef = useRef(focusedPane)
  const [showChord, setShowChord] = useState(false)
  const [startTime] = useState(Date.now())

  layoutRef.current = layout
  focusedRef.current = focusedPane

  useEffect(() => {
    if (layout.type === 'leaf') {
      setFocusedPane(layout.id)
    }
  }, [layout])

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === 'b') {
        e.preventDefault()
        e.stopPropagation()
        setChordActive(true)
        setShowChord(true)
        if (chordTimeoutRef.current) clearTimeout(chordTimeoutRef.current)
        chordTimeoutRef.current = setTimeout(() => {
          setChordActive(false)
          setShowChord(false)
        }, 1200)
        return
      }

      if (chordActive) {
        setChordActive(false)
        setShowChord(false)
        if (chordTimeoutRef.current) clearTimeout(chordTimeoutRef.current)

        const currentLayout = layoutRef.current
        const currentFocused = focusedRef.current

        if (e.key === '%') {
          e.preventDefault()
          e.stopPropagation()
          const newLeaf = createLeaf()
          const splitPane: SplitPane = {
            id: genId(),
            type: 'split',
            direction: 'horizontal',
            children: [createLeaf(), newLeaf],
            sizes: [50, 50],
          }
          setLayout(prev => replaceNode(prev, currentFocused, splitPane))
          setFocusedPane(newLeaf.id)
          return
        }

        if (e.key === '"') {
          e.preventDefault()
          e.stopPropagation()
          const newLeaf = createLeaf()
          const splitPane: SplitPane = {
            id: genId(),
            type: 'split',
            direction: 'vertical',
            children: [createLeaf(), newLeaf],
            sizes: [50, 50],
          }
          setLayout(prev => replaceNode(prev, currentFocused, splitPane))
          setFocusedPane(newLeaf.id)
          return
        }

        const arrowMap: Record<string, string> = {
          ArrowLeft: 'prev',
          ArrowRight: 'next',
          ArrowUp: 'prev',
          ArrowDown: 'next',
        }

        if (arrowMap[e.key]) {
          e.preventDefault()
          e.stopPropagation()
          const parentInfo = findParent(currentLayout, currentFocused)
          if (parentInfo) {
            const { parent, index } = parentInfo
            const dir = arrowMap[e.key]
            const targetIdx = dir === 'next' ? Math.min(index + 1, parent.children.length - 1) : Math.max(index - 1, 0)
            if (targetIdx !== index) {
              setFocusedPane(parent.children[targetIdx].id)
            }
          }
          return
        }

        if (e.key === 'z') {
          e.preventDefault()
          e.stopPropagation()
          const parentInfo = findParent(currentLayout, currentFocused)
          if (parentInfo) {
            setFocusedPane(parentInfo.parent.id)
          }
          return
        }
      }
    }

    document.addEventListener('keydown', handleKey, true)
    return () => {
      document.removeEventListener('keydown', handleKey, true)
      if (chordTimeoutRef.current) clearTimeout(chordTimeoutRef.current)
    }
  }, [chordActive])

  const handleFocus = useCallback((id: string) => {
    setFocusedPane(id)
  }, [])

  const [resizing, setResizing] = useState<{
    parentId: string
    index: number
    direction: 'horizontal' | 'vertical'
    startX: number
    startY: number
  } | null>(null)

  useEffect(() => {
    if (!resizing) return

    const handleMouseMove = (e: MouseEvent) => {
      const r = resizing
      setLayout(prev => {
        const newLayout = cloneTree(prev)
        const resizeParent = findNode(newLayout, r.parentId) as SplitPane | null
        if (!resizeParent) return prev

        const delta = r.direction === 'horizontal'
          ? (e.clientX - r.startX) / window.innerWidth * 100
          : (e.clientY - r.startY) / window.innerHeight * 100

        const newSizes = [...resizeParent.sizes]
        const minSize = 15
        let s1 = newSizes[r.index] + delta
        let s2 = newSizes[r.index + 1] - delta
        if (s1 < minSize) { s2 -= (minSize - s1); s1 = minSize }
        if (s2 < minSize) { s1 -= (minSize - s2); s2 = minSize }
        if (s1 < minSize || s2 < minSize) return prev

        newSizes[r.index] = s1
        newSizes[r.index + 1] = s2

        const updateSizes = (node: PaneNode): PaneNode => {
          if (node.id === r.parentId && node.type === 'split') {
            return { ...node, sizes: newSizes }
          }
          if (node.type === 'split') {
            return { ...node, children: node.children.map(updateSizes) }
          }
          return node
        }
        return newLayout.id === r.parentId && newLayout.type === 'split'
          ? { ...newLayout, sizes: newSizes } as SplitPane
          : updateSizes(newLayout)
      })
    }

    const handleMouseUp = () => {
      setResizing(null)
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    }
  }, [resizing])

  const handleResizeStart = useCallback((parentId: string, index: number, direction: 'horizontal' | 'vertical') => {
    return (e: React.MouseEvent) => {
      e.preventDefault()
      setResizing({ parentId, index, direction, startX: e.clientX, startY: e.clientY })
      document.body.style.cursor = direction === 'horizontal' ? 'col-resize' : 'row-resize'
      document.body.style.userSelect = 'none'
    }
  }, [])

  const renderPane = (node: PaneNode): React.ReactNode => {
    if (node.type === 'leaf') {
      const isFocused = node.id === focusedPane
      return (
        <div
          key={node.id}
          className="flex-1 flex flex-col overflow-hidden min-w-0 min-h-0 relative"
          onClick={() => handleFocus(node.id)}
        >
          <div
            className="flex-1 flex flex-col"
            style={{
              outline: isFocused ? '1px solid rgba(0, 255, 136, 0.25)' : '1px solid rgba(0, 255, 136, 0.05)',
              transition: 'outline 0.2s ease',
            }}
          >
            <Terminal embedded />
          </div>
        </div>
      )
    }

    const isHorizontal = node.direction === 'horizontal'
    return (
      <div
        key={node.id}
        className={`flex flex-1 min-w-0 min-h-0 ${isHorizontal ? 'flex-row' : 'flex-col'}`}
      >
        {node.children.map((child, i) => (
          <Fragment key={child.id}>
            <div
              className="flex min-w-0 min-h-0 overflow-hidden"
              style={{
                flex: `${node.sizes[i]} 1 0`,
                animation: 'paneFadeIn 0.2s ease',
              }}
            >
              {renderPane(child)}
            </div>
            {i < node.children.length - 1 && (
              <div
                className="resize-handle"
                style={{
                  [isHorizontal ? 'width' : 'height']: '4px',
                  [isHorizontal ? 'height' : 'width']: '100%',
                  flexShrink: 0,
                  cursor: isHorizontal ? 'col-resize' : 'row-resize',
                  position: 'relative',
                  zIndex: 10,
                }}
                onMouseDown={handleResizeStart(node.id, i, node.direction)}
              >
                <div
                  style={{
                    position: 'absolute',
                    [isHorizontal ? 'top' : 'left']: '50%',
                    [isHorizontal ? 'left' : 'top']: '50%',
                    transform: 'translate(-50%, -50%)',
                    [isHorizontal ? 'height' : 'width']: '24px',
                    [isHorizontal ? 'width' : 'height']: '3px',
                    borderRadius: '2px',
                    background: 'rgba(0, 255, 136, 0.3)',
                    transition: 'background 0.15s ease, transform 0.15s ease',
                  }}
                />
              </div>
            )}
          </Fragment>
        ))}
      </div>
    )
  }

  const uptime = Math.floor((Date.now() - startTime) / 1000)
  const uptimeStr = `${Math.floor(uptime / 3600)}h ${Math.floor((uptime % 3600) / 60)}m`

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden" style={{ background: '#0a1a14' }}>
      <div className="flex items-center justify-between px-4 py-1 text-xs" style={{ background: '#0d2018', borderBottom: '1px solid #1a3a2a' }}>
        <div className="flex items-center gap-4">
          <span className="text-green font-bold">🐱 MIAU FINANCE</span>
           <span className="text-dim">v2.5.1</span>
          <span className="text-dim">|</span>
          <span className="text-dim">uptime: {uptimeStr}</span>
        </div>
        <div className="flex items-center gap-4">
          {showChord && <span className="text-yellow">⏎ CHORD</span>}
          <span className="text-dim">Ctrl+B · %"' ↩</span>
        </div>
      </div>

      {showChord && (
        <div
          style={{
            position: 'fixed',
            top: 8,
            right: 16,
            zIndex: 9999,
            color: '#ffcc00',
            fontSize: '11px',
            fontFamily: '"JetBrains Mono", monospace',
            background: 'rgba(10, 26, 20, 0.9)',
            padding: '4px 10px',
            borderRadius: '4px',
            border: '1px solid rgba(255, 204, 0, 0.3)',
            pointerEvents: 'none',
          }}
        >
          Ctrl+B · %=vert │ "=horiz │ arrows=nav
        </div>
      )}

      <div className="flex flex-1 overflow-hidden">
        {renderPane(layout)}
      </div>

      <style>{`
        @keyframes paneFadeIn {
          from { opacity: 0; transform: scale(0.96); }
          to { opacity: 1; transform: scale(1); }
        }
        .resize-handle:hover div {
          background: rgba(0, 255, 136, 0.6) !important;
          transform: translate(-50%, -50%) scale(1.3) !important;
        }
      `}</style>
    </div>
  )
}
