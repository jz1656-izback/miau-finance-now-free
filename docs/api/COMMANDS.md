# Miau Finance Terminal Commands

## Overview

The Miau Finance terminal provides a green-on-dark, CRT-styled command-line interface to access all financial data and analytics. Commands are executed by typing after the `miau@finance:~$` prompt. Results are displayed as formatted tables, color-coded values, ASCII charts, and sparklines — all within the terminal.

### Keyboard Shortcuts

| Key | Action |
|---|---|
| **TAB** | Autocomplete command or ticker |
| **↑ / ↓** | Scroll through command history |
| **Enter** | Execute command |
| **Ctrl+C** | Cancel current operation |
| **Escape** | Dismiss autocomplete suggestions |

### Output Conventions

- **Green** — Positive values, prices, tables
- **Red** — Negative values, errors
- **Cyan** — Information, headers
- **Yellow** — Warnings, signals, crypto
- **Dim** — Loading states, secondary info
- `$1.2K`, `$45.5M`, `$2.3B` — Formatted currency values
- `+1.25%`, `-0.50%` — Percentage changes with sign
- `▁▂▃▄▅▆▇█` — Sparkline characters for compact charts

---

## 📊 Market Data Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `price` | `<ticker>` | Live price, change, high, low, volume + sparkline | `price AAPL` |
| `chart` | `<ticker>` | ASCII candlestick chart (1 month) | `chart TSLA` |
| `sparkline` | `<t1> <t2> ...` | Compact sparklines for multiple tickers | `sparkline AAPL MSFT GOOGL` |
| `crypto` | `[--top]` | Bitcoin price + Fear & Greed; `--top` shows top 10 | `crypto` / `crypto --top` |
| `btc` | — | Alias for `crypto` | `btc` |
| `cryptomkt` | — | Crypto market overview (cap, volume, dominance) | `cryptomkt` |
| `cryptohist` | `<coin>` | Crypto historical ASCII chart (7 days) | `cryptohist bitcoin` |
| `cryptotop` | `[limit]` | Top N cryptocurrencies table | `cryptotop 10` |
| `fear` | — | Fear & Greed index (color-coded) | `fear` |
| `forex` | — | Forex rates (base USD) | `forex` |
| `sectors` | — | Sector performance table | `sectors` |
| `movers` | — | Top gainers and losers | `movers` |
| `commodities` | — | Commodity prices (Gold, Oil, Silver, etc.) | `commodities` |
| `treasury` | — | US Treasury yields (2y, 5y, 10y, 30y) | `treasury` |
| `breadth` | — | Market breadth indices (S&P, NASDAQ, VIX, etc.) | `breadth` |
| `indicators` | — | US market indicators (GDP, CPI, unemployment) | `indicators` |

### Example: `price AAPL`

```
😸 AAPL  Apple Inc.  ▁▂▃▄▅▆▇█
price:   $186.9000
change:  +1.25%
high:    $187.50
low:     $185.20
volume:  45,200,000
```

### Example: `sparkline AAPL MSFT GOOGL`

```
AAPL   ▁▂▃▄▅▆▇█  $186.90  +2.35 (+1.25%)
MSFT   ▂▁▃▄▅▆▇█  $420.15  +5.10 (+1.23%)
GOOGL  ▃▂▁▄▅▆▇█  $142.30  -1.20 (-0.83%)
```

### Example: `sectors`

```
Ticker   Sector                         Price     Change
──────────────────────────────────────────────────────────
XLK      Technology Select Sector...   $215.50   +1.82%
XLF      Financial Select Sector...    $38.20    +0.45%
XLV      Health Care Select Sector..   $142.80   -0.32%
```

---

## 📈 Portfolio Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `login` | `<user> <pass>` | Authenticate with platform | `login <username> <password>` |
| `logout` | — | End session and clear token | `logout` |
| `ontypes` | — | List ontology types | `ontypes` |
| `onobjects` | — | List ontology objects | `onobjects` |
| `instypes` | — | List instrument types | `instypes` |
| `sectorslist` | — | List all sectors | `sectorslist` |
| `anportfolio` | `<id>` | Portfolio analytics JSON dump | `anportfolio <uuid>` |
| `anrisk` | `<id>` | Portfolio risk analytics JSON dump | `anrisk <uuid>` |
| `attrib` | `[full\|sector\|security\|factor] <pid>` | Portfolio attribution (Brinson, factor, security) | `attrib full <pid>` |
| `pnl` | `[days] [pid]` | Portfolio/Platform P&L series | `pnl 30` |
| `performance` | `<inst_id>` | Instrument performance metrics | `performance <uuid>` |
| `pipelines` | — | List pipeline runs | `pipelines` |
| `optperf` | — | Optimizer performance metrics | `optperf` |
| `newsbatch` | `<t1,t2...>` | Batch news for tickers | `newsbatch AAPL,MSFT` |
| `cryptotop` | `[limit]` | Top N cryptocurrencies | `cryptotop 10` |

### Example: `portfolios`

```
ID         Name                         Value       Pos
───────────────────────────────────────────────────────────
a1b2c3d4   Tech Growth Fund          $2,500,000     15
e5f6g7h8   Value Income Portfolio    $1,800,000     22
```

### Example: `summary`

```
Miau Finance Platform:
Portfolios:    3
Instruments:   1,250
Trades:        5,432
Total AUM:     $4,300,000
Unrealised P&L: $125,000
```

### Example: `pnl 30`

```
fetching P&L timeseries (30 days)...
Last 10 days:
Date         P&L          Change
─────────────────────────────────────
2024-01-15   $12,500.00   +2.50%
2024-01-14   $8,200.00    +1.65%
```

---

## 🎯 Trading Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `trades` | — | Recent trades (last 20) | `trades` |
| `signals` | `<ticker>` | Technical trading signals (SMA, MACD, RSI) | `signals AAPL` |
| `multisig` | `<t1,t2,...>` | Multi-asset signals | `multisig AAPL,MSFT,GOOGL` |
| `backtest` | `<ticker>` | SMA crossover backtest results | `backtest AAPL` |

### Example: `signals TSLA`

```
TSLA @ $245.80  |  Trend: bullish  |  RSI: 58.2
SMA20: $238.50  SMA50: $225.00  MACD: 2.35
Signals:
  BUY [strong]: MACD — MACD crossed above signal line
  BUY [medium]: SMA — Price above SMA50
```

### Example: `backtest AAPL`

```
SMA(20/50) Backtest — AAPL
Return:       +18.50%
Buy&Hold:     +15.20%
Alpha:        +3.30%
Sharpe:       1.25
Max DD:       8.50%
Win Rate:     55.0%
Trades:       12
Final:        $118,500.00
```

---

