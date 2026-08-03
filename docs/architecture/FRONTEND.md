# 🐱 MIAU FINANCE — Frontend Architecture

## React 18 · TypeScript 5 · Vite 6 · Three.js · Tailwind CSS

### Structure
```
frontend/src/
├── App.tsx              # Root + billing redirects
├── components/          # Terminal, Pricing, Charts, Globe, Map
│   ├── Terminal.tsx     # Main terminal (1400+ lines)
│   ├── CFODashboard.tsx
│   ├── TunaWallet.tsx   # Crypto wallet display
│   └── ...
├── lib/
│   ├── commands.ts      # ALL 160+ commands (5800 lines)
│   ├── api.ts           # HTTP client with JWT auth
│   ├── auth.ts          # LocalStorage token management
│   └── themes.ts        # Terminal themes + CRT effects
└── index.css            # Scanlines, CRT, green phosphor
```

### Key Decisions
- **Terminal-first**: Everything runs inside CRT terminal
- **Single command file**: 5800-line switch statement
- **State-based routing**: No React Router, conditional renders
- **PWA**: Installable, offline mode, push notifications
- **Three.js 3D**: MiauGlobe with globe.gl wrapper

### Commands by Category
Market(30+) | TA(17) | Quant(8) | AI(8) | Portfolio(10) | Fixed Income(6) | Maps(4) | CFO(5) | Jobs(3) | Billing(4)

> *"5800 lines. 160 commands. 0 broken tests." 🐱*
