# Miau Finance Design System

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "Good design is like a cat — clean, intentional, and never accidental."
```

This document describes the visual design language, component patterns, and accessibility principles of Miau Finance.

---

## Design Philosophy

Miau Finance follows a **CRT terminal retro-futuristic** aesthetic — a monospace green-on-dark palette with scanlines, phosphor glow, and subtle spring animations. Every visual choice supports the "financial cat" brand:

- **Green = profit, life, cats in sunbeams**
- **Cyan = data, insight, cool analysis**
- **Red = danger, loss, the vacuum cleaner**
- **Yellow = warning, crypto, catnip**

---

## Color Palette

| Token | Hex | HSL | Usage |
|-------|-----|-----|-------|
| `primary` | `#00ff88` | 152/100/50 | Brand, success, positive values, cat eye glow |
| `secondary` | `#00ccff` | 195/100/50 | Information, headers, links, water bowl |
| `accent` | `#ff8844` | 25/100/63 | Highlights, call-to-action, laser pointer |
| `warning` | `#ffcc00` | 48/100/50 | Warnings, crypto, signals, cat treats |
| `error` | `#ff4444` | 0/100/63 | Errors, losses, negative values, hissing |
| `info` | `#4488ff` | 220/100/63 | Secondary info, muted data |
| `background` | `#0a1a14` | 157/44/7 | Page background, deepest green-black |
| `surface` | `#0d2018` | 158/44/9 | Panel backgrounds, status bar |
| `surface-elevated` | `#122a20` | 158/42/12 | Elevated cards, modals |
| `border` | `#1a3a2a` | 158/38/16 | Borders, dividers |
| `text-dim` | `#4a7a5a` | 140/24/38 | Secondary text, timestamps |

### Color Scales

```typescript
greenScale:  ['#0a1a14', '#0d2a1e', '#113a28', '#154a32', '#195a3c',
              '#1d6a46', '#217a50', '#258a5a', '#299a64', '#00ff88']
cyanScale:   ['#0a181a', '#0d2428', '#113036', '#153c44', '#194852',
              '#1d5460', '#21606e', '#256c7c', '#29788a', '#00ccff']
```

---

## Typography

| Token | Value | Usage |
|-------|-------|-------|
| `fontFamily` | `'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace` | All text |
| `fontSize-xs` | `0.625rem` (10px) | Status bar, tooltips, micro text |
| `fontSize-sm` | `0.75rem` (12px) | Secondary info, table cells |
| `fontSize-base` | `0.875rem` (14px) | Body text, commands |
| `fontSize-lg` | `1rem` (16px) | Headings, emphasis |
| `fontSize-xl` | `1.25rem` (20px) | Large headers, ASCII art |
| `letterSpacing` | `0.05em` | Brand text, labels |

### Text Glow Classes

- `text-glow-green` — `text-shadow: 0 0 8px rgba(0,255,136,0.4)`
- `text-glow-cyan` — `text-shadow: 0 0 8px rgba(0,204,255,0.4)`
- `text-glow-red` — `text-shadow: 0 0 8px rgba(255,68,68,0.4)`
- `text-glow-yellow` — `text-shadow: 0 0 8px rgba(255,204,0,0.4)`

---

## Spacing Scale

```typescript
spacing: {
  xs:  '0.25rem',  // 4px — micro gaps
  sm:  '0.5rem',   // 8px — compact gaps
  md:  '0.75rem',  // 12px — default padding
  lg:  '1rem',     // 16px — comfortable padding
  xl:  '1.5rem',   // 24px — section spacing
  '2xl': '2rem',   // 32px — layout breaks
  '3xl': '3rem',   // 48px — major sections
}
```

---

## CRT Terminal Effects

### Scanlines
```css
.crt::after {
  background: repeating-linear-gradient(
    0deg,
    transparent, transparent 2px,
    rgba(0,0,0,0.12) 2px, rgba(0,0,0,0.12) 4px
  );
  animation: scanline-move 10s linear infinite;
}
```

### Phosphor Bloom
```css
.crt-bloom {
  filter: blur(1px) brightness(1.1) contrast(1.05) saturate(0.95);
}
```

### Beam Cursor
```css
.terminal-cursor-smooth {
  width: 8px; height: 16px;
  background: linear-gradient(to bottom, transparent, #00ff88 20%, #88ffbb, #00ff88 80%, transparent);
  box-shadow: 0 0 8px rgba(0,255,136,0.5);
  animation: cursor-blink-smooth 1.2s ease-in-out infinite;
}
```

### Screen Glitch
```css
@keyframes screen-flicker {
  0%, 99.5%, 100% { opacity: 1; }
  99.6%, 99.8% { opacity: 0.85; }
}
@keyframes glitch-skew {
  0%, 100% { transform: skewX(0deg); }
  90%, 92% { transform: skewX(0.5deg); }
}
```

---

## Animations

| Animation | Duration | Easing | Usage |
|-----------|----------|--------|-------|
| `scale-in` | 300ms | `cubic-bezier(0.16,1,0.3,1)` | Component entrance |
| `slide-in-up` | 300ms | `cubic-bezier(0.16,1,0.3,1)` | Toast notifications |
| `slide-in-down` | 400ms | `cubic-bezier(0.16,1,0.3,1)` | Status bar entrance |
| `fade-in` | 200ms | `ease` | Line output appearance |
| `scale-in-up` | 500ms | Spring (damping: 0.7) | Major component mount |
| `map-pulse` | 2s | `ease-in-out` | Map data point pulse |
| `shimmer` | 1.5s | `ease-in-out` | Loading skeleton |
| `spinner-ring` | 0.8s | `linear` infinite | Loading spinner |
| `scanline-move` | 10s | `linear` infinite | CRT scanline |
| `cursor-blink-smooth` | 1.2s | `ease-in-out` infinite | Cursor pulse |
| `glow-pulse` | 2s | `ease-in-out` infinite | Connection dot |
| `screen-flicker` | 0.15s | `linear` infinite | CRT authenticity |
| `glitch-skew` | periodic | `ease` infinite | Glitch effect |

