/**
 * Miau Finance Design System Tokens
 *
 * Cat-themed terminal aesthetic design system.
 * All values tuned for 60fps animations and CRT aesthetics.
 *
 * @design-dev
 */

/* ── Core Colors ── */

/** Primary brand color - vibrant green */
export const primary = '#00ff88'
export const primaryRgba = (a: number) => `rgba(0, 255, 136, ${a})`

/** Secondary brand color - bright cyan */
export const secondary = '#00ccff'
export const secondaryRgba = (a: number) => `rgba(0, 204, 255, ${a})`

/** Accent color - warm orange */
export const accent = '#ff8844'
export const accentRgba = (a: number) => `rgba(255, 136, 68, ${a})`

/** Warning color - amber yellow */
export const warning = '#ffcc00'
export const warningRgba = (a: number) => `rgba(255, 204, 0, ${a})`

/** Error/danger color - soft red */
export const error = '#ff4444'
export const errorRgba = (a: number) => `rgba(255, 68, 68, ${a})`

/** Success color - same as primary but separate token */
export const success = '#00ff88'
export const successRgba = (a: number) => `rgba(0, 255, 136, ${a})`

/** Info color - blue */
export const info = '#4488ff'
export const infoRgba = (a: number) => `rgba(68, 136, 255, ${a})`

/* ── Color Scales (for depth/gradients) ── */

export const greenScale = {
  50: '#e6fff0',
  100: '#b3ffd9',
  200: '#80ffc2',
  300: '#4dffaa',
  400: '#1aff93',
  500: '#00ff88',
  600: '#00cc6d',
  700: '#009952',
  800: '#006636',
  900: '#00331b',
} as const

export const cyanScale = {
  50: '#e6f9ff',
  100: '#b3f0ff',
  200: '#80e5ff',
  300: '#4dd9ff',
  400: '#1accff',
  500: '#00ccff',
  600: '#00a3cc',
  700: '#007a99',
  800: '#005266',
  900: '#002933',
} as const

/* ── Semantic Colors ── */

/** Base background - dark green-black */
export const background = '#0a1a14'
export const backgroundRgba = (a: number) => `rgba(10, 26, 20, ${a})`

/** Surface color - slightly lighter than background */
export const surface = '#0d2018'
export const surfaceRgba = (a: number) => `rgba(13, 32, 24, ${a})`

/** Elevated surface - for cards/panels */
export const surfaceElevated = '#112a1e'
export const surfaceElevatedRgba = (a: number) => `rgba(17, 42, 30, ${a})`

/** Primary text - bright green */
export const textPrimary = '#00ff88'
export const textPrimaryRgba = (a: number) => `rgba(0, 255, 136, ${a})`

/** Secondary text - light cyan */
export const textSecondary = '#00ccff'
export const textSecondaryRgba = (a: number) => `rgba(0, 204, 255, ${a})`

/** Dim/muted text - washed out green */
export const textDim = '#4a7a5a'
export const textDimRgba = (a: number) => `rgba(74, 122, 90, ${a})`

/** Bright text - lighter green for emphasis */
export const textBright = '#88ffbb'
export const textBrightRgba = (a: number) => `rgba(136, 255, 187, ${a})`

/** Inverse text for dark backgrounds */
export const textInverse = '#0a1a14'

/** Border color for UI elements */
export const border = '#1a3a2a'
export const borderRgba = (a: number) => `rgba(26, 58, 42, ${a})`

/** Border hover/active */
export const borderActive = '#2a5a3a'

/** Highlight color for selections */
export const highlight = '#00ff8855'
export const highlightRgba = (a: number) => `rgba(0, 255, 136, ${a * 0.33})`

/* ── Map / Visualization Colors ── */

export const mapColors = {
  ocean: '#0a1a2e',
  oceanDeep: '#070f1a',
  grid: 'rgba(0, 150, 255, 0.04)',
  continentFill: 'rgba(0, 200, 150, 0.08)',
  continentStroke: 'rgba(0, 255, 180, 0.5)',
  globeOutline: 'rgba(0, 255, 180, 0.6)',
  atmosphere: 'rgba(0, 100, 200, 0.1)',
  panelBg: 'rgba(10, 26, 46, 0.85)',
  panelBorder: 'rgba(0, 200, 150, 0.4)',
  label: '#88ddbb',
  up: '#00ff88',
  down: '#ff4444',
} as const

/* ── Spacing (4px grid) ── */

export const spacing = {
  '0': 0,
  'px': 1,
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  '2xl': 32,
  '3xl': 48,
  '4xl': 64,
  '5xl': 96,
} as const