## ⚡ Analytics Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `optimize` | `<t1,t2,...>` | Max Sharpe portfolio optimization | `optimize AAPL,MSFT,GOOGL` |
| `minvar` | `<t1,t2,...>` | Min variance portfolio | `minvar AAPL,MSFT,GOOGL` |
| `eqweight` | `<t1,t2,...>` | Equal weight portfolio | `eqweight AAPL,MSFT,GOOGL` |
| `optperf` | — | Optimizer performance metrics | `optperf` |
| `risk` | `<ticker>` | Comprehensive risk report (VaR, Beta, Stress) | `risk AAPL` |
| `var` | `<ticker>` | Value at Risk (VaR 95%) | `var SPY` |
| `beta` | `<ticker>` | Beta vs market (SPY) | `beta AAPL` |
| `stress` | `<ticker>` | Stress test scenarios | `stress SPY` |
| `greeks` | `[spot] [strike]` | Options Greeks calculator | `greeks 100 105` |
| `correlation` | — | Asset correlation matrix | `correlation` |
| `factors` | `<ticker>` | Fama-French factor regression | `factors AAPL` |
| `sectorsexposure` | `<ticker>` | Sector exposure breakdown | `sectorsexposure AAPL` |
| `ai` | `<query>` | AI portfolio analysis & recommendations | `ai analyze my risk` |
| `ask` | `<question>` | Natural language query interface | `ask what is the PE of AAPL` |

### Example: `optimize AAPL,MSFT,GOOGL`

```
Max Sharpe Portfolio:
Expected Return:  +15.23%
Expected Vol:     18.21%
Sharpe Ratio:     0.84
Weights:
Asset     %
──────────────
AAPL     35.0%
MSFT     40.0%
GOOGL    25.0%
```

### Example: `risk AAPL`

```
Risk Report — AAPL
VaR 95% (1d):    2.15%
CVaR 95% (1d):   3.18%
VaR 95% (1mo):   9.23%
VaR 99% (1d):    3.58%
Beta (vs SPY):   1.25
Correlation:     0.82
Stress Scenarios:
  2008 financial crisis: -37.2%
  covid crash:           -34.1%
  rate hike shock:       -15.0%
```

### Example: `greeks 100 105`

```
Options Greeks — Spot: 100, Strike: 105
Type:    call
Price:   3.2521
Delta:   0.4521
Gamma:   0.0321
Theta:   -0.0521
Vega:    0.0821
Rho:     0.0121
```

---

## 📰 Fundamentals Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `fundamentals` | `<ticker>` | Company overview with valuation metrics | `fundamentals AAPL` |
| `news` | `<ticker>` | Company news articles | `news AAPL` |
| `marketnews` | — | Market-wide news feed | `marketnews` |
| `newsbatch` | `<t1,t2,...>` | Batch news for multiple tickers | `newsbatch AAPL,MSFT,GOOGL` |
| `earnings` | `<ticker>` | Earnings calendar | `earnings AAPL` |

### Example: `fundamentals AAPL`

```
Apple Inc. (AAPL)
Sector: Technology  |  Industry: Consumer Electronics
Employees: 164,000
...
Valuation:
Market Cap: $2.80T
P/E:         28.5
Fwd P/E:     25.2
P/B:         45.0
P/S:         7.8
EV/EBITDA:   22.5
Analyst Targets:
Mean:  $200.00
High:  $250.00
Low:   $165.00
Rec:   Buy
```

---

## 🔍 Search Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `search` | `<query>` | Full-text search across all instruments | `search Apple` |

### Example: `search Apple`

```
Found 3 results:
  [Instrument] Apple Inc.
  [Instrument] Apple Hospitality REIT
  [Counterparty] Apple Bank
```

---

## 🏛️ Ontology Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `ontypes` | — | List ontology types | `ontypes` |
| `onobjects` | — | List ontology objects | `onobjects` |
| `instruments` | — | List all instruments | `instruments` |
| `instypes` | — | List instrument types | `instypes` |
| `sectorslist` | — | List all sectors | `sectorslist` |

---

## 📋 Watchlist Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `watch list` | — | Show watchlist items as table | `watch list` |
| `watch add` | `<ticker>` | Add ticker to watchlist | `watch add AAPL` |
| `watch rm` | `<ticker>` | Remove ticker from watchlist | `watch rm AAPL` |

```
📋 Watchlist (3 items):
Ticker  Added
────── ──────────
AAPL    1/15/2025
MSFT    1/15/2025
GOOGL   1/16/2025
```

## 🔔 Alert Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `alert list` | — | List active alerts | `alert list` |
| `alert create` | `<type> <ticker> <cond> <val>` | Create price alert | `alert create price AAPL > 200` |
| `alert enable` | `<id>` | Enable alert | `alert enable <uuid>` |
| `alert disable` | `<id>` | Disable alert | `alert disable <uuid>` |
| `alert delete` | `<id>` | Delete alert | `alert delete <uuid>` |
| `alert history` | — | Show alert trigger history | `alert history` |
| `alert examples` | — | Load example alerts | `alert examples` |

---

## 🏭 Pipeline & System Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `pipelines` | — | List pipeline runs | `pipelines` |
| `calc pnl` | — | Calculate P&L from positions | `calc pnl` |
| `all` | — | Comprehensive data dump (all markets) | `all` |

### Example: `scorecard`

```
🏆 MIAU FINANCE SCORECARD 🏆
🐟 Fish Earned:  42 commands executed
😺 Purr Meter:   98% uptime
🐱 Cat Lives:    9 (0 errors today)
🎯 Whisker Quality: 92% accuracy
🐾 Paw Prints:   156 lines of output

🐱 You got this, whisker!
```

### Example: `watch add AAPL`

```
adding AAPL to watchlist...
✅ Added AAPL to watchlist
```

---

## 🛒 Order Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `order` | `create <pfid> <iid> <type> <side> <qty>` | Create an order | `order create pf123 inst123 MARKET BUY 100` |
| `orders` | `[--status] [--portfolio]` | List orders with filters | `orders --status FILLED` |
| `order cancel` | `<id>` | Cancel an order | `order cancel ord123` |

---

## 📝 Paper Trading Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `paper create` | `<name> [cash]` | Create paper portfolio | `paper create Test 50000` |
| `paper portfolios` | — | List paper portfolios | `paper portfolios` |
| `paper buy` | `<pfid> <ticker> <qty>` | Execute a simulated buy | `paper buy pf123 AAPL 10` |
| `paper sell` | `<pfid> <ticker> <qty>` | Execute a simulated sell | `paper sell pf123 AAPL 5` |

---

## 🔌 Broker Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `brokers` | — | List configured brokers | `brokers` |
| `broker connect` | `<name> [key] [secret]` | Connect to a broker | `broker connect alpaca` |
| `broker account` | `<name>` | View broker account | `broker account alpaca` |

---
- Live prices for AAPL, MSFT, GOOGL, AMZN, TSLA, SPY
- Bitcoin price and Fear & Greed index
- Forex rates (USD base)
- Commodity prices
- Treasury yields
- Market breadth indices
- Sector performance
- Top gainers and losers
- Platform summary stats

