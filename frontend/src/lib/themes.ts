/**
 * 🐱 CAT TERMINAL THEMES
 * Phase 2.5 INNOVATION.md #5 — Customizable terminal color schemes.
 * Persists to localStorage.
 */

export interface TerminalTheme {
  id: string
  name: string
  emoji: string
  description: string
  colors: {
    bg: string
    bgSecondary: string
    border: string
    text: string
    textBright: string
    textDim: string
    green: string
    accent: string
    red: string
    yellow: string
    cyan: string
    purple: string
    orange: string
  }
}

export const THEMES: TerminalTheme[] = [
  {
    id: 'sleek-black',
    name: 'Sleek Black Cat',
    emoji: '🐱⬛',
    description: 'Pure black bg, neon green text — the classic hacker aesthetic.',
    colors: {
      bg: '#0a1a14',
      bgSecondary: '#0d2018',
      border: '#1a3a2a',
      text: '#d1d5db',
      textBright: '#ffffff',
      textDim: '#6b7280',
      green: '#00ff88',
      accent: '#00ff88',
      red: '#ff4444',
      yellow: '#ffcc00',
      cyan: '#00ddff',
      purple: '#c084fc',
      orange: '#ff8800',
    },
  },
  {
    id: 'orange-tabby',
    name: 'Orange Tabby',
    emoji: '🐱🟠',
    description: 'Warm amber tones — cozy vibes for late-night trading.',
    colors: {
      bg: '#1a1410',
      bgSecondary: '#201a14',
      border: '#3a2a1a',
      text: '#e5d5c0',
      textBright: '#fff8f0',
      textDim: '#8a7a6a',
      green: '#ffaa44',
      accent: '#ff8800',
      red: '#ff6644',
      yellow: '#ffcc44',
      cyan: '#ffcc88',
      purple: '#d4a574',
      orange: '#ff7700',
    },
  },
  {
    id: 'siamese',
    name: 'Siamese Point',
    emoji: '🐱💙',
    description: 'Dark blue with light blue accents — elegant and refined.',
    colors: {
      bg: '#0a1428',
      bgSecondary: '#0d1832',
      border: '#1a2846',
      text: '#c0d0e8',
      textBright: '#e8f0ff',
      textDim: '#6080a0',
      green: '#44aaff',
      accent: '#4488ff',
      red: '#ff5588',
      yellow: '#ffcc44',
      cyan: '#66ddff',
      purple: '#8888ff',
      orange: '#ff8855',
    },
  },
  {
    id: 'snow-white',
    name: 'Snow White Cat',
    emoji: '🐱⚪',
    description: 'Light theme — soft colors for daytime trading.',
    colors: {
      bg: '#f5f0eb',
      bgSecondary: '#ede8e3',
      border: '#d5d0cb',
      text: '#333333',
      textBright: '#111111',
      textDim: '#888888',
      green: '#228855',
      accent: '#227744',
      red: '#cc3333',
      yellow: '#aa8800',
      cyan: '#3388aa',
      purple: '#7744aa',
      orange: '#cc6622',
    },
  },
  {
    id: 'calico',
    name: 'Calico',
    emoji: '🐱🎨',
    description: 'Multi-color gradient effects — playful and energetic.',
    colors: {
      bg: '#14101a',
      bgSecondary: '#1a1420',
      border: '#2a1a3a',
      text: '#e0d0f0',
      textBright: '#f8f0ff',
      textDim: '#8878a0',
      green: '#44ff88',
      accent: '#ff88cc',
      red: '#ff4488',
      yellow: '#ffcc44',
      cyan: '#44ddff',
      purple: '#cc88ff',
      orange: '#ff8844',
    },
  },
  {
    id: 'matrix-cat',
    name: 'Matrix Cat',
    emoji: '🐱💚',
    description: 'Green-on-black digital rain — hack the markets.',
    colors: {
      bg: '#000a00',
      bgSecondary: '#001400',
      border: '#003300',
      text: '#00cc44',
      textBright: '#00ff55',
      textDim: '#006622',
      green: '#00ff44',
      accent: '#00ff44',
      red: '#ff2222',
      yellow: '#44ff00',
      cyan: '#00ffaa',
      purple: '#00aa44',
      orange: '#88ff00',
    },
  },
  {
    id: 'neon-ocean',
    name: 'Neon Ocean',
    emoji: '🐱🌊',
    description: 'Deep sea blues with electric cyan — dive into data.',
    colors: {
      bg: '#000a1a',
      bgSecondary: '#00142a',
      border: '#003355',
      text: '#88ddff',
      textBright: '#bbeeff',
      textDim: '#4488aa',
      green: '#00ffcc',
      accent: '#00ddff',
      red: '#ff4466',
      yellow: '#ffcc00',
      cyan: '#00eeff',
      purple: '#8866ff',
      orange: '#ff8844',
    },
  },
  {
    id: 'sunset-paw',
    name: 'Sunset Paw',
    emoji: '🐱🌅',
    description: 'Warm sunset gradients — pink, purple, and gold.',
    colors: {
      bg: '#1a0a14',
      bgSecondary: '#24101e',
      border: '#3a1a2a',
      text: '#e8c8d8',
      textBright: '#ffddee',
      textDim: '#886878',
      green: '#ff88aa',
      accent: '#ff4488',
      red: '#ff2244',
      yellow: '#ffcc44',
      cyan: '#ff88cc',
      purple: '#cc44ff',
      orange: '#ff6622',
    },
  },
  {
    id: 'forest-paws',
    name: 'Forest Paws',
    emoji: '🐱🌲',
    description: 'Earthy greens and browns — natural, grounded trading.',
    colors: {
      bg: '#0a140e',
      bgSecondary: '#0e1a12',
      border: '#1a3524',
      text: '#b8d4c0',
      textBright: '#d8f0d8',
      textDim: '#688870',
      green: '#55cc66',
      accent: '#44aa55',
      red: '#cc5533',
      yellow: '#ccaa33',
      cyan: '#44aa88',
      purple: '#888866',
      orange: '#bb6633',
    },
  },
  {
    id: 'midnight-meow',
    name: 'Midnight Meow',
    emoji: '🐱🌙',
    description: 'Inky dark with icy blue — for nocturnal traders.',
    colors: {
      bg: '#060612',
      bgSecondary: '#0a0a1e',
      border: '#1a1a3a',
      text: '#8888cc',
      textBright: '#bbbbee',
      textDim: '#555588',
      green: '#6666ff',
      accent: '#4444ee',
      red: '#ff3366',
      yellow: '#ddaa00',
      cyan: '#44aadd',
      purple: '#8844ff',
      orange: '#ff6622',
    },
  },
]

const STORAGE_KEY = 'miau_terminal_theme'

export function getTheme(): TerminalTheme {
  try {
    const id = localStorage.getItem(STORAGE_KEY)
    const theme = THEMES.find(t => t.id === id)
    if (theme) return theme
  } catch { /* ignore */ }
  return THEMES[0] // sleek-black default
}

export function setTheme(themeId: string): TerminalTheme {
  const theme = THEMES.find(t => t.id === themeId) || THEMES[0]
  localStorage.setItem(STORAGE_KEY, theme.id)
  // Notify all terminal instances
  window.dispatchEvent(new CustomEvent('miau-theme-changed', { detail: theme }))
  return theme
}

export function listThemes(): TerminalTheme[] {
  return THEMES
}
