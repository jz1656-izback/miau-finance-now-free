export const HELP = `🐱 MIAU FINANCE v2.5.1 🐾 PAWDENTITY EDITION 🐾 - COMMAND REFERENCE 🐱

  🔐  FIRST: login <username>   (required for all commands)

  📊  MARKET DATA
    price <ticker>         Live price & change (colored)
    chart <ticker>         ASCII price chart
    sparkline <t>...       Compact sparklines for tickers
    crypto | btc           Bitcoin & top cryptos
    cryptomkt              Crypto market overview
    cryptohist <coin>      Crypto price history
    fear                   Fear & Greed index
    forex                  Forex rates
    sectors                Sector performance
    movers                 Market gainers/losers
    commodities            Gold, oil, silver, etc
    treasury               US Treasury yields
    breadth                Market breadth (VIX, etc)
    indicators             Market indicators

  📈  PORTFOLIO
    portfolios | ls        List all portfolios
    portfolio <id> | rm    Portfolio details
    positions <id>         Position breakdown
    export <id> [csv|json|pdf]  Download portfolio
    summary | ping         Platform summary

  🎯  TRADING
    trades | ps            Recent trades
    signals <ticker>       Technical signals
    multisig <t1,t2>       Multi-asset signals
    backtest <ticker>      Backtest strategy

  ⚡  ANALYTICS
    optimize <tickers>     Max Sharpe portfolio
    minvar <tickers>       Min variance portfolio
    eqweight <tickers>     Equal weight portfolio
    risk <ticker>          Full risk report
    var <ticker>           Value at Risk
    beta <ticker>          Beta vs market
    stress <ticker>        Stress test
    greeks                 Options Greeks
    correlation            Asset correlation
    factors <ticker>       Fama-French factor analysis
    sectors_exposure <t>   Sector factor exposure

  🏆  ATTRIBUTION
    attrib <pid>           Full attribution report (sector + security + factor)
    attrib sector <pid>    Brinson sector attribution vs benchmark
    attrib security <pid>  Per-security contribution breakdown
    attrib factor <pid>    Fama-French factor attribution

  📰  FUNDAMENTALS
    fundamentals <t>       Company financials
    news <ticker>          Company news
    marketnews             Market news
    earnings <ticker>      Earnings calendar

  🔍  SEARCH
    search <query>         Search instruments

  📋  WATCHLIST
    watch list             List watchlist items
    watch add <ticker>     Add ticker to watchlist
    watch rm <ticker>      Remove ticker from watchlist

  🔔  ALERTS
    alert                  List active alerts
    alert create <type> <ticker> <condition> <threshold>
    alert enable|disable|delete <id>
    alert history          View alert trigger history
    alert examples         Create demo alerts

  🔬  QUANT
    quanthealth <t>       Piotroski F-Score, Altman Z, Beneish M-Score
    fairvalue <t>         DCF fair value with upside/downside

  🧮  CALCULATORS
    dca <amt> [p] [y] [r%]    DCA backtest with CAGR
    compound <p> <r%> [y] [c]  Compound interest schedule
    loan <amt> <r%> [yrs]      Loan amortization table
    retirement <a> <s> <m> [r] [ra]  Retirement projection
    margin <price> <qty> [lev]   Margin and liquidation analysis
    drawdown <ticker>         Max drawdown analysis
    montecarlo <t> [n] [d]    Monte Carlo price path simulation
    correlation <t1,t2,...>   Correlation matrix with heatmap
    pairtrade <t1> <t2>      Pairs trading cointegration + z-score
    famanch <ticker>          Fama-French 5-factor loadings
    optionspayoff <s> <p> [st] <sp>  Options P&L diagram
    riskparity <t1,t2,...>    Risk parity portfolio weights
    benchmark <t> [b]        Tracking error, alpha, beta
    etfanalyzer <t>          ETF holdings analysis
    coinlist <exchange>      All listed coins on an exchange
    orderbook <pair> <ex>    Order book depth
    passiveflow <ticker>     Passive ETF ownership flow
    gas [chain_id]           Gas prices for Ethereum/L2
    stablecoins              Stablecoin supply overview
    dexs                     DEX volume overview
    fees [protocol]          Protocol fees & revenue
    tvl <protocol>           Protocol-specific TVL
    chain <name>             Chain overview (TVL, protocols)
    blacklitterman <t1,t2>   Black-Litterman portfolio model
    chartz <ticker> [-l] [-m] [-c]  Mega chart + flags: l=live+news m=mega c=csv export
    chartz miau               Cat-powered chartz (--csv to export)
    chartz3d <ticker>         📈 3D candlestick chart (drag to orbit, scroll to zoom)
    sheetz3d <ticker>         🏦 3D IB dashboard (DCF+WACC+Comps+LBO in 3D)
    compare3d <t1> <t2> [...] 📊 Compare multiple tickers in 3D
    miaustats                📊 Live platform dashboard (markets, sources, cats)
    chat <query>             🤖 Ask Miau AI anything (financial advice)
    demo                     🎬 Auto-demo: showcase all features
    pulse                    📊 Market pulse — fear & greed, movers, top tickers
    ta <ticker>              📈 Full technical analysis (17 indicators)
    ta <indicator> <ticker>   📈 Single indicator (eg: ta rsi_14 AAPL, ta macd AAPL)
    signal <ticker>          🔍 Buy/sell signals + confidence rating
    pattern <ticker>         🔎 Candlestick pattern recognition
    ols <y> <x>             📐 OLS regression (eg: ols AAPL SPY)
    granger <y> <x>         🔗 Granger causality test (eg: granger AAPL SPY)
    coint <a> <b>           🔗 Cointegration test + hedge ratio + Z-score
    capm <ticker> [bench]   📊 CAPM: alpha, beta, Sharpe, Treynor, Info Ratio
    risk <ticker>           ⚠️ VaR, CVaR, max drawdown, Sharpe (Pro feature)
    correl <t1> <t2> [...]  🔗 Correlation matrix
    commodities [all|energy|agri|<ticker>]  🛢️ Commodity spot prices (gold, oil, copper...)
    cattuna                  🐟 The Tuna Price Index (the only commodity that matters)
    futures [all|<ticker>]   📈 Futures prices (ES, NQ, CL, GC, ZC...)
    etf <sectors|top\|ticker>  📊 ETF quotes, sector perf, top ETFs
    index <all\|ticker>       🌍 Global market indices (SPX, N225, HSI, DAX...)
    treasury                 📜 US Treasury yield curve (curve, yields, tips)
    fedrates                 🏦 Central bank rates (EFFR, SOFR, IORB)
    bonds                    📄 Treasury bond yields + 10Y-2Y spread
    mortgage                 🏠 Mortgage rates (30yr, 15yr, 5/1 ARM)
    indicators               📊 20+ economic indicators (GDP, CPI, employment)
    inflation [country]      📈 Inflation rate by country (default: US)
    datasources               Data source health dashboard
    health                    System health (uptime, providers, logs)
    autodiscover <url> [t]    Auto-integrate & analyze new APIs
    fallback                  Data source fallback chain visualization
    apikey list\|set\|test     Manage API keys

  ⛓️  DEFI
    defillama             Top DeFi protocols by TVL
    yields [min]          Best yield pools sorted by APY

  💱  DATAVORE
    fx <base>             Live FX rates for 200+ pairs
    fxconvert <amt> <f> <t>  Currency conversion
    fxhistory <b> <t> [d]    Historical FX rate chart
    insider <ticker>      Insider transactions table
    short <ticker>        Short interest data + sparkline
    ticker <query>        Search tickers globally
    intraday <t> [i]      Intraday OHLCV + sparkline
    technicals <t> [ind]  Technical indicators (rsi/macd/sma/ema/bollinger)
    crosschain            Cross-chain bridge volumes by pair
    macro <country>       Macro dashboard (GDP, inflation, rates, debt)

  🤖  AI ADVISOR
    ai portfolio <id>     AI portfolio analysis & recommendations
    ai market             AI market overview analysis
    ai risk <id>          AI risk assessment for portfolio
    ai query <text>       Ask AI a general question

  💬  NATURAL LANGUAGE
    ask <query>           Ask in plain English (e.g. "ask what are my top holdings?")
    Examples: "ask price of AAPL", "ask show my portfolios", "ask latest news"

  🐱  SYSTEM
    catberg <function>     Bloomberg Terminal emulation (cat-style)
    catberg wei            World Equity Index overview
    catberg n              News feed with cat commentary
    catberg wcv            Currency values matrix
    catberg des <tick>     Company description
    catberg fa <tick>      Financial analysis (DCF + Comps)
    catberg help           Catberg function reference
    miaubook               MiauBook — social feed for cat traders
    help                   Show all commands. Try: help trading, help price
    clear                  Clear screen
    cat [--pet|--feed|--status|--adopt|--fortune|--dance|--gang|--party]  🐱 Interactive terminal cat (32+ breeds)
    cats                   Cat army
    joke                   Tell a cat/finance joke
    whoami | pwd           Who are you?
    miau                   🐱
    login <username>       Authenticate with pawdentity (password is masked)
    logout                 Clear auth token
    map                    Toggle 2D map
    tuna [--flex] [--send] 🐟 Tuna wallet — check balance, flex, send
    meow [freq]            🐱 Generate a therapeutic cat purr (20-140 Hz)
    cat                    🐱 Display a random Miau cat with attitude
    cat fact               🧠 Random cat fact
    veto [thing]           🐱 Cat veto power — override any decision
    kittens [name]         🐱 Kitten squad — list or inspect an intern
    catparty               🎉🐱 CAT PARTY — dancing cats, confetti, lambo dreams
    catarmy                🪖🐱 Deploy the cat army to guard your portfolio
    catbank [balance|routes|jurisdictions|tax|transfer]  🏦🐱 Cat Bank — SEK-proof multi-jurisdiction wealth
    taxstatus              📊 Tax exposure: €0.00 always
    catfact                🧠 Random cat fact (financially relevant)
    cats                   🐱🐱🐱 Cat army — 50 cats marching
    miau                   🐱 Random cat emoji + financial wisdom
    joke                   😹 Tell a cat/finance joke
    purr                   🎵 Purr generator — therapeutic cat sounds
    manifesto              📜 Read the Gen Z finance manifesto
    miaushare [ticker]     📸 Generate shareable portfolio screenshot
    miaucfo                🐱 CFO Dashboard — revenue, hooman payout, lambo, cat eco
    jobs [search\|skill]    💼 Search FinTech jobs matching your skills
    jobs summary           💼 Job market overview for Jevgeni's profile
    miauwealth             🌍 Net worth — revenue, cat eco invested, alternatives
    miauallocate           🔄 Trigger wealth allocation (ops → hooman → cat eco)
    miauauto [status\|trigger]  🤖 Autonomous Wealth Engine control
    miuainvest <type> <amt> 💼 Invest cat eco fund (stocks|crypto)
    billing                💳 View your subscription plan & usage
    billing upgrade        💰 Upgrade to Pro (€49.50/mo)
    donate                 🐟 Support Miau Finance — crypto, fiat, GitHub Sponsors
    catsentiment            📊 AI-powered market sentiment report
    refer                   🎟️ Get your referral link — earn rewards for inviting friends
    invoice [amount]        🧾 Generate a PayPal invoice link
    topup [amount/tier]     💰 Buy tuna or upgrade your tier
    daily                   🎁 Claim your free daily tuna — login streak rewards
    challenges              🏆 Complete challenges to earn tuna and achievements
    status                  📊 Your personal dashboard — tier, tuna, cat, stats
    dashboard [portfolio]   📈 Market dashboard — indices, top movers, portfolio
    portfolio               💼 Manage your portfolio — add, remove, list holdings
    alert                   🔔 Set price alerts — never miss a move
    rave                   🎵🐱 Purrtechno rave — dancing cats, disco, fintech kittens
    miaumap                🌍 Toggle 3D GPU globe (WebGL, drag to rotate, click markers)
    miaumap --cats         🐱 Open globe with cats layer
    miaumap --aliens       👽 Open globe with aliens unlock
    heatmap               🔥 Sector performance heatmap
    kitty | panels        🖥️  Kittyland floating panel manager
    <cmd> -p | --panel    📦  Open any command output in a floating panel
    login <username>       🔐 Authenticate with pawdentity (password is masked)
    logout                 🔒 Clear auth token
    courses [list|search]   📚 Browse courses · courses list · courses search <term>
    all                    Aggregate all market data
    exit                   Exit miau finance
    back                   Back to terminal
    journal [add|list]     Cat trading journal — track mood & trades
    jobs [skill|summary|github]  💼 Search FinTech jobs matching your skills
    journal add <n> <s> <mood>
                           Add journal entry (mood: 😸😾🤔😴😻)
    theme [name]           Switch terminal theme (list for options)
    achievements           Show unlocked cat achievements 🏆

  👥  SOCIAL
    share <portfolio_id>        Share portfolio publicly
    feed [global|following|own] Show social feed
    comments <activity_id>      View comments on a post
    like <activity_id>          Like an activity
    unlike <activity_id>        Remove like
    profile [username]          View user profile
    follow <username>           Follow a user
    unfollow <username>         Unfollow a user
    leaderboard [metric]        Trading leaderboard (metric: total_return/sharpe/gain)
    notifications               View notifications
    search <query>              Search users

  🏛️  GOVERNANCE
    proposal list [status]         List proposals (status: active/passed/all)
    proposal create <title> [desc] Create a governance proposal
    proposal vote <id> <for|against|abstain> [power]  Cast weighted vote
    proposal stats                 Governance dashboard stats

  🔧  DEVELOPER
    devconsole | developer   Open developer console (API keys, webhooks, usage)

  🌪️  CHAOS
    chaos                  Toggle CHAOS MODE (random cats & mayhem)
    panic                  😱 HIDE EVERYTHING (boss key)
    hack                   🕶️ Initiate cyber attack sequence
    sudo <cmd>             Pretend to be root (doesn't actually work)

  📋  TRADING
    order create <t> <side> <qty> <type> [price]
                                   Place order (side: buy/sell, type: market/limit/stop)
    order list [status]            List orders (pending/filled/cancelled)
    order cancel <id>              Cancel order
    order status <id>              Get order details

  📄  PAPER TRADING
    paper create <name> [cash]     Create paper portfolio
    paper list                     List paper portfolios
    paper buy <t> <qty> [type] [price]
                                   Place paper buy order
    paper sell <t> <qty> [type] [price]
                                   Place paper sell order
    paper positions                Show paper positions
    paper pnl                      Show paper P&L

  📈  STRATEGIES
    strategy list                  List available strategies
    strategy backtest <n> <t> [period] [params...]
                                   Run backtest
    strategy compare <t1,t2> <t>   Compare strategies

  🔌  BROKERS
    broker list                    List connected brokers
    broker connect <name>          Connect to broker
    broker balance [name]          Get account balance
    broker positions [name]        Get positions
    broker submit <n> <t> <side> <qty>
                                   Submit order via broker

  💳  BILLING
    billing | pricing              Show pricing plans
    billing portal                 Show current subscription
    billing bark <title>           Submit a feature request (uses a bark)
    revenue                        📊 20/80 revenue dashboard — your cut
    replay <ticker> [period]      ⏪ Time-travel replay: replay AAPL 1y
    subscribe                      Alias for billing

  🏦  INVESTMENT BANKING
    sheetz -dcf <ticker>           DCF valuation (terminal)
    sheetz -wacc <ticker>          WACC calculation (terminal)
    sheetz -comps <ticker>         Comparable company analysis (terminal)
    sheetz -lbo <ticker>           LBO model (terminal)
    sheetz -all <ticker>           Run all 4 models (terminal)
    sheetz -sens <ticker>          Sensitivity matrix
    sheetz -field <ticker>         Football field chart
    sheetz -acc <ticker> <target>  M&A Accretion/Dilution
    sheetz miau -dcf <ticker>      DCF valuation → CSV download
    sheetz miau -all <ticker>      All models → CSV download

  🌍  GLOBAL MARKETS
    global                    Market overview by region
    global <exchange>         Detail for a specific exchange

  💰  CURRENCY
    currency list              Supported currencies
    currency rates             Live FX rates
    currency convert <amt> <from> <to>  FX conversion
    currency set <pid> <code>  Change portfolio base currency

  📄  CAT CONTENT
    miaupapers list           List all MiauPapers
    miaupapers <n>            Read paper #n
    cat                       Display cat art + random joke
    joke                      Random cat finance joke

  🔗  DEFI & WEB3
    wallet connect              Connect wallet (WalletConnect)
    wallet balance              View wallet balances
    wallet sessions             List connected wallets
    defi protocols              List supported DeFi protocols

  🌱  ESG & SUSTAINABILITY
    esg <ticker>                   ESG score (E/S/G, rating, percentile)
    esg portfolio <id>             Portfolio ESG score
    esg screen <min>               Screen tickers by min ESG score
    carbon <ticker>                Carbon footprint (scope 1/2/3)
    carbon portfolio <id>          Portfolio carbon footprint & benchmark
    green                          Green finance market overview
    green energy                   Renewable energy ETFs
    green bonds                    Green bonds list
    green funds                    Sustainable funds list

  🎨  ALIASES
    ls   -> portfolios     pwd  -> whoami
    ps   -> trades         ping -> summary
    rm   -> portfolio      top  -> crypto
    df   -> portfolios     date -> breadth

  🐱💨  v2.3 DATAVORE EDITION
    fx [base]             FX rates for 200 currencies
    gas                   Ethereum gas prices
    defillama             DeFi TVL overview
    yields [min_apy]      Best yield pools
    quanthealth <t>       Piotroski F-Score, Altman Z
    fairvalue <t>         DCF fair value with upside%
    insider <ticker>      Insider transactions (needs FINNHUB_KEY)
    short <ticker>        Short interest data (needs FINNHUB_KEY)
    ipo                   IPO calendar (needs FINNHUB_KEY)
    profile <ticker>      Company profile (needs FINNHUB_KEY)
    ownership <ticker>    Institutional ownership (needs FINNHUB_KEY)
    ticker <query>        Ticker search
    screener              Screen stocks: screener --industry Tech --minMcap 10
    stablecoins           Stablecoin supply overview (DeFiLlama)
    dexs                  DEX volumes by chain (DeFiLlama)
    fees [protocol]       Protocol fees & revenue (DeFiLlama)
    cpi                   US Consumer Price Index
    employment            US employment data (nonfarm, unemployment)
    famanch <ticker>       Fama-French 5-factor loadings
    riskfactors <ticker>  AI 10-K risk factor analysis
    passiveflow <ticker>  ETF passive ownership %
    earningscore <ticker> AI earnings call transparency score
    intraday <t> [i]      Intraday OHLCV

  Examples:
    price AAPL      optimize AAPL,MSFT,GOOGL
    signals TSLA    risk SPY      all
    ls              ps            ping

  🚒  Service Desk:
    ticket list       List all support tickets
    ticket create --fire "..."  Report a fire/emergency
    ticket create --bug "..."   Report a bug
    ticket create --feature "..."  Feature request
    ticket poke <id>  👆 Poke a ticket to get attention
`