---

## 🗺️ Navigation Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `map` | — | Toggle 3D globe overlay | `map` |
| `back` | — | Return to terminal from map | `back` |

---

## 🐱 System Commands

| Command | Arguments | Description | Example |
|---|---|---|---|
| `help` | — | Display full help text | `help` |
| `clear` | — | Clear terminal screen | `clear` |
| `cat` | — | Random ASCII cat art | `cat` |
| `cats` | — | Summon a cat army (5 cats) | `cats` |
| `whoami` | — | Display user identity | `whoami` |
| `miau` | — | Meow with cat art | `miau` |
| `joke` | — | Purr-fectly timed financial cat humor | `joke` |
| `exit` | — | Exit miau finance (cat goodbye) | `exit` |
| `scorecard` | — | Show gamified productivity metrics | `scorecard` |
| `all` | — | Comprehensive market data dump | `all` |
| `split` | — | Enter tmux-style split-pane mode | `split` |
| `heatmap` | — | Toggle sector/performance heatmap | `heatmap` |

### Example: `exit`
```
miau finance signing off...
  /\_/\
 ( x.x )
  > ^ <   bye! 🐱
```

### Example: `joke`

```
😸 Why did the cat invest in Bitcoin?
Because it wanted to be a crypto-kitty! 🐱₿

😸 What's a cat's favorite investment strategy?
Paws and hold. 🐾

😸 Why don't cats trade options?
They prefer simple futures — like chasing laser pointers.

😸 What's a cat's favorite stock?
Meowzon (AMZN).

😸 Why was the cat a great day trader?
It always landed on its feet after a crash.

😸 What's the difference between a cat and a hedge fund manager?
The cat purrs when you pet it.

😸 Why do cats make bad portfolio managers?
They keep chasing the red dots (losses).

😸 What's the purr-fect portfolio?
60% bonds, 30% stocks, 10% catnip futures.

😸 How many traders does it take to change a lightbulb?
None — they just wait for the market to correct itself.

😸 A cat's financial advice:
Diversify into cardboard boxes. Low risk, high nap potential.

😸 Bull market:
Cat eats your portfolio.

😸 Bear market:
Cat sleeps on it.

😸 Why did the cat short the market?
It smelled a bear — from 3 rooms away.

😸 What are the four market cycles?
Accumulation, markup, distribution, and cat nap.

😸 Why did the cat cross the road?
To get to the other side of the trade.

😸 What's a cat's favorite token?
Purr-otocol (PURR).

😸 Why don't cats do technical analysis?
They use whisker analysis. If whiskers twitch right → buy.

😸 Trend is your friend — unless you're a cat.
Then the trend is whatever direction the laser pointer goes.

😸 My portfolio is down 30%.
Good thing I have 9 lives — only used 7 so far.

😸 What's a cat's opinion on crypto?
It's great — finally something more volatile than a cat in a bathtub.
```

### Example: `cat`

```
    /\_/\
   ( o.o )
    > ^ <
```

---

## Workflows

### Quick Market Check
```
> price AAPL
> crypto
> fear
> sectors
```

### Portfolio Analysis
```
> portfolios
> portfolio <id>
> risk AAPL
> optimize AAPL,MSFT,GOOGL
```

### Trading Research
```
> fundamentals TSLA
> signals TSLA
> backtest TSLA
> news TSLA
```

### Full Market Scan
```
> all
```

### Watchlist Management
```
> watch add AAPL
> watch add MSFT
> watch list
> watch rm AAPL
```

### Multi-Ticker Sparkline Watch
```
> sparkline AAPL MSFT GOOGL AMZN TSLA NVDA
```

### Quick Scorecard
```
> scorecard
```

---

## Command Reference Summary (60+ Commands)

| Category | Commands |
|---|---|
| **Market Data** | `price`, `chart`, `sparkline`, `crypto`, `btc`, `cryptomkt`, `cryptohist`, `cryptotop`, `fear`, `forex`, `currency`, `global`, `sectors`, `movers`, `commodities`, `treasury`, `breadth`, `indicators` |
| **Portfolio** | `portfolios`, `portfolio`, `positions`, `summary`, `pnl`, `performance`, `anportfolio`, `anrisk` |
| **Trading** | `trades`, `signals`, `multisig`, `backtest` |
| **Analytics** | `optimize`, `minvar`, `eqweight`, `optperf`, `risk`, `var`, `beta`, `stress`, `greeks`, `correlation` |
| **Fundamentals** | `fundamentals`, `news`, `marketnews`, `newsbatch`, `earnings` |
| **AI / NLQ** | `ai <query>` (portfolio analysis via AI), `ask <query>` (natural language → API) |
| **Search** | `search` |
| **Watchlist** | `watch list`, `watch add`, `watch rm` |
| **Ontology** | `ontypes`, `onobjects`, `instruments`, `instypes`, `sectorslist` |
| **Pipeline** | `pipelines`, `calc pnl`, `all` |
| **Navigation** | `map`, `back` |
| **System** | `help`, `clear`, `cat`, `cats`, `whoami`, `miau`, `joke`, `purr`, `exit`, `scorecard`, `split`, `heatmap` |
| **AI & NLQ** | `ai`, `ask` |
| **Aliases** | `ls` → `portfolios`, `ps` → `trades`, `rm` → `portfolio`, `top` → `crypto`, `ping` → `summary`, `pwd` → `whoami`, `df` → `portfolios`, `date` → `breadth` |

---

### AI Commands

#### `ai <subcommand> [args]`
AI-powered financial analysis. Multiple subcommands:

| Subcommand | Description | Example |
|---|---|---|
| `ai portfolio <id>` | Portfolio analysis & recommendations | `ai portfolio <uuid>` |
| `ai market` | Market overview analysis | `ai market` |
| `ai risk <id>` | Risk assessment for portfolio | `ai risk <uuid>` |
| `ai query <text>` | Ask AI any financial question | `ai query explain CAPM` |
| `ai explain attribution` | AI explains attribution results | `ai explain attribution` |

Output includes summary, risk level, strengths, weaknesses, and actionable recommendations with color-coding.

#### `ask <query>`
Natural language query interface. Converts plain English questions into API calls.
```
miau@finance:~$ ask what is AAPL price?
AAPL: $150.25 (+1.2%)
```
```
miau@finance:~$ ask show me my portfolio risk
Risk Score: 45/100 — Medium risk
```

After running `attrib` on a portfolio, a hint invites `ai explain attribution` for AI-powered explanation of the attribution results.

#### Examples
- `ai portfolio 550e8400-e29b-41d4-a716-446655440000`
- `ai market`
- `ai query what is the Sharpe ratio?`
- `ask show me top tech stocks`
- `ask what's the market sentiment today`

---

---

## Phase 8: Trading Commands

### Order Management

