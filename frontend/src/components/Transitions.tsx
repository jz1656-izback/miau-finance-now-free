import { useState, useEffect, useRef, CSSProperties, ReactNode } from 'react'

/* ── Hooks ── */

function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(false)
  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
    setPrefersReduced(mq.matches)
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [])
  return prefersReduced
}

/* ── FadeIn ── */

interface FadeInProps {
  children: ReactNode
  duration?: number
  delay?: number
  className?: string
}

export function FadeIn({ children, duration = 300, delay = 0, className = '' }: FadeInProps) {
  const reduced = useReducedMotion()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay)
    return () => clearTimeout(t)
  }, [delay])

  const style: CSSProperties = reduced
    ? {}
    : {
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(8px)',
        transition: `opacity ${duration}ms cubic-bezier(0.16, 1, 0.3, 1), transform ${duration}ms cubic-bezier(0.16, 1, 0.3, 1)`,
      }

  return <div className={className} style={style}>{children}</div>
}

/* ── SlideIn ── */

interface SlideInProps {
  children: ReactNode
  direction?: 'up' | 'down' | 'left' | 'right'
  duration?: number
  delay?: number
  className?: string
}

export function SlideIn({ children, direction = 'up', duration = 400, delay = 0, className = '' }: SlideInProps) {
  const reduced = useReducedMotion()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay)
    return () => clearTimeout(t)
  }, [delay])

  const offsets: Record<string, string> = {
    up: 'translateY(24px)',
    down: 'translateY(-24px)',
    left: 'translateX(24px)',
    right: 'translateX(-24px)',
  }

  const style: CSSProperties = reduced
    ? {}
    : {
        opacity: visible ? 1 : 0,
        transform: visible ? 'translate(0)' : offsets[direction],
        transition: `opacity ${duration}ms cubic-bezier(0.16, 1, 0.3, 1), transform ${duration}ms cubic-bezier(0.16, 1, 0.3, 1)`,
      }

  return <div className={className} style={style}>{children}</div>
}

/* ── ScaleIn ── */

interface ScaleInProps {
  children: ReactNode
  duration?: number
  delay?: number
  className?: string
}

export function ScaleIn({ children, duration = 350, delay = 0, className = '' }: ScaleInProps) {
  const reduced = useReducedMotion()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), delay)
    return () => clearTimeout(t)
  }, [delay])

  const style: CSSProperties = reduced
    ? {}
    : {
        opacity: visible ? 1 : 0,
        transform: visible ? 'scale(1)' : 'scale(0.92)',
        transition: `opacity ${duration}ms cubic-bezier(0.16, 1, 0.3, 1), transform ${duration}ms cubic-bezier(0.34, 1.56, 0.64, 1)`,
      }

  return <div className={className} style={style}>{children}</div>
}

/* ── StaggerChildren ── */

interface StaggerChildrenProps {
  children: ReactNode[]
  staggerDelay?: number
  baseDelay?: number
  childClassName?: string
}

export function StaggerChildren({
  children,
  staggerDelay = 60,
  baseDelay = 0,
  childClassName = '',
}: StaggerChildrenProps) {
  return (
    <>
      {children.map((child, i) => (
        <FadeIn key={i} delay={baseDelay + i * staggerDelay} className={childClassName}>
          {child}
        </FadeIn>
      ))}
    </>
  )
}

/* ── Typewriter ── */

interface TypewriterProps {
  text: string
  speed?: number
  delay?: number
  className?: string
  onComplete?: () => void
}

export function Typewriter({ text, speed = 40, delay = 0, className = '', onComplete }: TypewriterProps) {
  const reduced = useReducedMotion()
  const [displayed, setDisplayed] = useState(reduced ? text : '')
  const idxRef = useRef(0)

  useEffect(() => {
    if (reduced) {
      setDisplayed(text)
      onComplete?.()
      return
    }

    idxRef.current = 0
    setDisplayed('')

    const startTimeout = setTimeout(() => {
      idxRef.current = 0
      const interval = setInterval(() => {
        idxRef.current++
        setDisplayed(text.slice(0, idxRef.current))
        if (idxRef.current >= text.length) {
          clearInterval(interval)
          onComplete?.()
        }
      }, speed)
      return () => clearInterval(interval)
    }, delay)

    return () => clearTimeout(startTimeout)
  }, [text, speed, delay, reduced, onComplete])

  return <span className={className}>{displayed}</span>
}

