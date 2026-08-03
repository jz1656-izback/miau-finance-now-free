# 🐱 MIAU FINANCE — Testing Guide

## 93 Tests · All Passing ✅

### Run Tests
```bash
cd frontend
npm test              # All tests
npm run test:watch    # Watch mode
npm run test:e2e      # Playwright E2E
```

### Test Files
```
tests/
├── commands.test.ts     # 40+ command tests
├── map.test.ts          # Map component
├── globe.test.ts        # MiauGlobe
├── catgalaxy.test.ts    # Cat galaxy
├── pwa.test.ts          # PWA/offline
└── responsive.test.ts   # Mobile
```

### Writing Tests
```typescript
import { describe, it, expect } from 'vitest'

describe('market commands', () => {
  it('should parse price command', () => {
    const result = executeCommand('price AAPL')
    expect(result).toHaveProperty('ticker', 'AAPL')
  })
})
```

### CI/CD
GitHub Actions: `npm test` → `tsc --noEmit` → build → lint