#### `order create <ticker> <side> <qty> <type> [price]`
Place a new order with pre-trade risk validation.

| Argument | Description | Example |
|---|---|---|
| `ticker` | Stock symbol | `AAPL` |
| `side` | `buy` or `sell` | `buy` |
| `qty` | Number of shares | `100` |
| `type` | `market`, `limit`, `stop`, or `stop_limit` | `limit` |
| `price` | Required for limit/stop orders | `150.00` |

```
miau@finance:~$ order create AAPL buy 100 limit 150.00
✅ order placed: 550e8400-e29b-41d4-a716-446655440000
```

#### `order list [status]`
List orders, optionally filtered by status (`pending`, `filled`, `cancelled`).

```
miau@finance:~$ order list
ID       Ticker  Side  Qty    Price Status
────────────────────────────────────────────────
a1b2c3d4 AAPL    BUY    100 $150.00 FILLED
e5f6g7h8 TSLA    SELL    50 $250.00 PENDING
```

#### `order cancel <id>`
Cancel an open order.

```
miau@finance:~$ order cancel e5f6g7h8
✅ order e5f6g7h8 cancelled
```

#### `order status <id>`
Get full order details with fill history and status timeline.

```
miau@finance:~$ order status a1b2c3d4
📋 Order Detail:
  ID:       a1b2c3d4
  Ticker:   AAPL
  Side:     BUY
  Type:     limit
  Quantity: 100
  Price:    $150.00
  Status:   FILLED
  Filled:   100 / 100
  Created:  1/15/2025, 12:00:00 PM
```

### Paper Trading

#### `paper create <name> [cash]`
Create a paper trading portfolio with optional initial cash (default: $100,000).

```
miau@finance:~$ paper create "My Strategy" 50000
✅ paper portfolio created: uuid
```

#### `paper list`
List all paper portfolios with cash balance and returns.

```
miau@finance:~$ paper list
ID       Name                  Cash       Return
─────────────────────────────────────────────────────
a1b2     My Strategy         $50,000    +3.20%
c3d4     Test Portfolio     $100,000    -1.50%
```

#### `paper buy <ticker> <qty> [type] [price]`
Place a paper buy order.

```
miau@finance:~$ paper buy AAPL 10
✅ buy order placed: uuid
```

#### `paper sell <ticker> <qty> [type] [price]`
Place a paper sell order.

#### `paper positions`
View current open paper positions.

#### `paper pnl`
View paper trading P&L summary with win rate.

```
miau@finance:~$ paper pnl
📈 Paper Trading P&L:
  Total P&L:     $1,500.00
  Unrealized:    $500.00
  Realized:      $1,000.00
  Win Rate:      65.0%
  Total Trades:  40
```

### Strategies & Backtesting

#### `strategy list`
List available backtesting strategies.

```
miau@finance:~$ strategy list
Strategy                  Description
───────────────────────────────────────────────────────
sma_cross                SMA(20) / SMA(50) crossover
rsi_mean_reversion       RSI-based mean reversion
momentum                 Price momentum strategy
bollinger_breakout       Bollinger Band breakout
macd_signal              MACD crossover signal
vwap_reversion           VWAP mean reversion
```

#### `strategy backtest <name> <ticker> [period]`
Run a strategy backtest.

```
miau@finance:~$ strategy backtest sma_cross AAPL 1y
📊 Backtest Results — sma_cross on AAPL
  Return:      +15.30%
  Buy & Hold:  +12.10%
  Alpha:       +3.20%
  Sharpe:      1.45
  Max DD:      -8.50%
  Win Rate:    58.0%
  Trades:      32
```

#### `strategy compare <s1,s2,...> <ticker>`
Compare multiple strategies side-by-side.

```
miau@finance:~$ strategy compare sma_cross,momentum AAPL
  sma_cross                Return: +15.30%  Sharpe: 1.45  DD: -8.5%
  momentum                 Return: +18.20%  Sharpe: 1.62  DD: -10.2%
```

### Broker Integration

#### `broker list`
List connected brokers with status and balance.

```
miau@finance:~$ broker list
Broker                Status       Balance
──────────────────────────────────────────────
alpaca                connected    $50,000
```

#### `broker connect <name>`
Connect to a broker (interactive — requires UI mode for API key input).

#### `broker balance [name]`
Get account balance from broker(s).

```
miau@finance:~$ broker balance
💰 Balance: $50,000
```

#### `broker positions [name]`
Get current positions from broker(s).

#### `broker submit <name> <ticker> <side> <qty>`
Submit a live order through a connected broker.

```
miau@finance:~$ broker submit alpaca AAPL BUY 100
✅ order submitted: uuid
```

---

### Push Notifications

#### `notify subscribe`
Subscribe the current browser to push notifications. Requires browser push API support.

#### `notify unsubscribe`
Remove push notification subscription.

### Social: Sharing & Leaderboards

#### `share create <portfolio_id> [--public] [--expires]`
Create a shareable portfolio link.

```
miau@finance:~$ share create a1b2c3d4 --public
🔗 Share link: /api/v1/public/portfolio/abc123...
```

#### `leaderboard [--period] [--metric] [--limit]`
View community trading leaderboard.

```
miau@finance:~$ leaderboard --period monthly
🥇 user1     +32.5%
🥈 user2     +28.1%
🥉 user3     +24.3%
```

### Social: Activity Feed

#### `feed [--filter]`
View the community activity feed.

```
miau@finance:~$ feed --filter following
🐱 @user1 just completed a trade: AAPL +$500
💬 @user2 reached 10 trades! 🎉
```

#### `feed comment <activity_id> <text>`
Comment on an activity.

#### `feed comments <activity_id>`
View comments on an activity.

### Social: Follows

#### `follow <username>`
Follow another trader.

#### `unfollow <username>`
Unfollow a trader.

### Social: Reputation & Badges

#### `reputation`
View your reputation score and level.

```
miau@finance:~$ reputation
🏆 Reputation: 1,250 pts — Level: Silver Analyst
```

#### `badges`
View your earned badges.

```
miau@finance:~$ badges
🎖️ Badges (3/12):
  ✅ First Trade
  ✅ Market Watcher
  ✅ AI Master
  ❌ Diamond Paws (0/10 trades held 1y+)
```

---

## Phase 9: Mobile & Notifications

### Responsive UI
The terminal is fully responsive across mobile (320px), tablet (768px), and desktop (1024px+):
- **Mobile**: Bottom navigation bar, collapsible sidebar, swipe gestures, touch-friendly inputs (44px min tap target)
- **Tablet**: Sidebar visible, split view support, font scaling via `clamp()`
- **Desktop**: Full terminal with CRT effects, keyboard shortcuts, map/heatmap

### Touch & Gestures
- **Swipe left** on command output → show command history
- **Pull down** → refresh market data
- **Tap** quick action buttons for common commands
- Virtual keyboard optimized input fields