/* ── PulseLoader (three dots) ── */

interface PulseLoaderProps {
  className?: string
  color?: string
}

export function PulseLoader({ className = '', color = '#00ff88' }: PulseLoaderProps) {
  return (
    <span className={`inline-flex items-center gap-1 ${className}`}>
      {[0, 1, 2].map(i => (
        <span
          key={i}
          className="inline-block rounded-full"
          style={{
            width: 6,
            height: 6,
            backgroundColor: color,
            animation: `pulse-dot 1.4s cubic-bezier(0.4, 0, 0.6, 1) ${i * 0.2}s infinite`,
          }}
        />
      ))}
    </span>
  )
}

/* ── Spinner ── */

interface SpinnerProps {
  className?: string
  size?: number
  color?: string
}

export function Spinner({ className = '', size = 16, color = '#00ff88' }: SpinnerProps) {
  return (
    <span
      className={`inline-block ${className}`}
      style={{
        width: size,
        height: size,
        border: `2px solid ${color}33`,
        borderTopColor: color,
        borderRadius: '50%',
        animation: 'spinner-rotate 0.8s linear infinite',
      }}
    />
  )
}

/* ── ProgressBar ── */

interface ProgressBarProps {
  progress: number
  className?: string
  color?: string
  height?: number
}

export function ProgressBar({ progress, className = '', color = '#00ff88', height = 4 }: ProgressBarProps) {
  const reduced = useReducedMotion()
  const clamped = Math.max(0, Math.min(100, progress))

  return (
    <div
      className={`overflow-hidden ${className}`}
      style={{
        height,
        background: 'rgba(0, 255, 136, 0.1)',
        borderRadius: height / 2,
      }}
    >
      <div
        style={{
          width: `${clamped}%`,
          height: '100%',
          background: color,
          borderRadius: height / 2,
          transition: reduced ? 'none' : `width 300ms cubic-bezier(0.16, 1, 0.3, 1)`,
        }}
      />
    </div>
  )
}

/* ── LoadingBlock ── */

interface LoadingBlockProps {
  className?: string
  lines?: number
  width?: string | number
}

export function LoadingBlock({ className = '', lines = 3, width = '100%' }: LoadingBlockProps) {
  return (
    <div className={`flex flex-col gap-2 ${className}`} style={{ width }}>
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className="shimmer rounded"
          style={{
            height: 14,
            width: i === lines - 1 ? '60%' : '100%',
            background: 'rgba(0, 255, 136, 0.06)',
            borderRadius: 2,
          }}
        />
      ))}
    </div>
  )
}

/* ── TerminalLoading ── */

interface TerminalLoadingProps {
  text?: string
  className?: string
}

export function TerminalLoading({ text = 'processing', className = '' }: TerminalLoadingProps) {
  return (
    <div className={`flex items-center gap-2 text-dim text-sm ${className}`}>
      <span className="spinner-ring" />
      <span>{text}...</span>
    </div>
  )
}

/* ── SkeletonText ── */

interface SkeletonTextProps {
  className?: string
  width?: string | number
  height?: number
}

export function SkeletonText({ className = '', width = '100%', height = 14 }: SkeletonTextProps) {
  return (
    <div
      className={`shimmer rounded ${className}`}
      style={{
        width,
        height,
        background: 'rgba(0, 255, 136, 0.05)',
        borderRadius: height / 4,
      }}
    />
  )
}

/* ── PageTransition ── */

interface PageTransitionProps {
  children: ReactNode
  className?: string
}

export function PageTransition({ children, className = '' }: PageTransitionProps) {
  const reduced = useReducedMotion()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  const style: CSSProperties = reduced
    ? {}
    : {
        opacity: mounted ? 1 : 0,
        transform: mounted ? 'translateY(0)' : 'translateY(16px)',
        transition: 'opacity 400ms cubic-bezier(0.16, 1, 0.3, 1), transform 400ms cubic-bezier(0.16, 1, 0.3, 1)',
      }

  return <div className={className} style={style}>{children}</div>
}