/** Spacing helper for inline styles */
export const space = (key: keyof typeof spacing) => `${spacing[key]}px`

/* ── Typography ── */

export const fontFamily = {
  mono: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace",
  sans: "'Inter', 'SF Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  serif: "'Georgia', 'Times New Roman', serif",
} as const

export const fontSize = {
  '2xs': 10,
  xs: 11,
  sm: 12,
  md: 14,
  lg: 16,
  xl: 20,
  '2xl': 24,
  '3xl': 32,
  '4xl': 40,
} as const

export const lineHeight = {
  tight: 1.2,
  snug: 1.35,
  normal: 1.5,
  relaxed: 1.75,
} as const

export const fontWeight = {
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const

export const letterSpacing = {
  tight: '-0.02em',
  normal: '0',
  wide: '0.05em',
  wider: '0.1em',
} as const

/* ── Borders ── */

export const borderRadius = {
  none: 0,
  sm: 2,
  md: 4,
  lg: 8,
  xl: 12,
  full: 9999,
} as const

export const borderWidth = {
  thin: 1,
  normal: 2,
  thick: 4,
} as const

/* ── Shadows (glow effects) ── */

export const shadows = {
  /** Soft green glow */
  greenGlow: '0 0 5px rgba(0, 255, 136, 0.3), 0 0 15px rgba(0, 255, 136, 0.1)',
  /** Medium green glow */
  greenGlowStrong: '0 0 10px rgba(0, 255, 136, 0.5), 0 0 30px rgba(0, 255, 136, 0.2)',
  /** Intense green glow */
  greenGlowIntense: '0 0 20px rgba(0, 255, 136, 0.6), 0 0 60px rgba(0, 255, 136, 0.3)',
  /** Cyan glow effect */
  cyanGlow: '0 0 5px rgba(0, 204, 255, 0.3), 0 0 15px rgba(0, 204, 255, 0.1)',
  /** Cyan strong glow */
  cyanGlowStrong: '0 0 10px rgba(0, 204, 255, 0.5), 0 0 30px rgba(0, 204, 255, 0.2)',
  /** Red/danger glow */
  redGlow: '0 0 5px rgba(255, 68, 68, 0.3), 0 0 15px rgba(255, 68, 68, 0.1)',
  /** Yellow glow */
  yellowGlow: '0 0 5px rgba(255, 204, 0, 0.3), 0 0 15px rgba(255, 204, 0, 0.1)',
  /** Text shadow for glow */
  textGlow: '0 0 8px rgba(0, 255, 136, 0.4)',
  textGlowCyan: '0 0 8px rgba(0, 204, 255, 0.4)',
  textGlowRed: '0 0 8px rgba(255, 68, 68, 0.4)',
  textGlowYellow: '0 0 8px rgba(255, 204, 0, 0.4)',
  /** Inner shadow for depth */
  inset: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
} as const

/* ── Animations ── */

export const duration = {
  instant: 50,
  fast: 150,
  normal: 300,
  slow: 500,
  verySlow: 1000,
  cinematic: 1500,
} as const

export const easing = {
  easeOut: 'cubic-bezier(0.16, 1, 0.3, 1)',
  easeInOut: 'cubic-bezier(0.65, 0, 0.35, 1)',
  easeOutExpo: 'cubic-bezier(0.16, 1, 0.3, 1)',
  easeInOutQuad: 'cubic-bezier(0.45, 0, 0.25, 1)',
  spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
} as const

/* ── Z-Index Layers ── */

export const zIndex = {
  base: 0,
  map: 5,
  terminal: 10,
  overlay: 50,
  modal: 100,
  tooltip: 200,
  notification: 300,
  scanline: 9998,
  crt: 9999,
} as const

/* ── CRT / Terminal Specific ── */

export const crt = {
  /** Scanline color */
  scanlineColor: 'rgba(0, 0, 0, 0.12)',
  /** Scanline height in px */
  scanlineHeight: 4,
  /** Curvature vignette intensity */
  curvatureOpacity: 0.45,
  /** Screen flicker animation duration */
  flickerDuration: '8s',
  /** Subtle chromatic aberration offset */
  fringeOffset: 0.5,
  /** Terminal cursor blink rate */
  cursorBlinkRate: '1s',
  /** Background color */
  bg: '#0a1a14',
  /** Status bar bg */
  statusBarBg: '#0d2018',
} as const

/* ── Breakpoints (px) ── */

export const breakpoints = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const