### Dark Mode
Toggle dark mode with `dark-mode` CSS class on `<body>`.

### Command Palette
`Ctrl+K` or `Cmd+K` opens the command palette for quick command search.

### PWA Features
- **Installable**: Add to home screen on mobile (Chrome/Safari)
- **Offline mode**: Previously viewed data available offline
- **Background sync**: Alerts and watchlist updates sync when online
- **Push notifications**: Receive alerts even when the terminal is closed
- **Share target**: Share ticker symbols directly to Miau Finance

### Push Notifications
Enable push notifications to receive:
- **Price alerts**: Get notified when a stock hits your target price
- **Trade confirmations**: Instant notification when an order fills
- **AI analysis ready**: Get pinged when AI portfolio/market analysis completes
- **Daily summary**: End-of-day portfolio P&L summary
- **Alert triggers**: Watchlist and custom alert notifications

Configuration is available under Settings → Notifications, where you can:
- Subscribe/unsubscribe to push
- Choose notification types
- Set quiet hours
- View notification history

---

> Pro tip: You can type any ticker symbol directly (e.g., just `AAPL`) and it will execute as a `price` command.

---

## Phase 10: Social & Community Commands

### Portfolio Sharing

| Command | Description | Example |
|---------|-------------|---------|
| `share portfolio <id>` | Create public share link | `share portfolio 550e8400` |
| `share list` | List shared portfolios | `share list` |
| `leaders [weekly\|monthly\|all]` | View leaderboard | `leaders weekly` |

```
miau@finance:~$ share portfolio 550e8400
🔗 https://miau.finance/p/abc123def456 — Share this link!

miau@finance:~$ leaders weekly
🏆 WEEKLY LEADERBOARD
#1  CatTrader   +5.2%  🥇
#2  MiauKing    +4.8%  🥈
#3  YourName    +3.1%  🥉
```

### Activity Feed

| Command | Description | Example |
|---------|-------------|---------|
| `feed [following\|global]` | View activity feed | `feed` |
| `comment <id> <text>` | Comment on activity | `comment abc123 "nice trade!"` |

```
miau@finance:~$ feed
📰 ACTIVITY FEED
  CatTrader bought AAPL (100 shares @ $186.90) — 2m ago
  MiauKing earned badge: 🏆 Top 10 Weekly — 5m ago
  You gained a new follower! — 10m ago
```

### Follow & Profiles

| Command | Description | Example |
|---------|-------------|---------|
| `follow <username>` | Follow a user | `follow CatTrader` |
| `unfollow <username>` | Unfollow a user | `unfollow CatTrader` |
| `profile [username]` | View user profile | `profile` |
| `reputation` | View your badges and points | `reputation` |

```
miau@finance:~$ follow CatTrader
✅ Following CatTrader (1,234 followers)

miau@finance:~$ reputation
🏅 YOUR REPUTATION
  Points: 520 (Level 5)
  Badges: 🐣 First Trade  🔥 Profitable Week  🥉 Top 10 Weekly
```

---

## Phase 11: Billing & Developer Commands

### Subscriptions & Billing

| Command | Description | Example |
|---------|-------------|---------|
| `billing` | Show pricing plans | `billing` |
| `pricing` | Alias for billing | `pricing` |
| `subscribe` | Alias for billing | `subscribe` |
| `billing portal` | Manage subscription (Stripe portal) | `billing portal` |

```
miau@finance:~$ billing
💳 MIAU FINANCE PRICING

FREE TIER
  Market data · Portfolio tracking · Terminal
  ✓ Real-time data  ✓ Basic portfolio  ✓ 5 calls/min

PRO TIER ($29/mo)
  AI advisor · Paper trading · Backtesting
  ✓ Everything in Free  ✓ AI portfolio advisor
  ✓ Paper trading       ✓ Strategy backtesting
  ✓ 100 calls/min

ENTERPRISE ($99/mo)
  Workspaces · Custom brokers · Unlimited
  ✓ Everything in Pro   ✓ Multi-user workspaces
  ✓ Custom brokers      ✓ Unlimited API calls
```

### API Key Management

| Command | Description | Example |
|---------|-------------|---------|
| `apikey create <name>` | Create a new API key | `apikey create MyBot` |
| `apikey list` | List all API keys | `apikey list` |
| `apikey revoke <id>` | Revoke an API key | `apikey revoke abc123` |

```
miau@finance:~$ apikey create MyTradingBot
🔑 API Key: miau_a1b2c3d4e5f6...
  Store this securely — it won't be shown again.

miau@finance:~$ apikey list
  Name             Prefix   Created     Scopes
  ────────────────────────────────────────────
  MyTradingBot     miau_a1b  2026-05-19  market:read, orders:create
  DevConsole       miau_x9  2026-05-18  market:read, portfolios:read
```

### Usage & Developer Console

| Command | Description | Example |
|---------|-------------|---------|
| `usage` | View API usage statistics | `usage` |
| `devconsole` | Open developer dashboard | `devconsole` |

---

## Phase 12: Enterprise Commands

| Command | Description | Example |
|---------|-------------|---------|
| `audit log` | Export audit log (CSV/JSON) | `audit log --format json --days 7` |
| `webhook create <url> <events>` | Create webhook endpoint | `webhook create https://my.app/events --events trade.filled,alert.triggered` |
| `webhook list` | List webhook endpoints | `webhook list` |
| `webhook delete <id>` | Delete webhook | `webhook delete wh_123` |

---

## Phase 12.5: Investment Banking & Advanced Analytics

### `sheetz miau` — Investment Banking Valuations

Simulate investment banker workflows directly from the terminal. Each command runs a financial model against live market data.

| Command | Description | Example |
|---------|-------------|---------|
| `sheetz miau` | Show help for all valuation commands | `sheetz miau` |
| `sheetz miau -dcf <ticker>` | Discounted Cash Flow valuation | `sheetz miau -dcf AAPL` |
| `sheetz miau -wacc <ticker>` | Weighted Average Cost of Capital | `sheetz miau -wacc MSFT` |
| `sheetz miau -comps <ticker>` | Comparable Company Analysis | `sheetz miau -comps GOOGL` |
| `sheetz miau -lbo <ticker>` | Leveraged Buyout model | `sheetz miau -lbo AAPL` |
 | `sheetz miau -all <ticker>` | Run all 4 models (DCF, WACC, Comps, LBO) | `sheetz miau -all AAPL` |
 | `sheetz -sens <ticker>` | Sensitivity matrix — WACC vs Growth fair price table | `sheetz -sens AAPL` |
 | `sheetz -field <ticker>` | Football field valuation — 5 methods with ranges | `sheetz -field AAPL` |
 | `sheetz -acc <acquirer> <target>` | M&A Accretion/Dilution merger model | `sheetz -acc MSFT AAPL` |
 | `sheetz -lbo <ticker>` | LBO model (terminal display) | `sheetz -lbo AAPL` |