### Spring Physics
```css
transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
```
This spring curve provides a subtle overshoot and settle — like a cat landing on its feet.

---

## Component Patterns

### Glass Panel
```css
.glass-panel {
  background: rgba(18, 42, 32, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(0, 255, 136, 0.15);
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}
```

### Glow Border
```css
.glow-border {
  border: 1px solid rgba(0, 255, 136, 0.2);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glow-border:hover {
  border-color: rgba(0, 255, 136, 0.6);
  box-shadow: 0 0 16px rgba(0, 255, 136, 0.15);
}
```

### Pill Label
```css
/* Rounded pill with background, used for map labels */
background: rgba(10, 26, 20, 0.85);
border: 1px solid currentColor;
border-radius: 12px;
padding: 2px 8px;
```

---

## Accessibility (a11y)

### Principles
1. **Perceivable** — All information is conveyed through both visual (color, glow) and structural (aria, labels) means
2. **Operable** — Full keyboard navigation, no mouse-only interactions
3. **Understandable** — Consistent command syntax, predictable output format
4. **Robust** — Works with screen readers, high-contrast mode, reduced motion

### Implemented Features

| Feature | Where | Status |
|---------|-------|--------|
| `role="application"` | Terminal container | ✅ |
| `role="log"` / `aria-live="polite"` | Output area | ✅ |
| `aria-label` on input | Command input | ✅ |
| `aria-autocomplete="list"` | Autocomplete suggestions | ✅ |
| `aria-expanded` | Suggestion visibility | ✅ |
| Skip-to-input link | Hidden focusable link | ✅ |
| `role="status"` | Status bar | ✅ |
| `role="combobox"` | Command input | ✅ |
| Keyboard shortcuts overlay | `Ctrl+H` | ✅ |
| `prefers-reduced-motion` | CSS media query | ✅ |
| High-contrast color scheme | Green-on-dark default | ✅ |
| Focus visible styles | Input, buttons | ✅ |
| `aria-label` on map controls | WorldMap | pending |
| Screen reader output for map data | WorldMap | pending |

### Keyboard Navigation

| Key | Action |
|-----|--------|
| **Tab** | Autocomplete current command/ticker |
| **↑ / ↓** | Navigate command history |
| **Enter** | Execute command |
| **Escape** | Dismiss autocomplete / close modals |
| **Ctrl+L** | Clear terminal |
| **Ctrl+H** | Show keyboard shortcuts overlay |
| **Ctrl+C** | Cancel loading operation |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Z-Index Scale

| Layer | z-index | Component |
|-------|---------|-----------|
| Base | 0 | Page content |
| Terminal | 10 | Terminal layer |
| Map | 0 | Map layer (behind terminal) |
| Heatmap | 0 | Heatmap overlay |
| Toast | 50 | Toast notifications |
| Modal | 100 | Shortcuts overlay |
| Skip link | 9999 | Accessibility skip link |
| CRT scanlines | 9999 | CRT effect overlay |

---

## Map Visualization Palette

```typescript
mapColors: {
  land:           '#0a1a14',    // Base land
  continent:      '#1a3a2a',    // Continent fill (alpha 0.22)
  continentGL:    '#00ff88',    // Continent glow highlight
  ocean:          '#061210',    // Deep ocean
  grid:           '#1a4a2a',    // Grid lines (alpha 0.30)
  outline:        '#00cc88',    // Globe outline (alpha 0.65)
  pointGreen:     '#00ff88',    // Positive data points
  pointRed:       '#ff4444',    // Negative data points
  pointCyan:      '#00ccff',    // Neutral data points
  arc:            '#00ff8840',  // Trade relationship arcs
  atmosphere:     '#00ff8810',  // Atmosphere glow
  labelBg:        'rgba(10,26,20,0.85)',  // Pill label background
}
```

---

## File Locations

| File | Content |
|------|---------|
| `frontend/src/design/tokens.ts` | Design tokens (colors, spacing, typography, animations) |
| `frontend/src/index.css` | Global styles, CRT effects, keyframes, utility classes |
| `frontend/src/components/Transitions.tsx` | Animation components (FadeIn, SlideIn, ScaleIn, Stagger) |
| `frontend/src/components/CatLoaders.tsx` | Loading animations (paws, walking, yarn, napping, hunting) |
| `docs/DESIGN.md` | This file — design system documentation |

---

## Contributing to Design

1. Read `frontend/src/design/tokens.ts` for all design tokens
2. Use the tailwind `@apply` pattern in `index.css` for component classes
3. All animations must use the spring curve: `cubic-bezier(0.16, 1, 0.3, 1)`
4. New components must have accessibility labels
5. Test with `prefers-reduced-motion: reduce` enabled
6. Maintain the cat theme — if it doesn't feel like a cat, redesign it

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "A beautiful terminal is a happy terminal.
               Make it purr."
```

---
_[Back to README](../README.md) | [Architecture](./ARCHITECTURE.md) | [Developer Guide](./DEVELOPER.md)_