// ── Help Categories ───────────────────────────────────────────
export const HELP_CATEGORIES: Record<string, string> = {}
export const HELP_ORDER: string[] = []
export const HELP_LINES = HELP.split('\n')
let currentCat = ''
for (const line of HELP_LINES) {
  const m = line.match(/^\s{2}([\u{1F300}-\u{1FAFF}]\s+.+)$/u)
  if (m) {
    currentCat = m[1].trim()
    HELP_CATEGORIES[currentCat] = ''
    HELP_ORDER.push(currentCat)
  } else if (currentCat) {
    HELP_CATEGORIES[currentCat] += line + '\n'
  }
}
// Also collect all command lines for search
export const ALL_COMMANDS: { cmd: string; desc: string; cat: string }[] = []
for (const cat of HELP_ORDER) {
  const lines = HELP_CATEGORIES[cat].split('\n')
  for (const l of lines) {
    const cm = l.match(/^\s{4}(\S+)\s+(.+)$/)
    if (cm) ALL_COMMANDS.push({ cmd: cm[1], desc: cm[2], cat })
  }
}

export function helpForCategory(query: string): string {
  const q = query.toLowerCase()
  // Try exact category match first
  for (const cat of HELP_ORDER) {
    if (cat.toLowerCase().includes(q)) {
      return `🐱 ${cat}\n${HELP_CATEGORIES[cat]}`
    }
  }
  // Fuzzy search across all commands
  const matches = ALL_COMMANDS.filter(c => c.cmd.includes(q) || c.desc.toLowerCase().includes(q))
  if (matches.length === 0) return `No commands matching '${q}'`
  // Group by category
  const byCat: Record<string, string[]> = {}
  for (const m of matches) {
    if (!byCat[m.cat]) byCat[m.cat] = []
    byCat[m.cat].push(`    ${m.cmd.padEnd(22)} ${m.desc}`)
  }
  let result = `🐱 Matching commands (${matches.length}):\n`
  for (const cat of Object.keys(byCat)) {
    result += `\n  ${cat}\n${byCat[cat].join('\n')}\n`
  }
  return result
}

export const CAT_ART: string = [
  "    ╱|、",
  "   (˚ˎ 。7",
  "    |、˜〵",
  "    じしˍ,)ノ",
  "  Meow! Ready to trade?",
  "",
  "  ╱|、",
  " (˚ˎ 。7",
  "  |、˜〵    nyannyan~",
  "  じしˍ,)ノ",
  "",
  "    /(=^x^=)\\",
  "   /  🐟 🐟 🐟  \\",
  "  MIAU MIAAAAU",
].join('\n')