**DCF Valuation:**
```
miau@finance:~$ sheetz miau -dcf AAPL

🏦  DCF VALUATION — AAPL
══════════════════════════════════════════════
  WACC: 8.4%  |  Growth: 5%  |  Terminal: 2.5%
  Initial FCF: $109,234M

  Year 1:  FCF $114,695M  →  PV $105,783M  (disc 1.08x)
  Year 2:  FCF $120,430M  →  PV $102,441M  (disc 1.18x)
  Year 3:  FCF $126,452M  →  PV $99,206M   (disc 1.27x)
  Year 4:  FCF $132,775M  →  PV $96,068M   (disc 1.38x)
  Year 5:  FCF $139,413M  →  PV $93,014M   (disc 1.50x)

  Terminal Value: $2,471B  (PV: $1,226B)
──────────────────────────────────────────────
  Enterprise Value: $2,427B
  Fair Price:       $178.20
  Current Price:    $186.90
  Upside:           -4.7%
  Recommendation:   HOLD
```

**WACC Calculation:**
```
miau@finance:~$ sheetz miau -wacc MSFT

🏦  WACC ANALYSIS — MSFT
──────────────────────────────────────────────
  Cost of Equity:  8.25%  (β=0.95)
  Cost of Debt:    3.50%
  Risk-Free Rate:  4.25%
  WACC:            8.10%
──────────────────────────────────────────────
  Market Cap:      $2,847B
  Enterprise Val:  $2,912B
  D/E:             15% / 85%
```

**Comparable Company Analysis:**
```
miau@finance:~$ sheetz miau -comps GOOGL

🏦  COMPARABLE COMPANY ANALYSIS — GOOGL
══════════════════════════════════════════════
  Sector: Technology  |  Industry: Internet Content
  Peers: AAPL, MSFT, META, AMZN
──────────────────────────────────────────────
  P/E:        25.4x
  EV/EBITDA:  17.2x
  P/B:        7.30x
  P/S:        6.80x
  EPS:        $5.92
```

**LBO Model:**
```
miau@finance:~$ sheetz miau -lbo AAPL

🏦  LBO MODEL — AAPL
══════════════════════════════════════════════
  Entry EV:      $2,900B
  Debt:          $1,740B (60%)  |  Equity: $1,160B
  Exit EV:       $3,480B  (12.0x EBITDA)
  Exit Equity:   $1,740B

  Year 1: EBITDA $376B  Interest -$104B  FCF $272B  Debt $1.5B
  Year 2: EBITDA $395B  Interest -$92B   FCF $303B  Debt $1.2B
  Year 3: EBITDA $414B  Interest -$80B   FCF $334B  Debt $0.9B
  Year 4: EBITDA $435B  Interest -$69B   FCF $366B  Debt $0.6B
  Year 5: EBITDA $457B  Interest -$57B   FCF $400B  Debt $0.3B
──────────────────────────────────────────────
  MoM (Multiple of Money):  1.5x
  IRR:                      8.4%
  Verdict:                  OK LBO
```

### `scenario <ticker>` — Scenario Analysis

Run 6 predefined market scenarios against a position. Shows price impact under bear, bull, and black swan conditions, weighted by the stock's beta.

```
miau@finance:~$ scenario AAPL

🧪  SCENARIO ANALYSIS — AAPL  (β=1.20)
══════════════════════════════════════════════
  Bear Case (-20%)       $149.52  (-20.0%)
  Mild Dip (-10%)        $168.21  (-10.0%)
  Base Case (0%)         $186.90  (+0.0%)
  Bull Case (+10%)       $205.59  (+10.0%)
  Melt Up (+20%)         $224.28  (+20.0%)
  Black Swan (-40%)      $112.14  (-40.0%)
──────────────────────────────────────────────
  Worst Case:  $112.14  (-40.0%)
  Best Case:   $224.28  (+20.0%)
```

### `dividends <ticker>` — Dividend Calendar

Fetch dividend data including yield, payout ratio, ex-dividend date, and trailing annual figures.

```
miau@finance:~$ dividends AAPL

💰  DIVIDENDS — AAPL
══════════════════════════════════════════════
  Yield:           0.48%
  Annual Dividend: $0.96
  Payout Ratio:    15.3%
  5Y Avg Yield:    0.82%
```

### `rolling <ticker>` — Rolling Metrics

Calculate trailing 12-month Sharpe ratio, volatility, and beta. Shows the last 20 periods for trend analysis.

```
miau@finance:~$ rolling AAPL

📐  ROLLING METRICS (12mo) — AAPL vs SPY
══════════════════════════════════════════════
  Current Sharpe:     1.20
  Current Volatility: 25.3%
  Current Beta:       1.20

  Rolling Sharpe (last 20 periods):
    2026-04-01: 1.4
    2026-03-15: 1.3
    2026-03-01: 1.1
    2026-02-15: 0.9
    ...
```

### `journal` — Trading Journal

Log trades with mood tracking, free-text reasons, and local storage persistence. Cat-approved trades get bonus luck.

| Command | Description | Example |
|---------|-------------|---------|
| `journal buy <ticker> <qty> [--reason <text>] [--mood <emoji>]` | Log a buy | `journal buy AAPL 10 --reason "felt bullish" --mood 😸` |
| `journal sell <ticker> <qty> [--reason <text>] [--mood <emoji>]` | Log a sell | `journal sell TSLA 5 --reason "taking profits" --mood 😼` |
| `journal` | Show last 7 days | `journal` |
| `journal clear` | Clear journal | `journal clear` |

```
miau@finance:~$ journal buy 10 AAPL --reason "felt bullish, cat approved" --mood 😸
✅ logged: BUY 10 AAPL @ $186.90

miau@finance:~$ journal
📓 Trading Journal (last 7 days)
────────────────────────────────────────
  Today    BUY  10 AAPL  $186.90  😸  "cat approved"
  Yesterday  SELL  5 TSLA  $250.00  😿  "mistake"
  Last week  BUY  20 SPY  $480.00  😐  "rebalance"
```

---

## Phase 14: Global Markets

### `currency` — Multi-Currency Toolkit

Live FX rates, currency conversion, and portfolio base currency management.

| Command | Description | Example |
|---------|-------------|---------|
| `currency list` | Show all supported currencies | `currency list` |
| `currency rates` | Show live FX rates (USD base) | `currency rates` |
| `currency convert <amount> <from> <to>` | Convert between currencies | `currency convert 100 USD EUR` |
| `currency set <portfolio_id> <code>` | Change portfolio base currency | `currency set p_abc123 EUR` |

```
miau@finance:~$ currency rates
💱  LIVE FX RATES (vs USD)
══════════════════════════════════════════════
  EUR:  0.9250     GBP:  0.7900     JPY:  149.50
  CHF:  0.8700     CAD:  1.3600     AUD:  1.5200
  BRL:  5.0500     INR:  83.2000    KRW:  1320.00
  CNY:  7.2400     SEK:  10.3500    NOK:  10.6200
```

