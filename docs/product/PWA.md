# Miau Finance — PWA Guide

> How to install, use, and troubleshoot the Miau Finance Progressive Web App.

---

## Installing Miau Finance as a PWA

### iOS (Safari)
1. Open `https://miau.finance` in Safari
2. Tap the **Share** button (square with arrow)
3. Scroll down and tap **Add to Home Screen**
4. Tap **Add** in the top-right corner
5. Miau Finance is now installed — launch from home screen

### Android (Chrome)
1. Open `https://miau.finance` in Chrome
2. Tap the three-dot menu (⋮)
3. Tap **Add to Home Screen**
4. Tap **Install** in the dialog
5. Miau Finance is now installed — launch from home screen

### Desktop (Chrome/Edge)
1. Open `https://miau.finance`
2. Click the install icon in the address bar (➕ or computer icon)
3. Click **Install**
4. Miau Finance launches in its own window

---

## Offline Mode

The service worker caches the following data for offline use:
- App shell (HTML, CSS, JavaScript) — always available
- API responses: market data, portfolio data — 5-minute cache
- Terminal commands: `whoami`, `help`, `cats`, `history`, `clear`, `echo`, `joke` — fully offline
- Portfolio data stored in IndexedDB — persists across sessions

### How to Test Offline
1. Open the app normally
2. Turn off Wi-Fi / enable airplane mode
3. Commands like `help` and `joke` still work
4. Market data from the last 5 minutes is available
5. Paper trades queue for execution when connection returns

### Storage Management
The app uses IndexedDB for portfolio cache. Data is automatically pruned:
- Command history: last 100 commands
- Cache storage: auto-cleaned by service worker
- App data: persists until you clear browser storage

---

## Push Notifications

Miau Finance supports push notifications through the Web Push API.

### Enabling Notifications
1. Click the notification bell icon in the terminal header
2. Click **Allow** when prompted by the browser
3. Choose notification types in Settings → Notifications

### Notification Types
| Type | Trigger | Example |
|------|---------|---------|
| **Price Alert** | Target price reached | "AAPL hit $200 — your target of $190" |
| **Trade Confirmation** | Order filled | "✅ AAPL BUY 100 filled @ $186.90" |
| **AI Ready** | AI analysis complete | "🤖 AI analysis ready for AAPL" |
| **Daily Summary** | Daily at 08:00 | "📊 Your portfolio is up 1.2% today" |

### WhatsApp & Telegram
Notifications can also be routed through:
- **WhatsApp**: Via Twilio API. Opt-in required.
- **Telegram**: Bot integration with inline keyboard for quick actions.

See Settings → Notifications to configure delivery channels.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't install | Chrome: clear service worker in `chrome://serviceworker-internals/`. Safari: enable "Add to Home Screen" in Settings → Safari → Advanced |
| Offline mode not working | Hard refresh (Cmd+Shift+R). Clear IndexedDB from DevTools → Application → Storage |
| Push notifications not arriving | Check OS notification settings. Re-subscribe in Settings → Notifications |
| App feels slow | Clear browser cache. Service worker might have stale file versions |
| Updates not appearing | Click "New version available" banner, or close all tabs and reopen |

---

## Technical Details

| Feature | Implementation |
|---------|---------------|
| Service Worker | Custom `sw.js` with Workbox precaching |
| Cache Strategy | Stale-while-revalidate for API, Cache-first for assets |
| Offline Storage | IndexedDB via `idb-keyval` library |
| Push Protocol | Web Push API with VAPID keys |
| Manifest | `manifest.json` with `display: standalone` |
| Icons | 192x192, 512x512, maskable, monochrome |
| iOS | Apple touch icon `180x180`, `apple-mobile-web-app-capable` |
