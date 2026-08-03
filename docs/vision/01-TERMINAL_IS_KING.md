```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ
```

# 🖥️ Terminal Is King — Shell Supremacy

## The Glowing Green Cursor

Miau Finance is built on a radical premise: the terminal is the future of financial software. Not dashboards. Not web apps with 47 JavaScript frameworks. The terminal. A green-on-black CRT-style interface that respects your intelligence, your bandwidth, and your attention span.

### Why the Terminal?

1. **No loading spinners** — The terminal outputs data as fast as the API can return it. No React suspense, no skeleton screens, no "optimistic UI" that lies to you.

2. **Keyboard-driven** — Every command is 1-3 words. No clicking through 15 menu items to find a feature. Type `risk AAPL` and get your VaR in 200ms.

3. **Scriptable** — Every terminal action is a command. Every command can be chained. Pipelines compose naturally. The terminal is an API explorer, not a walled garden.

4. **Universal** — SSH into a server, open a web browser, connect from your phone. The terminal works everywhere. No PWA manifest required.

### The 193 Command Standard

Miau Finance ships with 193 terminal commands organized into 8 categories:

**Market Data (42 commands):** `price`, `chart`, `sparkline`, `crypto`, `cryptomkt`, `cryptohist`, `cryptotop`, `fear`, `forex`, `sectors`, `movers`, `commodities`, `treasury`, `breadth`, `indicators`, `insider`, `short`, `ipo`, `ownership`, `ticker`, `intraday`, `technicals`, `crosschain`, `macro`, `screener`, `cpi`, `employment`, `risk-factors`, `earnings-score`, `fama-french`, `passive-float`, `quanthealth`, `fairvalue`

**Portfolio (18 commands):** `portfolios`, `portfolio`, `positions`, `trades`, `pnl`, `performance`, `anportfolio`, `anrisk`, `optperf`, `calc pnl`

**Analytics (24 commands):** `risk`, `var`, `beta`, `stress`, `greeks`, `correlation`, `benchmark`, `scenario`, `dividends`, `rolling`

**Calculators (15 commands):** `dca`, `compound`, `loan`, `retirement`, `margin`, `rebalance`, `riskparity`, `blacklitterman`, `pairtrade`, `optionspayoff`, `taxlot`, `correlation`, `montecarlo`, `drawdown`, `gas`

**Trading (12 commands):** `signals`, `multisig`, `backtest`, `optimize`, `minvar`, `eqweight`

**AI (8 commands):** `aisummary`, `aisentiment`, `aiinsight`, `aireport`, `aiallocate`, `airisk`, `aitrade`, `aichooser`

**IB Toolkit (4 commands):** `sheetz miau -dcf`, `-wacc`, `-comps`, `-lbo`

**System (20+ commands):** `help`, `clear`, `cat`, `joke`, `cats`, `map`, `miaumap`, `map2d`, `back`, `login`, `logout`, `register`

### CatProtocol — The Terminal Communication Protocol

CatProtocol is the binary protocol that governs communication between the terminal and the backend. It is:
- **Compact** — Headers are 12 bytes. Payloads are compressed with zstd.
- **Streaming** — Server-sent events for real-time data. No WebSocket handshake overhead.
- **Versioned** — Every message carries a protocol version. Backward compatible forever.

CatProtocol is not HTTP. It is not WebSocket. It is CatProtocol. Meow.

### The CRT Experience

The terminal renders with a custom CRT scanline effect:
- 3px alternating dark/light horizontal lines
- Green phosphor glow (#00ff41 with 0.15 opacity)
- Subtle horizontal jitter on text
- Flicker effect on active cursor
- Character-spacing optimized for monospace readability

This is not cosmetic. The CRT effect reduces eye strain during 12-hour trading sessions and establishes the Miau Finance brand identity. Every pixel is intentional.

### Command Autocomplete

The terminal engine provides context-aware autocomplete:
- Type `ri` and press Tab → autocompletes to `risk`
- Type `risk A` and press Tab → shows matching tickers from disk cache
- Type `--` → shows available flags
- History search with Ctrl+R matching

The autocomplete engine indexes all 193 commands plus user history plus ticker cache. It learns your patterns. It anticipates your needs. It is basically a cat that knows what you want before you do.

### The Terminal Is the Platform

Every Miau Finance app is accessible from the terminal:
- `service-desk` → opens ticket board
- `miaubook` → opens social trading
- `education` → opens course catalog
- `catgalaxy` → opens 3D service universe

The terminal is not just an interface. The terminal is the operating system of Miau Finance. Type your way to financial freedom.

```
  ╱|、
 (˚ˎ 。7    "The terminal is patient.
  |、˜〵     The terminal is wise.
  じしˍ,)ノ   The terminal purrs."
```