```
miau@finance:~$ currency convert 500 USD EUR
💱  CONVERSION
══════════════════════════════════════════════
  500.00 USD  →  462.50 EUR
  Rate: 0.9250 EUR/USD
```

### `global` — Global Market Overview

Regional market data across 40 international exchanges in Asia, Europe, LatAm, and MEA.

| Command | Description | Example |
|---------|-------------|---------|
| `global` | Overview by region with index prices | `global` |
| `global <exchange>` | Detailed exchange view with stocks | `global TSE` |

```
miau@finance:~$ global
🌍  GLOBAL MARKETS
══════════════════════════════════════════════
  🇯🇵 TSE    ^N225    38,500.00  +1.25%   JPY
  🇭🇰 HKEX   ^HSI     22,150.00  -0.80%   HKD
  🇨🇳 SSE    000001.SS 3,020.00  +0.45%   CNY
  🇬🇧 LSE    ^FTSE     8,250.00  -0.30%   GBP
  🇫🇷 EURONEXT ^FCHI  7,850.00  +0.60%   EUR
  🇩🇪 XETRA  ^GDAXI   18,200.00  +0.90%   EUR
  🇧🇷 B3     ^BVSP    128,500.00 +0.30%   BRL
  🇲🇽 BMV    ^MXX     55,200.00  -0.15%   MXN
  🇿🇦 JSE    ^J203    78,500.00  +0.55%   ZAR
  🇸🇦 TADAWUL ^TASI   12,100.00  +0.25%   SAR
```

```
miau@finance:~$ global TSE
🌍  TOKYO STOCK EXCHANGE
══════════════════════════════════════════════
  Index:  ^N225    38,500.00  +1.25%   JPY
  Status: 🟢 OPEN (Asia/Tokyo, 09:00-15:00)

  Market Stocks:
    7203.T  Toyota      ¥3,200    +0.80%
    9984.T  SoftBank    ¥12,500   -0.50%
    6758.T  Sony        ¥14,200   +1.10%
```

---

## 🏦 Catberg — Bloomberg Terminal Emulation

The `catberg` command opens a split-screen Bloomberg-style terminal view with real-time ticker bar, function codes, and cat commentary.

### Commands

| Command | Description |
|---------|-------------|
| `catberg` | Launch Catberg Bloomberg view |
| `catberg wei` | World Equity Index overview |
| `catberg n` | News feed with cat commentary |
| `catberg top` | Top headlines |
| `catberg wcv` | Currency values matrix |
| `catberg gpo AAPL` | Price chart OHLC |
| `catberg gip AAPL` | Intraday price chart |
| `catberg des AAPL` | Company description |
| `catberg fa AAPL` | Financial analysis (DCF + Comps) |
| `catberg rv AAPL` | Relative value vs peers |
| `catberg wb` | World government bonds |
| `catberg ecst` | Economy statistics |
| `catberg weco` | Economic calendar |
| `catberg acdr` | Earnings announcement calendar |
| `catberg anr AAPL` | Analyst recommendations |
| `catberg em AAPL` | Earnings matrix |
| `catberg mgmt AAPL` | Management profiles |
| `catberg phdc AAPL` | Institutional holders |
| `catberg yas` | Yield and spread analysis |
| `catberg ws` | Swap rates |
| `catberg cbq US` | Country overview |
| `catberg help` | Catberg function reference |

### Function Keys

| Key | Action |
|-----|--------|
| `F1` | Help reference |
| `F2` | News feed |
| `F3` | Currency values (FX) |
| `F4` | Price chart |
| `F5` | Company description |
| `F6` | Financial analysis |

### Features

- **Real-time ticker bar** — auto-refreshes every 5 seconds with major indices + user watchlist
- **Cat commentary** — every panel has cat-written analysis ("The Cat, CFA")
- **Cat walk interruption** — 7% chance per refresh of cat walking across screen
- **Miau Score** — every function returns a cat-rated score (1-10 paws)
- **Function input bar** — type Bloomberg codes directly + Enter to execute
- **Ticker input field** — specify ticker for equity analysis functions

---

## 📈 Market Data Commands (v2.3 Datavore Edition)

| Command | Description | Example |
|---------|-------------|---------|
| `screener` | Screen stocks by industry, market cap, country | `screener --industry Tech --minMcap 10` |
| `insider <ticker>` | Insider transactions, net buy/sell ratio | `insider AAPL` |
| `short <ticker>` | Short interest, short % float, days to cover | `short TSLA` |
| `ipo` | IPO calendar with filings, pricing, dates | `ipo` |
| `ownership <ticker>` | Institutional ownership %, top holders | `ownership MSFT` |
| `quanthealth <ticker>` | Piotroski F-Score (0-9), Altman Z-Score, Beneish M-Score | `quanthealth AAPL` |
| `fairvalue <ticker>` | DCF fair value, upside %, sensitivity matrix 3x3 | `fairvalue GOOGL` |
| `passiveflow <ticker>` | % trapped in passive ETFs, blind dollar flow | `passiveflow SPY` |
| `riskfactors <ticker>` | AI-extracted 10-K risk factor word count trend | `riskfactors AAPL` |
| `earningscore <ticker>` | AI-scored earnings call transparency (1-10) | `earningscore TSLA` |
| `famanch <ticker>` | Fama-French 5-factor loadings (Market, Size, Value, Profitability, Investment) | `famanch AAPL` |
| `profile <ticker>` | Extended company profile with executives, peers, suppliers | `profile AAPL` |
| `ticker <query>` | Ticker search across all global exchanges | `ticker apple` |
| `intraday <ticker> [interval]` | Intraday 1min/5min/15min OHLCV chart | `intraday AAPL 5min` |
| `technicals <ticker>` | RSI, MACD, SMA, EMA, Bollinger, Stochastic | `technicals TSLA` |
| `dividend <ticker>` | Full dividend history, growth streak, payout ratios | `dividend AAPL` |
| `catalyst <ticker>` | SEC filing catalysts from 8-K/10-Q/10-K with links | `catalyst MSFT` |

## 🔗 DeFi & Crypto Commands (v2.3 Datavore Edition)

| Command | Description | Example |
|---------|-------------|---------|
| `defillama` | DeFi TVL overview bar | `defillama` |
| `yields [--min APY] [--chain]` | Best yield pools across DeFi | `yields --min 5 --chain ethereum` |
| `stablecoins` | Stablecoin supply overview (DeFiLlama) | `stablecoins` |
| `gas [chain]` | Gas price for Ethereum/L2 | `gas ethereum` |
| `dexs` | DEX volumes by chain (DeFiLlama) | `dexs` |
| `fees [protocol]` | Protocol fees & revenue (DeFiLlama) | `fees uniswap` |
| `crosschain` | Bridge volume, cross-chain activity | `crosschain` |
| `tvl <protocol>` | Protocol-specific TVL with history | `tvl aave` |
| `stablecoin <symbol>` | Per-stablecoin details | `stablecoin USDC` |
| `chain <name>` | Chain overview with TVL and activity | `chain ethereum` |

## 💱 FX & Macro Commands (v2.3 Datavore Edition)

| Command | Description | Example |
|---------|-------------|---------|
| `fx <base>` | All exchange rates for a base currency (200 pairs) | `fx USD` |
| `fxhistory <base> <target>` | Historical FX rate chart | `fxhistory USD EUR` |
| `fxconvert <amount> <from> <to>` | Currency conversion | `fxconvert 100 USD EUR` |
| `cpi [country]` | Consumer Price Index data | `cpi US` |
| `inflation [country]` | Inflation rate time-series | `inflation US` |
| `employment` | Employment data (nonfarm, unemployment) | `employment` |
| `energy <commodity>` | Oil, gas, coal, electricity prices | `energy oil` |
| `agriculture <commodity>` | Crop prices, livestock, dairy | `agriculture wheat` |
| `gdp <country>` | GDP data with history | `gdp US` |
| `macro <country>` | Comprehensive macro dashboard | `macro US` |
| `treasury` | Yield curve history visualization | `treasury` |
| `indicators` | 20+ economic indicators | `indicators` |

## 🧮 Calculator Commands (v2.3 Datavore Edition)

| Command | Description | Example |
|---------|-------------|---------|
| `dca <ticker> <amount> <period>` | Dollar-cost average backtest | `dca AAPL 100 monthly` |
| `compound <principal> <rate> <years> [contribution]` | Compound interest calculator | `compound 10000 0.08 30 500` |
| `retirement <age> <savings> <monthly> <return>` | Retirement planning calculator | `retirement 30 50000 2000 0.07` |
| `loan <amount> <rate> <years>` | Loan amortization schedule | `loan 300000 0.065 30` |
| `margin <price> <qty> <leverage>` | Margin trading calculator | `margin 100 1000 2` |
| `rebalance <pid>` | Portfolio rebalancing calculator | `rebalance 1` |
| `benchmark <pid> <benchmark>` | Tracking error, alpha, beta vs benchmark | `benchmark 1 SPY` |
| `drawdown <ticker>` | Maximum drawdown analysis | `drawdown SPY` |
| `montecarlo <ticker> [years]` | Monte Carlo price path simulation | `montecarlo AAPL 5` |
| `blacklitterman <t1,t2,...>` | Black-Litterman portfolio model | `blacklitterman AAPL,MSFT,GOOGL` |
| `riskparity <t1,t2,...>` | Risk parity portfolio allocation | `riskparity AAPL,TLT,GLD` |
| `pairtrade <t1> <t2>` | Pairs trading analysis | `pairtrade AAPL MSFT` |
| `optionspayoff <strike> <premium> [strategy]` | Options payoff calculator | `optionspayoff 150 5.20 call` |
| `taxlot <ticker>` | Tax lot accounting | `taxlot AAPL` |
| `correlation <t1,t2,...>` | Correlation matrix | `correlation AAPL,MSFT,GOOGL` |

## 🤖 AI Intelligence Commands (v2.3 Datavore Edition)

| Command | Description | Example |
|---------|-------------|---------|
| `aisummary <ticker>` | AI 3-paragraph company summary | `aisummary AAPL` |
| `aisentiment <ticker>` | Multi-source sentiment analysis | `aisentiment TSLA` |
| `aiinsight <ticker>` | AI deep research on a company | `aiinsight NVDA` |
| `aireport` | Daily/weekly AI market report | `aireport` |
| `aiallocate <risk_profile>` | AI portfolio allocation suggestion | `aiallocate moderate` |
| `airisk <pid>` | AI narrative risk assessment | `airisk 1` |
| `aitrade <ticker>` | AI analyzes and executes paper trade | `aitrade AAPL` |
| `aichooser <t1> <t2> <capital>` | AI picks best investment | `aichooser AAPL MSFT 10000` |

## 🐱 Social & Fun Commands

| Command | Description | Example |
|---------|-------------|---------|
| `miaubook` | MiauBook social feed for cat traders | `miaubook` |
| `chartz [-l] [-m] [-lm] [-c]` | Enhanced chart with modes: `-l` live+news, `-m` mega BBands/SR, `-lm` max+cats, `-c` CSV export | `chartz AAPL -l` |
| `kittens [name]` | List kitten squad or inspect an intern | `kittens luna` |
| `rave` | Purrtechno rave — dancing cats, DJ drops, light show | `rave` |
| `revenue` | Revenue dashboard — 20/80 split, your cut | `revenue` |
| `replay <ticker> [period]` | Time-travel replay of any market day | `replay AAPL 1y` |
| `dashboard` | Visual dashboard — world indices, portfolio, quick actions | `dashboard` |
| `cats` | Cat army — 50 cats marching in formation | `cats` |
| `miau` | Random cat emoji + financial wisdom | `miau` |
| `joke` | 20 cat/finance puns | `joke` |
| `purr` | Therapeutic purr generator (20-140 Hz) | `purr` |
| `cat --pet` | Pet the cat companion | `cat --pet` |
| `cat --feed` | Feed the cat tuna | `cat --feed` |
| `cat --adopt` | Adopt a cat companion | `cat --adopt` |
| `cat --fortune` | Financial wisdom from the cat | `cat --fortune` |
| `cat --status` | Cat companion stats | `cat --status` |
| `play` | Play with the cat (laser pointer game) | `play` |
| `meow` | Cat purr generator with frequency analysis | `meow` |
| `veto` | Cat veto power — override any decision | `veto` |
| `manifesto` | Gen Z Finance Manifesto | `manifesto` |
| `miaushare` | Generate shareable snapshot for a ticker | `miaushare AAPL` |
| `miaustats` | Platform dashboard — system health, market watch | `miaustats` |
| `miaucfo` / `cfodashboard` | Revenue breakdown — 80% hooman, 10% ops, 10% cat eco | `miaucfo` |
| `miauwealth` | Net worth — revenue, cat eco invested, alternative assets | `miauwealth` |
| `miauallocate` | Wealth allocation cycle — revenue split | `miauallocate` |
| `miauauto` / `autonomous` | Autonomous Wealth Engine status | `miauauto` |
| `miauinvest` | Invest cat eco fund into stocks/crypto | `miauinvest AAPL` |
| `catsentiment` | AI-powered market sentiment with cat verdict | `catsentiment` |
| `catberg [func]` | Bloomberg-style terminal with cat commentary | `catberg AAPL` |

## 🔐 Authentication

| Command | Description |
|---------|-------------|
| `login <username> <password>` | Authenticate with your credentials |
| `logout` | Clear authentication token |

---
