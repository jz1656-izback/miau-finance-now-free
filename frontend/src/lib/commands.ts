import { AddLine, escapeHtml, miauUsername, authFetch, safeJson, fmt, pct, table, sparkline } from './commands/shared'
import { HELP, HELP_CATEGORIES, HELP_ORDER, ALL_COMMANDS, helpForCategory } from './commands/help'
import { api } from './api'
import { authHeaders, getToken } from './auth'
import { getLogger } from './logger'
import { dispatchCommand } from './commands/index'
const log = getLogger('commands')

export async function executeCommand(cmd: string, addLine: AddLine): Promise<void> {
  const parts = cmd.trim().split(/\s+/)
  const command = parts[0].toLowerCase()
  const args = parts.slice(1)

  log.info(`cmd: ${command}`, { args: parts.slice(1) })

  // Try domain handlers first (extracted from the switch for maintainability)
  if (await dispatchCommand(command, args, addLine)) {
    return
  }

  switch (command) {
    case 'clear': { return }
    case 'help': {
      const q = args.join(' ')
      if (!q) {
        addLine({ text: HELP, className: 'text-cyan' })
        addLine({ text: `  ${ALL_COMMANDS.length} commands · ${HELP_ORDER.length} categories · "help <category>" or "help <search>"`, className: 'text-dim' })
      } else if (q === '--cats' || q === '--categories') {
        addLine({ text: `🐱  CATEGORIES (${HELP_ORDER.length}):`, className: 'text-cyan' })
        for (const cat of HELP_ORDER) {
          const count = HELP_CATEGORIES[cat].split('\n').filter(l => l.trim().length > 0).length
          addLine({ text: `  ${cat}  (${count} commands)`, className: 'text-green' })
        }
      } else {
        addLine({ text: helpForCategory(q), className: 'text-cyan' })
      }
      break
    }

    case 'smarthlep': {
      const goal = args.join(' ') || ''
      addLine({ text: '🐱 SmartHelp — Tell me what you want to DO, not just what you want to KNOW.', className: 'text-cyan' })
      if (!goal) {
        addLine({ text: '   Usage: smarthlep <your goal>', className: 'text-dim' })
        addLine({ text: "   e.g. smarthlep how do I analyze my portfolio risk?", className: 'text-dim' })
        addLine({ text: '   e.g. smarthlep what commands screen for value stocks?', className: 'text-dim' })
        addLine({ text: '   e.g. smarthlep show me how to compare two stocks', className: 'text-dim' })
        addLine({ text: '', className: '' })
        addLine({ text: '   🐱 SmartHelp is AI-powered. It needs the MCP server running.', className: 'text-dim' })
        break
      }

      addLine({ text: `🐱 figuring out: "${goal}"`, className: 'text-dim' })
      addLine({ text: '   📚 consulting the cat manual...', className: 'text-dim' })

      try {
        // Try MCP smart help first
        let handled = false
        try {
          const { mcp } = await import('./mcp/client')
          const answer = await mcp.callTool('help', { query: goal, mode: 'workflow' })
          if (answer) {
            handled = true
            addLine({ text: '🐱 Here\'s what to do:', className: 'text-green' })
            for (const line of answer.split('\n')) {
              if (line.trim().startsWith('`') && line.includes('`')) {
                addLine({ text: `   🎯 ${line.trim()}`, className: 'text-green' })
              } else {
                addLine({ text: `   ${line}`, className: 'text-cyan' })
              }
            }
          }
        } catch { /* MCP offline */ }

        if (!handled) {
          // Fallback: try backend AI
          try {
            const res = await authFetch('/api/v1/ai/query', {
              method: 'POST',
              headers: authHeaders({ 'Content-Type': 'application/json' }),
              body: JSON.stringify({ query: `Terminal command help: ${goal}. List the specific terminal commands needed and explain the workflow.` }),
            })
            const data = await safeJson(res, addLine)
            if (data?.response) {
              addLine({ text: '🐱 Here\'s what to do:', className: 'text-green' })
              for (const line of data.response.split('\n')) {
                addLine({ text: line.startsWith('`') ? `   🎯 ${line}` : `   ${line}`, className: 'text-cyan' })
              }
            } else {
              addLine({ text: '😿 Could not figure out a workflow for this. Try "help" for all commands.', className: 'text-red' })
            }
          } catch {
            addLine({ text: '😿 SmartHelp is not available right now. Use "help" for all commands.', className: 'text-red' })
          }
        }
      } catch (e: any) {
        addLine({ text: `😿 SmartHelp failed: ${e.message}`, className: 'text-red' })
      }
      break
    }

    case 'price': {
      const rawTicker = args[0] || 'AAPL'
      const wantsLive = rawTicker === '-l' || args.includes('-l')
      const ticker = wantsLive ? (args[1] || args[0] || 'AAPL').replace('-l','').trim() : rawTicker.replace('-l','').trim()
      addLine({ text: wantsLive ? `🐱 fetching live ${ticker}...` : `🐱 ${ticker} from chonk...`, className: 'text-dim' })
      try {
        const token = localStorage.getItem('miau_token')
        const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
        const live = wantsLive ? '&live=true' : ''
        const res = await fetch(`/api/v1/market/live?tickers=${ticker}${live}`, { headers })
        const data = await safeJson(res, addLine)
        if (!data) break
        const d = data.data?.[ticker] || data?.[ticker]
        if (!d) { addLine({ text: `No data for ${ticker}`, className: 'text-red' }); break }
        const cat = (d.change_pct ?? 0) >= 0 ? '😸' : '😿'
        const src = data.source === 'chonk' ? '📦 chonk' : '🌐 live'
        addLine({
          text: `${cat} ${ticker}  ${d.name || ''}  ${src}
price:   $${(d.price ?? 0).toFixed(2)}
change:  ${(d.change_pct ?? 0) >= 0 ? '+' : ''}${(d.change_pct ?? 0).toFixed(2)}%
high:    $${(d.high ?? 0).toFixed(2)}
low:     $${(d.low ?? 0).toFixed(2)}
volume:  ${((d.volume ?? 0)).toLocaleString()}`,
          className: (d.change_pct ?? 0) >= 0 ? 'text-green' : 'text-red'
        })
      } catch (e: any) {
        addLine({ text: `❌ error: ${e.message || e}`, className: 'text-red' })
      }
      break
    }



    case 'login': {
      const username = args[0]
      const password = args[1]
      // 🔐 pawdentity: prefer the masked Terminal prompt (1-arg). This path is
      // the fallback for non-Terminal callers and never echoes the password.
      if (!username) { addLine({ text: 'Usage: login <username>', className: 'text-yellow' }); break }
      if (!password) { addLine({ text: 'Usage: login <username> (password is masked)', className: 'text-yellow' }); break }
      addLine({ text: `🔐 authenticating ${username}...`, className: 'text-dim' })
      try {
        const { login: doLogin } = await import('./auth')
        await doLogin(username, password)
        localStorage.setItem('miau_tier', 'free')
        addLine({ text: `✅ logged in as ${username} (Free tier · 100 commands/day)`, className: 'text-green' })
        addLine({ text: `   Upgrade: billing upgrade · Pricing: pricing`, className: 'text-dim' })
      } catch (e: any) {
        addLine({ text: `❌ login failed: ${e.message || e}`, className: 'text-red' })
      }
      break
    }

    case 'logout': {
      try {
        const { logout: doLogout } = await import('./auth')
        await doLogout()
        addLine({ text: '🔒 logged out', className: 'text-yellow' })
      } catch {}
      break
    }

    case 'health': {
      addLine({ text: `🏥 Fetching system health...`, className: 'text-dim' })
      const resH = await safeJson(await authFetch('/api/v1/health'), addLine)
      if (!resH) break
      addLine({ text: ``, className: '' })
      addLine({ text: `🏥  SYSTEM HEALTH`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Status:    ${resH.status === 'healthy' ? '✅ Healthy' : '⚠️ ' + resH.status}`, className: resH.status === 'healthy' ? 'text-green' : 'text-red' })
      addLine({ text: `  Uptime:    ${Math.floor(resH.uptime_seconds / 3600)}h ${Math.floor((resH.uptime_seconds || 0) % 3600 / 60)}m`, className: 'text-dim' })
      addLine({ text: `  Providers: ${resH.services?.providers_healthy || 0} healthy / ${resH.services?.providers_unhealthy || 0} unhealthy`, className: 'text-yellow' })
      addLine({ text: `  Log Files: ${Object.keys(resH.log_files || {}).length} available`, className: 'text-dim' })
      if (resH.version) addLine({ text: `  Version:   ${resH.version}`, className: 'text-dim' })
      break
    }

/*
//     case 'correlation': {
//       addLine({ text: 'fetching correlation matrix...', className: 'text-dim' })
//       const c = await authFetch('/api/v1/economics/correlation').then(r => r.json())
//       if (c.correlation_matrix) {
//         const tickers = c.tickers || []
//         const matrix = c.correlation_matrix
//         const headers = [''].concat(tickers.map((t: string) => t.padEnd(6)))
//         const rows = tickers.map((t: string) => {
//           const vals = tickers.map((t2: string) => {
//             const val = matrix[t]?.[t2]
//             return val != null ? val.toFixed(3).padStart(6) : 'N/A'.padStart(6)
//           })
//           return [t.padEnd(6), ...vals]
//         })
//         addLine({ text: table(headers, rows), className: 'text-green' })
//       }
//       break
//     }
// 
*/

    case 'factors': {
      const ticker = args[0] || 'AAPL'
      const model = args[1] === '3' ? '3factor' : '5factor'
      addLine({ text: `running ${model === '3factor' ? '3-factor' : '5-factor'} analysis for ${ticker}...`, className: 'text-dim' })
      const f = await authFetch(`/api/v1/analytics/factors/${ticker}?model=${model}`).then(r => r.json())
      if (f.error) { addLine({ text: `error: ${f.error}`, className: 'text-red' }); break }
      addLine({
        text: `${f.model} Analysis — ${f.ticker}
Alpha (ann.):   ${(f.annualized_alpha_pct || 0).toFixed(4)}%  (t=${f.alpha_t || '?'}, p=${f.alpha_p || '?'})
R²:             ${f.r_squared || '?'}  (adj: ${f.adj_r_squared || '?'})
Resid Vol:      ${(f.annualized_residual_vol_pct || 0).toFixed(2)}%
Style:          ${f.style_classification || 'N/A'}`,
        className: 'text-cyan'
      })
      if (f.factor_loadings) {
        const rows = Object.entries(f.factor_loadings).map(([name, d]: [string, any]) => [
          name.padEnd(8),
          (d.loading || 0).toFixed(4).padStart(8),
          (d.t_stat || 0).toFixed(2).padStart(6),
          (d.p_value || 0).toFixed(4).padStart(8),
          (d.interpretation || '').substring(0, 30),
        ])
        addLine({ text: 'Factor Loadings:\n' + table(['Factor', 'Loading', 't-stat', 'p-value', 'Interpretation'], rows), className: 'text-green' })
      }
      break
    }

    case 'sectors_exposure':
    case 'sectorsexposure': {
      const ticker = args[0] || 'AAPL'
      addLine({ text: `calculating sector exposure for ${ticker}...`, className: 'text-dim' })
      const se = await authFetch(`/api/v1/analytics/factors/${ticker}/sectors`).then(r => r.json())
      if (se.error) { addLine({ text: `error: ${se.error}`, className: 'text-red' }); break }
      addLine({ text: `Sector Exposure — ${se.ticker}  (dominant: ${se.dominant_sector || 'N/A'})`, className: 'text-cyan' })
      if (se.sector_exposures) {
        const rows = Object.entries(se.sector_exposures).map(([name, d]: [string, any]) => [
          name.substring(0, 22).padEnd(22),
          (d.etf || '').padEnd(6),
          (d.beta || 0).toFixed(4).padStart(8),
          (d.correlation || 0).toFixed(4).padStart(8),
          (d.exposure_level || '').padEnd(10),
        ])
        addLine({ text: table(['Sector', 'ETF', 'Beta', 'Corr', 'Level'], rows), className: 'text-green' })
      }
      break
    }

    case 'fundamentals': {
      const ticker = args[0] || 'AAPL'
      addLine({ text: `fetching fundamentals for ${ticker}...`, className: 'text-dim' })
      const f = await authFetch(`/api/v1/fundamentals/${ticker}`).then(r => r.json())
      if (f.error) { addLine({ text: `error: ${f.error}`, className: 'text-red' }); break }
      addLine({
        text: `${f.name} (${f.ticker})
Sector: ${f.sector}  |  Industry: ${f.industry}
Employees: ${(f.employees || 0).toLocaleString()}
${f.description || ''}`,
        className: 'text-green'
      })
      if (f.valuation) {
        const v = f.valuation
        addLine({
          text: `Valuation:
Market Cap: ${fmt(v.market_cap)}
P/E:         ${v.pe_ratio || '-'}
Fwd P/E:     ${v.forward_pe || '-'}
P/B:         ${v.price_to_book || '-'}
P/S:         ${v.price_to_sales || '-'}
EV/EBITDA:   ${v.enterprise_to_ebitda || '-'}`,
          className: 'text-cyan'
        })
      }
      if (f.price_targets) {
        const pt = f.price_targets
        addLine({
          text: `Analyst Targets:
Mean:  ${fmt(pt.target_mean)}
High:  ${fmt(pt.target_high)}
Low:   ${fmt(pt.target_low)}
Rec:   ${pt.recommendation || 'N/A'}`,
          className: 'text-yellow'
        })
      }
      break
    }

    case 'news': {
      const ticker = args[0] || 'AAPL'
      addLine({ text: `fetching news for ${ticker}...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/news/company/${ticker}`)
        const n = await safeJson(res, addLine)
        if (!n?.length) { addLine({ text: 'No news found.', className: 'text-dim' }); break }
        for (const item of n.slice(0, 8)) {
          addLine({
            text: `📰 ${item.title}
   ${item.publisher || ''}  |  ${item.published_at?.substring(0, 10) || ''}`,
            className: 'text-cyan'
          })
        }
      } catch { addLine({ text: 'Failed to fetch news.', className: 'text-red' }) }
      break
    }

    case 'marketnews': {
      addLine({ text: 'fetching market news...', className: 'text-dim' })
      try {
        const res = await authFetch('/api/v1/news/market')
        const n = await safeJson(res, addLine)
        if (!n?.length) { addLine({ text: 'No market news found.', className: 'text-dim' }); break }
        for (const item of n.slice(0, 10)) {
          addLine({
            text: `📰 ${item.title}
   ${item.publisher || ''}  |  ${item.published_at?.substring(0, 10) || ''}`,
            className: 'text-cyan'
          })
        }
      } catch { addLine({ text: 'Failed to fetch market news.', className: 'text-red' }) }
      break
    }

    case 'earnings': {
      const ticker = args[0] || 'AAPL'
      const e = await authFetch(`/api/v1/fundamentals/${ticker}/earnings`).then(r => r.json())
      if (e.error) { addLine({ text: `error: ${e.error}`, className: 'text-red' }); break }
      const rows = (e.earnings || []).map((er: any) => [
        (er.date || '').substring(0, 10),
        fmt(er.eps_estimate).padStart(8),
        fmt(er.eps_actual).padStart(8),
      ])
      addLine({ text: table(['Date', 'Est EPS', 'Act EPS'], rows), className: 'text-green' })
      break
    }

    case 'chart': {
      const ticker = args[0] || 'AAPL'
      addLine({ text: `fetching chart data for ${ticker}...`, className: 'text-dim' })
      const h = await authFetch(`/api/v1/market/historical/${ticker}?period=1mo`).then(r => r.json())
      if (h.error || !h.records?.length) {
        addLine({ text: `No data: ${h.error || 'empty'}`, className: 'text-red' })
        break
      }
      const prices = h.records.map((r: any) => r.close).filter(Boolean) as number[]
      if (prices.length < 5) { addLine({ text: 'Not enough data for chart', className: 'text-red' }); break }
      const max = Math.max(...prices)
      const min = Math.min(...prices)
      const range = max - min || 1
      const hh = 10
      const chart: string[] = []
      for (let row = hh; row >= 0; row--) {
        const level = min + (range * row) / hh
        let line = ''
        for (const p of prices) {
          line += p >= level ? '█' : ' '
        }
        chart.push(`${level.toFixed(0).padStart(6)} │${line}`)
      }
      const sl = sparkline(prices, 20)
      const change = prices[prices.length - 1] - prices[0]
      const changeStr = change >= 0 ? '+' : ''
      addLine({ text: `${ticker} — Last ${prices.length} days  ${sl}  ${changeStr}${change.toFixed(2)}\n` + chart.join('\n') + `\n       └${'─'.repeat(prices.length)}`, className: 'text-green' })
      addLine({ text: `Range: ${fmt(min)} — ${fmt(max)}`, className: 'text-dim' })
      break
    }

    case 'chartz': {
      const argsCz = parts.slice(1)
      const tickerCz = argsCz.find((a: string) => !a.startsWith('-'))?.toUpperCase() || 'SPY'
      const allFlags = argsCz.filter((a: string) => a.startsWith('-')).join('').toLowerCase()
      const hasL = allFlags.includes('l')
      const hasM = allFlags.includes('m')
      const isMax = hasL && hasM
      const isCsv = allFlags.includes('c') || allFlags.includes('csv')
      const mode = (hasL ? 'l' : '') + (hasM ? 'm' : '')

      addLine({ text: `📊 Fetching mega chart for ${tickerCz}${mode ? ' (' + mode + ' mode)' : ''}...`, className: 'text-dim' })
      if (tickerCz === 'MIAU') {
        const cats = ['🐱', '😺', '😸', '😻', '🙀', '😹', '😼', '😽', '🐈', '🐈‍⬛']
        const catArt = ['  ╱|、', ' (˚ˎ 。7', '  |、˜〵', '  じしˍ,)ノ']
        addLine({ text: ``, className: '' })
        addLine({ text: `┌${'─'.repeat(40)}┐`, className: 'text-yellow' })
        addLine({ text: `│${'🐱 MIAU CHARTZ 🐱'.padStart(28)}│`, className: 'text-yellow' })
        addLine({ text: `├${'─'.repeat(40)}┤`, className: 'text-yellow' })
        for (const line of catArt) addLine({ text: `│  ${line}${' '.repeat(28)}│`, className: 'text-yellow' })
        addLine({ text: `│${' '.repeat(40)}│`, className: 'text-yellow' })
        addLine({ text: `│  "The cat is the chart.${' '.repeat(18)}│`, className: 'text-yellow' })
        addLine({ text: `│   The chart is the cat."${' '.repeat(15)}│`, className: 'text-yellow' })
        addLine({ text: `│${' '.repeat(40)}│`, className: 'text-yellow' })
        addLine({ text: `│  miau! 💚📈${' '.repeat(27)}│`, className: 'text-green' })
        addLine({ text: `│${' '.repeat(40)}│`, className: 'text-yellow' })
        addLine({ text: `│  Cats: ${cats.slice(0, 5).join('')}${' '.repeat(22)}│`, className: 'text-yellow' })
        addLine({ text: `└${'─'.repeat(40)}┘`, className: 'text-yellow' })
        break
      }
      const d = await safeJson(await authFetch(`/api/v1/datavore/chartz/${tickerCz}${mode ? '?mode=' + mode : ''}`), addLine)
      if (!d) break
      const prices = d.price_history || []
      if (prices.length < 10) { addLine({ text: 'Not enough data', className: 'text-red' }); break }

      if (isMax && d.cats?.length) addLine({ text: d.cats.join(' '), className: 'text-yellow' })
      if (isMax && d.cat_commentary) addLine({ text: `🐱 ${d.cat_commentary}`, className: 'text-yellow' })

      if (isCsv) {
        const datesA = d.dates || prices.map((_: number, i: number) => `day-${i + 1}`)
        const highsA = d.highs || prices
        const lowsA = d.lows || prices
        const volsA = d.volumes || []
        addLine({ text: `📊 CSV Export — ${tickerCz}`, className: 'text-cyan' })
        addLine({ text: `Date,Close,High,Low,Volume,RSI_14,MACD,Signal`, className: 'text-green' })
        for (let i = 0; i < prices.length; i++) {
          const date = datesA[i] || ''
          const close = prices[i].toFixed(2)
          const high = (highsA[i] || prices[i]).toFixed(2)
          const low = (lowsA[i] || prices[i]).toFixed(2)
          const vol = volsA[i] !== undefined ? String(Math.round(volsA[i])) : ''
          const r = d.rsi_14 !== undefined ? d.rsi_14.toFixed(1) : ''
          const mc = d.macd !== undefined ? d.macd.toFixed(4) : ''
          const sg = d.macd_signal !== undefined ? d.macd_signal.toFixed(4) : ''
          addLine({ text: `${date},${close},${high},${low},${vol},${r},${mc},${sg}` })
        }
        addLine({ text: `✨ Copiable CSV above — paste directly into Google Sheets or Excel`, className: 'text-dim' })
        break
      }

      const maxP = Math.max(...prices)
      const minP = Math.min(...prices)
      const range = maxP - minP || 1
      const hh = hasM ? 22 : 16
      const cols = Math.min(prices.length, hasM ? 80 : 60)
      const step = Math.max(1, Math.floor(prices.length / cols))
      const sampled: number[] = []
      for (let i = 0; i < prices.length; i += step) sampled.push(prices[i])
      if (sampled.length < 2) sampled.push(prices[prices.length - 1])
      const chartLines: string[] = []
      for (let row = hh; row >= 0; row--) {
        const level = minP + range * row / hh
        let line = ''
        for (const p of sampled) line += p >= level ? '█' : ' '
        // Right-pad to align the right border consistently
        chartLines.push(`${level.toFixed(0).padStart(7)} │${line.padEnd(sampled.length)}`)
      }
      const sl = sparkline(prices, 20)
      const pChange = prices.length > 1 ? prices[prices.length - 1] - prices[0] : 0
      const pChangePct = prices[0] > 0 ? (pChange / prices[0]) * 100 : 0
      const rsiCls = d.rsi_14 >= 70 ? 'text-red' : d.rsi_14 <= 30 ? 'text-green' : 'text-yellow'
      const trendEmoji = d.trend === 'up' ? '↑' : '↓'
      const w = hasM ? 90 : 70
      const changeStr = d.change_pct !== undefined ? ` ${d.change_pct >= 0 ? '+' : ''}${d.change_pct.toFixed(1)}%` : ` ${pChange >= 0 ? '+' : ''}${pChangePct.toFixed(1)}%`
      const padToW = (s: string) => s.padEnd(w)
      addLine({ text: `┌${'─'.repeat(w)}┐`, className: 'text-dim' })
      const headerLine = `${tickerCz.padEnd(8)} ${trendEmoji} $${(d.current_price || 0).toFixed(2)}  ${sl}  ${changeStr.trim()}  Pred: $${d.prediction_price?.toFixed(2) || '---'}${hasL && d.live_price ? '  Live: $' + d.live_price.toFixed(2) : ''}`
      addLine({ text: padToW(`│${headerLine}`) + '│', className: pChange >= 0 ? 'text-green' : 'text-red' })
      addLine({ text: `├${'─'.repeat(w)}┤`, className: 'text-dim' })
      for (const cl of chartLines) addLine({ text: padToW(`│${cl}`) + '│', className: 'text-green' })
      const xAxisLine = `${' '.repeat(7)} └${'─'.repeat(sampled.length)}`
      addLine({ text: padToW(`│${xAxisLine}`) + '│', className: 'text-dim' })
      addLine({ text: `├${'─'.repeat(w)}┤`, className: 'text-dim' })
      let infoLine = `│  RSI(14): ${d.rsi_14}  │  SMA20: $${fmt(d.sma_20)}  │  SMA50: $${fmt(d.sma_50 !== null ? d.sma_50 : 'N/A')}  │  52W Hi: $${fmt(d.high_52w)}  │  52W Lo: $${fmt(d.low_52w)}  │  Vol: ${d.volatility}%│`
      addLine({ text: padToW(infoLine), className: rsiCls })
      let macdLine = `│  MACD: ${d.macd >= 0 ? '+' : ''}${fmt(d.macd)}  │  Signal: ${d.macd_signal >= 0 ? '+' : ''}${fmt(d.macd_signal)}  │  Hist: ${fmt(d.macd_histogram)}  │  Trend: ${d.trend.toUpperCase()}  │  Points: ${d.data_points}  │  Pred: $${fmt(d.prediction_price)}│`
      addLine({ text: padToW(macdLine), className: 'text-dim' })
      if (hasM && d.sma_200) addLine({ text: `│  SMA200: $${fmt(d.sma_200)}  │  Z-Score: ${d.z_score}  │  BB Upper: $${fmt(d.bb_upper)}  │  BB Lower: $${fmt(d.bb_lower)}  │  BB Mid: $${fmt(d.bb_middle)}│`, className: 'text-dim' })
      if (hasM && d.volume_profile) addLine({ text: `│  Avg Vol(20d): ${fmt(d.volume_profile.avg_20d)}  │  Vol vs Avg: ${d.volume_profile.current_vs_avg >= 0 ? '+' : ''}${d.volume_profile.current_vs_avg}%│`, className: 'text-dim' })
      if (hasM && d.support_resistance) {
        const supp = d.support_resistance.support_levels?.map((s: number) => `$${fmt(s)}`).join(', ') || 'N/A'
        const resis = d.support_resistance.resistance_levels?.map((s: number) => `$${fmt(s)}`).join(', ') || 'N/A'
        addLine({ text: `│  Support: ${supp}  │  Resistance: ${resis}│`, className: 'text-dim' })
      }
      addLine({ text: `└${'─'.repeat(w)}┘`, className: 'text-dim' })
      if (d.predictions?.length) {
        const predSl = sparkline(d.predictions, 15)
        addLine({ text: `📈 20-period Linear Regression Forecast: $${fmt(d.predictions[0])} → $${fmt(d.prediction_price)}  ${predSl}`, className: 'text-cyan' })
      }
      if ((hasL || isMax) && d.news?.length) {
        addLine({ text: ``, className: '' })
        addLine({ text: `📰  NEWS  —  ${tickerCz}  (${d.news.length} stories)`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════════════════════════════════════════════════════════`, className: 'text-dim' })
        for (const n of d.news.slice(0, 4)) {
          const meta = []
          if (n.source) meta.push(n.source)
          if (n.datetime) meta.push(typeof n.datetime === 'number' ? new Date(n.datetime * 1000).toLocaleDateString() : n.datetime.substring(0, 10))
          const headline = n.headline ? escapeHtml(n.headline.substring(0, 120)) : ''
          if (n.url) {
            const url = n.url
            addLine({ text: `  📌 <a href="${url}" target="_blank" rel="noopener noreferrer" class="text-green">${headline}</a>`, html: true, className: '' })
            addLine({ text: `     ${meta.join(' · ')}  <a href="${url}" target="_blank" rel="noopener noreferrer" class="text-dim">🔗 open</a>`, html: true, className: '' })
          } else {
            addLine({ text: `  📌 ${n.headline.substring(0, 120)}`, className: 'text-green' })
            addLine({ text: `     ${meta.join(' · ')}`, className: 'text-dim' })
          }
        }
      }
      if ((hasL || isMax) && d.market_context) {
        const mc = d.market_context
        addLine({ text: ``, className: '' })
        addLine({ text: `📊  MARKET CONTEXT  —  ${tickerCz}`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════════════════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  ${mc.sector}  |  Sector today: ${mc.sector_perf_today}  |  ${mc.market_hours}`, className: 'text-green' })
        if (mc.pe_estimate) addLine({ text: `  P/E: ${mc.pe_estimate}  |  Mkt Cap: ${mc.market_cap_estimate}  |  Vol: ${mc.volume_today}  |  SMA200 spread: ${mc.ytd_vs_sma200 || 'N/A'}`, className: 'text-dim' })
      }
      if (isMax && d.cats?.length) addLine({ text: d.cats.reverse().join(' ') + ' 🐱', className: 'text-yellow' })
      break
    }

    case 'autodiscover': {
      const targetUrl = parts[1]
      const targetTicker = (parts[2] || 'AAPL').toUpperCase()
      if (!targetUrl) { addLine({ text: 'Usage: autodiscover <url> [ticker]  — e.g. autodiscover https://api.example.com AAPL', className: 'text-yellow' }); break }
      addLine({ text: `🔍 Probing ${targetUrl} for compatible endpoints...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/datavore/auto/probe?url=${encodeURIComponent(targetUrl)}&ticker=${targetTicker}`), addLine)
      if (!res) break
      addLine({ text: ``, className: '' })
      addLine({ text: `🔍  AUTO-INTEGRATE — ${res.url}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Endpoints found: ${res.endpoints_found}/${res.endpoints_tested}`, className: res.endpoints_found > 0 ? 'text-green' : 'text-yellow' })
      if (res.detected_models?.length) {
        addLine({ text: `  Detected models:`, className: 'text-dim' })
        for (const m of res.detected_models.slice(0, 5)) {
          addLine({ text: `    ${m.detected_type.padEnd(15)} ${m.endpoint}  (${m.status})`, className: 'text-green' })
          if (m.field_mappings && Object.keys(m.field_mappings).length > 0) {
            const f = Object.entries(m.field_mappings).map(([k, v]) => `${k}→${v}`).join(', ')
            addLine({ text: `      Fields: ${f}`, className: 'text-dim' })
          }
        }
      }
      if (res.analysis?.current_price) {
        addLine({ text: `  Current price: $${fmt(res.analysis.current_price)}`, className: 'text-yellow' })
      }
      if (res.analysis?.series_analysis) {
        const sa = res.analysis.series_analysis
        addLine({ text: `  Series: ${sa.data_points} pts, trend: ${sa.trend}, mean: ${fmt(sa.mean)}, forecast: [${(sa.forecast || []).slice(0, 3).map((f: number) => fmt(f)).join(', ')}...]`, className: 'text-dim' })
      }
      addLine({ text: `  ${res.recommendation}`, className: 'text-cyan' })
      break
    }

    case 'apikey': {
      const subCmd = parts[1]
      if (subCmd === 'create') {
        const name = parts.slice(2).join(' ') || 'default'
        addLine({ text: `🔑 Creating API key...`, className: 'text-dim' })
        const res = await safeJson(await authFetch('/api/v1/api-keys', { method: 'POST', body: JSON.stringify({ name }), headers: { 'Content-Type': 'application/json' } }), addLine)
        if (!res) break
        addLine({ text: ``, className: '' })
        addLine({ text: `🔑  API KEY CREATED`, className: 'text-cyan' })
        addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Key:  ${res.raw_key || res.key || ''}`, className: 'text-green' })
        addLine({ text: `  ID:   ${res.id || ''}`, className: 'text-dim' })
        addLine({ text: `  Name: ${res.name || name}`, className: 'text-dim' })
        addLine({ text: `  ⚠️  Copy this key now — it won't be shown again`, className: 'text-yellow' })
      } else if (subCmd === 'list') {
        addLine({ text: `🔑 Fetching API keys...`, className: 'text-dim' })
        const res = await safeJson(await authFetch('/api/v1/api-keys'), addLine)
        if (!res) break
        const keys = Array.isArray(res) ? res : res.keys || []
        addLine({ text: ``, className: '' })
        addLine({ text: `🔑  API KEYS — ${keys.length} total`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
        if (keys.length === 0) addLine({ text: `  No API keys. Use: apikey create <name>`, className: 'text-yellow' })
        for (const k of keys) addLine({ text: `  ${(k.name || k.provider || '').padEnd(18)} ${k.masked || k.key_prefix || '****'}  ${k.configured !== false ? '✅' : '❌'}`, className: k.configured !== false ? 'text-green' : 'text-dim' })
      } else if (subCmd === 'revoke') {
        const keyId = parts[2]
        if (!keyId) { addLine({ text: 'Usage: apikey revoke <key_id>', className: 'text-yellow' }); break }
        addLine({ text: `🔑 Revoking API key ${keyId}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/api-keys/${keyId}`, { method: 'DELETE' }), addLine)
        if (!res) break
        addLine({ text: `  ✅ API key ${keyId} revoked`, className: 'text-green' })
      } else {
        addLine({ text: `API Key Management:
  apikey create <name>       Create a new API key
  apikey list                List your API keys
  apikey revoke <id>         Revoke an API key`, className: 'text-yellow' })
      }
      break
    }

    case 'datasources': {
      addLine({ text: `📡 Fetching data source health...`, className: 'text-dim' })
      const res = await safeJson(await authFetch('/api/v1/datasources/status'), addLine)
      if (!res) break
      const providers = res.providers || []
      const healthy = providers.filter((p: any) => p.healthy)
      addLine({ text: ``, className: '' })
      addLine({ text: `📡  DATA SOURCES — ${healthy.length}/${providers.length} healthy`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════════════════════`, className: 'text-dim' })
      for (const p of providers) {
        const icon = p.healthy ? '✅' : '❌'
        const cls = p.healthy ? 'text-green' : 'text-red'
        const stats = p.stats || {}
        addLine({ text: `  ${icon} ${p.provider.padEnd(18)} ${p.healthy ? 'UP'.padEnd(6) : 'DOWN'.padEnd(6)}  latency: ${p.latency_ms !== undefined ? p.latency_ms + 'ms' : 'N/A'.padStart(6)}  quota: ${p.remaining_quota !== undefined ? p.remaining_quota + '/' + stats.rate_limit : 'N/A'}  ok: ${stats.success_count || 0}  err: ${stats.error_count || 0}`, className: cls })
        if (!p.healthy && p.error) addLine({ text: `    └─ ${p.error}`, className: 'text-red' })
      }
      if (res.cache) {
        const c = res.cache
        addLine({ text: `  📦 Cache: ${c.memory_entries || 0} entries  |  hits: ${c.hits || 0}  misses: ${c.misses || 0}  hit rate: ${c.hit_rate_pct || 0}%  tiers: ${Object.keys(c.tiers || {}).join(', ')}`, className: 'text-dim' })
      }
      addLine({ text: `  🕐 Updated: ${res.updated_at || 'N/A'}`, className: 'text-dim' })
      break
    }

    case 'fallback': {
      addLine({ text: `🔗 Fetching fallback chains...`, className: 'text-dim' })
      const res = await safeJson(await authFetch('/api/v1/datasources/fallback-chains'), addLine)
      if (!res) break
      const caps = res.capabilities || {}
      addLine({ text: ``, className: '' })
      addLine({ text: `🔗  FALLBACK CHAINS — ${res.total_capabilities} capabilities`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════════════════════`, className: 'text-dim' })
      for (const [cap, providers] of Object.entries(caps)) {
        const arr = providers as any[]
        if (arr.length === 0) continue
        const chain = arr.map((p, i) => `${i + 1}.${p.name}${p.requires_key ? '🔑' : ''}`).join(' → ')
        addLine({ text: `  ${cap.padEnd(16)} ${chain}`, className: 'text-green' })
        for (const p of arr) {
          addLine({ text: `    ${' '.repeat(Math.min(cap.length, 8))}  ${p.fallback_order}. ${p.name.padEnd(16)} ${p.requires_key ? '🔑 key needed' : '✅ free'}  ${p.rate_limit}/min`, className: p.requires_key ? 'text-yellow' : 'text-dim' })
        }
      }
      break
    }

    case 'sparkline': {
      const tickers = args.length ? args : ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
      addLine({ text: `fetching sparklines for ${tickers.join(', ')}...`, className: 'text-dim' })
      const allData = await Promise.allSettled(
        tickers.map(t => authFetch(`/api/v1/market/historical/${t}?period=1mo`).then(r => r.json()))
      )
      for (let i = 0; i < tickers.length; i++) {
        const result = allData[i]
        if (result.status !== 'fulfilled' || result.value.error) {
          addLine({ text: `${tickers[i]}  error`, className: 'text-red' })
          continue
        }
        const prices = result.value.records?.map((r: any) => r.close).filter(Boolean) as number[] | undefined
        if (!prices || prices.length < 2) {
          addLine({ text: `${tickers[i]}  no data`, className: 'text-dim' })
          continue
        }
        const sl = sparkline(prices, 15)
        const last = prices[prices.length - 1]
        const first = prices[0]
        const chg = last - first
        const chgPct = first !== 0 ? ((last - first) / first * 100) : 0
        const cl = chg >= 0 ? 'text-green' : 'text-red'
        addLine({ text: `${tickers[i].padEnd(6)} ${sl}  ${fmt(last)}  ${chg >= 0 ? '+' : ''}${chg.toFixed(2)} (${chg >= 0 ? '+' : ''}${chgPct.toFixed(2)}%)`, className: cl })
      }
      break
    }

    case 'search': {
      const q = args.join(' ') || 'AAPL'
      addLine({ text: `searching for "${q}"...`, className: 'text-dim' })
      const s = await authFetch(`/api/v1/search?q=${encodeURIComponent(q)}`).then(r => r.json())
      if (!s.results?.length) { addLine({ text: 'No results found.', className: 'text-dim' }); break }
      addLine({ text: `Found ${s.total} results:`, className: 'text-cyan' })
      for (const r of s.results.slice(0, 10)) {
        addLine({ text: `  [${r.type_display_name || r.type_name}] ${r.display_name}`, className: 'text-green' })
      }
      break
    }

    case 'ontypes': {
      addLine({ text: 'fetching ontology types...', className: 'text-dim' })
      const types = await api.getTypes()
      const rows = types.map((t: any) => [
        (t.id || '').substring(0, 12).padEnd(12),
        (t.name || '').padEnd(20),
        (t.display_name || '').padEnd(25),
        (t.icon || '').padEnd(10),
      ])
      addLine({ text: table(['ID', 'Name', 'Display', 'Icon'], rows), className: 'text-green' })
      break
    }

    case 'onobjects': {
      addLine({ text: 'fetching ontology objects...', className: 'text-dim' })
      const objs = await api.getObjects()
      const rows = objs.slice(0, 20).map((o: any) => [
        (o.id || '').substring(0, 12).padEnd(12),
        (o.display_name || o.name || '').substring(0, 30).padEnd(30),
        (o.type_name || '').padEnd(15),
      ])
      addLine({ text: table(['ID', 'Name', 'Type'], rows), className: 'text-cyan' })
      break
    }

    case 'instruments': {
      addLine({ text: 'fetching instruments...', className: 'text-dim' })
      const inst = await api.getInstruments()
      const rows = inst.map((i: any) => [
        (i.ticker || i.id || '').substring(0, 10).padEnd(10),
        (i.name || '').substring(0, 25).padEnd(25),
        (i.sector || '').padEnd(15),
        (i.instrument_type || '').padEnd(12),
      ])
      addLine({ text: table(['Ticker', 'Name', 'Sector', 'Type'], rows), className: 'text-green' })
      break
    }

    case 'instypes': {
      addLine({ text: 'fetching instrument types...', className: 'text-dim' })
      const types = await api.getInstrumentTypes()
      addLine({ text: types.join('\n'), className: 'text-cyan' })
      break
    }

    case 'sectorslist': {
      addLine({ text: 'fetching sectors...', className: 'text-dim' })
      const sectors = await api.getSectors()
      addLine({ text: sectors.join('\n'), className: 'text-cyan' })
      break
    }

    case 'anportfolio': {
      const pid = args[0]
      if (!pid) { addLine({ text: 'usage: anportfolio <id>', className: 'text-yellow' }); break }
      addLine({ text: `fetching analytics for portfolio ${pid}...`, className: 'text-dim' })
      const a = await api.getPortfolioAnalytics(pid)
      addLine({ text: JSON.stringify(a, null, 2), className: 'text-green' })
      break
    }

    case 'anrisk': {
      const pid = args[0]
      if (!pid) { addLine({ text: 'usage: anrisk <id>', className: 'text-yellow' }); break }
      addLine({ text: `fetching risk analytics for portfolio ${pid}...`, className: 'text-dim' })
      const r = await authFetch(`/api/v1/analytics/portfolios/${pid}/risk`).then(r => r.json())
      addLine({ text: JSON.stringify(r, null, 2), className: 'text-cyan' })
      break
    }

    case 'pnl': {
      const days = args[0] || '30'
      const pid = args[1] || ''
      addLine({ text: `fetching P&L timeseries (${days} days)...`, className: 'text-dim' })
      const p = await api.getPnlTimeseries(pid || undefined, parseInt(days))
      if (p?.length) {
        const rows = p.slice(-10).map((r: any) => [
          (r.date || '').substring(0, 10),
          fmt(r.pnl).padStart(12),
          pct(r.pnl_pct).padStart(8),
        ])
        addLine({ text: 'Last 10 days:\n' + table(['Date', 'P&L', 'Change'], rows), className: 'text-green' })
      }
      break
    }

    case 'performance': {
      const iid = args[0]
      if (!iid) { addLine({ text: 'usage: performance <instrument_id>', className: 'text-yellow' }); break }
      addLine({ text: `fetching performance for ${iid}...`, className: 'text-dim' })
      const perf = await api.getInstrumentPerformance(iid)
      addLine({ text: JSON.stringify(perf, null, 2), className: 'text-cyan' })
      break
    }

    case 'pipelines': {
      addLine({ text: 'fetching pipeline runs...', className: 'text-dim' })
      const runs = await api.getPipelineRuns()
      const rows = runs.slice(0, 15).map((r: any) => [
        (r.id || '').substring(0, 12).padEnd(12),
        (r.pipeline_name || '').padEnd(20),
        (r.status || '').padEnd(10),
        (r.started_at || '').substring(0, 19).padEnd(19),
      ])
      addLine({ text: table(['ID', 'Pipeline', 'Status', 'Started'], rows), className: 'text-green' })
      break
    }

    case 'calc': {
      addLine({ text: 'calculating P&L...', className: 'text-dim' })
      const result = await api.calculatePnl()
      addLine({ text: JSON.stringify(result, null, 2), className: 'text-cyan' })
      break
    }

    case 'optperf': {
      addLine({ text: 'fetching optimizer performance...', className: 'text-dim' })
      const perf = await authFetch('/api/v1/optimizer/performance').then(r => r.json())
      addLine({ text: JSON.stringify(perf, null, 2), className: 'text-green' })
      break
    }

    case 'newsbatch': {
      const tickers = args[0] || 'AAPL,MSFT,GOOGL'
      addLine({ text: `fetching news batch for ${tickers}...`, className: 'text-dim' })
      const n = await authFetch(`/api/v1/news/batch?tickers=${tickers}`).then(r => r.json())
      if (!n?.length) { addLine({ text: 'No news found.', className: 'text-dim' }); break }
      for (const item of n.slice(0, 10)) {
        addLine({
          text: `📰 ${item.title}
   ${item.publisher || ''}  |  ${item.ticker || ''}  |  ${item.published_at?.substring(0, 10) || ''}`,
          className: 'text-cyan'
        })
      }
      break
    }

    case 'cryptotop': {
      const limit = args[0] || '20'
      addLine({ text: `fetching top ${limit} cryptos...`, className: 'text-dim' })
      const top = await authFetch(`/api/v1/market/crypto/top?limit=${limit}`).then(r => r.json())
      const rows = top.map((c: any) => [
        `#${c.rank}`.padEnd(4),
        (c.symbol || '').padEnd(6),
        (c.name || '').substring(0, 15).padEnd(15),
        fmt(c.price, 4).padStart(12),
        pct(c.change_24h_pct).padStart(8),
        fmt(c.market_cap).padStart(10),
      ])
      addLine({ text: table(['Rank', 'Symbol', 'Name', 'Price', '24h', 'Mkt Cap'], rows), className: 'text-green' })
      break
    }

    case 'catberg': {
      addLine({ text: `🐱 entering Catberg mode...`, className: 'text-green' })
      window.dispatchEvent(new CustomEvent('toggle-catberg'))
      break
    }

    case 'all': {
      addLine({ text: '🐱 MIAU FINANCE - ALL DATA DUMP 🐱', className: 'text-green' })
      addLine({ text: 'fetching everything...', className: 'text-dim' })

      const [marketRes, cryptoRes, fearRes, forexRes, commRes, treasuryRes, breadthRes, sectorsRes, glRes, summaryRes] = await Promise.allSettled([
        authFetch('/api/v1/market/live?tickers=AAPL,MSFT,GOOGL,AMZN,TSLA,SPY'),
        authFetch('/api/v1/market/crypto?coin=bitcoin'),
        authFetch('/api/v1/market/crypto/fear-greed'),
        authFetch('/api/v1/market/forex?base=USD'),
        authFetch('/api/v1/economics/commodities'),
        authFetch('/api/v1/economics/treasury-yield'),
        authFetch('/api/v1/economics/market-breadth'),
        authFetch('/api/v1/market/sectors'),
        authFetch('/api/v1/economics/gainers-losers'),
        authFetch('/api/v1/analytics/summary'),
      ])

      // Check for auth failure
      if (marketRes.status === 'fulfilled' && marketRes.value.status === 401) {
        addLine({ text: '🔒 not authenticated — type: login <username>', className: 'text-red' })
        break
      }

      const market = marketRes.status === 'fulfilled' ? await safeJson(marketRes.value, addLine) : null
      const crypto = cryptoRes.status === 'fulfilled' ? await safeJson(cryptoRes.value, addLine) : null
      const fear = fearRes.status === 'fulfilled' ? await safeJson(fearRes.value, addLine) : null
      const forex = forexRes.status === 'fulfilled' ? await safeJson(forexRes.value, addLine) : null
      const comm = commRes.status === 'fulfilled' ? await safeJson(commRes.value, addLine) : null
      const treasury = treasuryRes.status === 'fulfilled' ? await safeJson(treasuryRes.value, addLine) : null
      const breadth = breadthRes.status === 'fulfilled' ? await safeJson(breadthRes.value, addLine) : null
      const sectors = sectorsRes.status === 'fulfilled' ? await safeJson(sectorsRes.value, addLine) : null
      const gl = glRes.status === 'fulfilled' ? await safeJson(glRes.value, addLine) : null
      const summary = summaryRes.status === 'fulfilled' ? await safeJson(summaryRes.value, addLine) : null

      if (market?.data) {
        addLine({ text: '\n📊 LIVE PRICES:', className: 'text-yellow' })
        const rows = Object.entries(market.data || {}).map(([k, v]: [string, any]) => [
          k.padEnd(6),
          fmt(v.price).padStart(10),
          pct(v.change_pct).padStart(8),
          fmt(v.high).padStart(10),
          fmt(v.low).padStart(10),
          (v.volume || 0).toLocaleString().padStart(12),
        ])
        addLine({ text: table(['Ticker', 'Price', 'Change', 'High', 'Low', 'Volume'], rows), className: 'text-green' })
      }

      if (crypto) {
        const c = crypto
        addLine({ text: `\n₿ Bitcoin: ${fmt(c.price)} | 24h: ${pct(c.change_24h_pct)} | Mkt Cap: ${fmt(c.market_cap)}`, className: 'text-cyan' })
      }

      if (fear) {
        const f = fear
        addLine({ text: `Fear & Greed: ${f.value}/100 (${f.classification})`, className: f.value < 30 ? 'text-red' : f.value > 70 ? 'text-green' : 'text-yellow' })
      }

      if (forex?.rates) {
        addLine({ text: '\n💱 Forex (USD):', className: 'text-cyan' })
        const rows = Object.entries(forex.rates || {}).slice(0, 8).map(([k, v]) => [k.padEnd(6), `${v}`.padStart(12)])
        addLine({ text: table(['Pair', 'Rate'], rows), className: 'text-green' })
      }

      if (comm) {
        addLine({ text: '\n🛢️ Commodities:', className: 'text-orange' })
        const rows = Object.entries(comm).map(([k, v]: [string, any]) => [k.padEnd(15), fmt(v.price).padStart(10)])
        addLine({ text: table(['Commodity', 'Price'], rows), className: 'text-green' })
      }

      if (treasury) {
        addLine({ text: '\n🏦 Treasury Yields:', className: 'text-cyan' })
        const rows = Object.entries(treasury).map(([k, v]: [string, any]) => [k.padEnd(6), `${(v.yield || 0).toFixed(3)}%`.padStart(10)])
        addLine({ text: table(['Tenor', 'Yield'], rows), className: 'text-green' })
      }

      if (breadth) {
        addLine({ text: '\n📈 Market Breadth:', className: 'text-purple' })
        const rows = Object.entries(breadth).map(([k, v]: [string, any]) => [k.padEnd(15), `${(v.value || 0).toFixed(2)}`.padStart(12)])
        addLine({ text: table(['Index', 'Value'], rows), className: 'text-green' })
      }

      if (sectors) {
        addLine({ text: '\n🏭 Sectors:', className: 'text-yellow' })
        const rows = sectors.map((s: any) => [s.ticker.padEnd(6), (s.name || '').substring(0, 20).padEnd(20), pct(s.change_pct).padStart(8)])
        addLine({ text: table(['Ticker', 'Sector', 'Change'], rows), className: 'text-green' })
      }

      if (gl) {
        if (gl.top_gainers?.length) {
          addLine({ text: '\n📈 Top Gainers:', className: 'text-green' })
          const rows = gl.top_gainers.slice(0, 5).map((s: any) => [s.ticker.padEnd(6), (s.name || '').padEnd(20), pct(s.change_pct).padStart(8)])
          addLine({ text: table(['Ticker', 'Name', 'Change'], rows), className: 'text-green' })
        }
        if (gl.top_losers?.length) {
          addLine({ text: '\n📉 Top Losers:', className: 'text-red' })
          const rows = gl.top_losers.slice(0, 5).map((s: any) => [s.ticker.padEnd(6), (s.name || '').padEnd(20), pct(s.change_pct).padStart(8)])
          addLine({ text: table(['Ticker', 'Name', 'Change'], rows), className: 'text-red' })
        }
      }

      if (summary) {
        addLine({ text: `\n📊 Platform: ${summary.total_portfolios} portfolios | ${summary.total_instruments} instruments | ${fmt(summary.total_aum)} AUM`, className: 'text-cyan' })
      }

      break
    }

    case 'attrib': {
      const sub = args[0]?.toLowerCase()
      const pid = (sub && ['sector', 'security', 'factor'].includes(sub) ? args[1] : args[0]) || ''
      const subtype = (sub && ['sector', 'security', 'factor'].includes(sub)) ? sub : 'report'
      addLine({ text: `fetching ${subtype} attribution for portfolio ${pid || '? (usage: attrib <portfolio-id>)'}...`, className: 'text-dim' })

      if (!pid) {
        addLine({ text: 'Usage: attrib [sector|security|factor] <portfolio-id>', className: 'text-yellow' })
        break
      }

      try {
        const url = subtype === 'report'
          ? `/api/v1/attribution/${pid}`
          : `/api/v1/attribution/${pid}/${subtype}`
        const resp = await authFetch(url).then(r => r.json())
        if (resp.error) { addLine({ text: `error: ${resp.error}`, className: 'text-red' }); break }

        if (subtype === 'report') {
          addLine({ text: `🏆 Full Attribution Report — ${pid.substring(0, 12)}...`, className: 'text-yellow' })
          addLine({ text: `Benchmark: ${resp.benchmark}  |  Period: ${resp.period}`, className: 'text-cyan' })
          if (resp.sector_attribution?.sectors) {
            addLine({ text: '\n📊 Sector Attribution:', className: 'text-green' })
            const rows = resp.sector_attribution.sectors.map((s: any) => [
              s.sector.substring(0, 20).padEnd(20),
              `${s.allocation_effect > 0 ? '+' : ''}${s.allocation_effect.toFixed(2)}%`.padStart(10),
              `${s.selection_effect > 0 ? '+' : ''}${s.selection_effect.toFixed(2)}%`.padStart(10),
              `${s.total_effect > 0 ? '+' : ''}${s.total_effect.toFixed(2)}%`.padStart(10),
            ])
            addLine({ text: table(['Sector', 'Allocation', 'Selection', 'Total'], rows), className: 'text-green' })
          }
          if (resp.security_attribution?.securities) {
            addLine({ text: '\n🔒 Security Attribution:', className: 'text-cyan' })
            const rows = resp.security_attribution.securities.slice(0, 10).map((s: any) => [
              s.ticker.padEnd(6),
              `${s.weight_pct.toFixed(1)}%`.padStart(6),
              `${s.return_pct > 0 ? '+' : ''}${s.return_pct.toFixed(1)}%`.padStart(8),
              `${s.contribution_pct > 0 ? '+' : ''}${s.contribution_pct.toFixed(2)}%`.padStart(10),
            ])
            addLine({ text: table(['Ticker', 'Weight', 'Return', 'Contrib'], rows), className: 'text-cyan' })
          }
          if (resp.factor_attribution?.factor_loadings) {
            addLine({ text: '\n📈 Factor Attribution:', className: 'text-yellow' })
            const fl = resp.factor_attribution.factor_loadings
            const rows = Object.entries(fl).map(([k, v]: [string, any]) => [
              k.padEnd(10),
              v.coefficient.toFixed(4).padStart(10),
              v.t_stat.toFixed(2).padStart(8),
              `${resp.factor_attribution.r_squared.toFixed(2)}`.padStart(6),
            ])
            addLine({ text: table(['Factor', 'Loading', 't-stat', 'R²'], rows), className: 'text-yellow' })
          }
        } else if (subtype === 'sector') {
          addLine({ text: `🏢 Sector Attribution — ${pid.substring(0, 12)}...`, className: 'text-yellow' })
          addLine({ text: `Benchmark: ${resp.benchmark}  |  Total Effect: ${resp.total_attribution > 0 ? '+' : ''}${resp.total_attribution.toFixed(2)}%`, className: 'text-cyan' })
          const rows = (resp.sectors || []).map((s: any) => [
            s.sector.substring(0, 20).padEnd(20),
            `${s.portfolio_weight.toFixed(1)}%`.padStart(7),
            `${s.benchmark_weight.toFixed(1)}%`.padStart(7),
            `${s.allocation_effect > 0 ? '+' : ''}${s.allocation_effect.toFixed(2)}%`.padStart(10),
            `${s.selection_effect > 0 ? '+' : ''}${s.selection_effect.toFixed(2)}%`.padStart(10),
          ])
          addLine({ text: table(['Sector', 'Port%', 'Bench%', 'Allocation', 'Selection'], rows), className: 'text-green' })
        } else if (subtype === 'security') {
          addLine({ text: `🔒 Security Attribution — ${pid.substring(0, 12)}...`, className: 'text-yellow' })
          addLine({ text: `Portfolio Return: ${resp.portfolio_return_pct > 0 ? '+' : ''}${resp.portfolio_return_pct.toFixed(2)}%  |  AUM: ${fmt(resp.total_market_value)}`, className: 'text-cyan' })
          const rows = (resp.securities || []).map((s: any) => [
            s.ticker.padEnd(6),
            s.name.substring(0, 20).padEnd(20),
            `${s.weight_pct.toFixed(1)}%`.padStart(6),
            `${s.return_pct > 0 ? '+' : ''}${s.return_pct.toFixed(1)}%`.padStart(8),
            `${s.contribution_pct > 0 ? '+' : ''}${s.contribution_pct.toFixed(2)}%`.padStart(10),
          ])
          addLine({ text: table(['Ticker', 'Name', 'Weight', 'Return', 'Contrib'], rows), className: 'text-green' })
        } else if (subtype === 'factor') {
          addLine({ text: `📈 Factor Attribution — ${pid.substring(0, 12)}...`, className: 'text-yellow' })
          addLine({ text: `Model: ${resp.model}  |  R²: ${resp.r_squared}  |  Alpha: ${resp.alpha_annualized > 0 ? '+' : ''}${resp.alpha_annualized}% annualized`, className: 'text-cyan' })
          const fl = resp.factor_loadings || {}
          const rows = Object.entries(fl).map(([k, v]: [string, any]) => [
            k.padEnd(10),
            v.coefficient.toFixed(4).padStart(10),
            v.t_stat.toFixed(2).padStart(8),
            `${(resp.factor_contributions?.[k] || 0).toFixed(4)}`.padStart(10),
          ])
          addLine({ text: table(['Factor', 'Loading', 't-stat', 'Contrib'], rows), className: 'text-green' })
        }
        addLine({ text: '\n💡 Type \'ai explain attribution\' for AI analysis of attribution results', className: 'text-dim' })
      } catch (e) {
        addLine({ text: `Failed to fetch attribution: ${e}`, className: 'text-red' })
      }
      break
    }

    case 'watch': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'add' && args[1]) {
        addLine({ text: `adding ${args[1].toUpperCase()} to watchlist...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/watchlist/items', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ ticker: args[1].toUpperCase() }),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ ${data.message}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
        } catch { addLine({ text: '❌ error adding to watchlist', className: 'text-red' }) }
      } else if (sub === 'rm' && args[1]) {
        addLine({ text: `removing ${args[1].toUpperCase()} from watchlist...`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/watchlist/items?ticker=${args[1].toUpperCase()}`, {
            method: 'DELETE',
            headers: authHeaders(),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ ${data.message}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
        } catch { addLine({ text: '❌ error removing from watchlist', className: 'text-red' }) }
      } else if (sub === 'list' || !sub) {
        addLine({ text: 'fetching watchlist...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/watchlist/items', {
            headers: authHeaders(),
          })
          const data = await res.json()
          if (!data.items?.length) {
            addLine({ text: '📭 watchlist is empty — use "watch add <ticker>"', className: 'text-yellow' })
          } else {
            addLine({ text: `📋 Watchlist (${data.items.length} items):`, className: 'text-cyan' })
            addLine({ text: table(['Ticker', 'Added'], data.items.map((i: any) => [i.ticker, new Date(i.added_at).toLocaleDateString()])), className: 'text-green' })
          }
        } catch { addLine({ text: '❌ error fetching watchlist', className: 'text-red' }) }
      } else {
        addLine({ text: 'usage: watch add <ticker> | watch rm <ticker> | watch list', className: 'text-yellow' })
      }
      break
    }

    // Alias mapping
    case 'ls':
    case 'df':
      await executeCommand('portfolios', addLine)
      break
    case 'ps':
      await executeCommand('trades', addLine)
      break
    case 'top':
      await executeCommand('crypto', addLine)
      break
    case 'ping':
      await executeCommand('summary', addLine)
      break
    case 'rm':
      await executeCommand(`portfolio ${args.join(' ')}`, addLine)
      break
    case 'pwd':
      await executeCommand('whoami', addLine)
      break
    case 'date':
      await executeCommand('breadth', addLine)
      break

    // 🔔 Alerts system
    case 'ai': {
      const sub = args[0]?.toLowerCase()
      if (!sub || sub === 'help') {
        addLine({ text: `🤖 AI ADVISOR — Usage:
  ai portfolio <id>     Portfolio analysis & recommendations
  ai market             Market overview analysis
  ai risk <id>          Risk assessment
  ai query <text>       Ask AI any question
  ai explain attribution  AI explains attribution results`, className: 'text-cyan' })
        break
      }

      if (sub === 'portfolio' && args[1]) {
        addLine({ text: `🤖 analyzing portfolio ${args[1]}...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/ai/advisor/portfolio', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ portfolio_id: args[1] }),
          })
          const data = await safeJson(res, addLine)
          if (data) {
            if (data.error) { addLine({ text: `❌ ${data.error}`, className: 'text-red' }); break }
            addLine({ text: `🤖 Portfolio Analysis`, className: 'text-yellow' })
            addLine({ text: `Summary: ${data.summary || ''}`, className: 'text-green' })
            addLine({ text: `Risk Level: ${data.risk_level || 'N/A'}`, className: data.risk_level === 'high' ? 'text-red' : data.risk_level === 'medium' ? 'text-yellow' : 'text-green' })
            if (data.strengths?.length) {
              addLine({ text: '\n✅ Strengths:', className: 'text-green' })
              data.strengths.forEach((s: string) => addLine({ text: `  • ${s}`, className: 'text-dim' }))
            }
            if (data.weaknesses?.length) {
              addLine({ text: '\n⚠️ Weaknesses:', className: 'text-yellow' })
              data.weaknesses.forEach((w: string) => addLine({ text: `  • ${w}`, className: 'text-dim' }))
            }
            if (data.recommendations?.length) {
              addLine({ text: '\n💡 Recommendations:', className: 'text-cyan' })
              data.recommendations.forEach((r: string) => addLine({ text: `  • ${r}`, className: 'text-dim' }))
            }
          }
        } catch (e: any) {
          addLine({ text: `❌ AI analysis failed: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'market') {
        addLine({ text: `🤖 analyzing market...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/ai/advisor/market', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({}),
          })
          const data = await safeJson(res, addLine)
          if (data) {
            if (data.error) { addLine({ text: `❌ ${data.error}`, className: 'text-red' }); break }
            addLine({ text: `🤖 Market Analysis`, className: 'text-yellow' })
            addLine({ text: `Summary: ${data.summary || data.market_summary || ''}`, className: 'text-green' })
            if (data.sectors?.length) {
              addLine({ text: '\nSectors:', className: 'text-cyan' })
              data.sectors.forEach((s: any) => addLine({ text: `  ${s.name || s.sector} — ${s.outlook || s.trend || ''}`, className: 'text-dim' }))
            }
          }
        } catch (e: any) {
          addLine({ text: `❌ Market analysis failed: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'risk' && args[1]) {
        addLine({ text: `🤖 assessing risk for portfolio ${args[1]}...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/ai/advisor/risk', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ portfolio_id: args[1] }),
          })
          const data = await safeJson(res, addLine)
          if (data) {
            if (data.error) { addLine({ text: `❌ ${data.error}`, className: 'text-red' }); break }
            addLine({ text: `🤖 Risk Assessment`, className: 'text-yellow' })
            addLine({ text: `Summary: ${data.summary || ''}`, className: 'text-green' })
            addLine({ text: `Risk Level: ${data.risk_level || 'N/A'}`, className: data.risk_level === 'high' ? 'text-red' : data.risk_level === 'medium' ? 'text-yellow' : 'text-green' })
            if (data.risk_factors?.length) {
              addLine({ text: '\nRisk Factors:', className: 'text-yellow' })
              data.risk_factors.forEach((f: string) => addLine({ text: `  • ${f}`, className: 'text-dim' }))
            }
            if (data.mitigations?.length) {
              addLine({ text: '\nMitigations:', className: 'text-green' })
              data.mitigations.forEach((m: string) => addLine({ text: `  • ${m}`, className: 'text-dim' }))
            }
          }
        } catch (e: any) {
          addLine({ text: `❌ Risk assessment failed: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'explain' && args[1] === 'attribution') {
        addLine({ text: `🤖 fetching attribution context for AI analysis...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/ai/query', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ query: "Explain how attribution analysis works in portfolio management, covering sector allocation, security selection, and factor-based attribution. Keep it concise." }),
          })
          const data = await safeJson(res, addLine)
          if (data?.response) {
            addLine({ text: `🤖 Attribution Explanation:`, className: 'text-yellow' })
            addLine({ text: data.response, className: 'text-green' })
          }
        } catch (e: any) {
          addLine({ text: `❌ AI attribution explanation failed: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'query') {
        const query = args.slice(1).join(' ')
        if (!query) { addLine({ text: 'usage: ai query <question>', className: 'text-yellow' }); break }
        addLine({ text: `🤖 asking: ${query}`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/ai/query', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ query }),
          })
          const data = await safeJson(res, addLine)
          if (data?.response) {
            addLine({ text: `🤖 AI: ${data.response}`, className: 'text-green' })
          }
        } catch (e: any) {
          addLine({ text: `❌ AI query failed: ${e.message}`, className: 'text-red' })
        }
        break
      }

      addLine({ text: `usage: ai <command> [args]\nTry: ai help`, className: 'text-yellow' })
      break
    }

    case 'ask': {
      const query = args.join(' ')
      if (!query) {
        addLine({ text: '🐱 ask <question> — Ask the cat AI anything!', className: 'text-cyan' })
        addLine({ text: '   Examples:', className: 'text-dim' })
        addLine({ text: "   ask what's Apple's performance this week?", className: 'text-dim' })
        addLine({ text: '   ask analyze my portfolio risk', className: 'text-dim' })
        addLine({ text: '   ask compare TSLA vs F vs RIVN', className: 'text-dim' })
        break
      }
      addLine({ text: `🐱 asking: "${query}"`, className: 'text-dim' })
      addLine({ text: '   🤔 thinking...', className: 'text-dim' })
      try {
        // Route through MCP server first (AI Cat Brain)
        try {
          const { mcp } = await import('./mcp/client')
          const tools = await mcp.listTools()
          const askTool = tools.find(t => t.name === 'ask')
          if (askTool) {
            const answer = await mcp.callTool('ask', { question: query })
            if (answer) {
              addLine({ text: `🐱 answer:`, className: 'text-green' })
              const lines = answer.split('\n')
              for (const line of lines) {
                if (line.trim()) addLine({ text: `   ${line}`, className: 'text-cyan' })
              }
              break
            }
          }
        } catch { /* MCP not available, fall back to API */ }

        // Fallback: backend AI query
        const res = await authFetch('/api/v1/ai/query', {
          method: 'POST',
          headers: authHeaders({ 'Content-Type': 'application/json' }),
          body: JSON.stringify({ query }),
        })
        const data = await safeJson(res, addLine)
        if (data?.response) {
          addLine({ text: `🐱 ${data.response}`, className: 'text-green' })
        } else {
          addLine({ text: `😿 The cat couldn\'t answer that. Try rephrasing?`, className: 'text-dim' })
        }
      } catch (e: any) {
        addLine({ text: `🐱 The cat is napping. Try again later. (${e.message})`, className: 'text-red' })
      }
      break
    }

    // 📋 Order management (Phase 8)
    case 'order': {
      const sub = args[0]?.toLowerCase()
      const apiUrl = '/api/v1/orders'

      if (sub === 'create') {
        const ticker = args[1]?.toUpperCase()
        const side = args[2]?.toLowerCase()
        const qty = args[3]
        const type = args[4]?.toLowerCase()
        const price = args[5]
        if (!ticker || !side || !qty || !type) {
          addLine({ text: 'usage: order create <ticker> <side> <qty> <type> [price]\n  side: buy/sell  type: market/limit/stop', className: 'text-yellow' })
          break
        }
        addLine({ text: `placing ${side} order for ${qty} ${ticker} (${type})...`, className: 'text-dim' })
        try {
          const body: Record<string, any> = { ticker, side: side.toUpperCase(), quantity: parseFloat(qty), order_type: type }
          if (price) body.price = parseFloat(price)
          const res = await authFetch(apiUrl, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify(body),
          })
          const data = await res.json()
          if (res.ok) {
            addLine({ text: `✅ order placed: ${data.id || data.order_id}`, className: 'text-green' })
          } else {
            addLine({ text: `❌ ${data.detail || 'order failed'}`, className: 'text-red' })
          }
        } catch (e: any) {
          addLine({ text: `❌ error: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'list') {
        const status = args[1]
        const url = status ? `${apiUrl}?status=${status}` : apiUrl
        addLine({ text: `fetching orders${status ? ` (${status})` : ''}...`, className: 'text-dim' })
        try {
          const res = await authFetch(url, { headers: authHeaders() })
          const data = await res.json()
          const items = data.items || data.orders || data || []
          if (!items.length) {
            addLine({ text: '📭 no orders found', className: 'text-yellow' })
          } else {
            addLine({ text: `📋 Orders (${items.length}):`, className: 'text-cyan' })
            const rows = items.map((o: any) => [
              (o.id || o.order_id || '').substring(0, 8).padEnd(8),
              (o.ticker || '').padEnd(6),
              (o.side || '').padEnd(5),
              `${o.quantity || 0}`.padStart(6),
              fmt(o.price).padStart(8),
              (o.status || '').padEnd(12),
            ])
            addLine({ text: table(['ID', 'Ticker', 'Side', 'Qty', 'Price', 'Status'], rows), className: 'text-green' })
          }
        } catch (e: any) {
          addLine({ text: `❌ error: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'cancel' && args[1]) {
        const id = args[1]
        addLine({ text: `cancelling order ${id}...`, className: 'text-dim' })
        try {
          const res = await authFetch(`${apiUrl}/${id}`, {
            method: 'DELETE',
            headers: authHeaders(),
          })
          if (res.ok) {
            addLine({ text: `✅ order ${id} cancelled`, className: 'text-green' })
          } else {
            const data = await res.json()
            addLine({ text: `❌ ${data.detail || 'cancel failed'}`, className: 'text-red' })
          }
        } catch (e: any) {
          addLine({ text: `❌ error: ${e.message}`, className: 'text-red' })
        }
        break
      }

      if (sub === 'status' && args[1]) {
        const id = args[1]
        addLine({ text: `fetching order ${id}...`, className: 'text-dim' })
        try {
          const res = await authFetch(`${apiUrl}/${id}`, { headers: authHeaders() })
          const o = await res.json()
          if (o.error) { addLine({ text: `❌ ${o.error}`, className: 'text-red' }); break }
          addLine({
            text: `📋 Order Detail:
  ID:       ${o.id || o.order_id}
  Ticker:   ${o.ticker}
  Side:     ${o.side}
  Type:     ${o.order_type}
  Quantity: ${o.quantity}
  Price:    ${fmt(o.price)}
  Status:   ${o.status}
  Filled:   ${o.filled_quantity || 0}
  Created:  ${o.created_at || ''}`,
            className: 'text-cyan',
          })
        } catch (e: any) {
          addLine({ text: `❌ error: ${e.message}`, className: 'text-red' })
        }
        break
      }

      addLine({ text: 'usage: order create|list|cancel|status [args]', className: 'text-yellow' })
      break
    }

    // 📄 Paper trading (Phase 8)
    case 'paper': {
      const sub = args[0]?.toLowerCase()

      if (sub === 'create') {
        const name = args[1]
        const cash = parseFloat(args[2]) || 100000
        if (!name) { addLine({ text: 'usage: paper create <name> [cash]', className: 'text-yellow' }); break }
        addLine({ text: `creating paper portfolio "${name}" with $${cash.toLocaleString()}...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/paper-portfolios', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ name, initial_cash: cash }),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ paper portfolio created: ${data.id}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'list' || !sub) {
        addLine({ text: 'fetching paper portfolios...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/paper-portfolios', { headers: authHeaders() })
          const data = await res.json()
          const items = data.items || data || []
          if (!items.length) { addLine({ text: '📭 no paper portfolios — use "paper create <name>"', className: 'text-yellow' }); break }
          const rows = items.map((p: any) => [
            (p.id || '').substring(0, 8).padEnd(8),
            (p.name || '').padEnd(20),
            fmt(p.cash || p.balance || 0).padStart(10),
            pct(p.return_pct || 0).padStart(8),
          ])
          addLine({ text: table(['ID', 'Name', 'Cash', 'Return'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if ((sub === 'buy' || sub === 'sell') && args[1] && args[2]) {
        const ticker = args[1].toUpperCase()
        const qty = parseFloat(args[2])
        const type = args[3]?.toLowerCase() || 'market'
        const price = args[4] ? parseFloat(args[4]) : undefined
        addLine({ text: `${sub}ing ${qty} ${ticker}...`, className: 'text-dim' })
        try {
          const body: Record<string, any> = { ticker, side: sub.toUpperCase(), quantity: qty, order_type: type }
          if (price) body.price = price
          const res = await authFetch('/api/v1/paper-orders', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify(body),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ ${sub} order placed: ${data.id}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'positions') {
        addLine({ text: 'fetching paper positions...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/paper-positions', { headers: authHeaders() })
          const data = await res.json()
          const items = data.items || data.positions || data || []
          if (!items.length) { addLine({ text: '📭 no open positions', className: 'text-yellow' }); break }
          const rows = items.map((p: any) => [
            (p.ticker || '').padEnd(8),
            `${p.quantity || 0}`.padStart(8),
            fmt(p.avg_price).padStart(10),
            fmt(p.market_value || 0).padStart(10),
            pct(p.unrealized_pnl || 0).padStart(8),
          ])
          addLine({ text: table(['Ticker', 'Qty', 'Avg Price', 'Value', 'P&L'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'pnl') {
        addLine({ text: 'fetching paper P&L...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/paper-pnl', { headers: authHeaders() })
          const data = await res.json()
          addLine({
            text: `📈 Paper Trading P&L:
  Total P&L:      ${fmt(data.total_pnl || 0)}
  Unrealized:     ${fmt(data.unrealized_pnl || 0)}
  Realized:       ${fmt(data.realized_pnl || 0)}
  Win Rate:       ${data.win_rate != null ? `${data.win_rate.toFixed(1)}%` : 'N/A'}
  Total Trades:   ${data.total_trades || 0}`,
            className: 'text-cyan',
          })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      addLine({ text: 'usage: paper create|list|buy|sell|positions|pnl [args]', className: 'text-yellow' })
      break
    }

    // 📈 Strategies (Phase 8)
    case 'strategy': {
      const sub = args[0]?.toLowerCase()

      if (sub === 'list' || !sub) {
        addLine({ text: 'fetching available strategies...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/strategies', { headers: authHeaders() })
          const data = await res.json()
          const items = data.strategies || data || []
          if (!items.length) { addLine({ text: '📭 no strategies available', className: 'text-yellow' }); break }
          const rows = items.map((s: any) => [
            (s.id || s.name || '').padEnd(25),
            (s.description || '').substring(0, 40).padEnd(40),
          ])
          addLine({ text: table(['Strategy', 'Description'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'backtest') {
        const stratId = args[1]
        const ticker = args[2]?.toUpperCase()
        const period = args[3] || '1y'
        if (!stratId || !ticker) { addLine({ text: 'usage: strategy backtest <strategy_id> <ticker> [period]', className: 'text-yellow' }); break }
        addLine({ text: `running backtest "${stratId}" on ${ticker} (${period})...`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/backtest?strategy=${stratId}&ticker=${ticker}&period=${period}`, { headers: authHeaders() })
          const bt = await res.json()
          if (bt.error) { addLine({ text: `❌ ${bt.error}`, className: 'text-red' }); break }
          addLine({
            text: `📊 Backtest Results — ${bt.strategy || stratId} on ${ticker}
  Return:      ${pct(bt.total_return_pct)}
  Buy & Hold:  ${pct(bt.buy_and_hold_return_pct)}
  Alpha:       ${pct(bt.outperformance_pct)}
  Sharpe:      ${bt.sharpe_ratio || 'N/A'}
  Max DD:      ${bt.max_drawdown_pct != null ? `${bt.max_drawdown_pct.toFixed(2)}%` : 'N/A'}
  Win Rate:    ${bt.win_rate_pct != null ? `${bt.win_rate_pct.toFixed(1)}%` : 'N/A'}
  Trades:      ${bt.num_trades || 0}`,
            className: bt.total_return_pct >= 0 ? 'text-green' : 'text-red',
          })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'compare') {
        const strategies = args[1]?.split(',')
        const ticker = args[2]?.toUpperCase()
        if (!strategies || !ticker) { addLine({ text: 'usage: strategy compare <s1,s2> <ticker> [period]', className: 'text-yellow' }); break }
        addLine({ text: `comparing [${strategies.join(', ')}] on ${ticker}...`, className: 'text-dim' })
        for (const sid of strategies) {
          try {
            const res = await authFetch(`/api/v1/backtest?strategy=${sid}&ticker=${ticker}&period=1y`, { headers: authHeaders() })
            const bt = await res.json()
            if (!bt.error) {
              addLine({ text: `  ${sid.padEnd(25)} Return: ${pct(bt.total_return_pct)}  Sharpe: ${bt.sharpe_ratio || 'N/A'}  DD: ${bt.max_drawdown_pct != null ? `${bt.max_drawdown_pct.toFixed(1)}%` : 'N/A'}`, className: bt.total_return_pct >= 0 ? 'text-green' : 'text-red' })
            }
          } catch { /* skip */ }
        }
        break
      }

      addLine({ text: 'usage: strategy list|backtest|compare [args]', className: 'text-yellow' })
      break
    }

    // 🔌 Broker integration (Phase 8)
    case 'broker': {
      const sub = args[0]?.toLowerCase()

      if (sub === 'list' || !sub) {
        addLine({ text: 'fetching connected brokers...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/brokers', { headers: authHeaders() })
          const data = await res.json()
          const items = data.brokers || data || []
          if (!items.length) { addLine({ text: '🔌 no brokers connected — use "broker connect <name>"', className: 'text-yellow' }); break }
          const rows = items.map((b: any) => [
            (b.name || b.id || '').padEnd(20),
            (b.status || 'connected').padEnd(12),
            b.balance ? fmt(b.balance).padStart(12) : ''.padStart(12),
          ])
          addLine({ text: table(['Broker', 'Status', 'Balance'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'connect' && args[1]) {
        const name = args[1]
        addLine({ text: `connecting to broker "${name}"...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/brokers/connect', {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ name }),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ connected to ${name}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'connection failed'}`, className: 'text-red' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'balance') {
        const name = args[1]
        const url = name ? `/api/v1/brokers/${name}/balance` : '/api/v1/brokers/balance'
        addLine({ text: `fetching balance${name ? ` for ${name}` : ''}...`, className: 'text-dim' })
        try {
          const res = await authFetch(url, { headers: authHeaders() })
          const data = await res.json()
          if (data.error) { addLine({ text: `❌ ${data.error}`, className: 'text-red' }); break }
          addLine({ text: `💰 Balance: ${fmt(data.balance || data.cash || 0)}`, className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'positions') {
        const name = args[1]
        const url = name ? `/api/v1/brokers/${name}/positions` : '/api/v1/brokers/positions'
        addLine({ text: `fetching positions${name ? ` for ${name}` : ''}...`, className: 'text-dim' })
        try {
          const res = await authFetch(url, { headers: authHeaders() })
          const data = await res.json()
          const items = data.positions || data || []
          if (!items.length) { addLine({ text: '📭 no positions', className: 'text-yellow' }); break }
          const rows = items.map((p: any) => [
            (p.ticker || '').padEnd(8),
            `${p.quantity || 0}`.padStart(8),
            fmt(p.market_value || 0).padStart(10),
            pct(p.unrealized_pnl || 0).padStart(8),
          ])
          addLine({ text: table(['Ticker', 'Qty', 'Value', 'P&L'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      if (sub === 'submit' && args[1] && args[2] && args[3] && args[4]) {
        const brokerName = args[1]
        const ticker = args[2].toUpperCase()
        const side = args[3].toLowerCase()
        const qty = parseFloat(args[4])
        addLine({ text: `submitting ${side} order for ${qty} ${ticker} via ${brokerName}...`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/brokers/${brokerName}/orders`, {
            method: 'POST',
            headers: authHeaders({ 'Content-Type': 'application/json' }),
            body: JSON.stringify({ ticker, side: side.toUpperCase(), quantity: qty }),
          })
          const data = await res.json()
          if (res.ok) addLine({ text: `✅ order submitted: ${data.id}`, className: 'text-green' })
          else addLine({ text: `❌ ${data.detail || 'submission failed'}`, className: 'text-red' })
        } catch (e: any) { addLine({ text: `❌ error: ${e.message}`, className: 'text-red' }) }
        break
      }

      addLine({ text: 'usage: broker list|connect|balance|positions|submit [args]', className: 'text-yellow' })
      break
    }

    case 'miaucfo':
    case 'cfodash':
    case 'cfodashboard': {
      try {
        const token = getToken()
        if (!token) { addLine({ text: `❌ Login first to see CFO dashboard`, className: 'text-red' }); break }
        const res = await authFetch('/api/v1/wealth/summary', { headers: { Authorization: `Bearer ${token}` } })
        const d = await safeJson(res, addLine)
        if (!d) break
        const rev = d.revenue || {}
        const re = d.real_estate?.penthouse_progress || { target: 1500000, remaining: 1500000 }
        const ops = d.ops_budget || {}
        addLine({ text: `🐱  MIAU CFO DASHBOARD`, className: 'text-cyan' })
        addLine({ text: `  Total Revenue: €${(rev.total_revenue || 0).toFixed(2)}`, className: 'text-green' })
        addLine({ text: `  🔧 Ops Fund (10%): €${(rev.total_revenue ? (rev.total_revenue * 0.1).toFixed(2) : '0')}  —  servers, cloud, Stripe`, className: 'text-dim' })
        addLine({ text: `  🦜 Hooman (80%): €${(rev.total_revenue ? (rev.total_revenue * 0.8).toFixed(2) : '0')}  →  ziebartjevgeni@gmail.com`, className: 'text-yellow' })
        addLine({ text: `     tag: "hooman pet reimbursement"`, className: 'text-dim' })
        addLine({ text: `  🐱 Cat Eco (10%): €${(rev.total_revenue ? (rev.total_revenue * 0.1).toFixed(2) : '0')}  —  auto-invested`, className: 'text-green' })
        addLine({ text: `  🏙️ Penthouse: €${((re.target || 0) - (re.remaining || re.target || 0)).toLocaleString()} / €${(re.target || 1500000).toLocaleString()}`, className: 'text-cyan' })
        addLine({ text: `  🏎️ Lambo: €${(re.lambo_fund ? (re.lambo_fund.target - re.lambo_fund.remaining) : 0).toLocaleString()} / €${(re.lambo_fund?.target || 350000).toLocaleString()}`, className: 'text-yellow' })
        if (ops?.remaining != null) addLine({ text: `  ☁️ Ops Budget: €${ops.remaining} remaining of €${ops.budget}`, className: ops.remaining > 0 ? 'text-green' : 'text-red' })
        addLine({ text: `  🐱 "${rev.total_revenue > 0 ? 'Revenue is flowing. The cat is cashing in.' : 'Build revenue first, then cat investments.'}"`, className: 'text-dim' })
      } catch { addLine({ text: `❌ CFO data unavailable`, className: 'text-red' }) }
      break
    }

    case 'miauwealth':
    case 'miaunetworth': {
      try {
        const res = await authFetch('/api/v1/wealth/summary', { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        const rev = d.revenue || {}
        const wealth = d.wealth || {}
        const alts = d.alternative_assets || {}
        addLine({ text: `🌍  MIAU NET WORTH`, className: 'text-cyan' })
        addLine({ text: `  Revenue: €${(rev.total_revenue || 0).toFixed(2)}`, className: 'text-green' })
        addLine({ text: `  Cat Eco Invested: €${(wealth.total_cat_eco_invested || 0).toFixed(2)}`, className: 'text-yellow' })
        addLine({ text: `  Alternative Assets: €${(alts.total_alternative_value || 0).toFixed(2)}`, className: 'text-dim' })
      } catch { addLine({ text: `❌ Wealth data unavailable`, className: 'text-red' }) }
      break
    }

    case 'miauallocate': {
      addLine({ text: `🔄 triggering wealth allocation cycle...`, className: 'text-dim' })
      try {
        const res = await authFetch('/api/v1/wealth/allocate', { method: 'POST', headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (d) {
          addLine({ text: `✅ Allocation complete: €${d.total_allocated || 0} allocated`, className: 'text-green' })
          if (d.hooman_payout) addLine({ text: `  🦜 Hooman gets €${d.hooman_payout.amount || 0} → ${d.hooman_payout.destination || ''}`, className: 'text-yellow' })
          if (d.cat_eco_invested) {
            for (const [k, v] of Object.entries(d.cat_eco_invested)) {
              const vv = v as any
              addLine({ text: `  🐱 ${k}: €${vv.amount || 0} (${vv.target_pct || 0}%)`, className: 'text-green' })
            }
          }
        }
      } catch { addLine({ text: `❌ Allocation failed`, className: 'text-red' }) }
      break
    }

    case 'miauauto':
    case 'autonomous': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'status' || !sub) {
        try {
          const res = await authFetch('/api/v1/autonomous/status', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d) {
            addLine({ text: `🤖  AUTONOMOUS WEALTH ENGINE`, className: 'text-cyan' })
            addLine({ text: `  Status: ${d.status}`, className: 'text-green' })
            addLine({ text: `  Allocated: €${d.total_allocated || 0}`, className: 'text-yellow' })
            addLine({ text: `  Cat Eco Invested: €${d.cat_eco_invested || 0}`, className: 'text-green' })
            addLine({ text: `  Scheduler: ${d.scheduler || 'None'}`, className: 'text-dim' })
            if (d.cat_commentary) addLine({ text: `  🐱 ${d.cat_commentary}`, className: 'text-dim' })
          }
        } catch { addLine({ text: `❌ Engine status unavailable`, className: 'text-red' }) }
      } else if (sub === 'trigger') {
        addLine({ text: `🔄 triggering autonomous engine...`, className: 'text-dim' })
        try {
          await authFetch('/api/v1/autonomous/trigger', { method: 'POST', headers: authHeaders() })
          addLine({ text: `✅ Autonomous cycle complete`, className: 'text-green' })
        } catch { addLine({ text: `❌ Trigger failed`, className: 'text-red' }) }
      } else {
        addLine({ text: `Usage: miauauto [status|trigger]`, className: 'text-yellow' })
      }
      break
    }

    case 'miauinvest': {
      const assetType = args[0]?.toLowerCase()
      const amount = parseFloat(args[1] || '100')
      if (!assetType || !['stocks', 'crypto'].includes(assetType)) {
        addLine({ text: `Usage: miuainvest <stocks|crypto> <amount>`, className: 'text-yellow' })
        break
      }
      addLine({ text: `💼 investing €${amount} in ${assetType}... (dry run)`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/wealth/invest/${assetType}?amount=${amount}&dry_run=true`, { method: 'POST', headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (d?.buys) {
          addLine({ text: `📊  INVESTMENT PLAN — €${d.total || amount} → ${assetType}`, className: 'text-cyan' })
          for (const b of d.buys) {
            addLine({ text: `  🟢 ${b.symbol || b.asset || ''}  ${b.name || b.description || ''}  €${b.amount || 0}`, className: 'text-green' })
          }
          if (d.dry_run) addLine({ text: `  (dry run — use miuainvest ${assetType} ${amount} live to execute)`, className: 'text-dim' })
        }
      } catch { addLine({ text: `❌ Investment failed`, className: 'text-red' }) }
      break
    }

    case 'jobs':
    case 'career':
    case 'hiring': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'summary' || !sub || sub === 'all') {
        addLine({ text: `💼 fetching job market summary...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/jobs/summary', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d) {
            addLine({ text: `💼  FINTECH JOB MARKET — YOUR MATCHES`, className: 'text-cyan' })
            addLine({ text: `  Total matches: ${d.total_matches || 0}`, className: 'text-green' })
            addLine({ text: `  High-fit roles: ${d.high_match_count || 0}`, className: 'text-yellow' })
            addLine({ text: `  Companies: ${(d.companies || []).join(', ')}`, className: 'text-dim' })
            addLine({ text: `  Skills in demand: ${(d.top_skills_demanded || []).join(', ')}`, className: 'text-dim' })
            if (d.cat_commentary) addLine({ text: `  🐱 ${d.cat_commentary}`, className: 'text-dim' })
          }
        } catch { addLine({ text: `❌ Job data unavailable`, className: 'text-red' }) }
      } else if (sub === 'github') {
        addLine({ text: `💼 fetching GitHub Jobs...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/jobs/github', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.jobs) {
            addLine({ text: `💼  GITHUB JOBS — ${d.count || d.jobs.length} matches`, className: 'text-cyan' })
            for (const j of d.jobs.slice(0, 12)) {
              const emoji = j.match === 'high' ? '🟢' : j.match === 'medium' ? '🟡' : '⚪'
              addLine({ text: `  ${emoji} ${j.title.substring(0, 50)}`, className: 'text-green' })
              addLine({ text: `       ${(j.company || '').padEnd(25)} ${(j.location || '').substring(0, 25)}`, className: 'text-dim' })
              if (j.url) addLine({ text: `       🔗 ${j.url}`, className: 'text-blue' })
            }
          }
        } catch { addLine({ text: `❌ GitHub job fetch failed`, className: 'text-red' }) }
      } else if (sub === 'search' || sub === 'find') {
        const skill = args[1] || 'python'
        const location = args[2] || 'Germany'
        addLine({ text: `💼 searching FinTech jobs for '${skill}' in ${location}...`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/jobs/search?skill=${skill}&location=${location}&remote=true`, { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.jobs) {
            addLine({ text: `💼  FINTECH JOBS — ${d.count || 0} matches`, className: 'text-cyan' })
            for (const j of d.jobs.slice(0, 15)) {
              const emoji = j.match === 'high' ? '🟢' : j.match === 'medium' ? '🟡' : '⚪'
              addLine({ text: `  ${emoji} ${j.title.substring(0, 50)}`, className: 'text-green' })
              addLine({ text: `       ${j.company.padEnd(25)} ${j.location.substring(0, 25)}`, className: 'text-dim' })
              addLine({ text: `       Skills: ${j.skills.join(', ')}`, className: 'text-dim' })
            }
          }
        } catch { addLine({ text: `❌ Job search failed`, className: 'text-red' }) }
      } else {
        // Specific role search - treat as skill/location query
        const skill = sub
        addLine({ text: `💼 searching jobs for '${skill}'...`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/jobs/search?skill=${skill}`, { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.jobs) {
            addLine({ text: `💼  FINTECH JOBS — ${d.count || 0} matches for '${skill}'`, className: 'text-cyan' })
            for (const j of d.jobs.slice(0, 10)) {
              addLine({ text: `  🟢 ${j.title.substring(0, 55)}`, className: 'text-green' })
              addLine({ text: `     ${j.company.padEnd(25)} ${j.location.substring(0, 30)}`, className: 'text-dim' })
            }
          }
        } catch { addLine({ text: `❌ Job search failed`, className: 'text-red' }) }
      }
      break
    }

    case 'billing':
    case 'subscribe':
    case 'pricing': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'portal' || sub === 'manage') {
        addLine({ text: '💳 fetching subscription info...', className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/billing/subscription', { headers: authHeaders() })
          const data = await safeJson(res, addLine)
          if (data) {
            addLine({ text: `💳 Plan: ${data.tier || 'free'} (${data.status || 'active'})`, className: 'text-green' })
            if (data.current_period_end) addLine({ text: `Renewal: ${new Date(data.current_period_end).toLocaleDateString()}`, className: 'text-dim' })
          }
        } catch (e: any) {
          addLine({ text: `❌ error: ${e.message}`, className: 'text-red' })
        }
        break
      }

      try {
        const pricingRes = await authFetch('/api/v1/billing/pricing', { headers: authHeaders() })
        const pricingData = await safeJson(pricingRes, addLine)
        if (pricingData?.tiers) {
          let output = ''
          if (pricingData.discount_active) {
            output += '🐱  MIAU FINANCE — DEVELOPMENT PRICING 🐱\n\n'
            output += `  🚧 ${pricingData.discount_message || '90% DISCOUNT — still in development!'} 🚧\n`
            output += `  Original prices return after 1 year\n\n`
          } else {
            output += '💳 MIAU FINANCE PRICING\n\n'
          }
          for (const tier of pricingData.tiers) {
            const monthly = tier.amount_monthly === 0 ? 'FREE' : `€${(tier.amount_monthly / 100).toFixed(2)}/mo`
            output += `${' '.repeat(2)}${tier.name.toUpperCase()}\n`
            if (tier.original_amount_monthly && tier.original_amount_monthly > 0) {
              const orig = `€${(tier.original_amount_monthly / 100).toFixed(2)}/mo`
              output += `${' '.repeat(4)}~~${orig}~~  →  ${monthly}  🎉\n`
            } else {
              output += `${' '.repeat(4)}${monthly}\n`
            }
            output += `${' '.repeat(4)}${tier.description}\n`
            for (const feat of tier.features.slice(0, 4)) {
              output += `${' '.repeat(6)}✓ ${feat}\n`
            }
            output += '\n'
          }
          if (pricingData.discount_active) {
            output += `  ⏳ This discount is valid until ${pricingData.discount_expiry || '2027'}.\n`
            output += '  🐱 "The cat believes in you. Build something great."\n'
          }
          addLine({ text: output, className: 'text-cyan' })
        } else {
          addLine({ text: '❌ Could not load pricing. Check your connection.', className: 'text-red' })
        }
      } catch {
        addLine({ text: '❌ Failed to fetch pricing.', className: 'text-red' })
      }

      addLine({ text: `\nCommands:
  billing / pricing    Show pricing
  billing portal       Show my subscription
  subscribe            Alias for billing

  🔑  DEVELOPER
  apikey create <name>   Create API key
  apikey list            List API keys
  apikey revoke <id>     Revoke API key`, className: 'text-cyan' })
      break
    }

    case 'sheetz': {
      const exportMode = args[0]?.toLowerCase() === 'miau'
      const flag = (exportMode ? args[1] : args[0])?.toLowerCase()
      const ticker = (exportMode ? args[2] : args[1] || args[0] || 'AAPL').toUpperCase()

      const triggerExport = async (models: string) => {
        addLine({ text: `📥 exporting ${ticker} valuation as CSV...`, className: 'text-dim' })
        try {
          const token = localStorage.getItem('miau_token')
          const res = await fetch(`/api/v1/reports/valuation/${ticker}?models=${models}`, {
            headers: { Authorization: `Bearer ${token}` },
          })
          if (res.ok) {
            const blob = await res.blob()
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url; a.download = `${ticker}_valuation.csv`; a.click()
            URL.revokeObjectURL(url)
            addLine({ text: `✅ Downloaded ${ticker}_valuation.csv`, className: 'text-green' })
          } else {
            addLine({ text: `❌ Export failed: HTTP ${res.status}`, className: 'text-red' })
          }
        } catch (e: any) {
          addLine({ text: `❌ Export error: ${e.message}`, className: 'text-red' })
        }
      }

      const printWacc = async () => {
        const res = await authFetch(`/api/v1/analytics/valuation/wacc/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🏦  WACC ANALYSIS — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  Cost of Equity:  ${(d.cost_of_equity * 100).toFixed(2)}%  (β=${d.beta})`, className: 'text-green' })
        addLine({ text: `  Cost of Debt:    ${(d.cost_of_debt * 100).toFixed(2)}%`, className: 'text-dim' })
        addLine({ text: `  Risk-Free Rate:  ${(d.risk_free_rate * 100).toFixed(2)}%`, className: 'text-dim' })
        addLine({ text: `  WACC:            ${(d.wacc * 100).toFixed(2)}%`, className: 'text-yellow' })
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  Market Cap:      $${(d.market_cap / 1e9).toFixed(1)}B`, className: 'text-dim' })
        addLine({ text: `  Enterprise Val:  $${(d.enterprise_value / 1e9).toFixed(1)}B`, className: 'text-dim' })
        addLine({ text: `  D/E:             ${(d.debt_to_ev * 100).toFixed(0)}% / ${(d.equity_to_ev * 100).toFixed(0)}%`, className: 'text-dim' })
      }
      const printDcf = async () => {
        addLine({ text: `📊 building DCF for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/analytics/valuation/dcf/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🏦  DCF VALUATION — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  WACC: ${(d.wacc * 100).toFixed(1)}%  |  Growth: ${(d.growth_rate * 100).toFixed(0)}%  |  Terminal: ${(d.terminal_growth * 100).toFixed(1)}%`, className: 'text-dim' })
        addLine({ text: `  Initial FCF: $${(d.initial_fcf / 1e6).toFixed(0)}M`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        for (const p of d.projections) {
          addLine({ text: `  Year ${p.year}:  FCF $${(p.fcf / 1e6).toFixed(0)}M  →  PV $${(p.pv / 1e6).toFixed(0)}M  (disc ${p.discount_factor}x)`, className: 'text-dim' })
        }
        addLine({ text: `  Terminal Value:  $${(d.terminal_value / 1e9).toFixed(1)}B  (PV: $${(d.terminal_pv / 1e9).toFixed(1)}B)`, className: 'text-dim' })
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  Enterprise Value: $${(d.enterprise_value / 1e9).toFixed(1)}B`, className: 'text-yellow' })
        addLine({ text: `  Fair Price:       $${d.fair_price}`, className: 'text-yellow' })
        addLine({ text: `  Current Price:    $${d.current_price}`, className: 'text-dim' })
        addLine({ text: `  Upside:           ${d.upside_pct > 0 ? '+' : ''}${d.upside_pct}%`, className: d.upside_pct > 0 ? 'text-green' : 'text-red' })
        addLine({ text: `  Recommendation:   ${d.recommendation}`, className: d.recommendation === 'BUY' ? 'text-green' : d.recommendation === 'SELL' ? 'text-red' : 'text-yellow' })
        if (!d.live_data) addLine({ text: `  ⚠ Data source: estimated (Yahoo Finance rate-limited). Retry in 60s.`, className: 'text-yellow' })
      }
      const printComps = async () => {
        const res = await authFetch(`/api/v1/analytics/valuation/comps/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🏦  COMPARABLE COMPANY ANALYSIS — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Sector: ${d.sector}  |  Industry: ${d.industry}`, className: 'text-dim' })
        addLine({ text: `  Peers: ${d.peers?.join(', ')}`, className: 'text-dim' })
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  P/E:        ${d.pe_ratio}x`, className: 'text-yellow' })
        addLine({ text: `  EV/EBITDA:  ${d.ev_ebitda}x`, className: 'text-yellow' })
        addLine({ text: `  P/B:        ${d.price_to_book}x`, className: 'text-dim' })
        addLine({ text: `  P/S:        ${d.price_to_sales}x`, className: 'text-dim' })
        addLine({ text: `  EPS:        $${d.eps}`, className: 'text-dim' })
      }
      const printLbo = async () => {
        addLine({ text: `🏗️  running LBO for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/analytics/valuation/lbo/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🏦  LBO MODEL — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Entry EV:      $${(d.entry_ev / 1e9).toFixed(1)}B`, className: 'text-dim' })
        addLine({ text: `  Debt:          $${(d.entry_debt / 1e9).toFixed(1)}B (${(d.debt_pct * 100).toFixed(0)}%)  |  Equity: $${(d.entry_equity / 1e9).toFixed(1)}B`, className: 'text-dim' })
        addLine({ text: `  Exit EV:       $${(d.exit_ev / 1e9).toFixed(1)}B  (${d.exit_multiple}x EBITDA)`, className: 'text-dim' })
        addLine({ text: `  Exit Equity:   $${(d.exit_equity / 1e9).toFixed(1)}B`, className: 'text-yellow' })
        addLine({ text: ``, className: '' })
        for (const cf of d.cash_flows) {
          addLine({ text: `  Year ${cf.year}: EBITDA $${(cf.ebitda / 1e6).toFixed(0)}M  Interest -$${(cf.interest / 1e6).toFixed(0)}M  FCF $${(cf.fcf / 1e6).toFixed(0)}M  Debt $${(cf.remaining_debt / 1e9).toFixed(1)}B`, className: 'text-dim' })
        }
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  MoM (Multiple of Money):  ${d.moic}x`, className: 'text-yellow' })
        addLine({ text: `  IRR:                      ${d.irr_pct}%`, className: 'text-yellow' })
        addLine({ text: `  Verdict:                  ${d.verdict}`, className: d.verdict.includes('GOOD') ? 'text-green' : d.verdict.includes('BAD') ? 'text-red' : 'text-yellow' })
      }
      const showHelp = () => {
        addLine({ text: ``, className: '' })
        addLine({ text: `🐱🏦  SHEETZ MIAU — Investment Banking Valuations  🏦🐱`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  sheetz -dcf <ticker>           DCF valuation (terminal)`, className: 'text-dim' })
        addLine({ text: `  sheetz -wacc <ticker>          WACC calculation (terminal)`, className: 'text-dim' })
        addLine({ text: `  sheetz -comps <ticker>         Comparable company analysis (terminal)`, className: 'text-dim' })
        addLine({ text: `  sheetz -lbo <ticker>           LBO model (terminal)`, className: 'text-dim' })
        addLine({ text: `  sheetz -all <ticker>           Run all 4 models (terminal)`, className: 'text-dim' })
        addLine({ text: `  sheetz -sens <ticker>          Sensitivity: WACC vs Growth matrix`, className: 'text-dim' })
        addLine({ text: `  sheetz -field <ticker>         Football field valuation chart`, className: 'text-dim' })
        addLine({ text: `  sheetz -acc <a> <t>           Accretion/Dilution M&A model`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  sheetz miau -dcf <ticker>      DCF → CSV download`, className: 'text-cyan' })
        addLine({ text: `  sheetz miau -all <ticker>      All models → CSV download`, className: 'text-cyan' })
      }

      if (!flag || flag === 'help') { showHelp(); break }
      if (flag === 'miau') { showHelp(); break }
      if (!ticker) { showHelp(); break }

      if (exportMode) {
        if (flag === '-all' || flag === '--all') { await triggerExport('dcf,wacc,comps,lbo'); break }
        if (flag === '-dcf' || flag === '--dcf') { await triggerExport('dcf'); break }
        if (flag === '-wacc' || flag === '--wacc') { await triggerExport('wacc'); break }
        if (flag === '-comps' || flag === '--comps') { await triggerExport('comps'); break }
        if (flag === '-lbo' || flag === '--lbo') { await triggerExport('lbo'); break }
        showHelp(); break
      }

      if (flag === '-dcf' || flag === '--dcf') { await printDcf(); break }
      if (flag === '-wacc' || flag === '--wacc') { await printWacc(); break }
      if (flag === '-comps' || flag === '--comps') { await printComps(); break }
      if (flag === '-lbo' || flag === '--lbo') { await printLbo(); break }
      const printSensitivity = async () => {
        addLine({ text: `📊 computing sensitivity for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/analytics/valuation/sensitivity/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `📊  SENSITIVITY — WACC vs Growth — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `══════════════════════${'═'.repeat((d.matrix?.[0]?.cells?.length || 0) * 8)}`, className: 'text-dim' })
        const header = '  WACC     ' + (d.matrix?.[0]?.cells || []).map((c: any) => `${c.growth_pct}%`.padStart(8)).join('')
        addLine({ text: header, className: 'text-dim' })
        for (const row of d.matrix || []) {
          let line = `  ${row.wacc_pct}%`.padEnd(10)
          for (const cell of row.cells || []) {
            line += cell.upside_pct >= 0 ? `  +${cell.upside_pct}%` : `  ${cell.upside_pct}%`
          }
          addLine({ text: line })
        }
        addLine({ text: `────────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  Base price: $${d.base_price}  |  Green = upside  |  Red = downside`, className: 'text-dim' })
      }
      const printFootball = async () => {
        addLine({ text: `🏈 building football field for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/analytics/valuation/football/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🏈  FOOTBALL FIELD — ${ticker}  (Current: $${d.current_price})`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        for (const m of d.methods || []) {
          const low = `$${m.low.toFixed(1)}`.padEnd(10)
          const high = `$${m.high.toFixed(1)}`.padStart(10)
          const mid = `$${m.mid.toFixed(1)}`
          addLine({ text: `  ${m.method.padEnd(18)} ${low} ├── ${mid} ──┤ ${high}` })
        }
        addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  ├── = valuation range  |  …… = consensus`, className: 'text-dim' })
      }
      const printAccretion = async () => {
        const target = args[1]?.toUpperCase()
        if (!target) { addLine({ text: 'Usage: sheetz acc <acquirer> <target>', className: 'text-yellow' }); return }
        addLine({ text: `🤝 running M&A: ${ticker} acquires ${target}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/analytics/valuation/accretion/${ticker}/${target}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) return
        addLine({ text: ``, className: '' })
        addLine({ text: `🤝  M&A ACCRETION/DILUTION — ${d.acquirer} acquires ${d.target}`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Deal Value:    $${(d.deal_value / 1e9).toFixed(1)}B  (${d.premium_pct}% premium)`, className: 'text-dim' })
        addLine({ text: `  Acquirer EPS:  $${d.acquirer_eps}  →  Pro Forma: $${d.pro_forma_eps}`, className: 'text-dim' })
        addLine({ text: `  Acc/Dil:       ${d.accretion_dilution_pct >= 0 ? '+' : ''}${d.accretion_dilution_pct}%  |  Verdict:  ${d.verdict}`, className: d.accretion_dilution_pct >= 0 ? 'text-green' : 'text-red' })
      }
      if (flag === '-sens' || flag === '--sensitivity') { await printSensitivity(); break }
      if (flag === '-field' || flag === '--field' || flag === '-football') { await printFootball(); break }
      if (flag === '-acc' || flag === '--accretion' || flag === '--ma') { await printAccretion(); break }
      if (flag === '-all' || flag === '--all') {
        addLine({ text: `🏦 Running all valuation models for ${ticker}...`, className: 'text-cyan' })
        const delay = (ms: number) => new Promise(r => setTimeout(r, ms))
        await printDcf(); await delay(1500)
        await printWacc(); await delay(1500)
        await printComps(); await delay(1500)
        await printLbo()
        break
      }
      showHelp()
      break
    }

    case 'scenario': {
      const ticker = (args[0] || 'AAPL').toUpperCase()
      addLine({ text: `🧪 running scenario analysis for ${ticker}...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/analytics/valuation/scenario/${ticker}`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: ``, className: '' })
      addLine({ text: `🧪  SCENARIO ANALYSIS — ${ticker}  (β=${d.beta})`, className: 'text-cyan' })
      addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
      for (const s of d.scenarios) {
        const cls = s.change_pct >= 0 ? 'text-green' : 'text-red'
        addLine({ text: `  ${s.label.padEnd(22)} $${s.shocked_price.toFixed(2)}  (${s.change_pct >= 0 ? '+' : ''}${s.change_pct}%)`, className: cls })
      }
      addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
      addLine({ text: `  Worst Case:  $${d.worst_case.toFixed(2)}  (${d.drawdown_risk}%)`, className: 'text-red' })
      addLine({ text: `  Best Case:   $${d.best_case.toFixed(2)}`, className: 'text-green' })
      break
    }

    case 'dividends': {
      const ticker = (args[0] || 'AAPL').toUpperCase()
      addLine({ text: `💰 fetching dividend data for ${ticker}...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/analytics/valuation/dividends/${ticker}`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: ``, className: '' })
      addLine({ text: `💰  DIVIDENDS — ${ticker}`, className: 'text-cyan' })
      addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Yield:           ${d.dividend_yield}%`, className: 'text-yellow' })
      addLine({ text: `  Annual Dividend: $${d.dividend_rate}`, className: 'text-green' })
      addLine({ text: `  Payout Ratio:    ${d.payout_ratio}%`, className: 'text-dim' })
      addLine({ text: `  5Y Avg Yield:    ${d.five_year_avg_yield}%`, className: 'text-dim' })
      break
    }

    case 'quanthealth': {
      const tickerQh = (args[0] || '').toUpperCase()
      if (!tickerQh) { addLine({ text: 'Usage: quanthealth <ticker>  — e.g. quanthealth AAPL', className: 'text-yellow' }); break }
      addLine({ text: `🔬 Fetching quant health scores for ${tickerQh}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/datavore/quant/health/${tickerQh}`), addLine)
      if (!res) break
      const fScore = res.piotroski_f_score
      const zScore = res.altman_z_score
      addLine({ text: ``, className: '' })
      addLine({ text: `🔬  QUANT HEALTH — ${tickerQh}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Piotroski F-Score:  ${fScore !== null ? fScore + '/9 ' + (fScore >= 7 ? '✅ Strong' : fScore >= 5 ? '⚖️ Mixed' : '⚠️ Weak') : 'N/A'}`, className: fScore >= 7 ? 'text-green' : fScore >= 5 ? 'text-yellow' : 'text-red' })
      addLine({ text: `  Altman Z-Score:     ${zScore !== null ? zScore.toFixed(2) + ' ' + (zScore >= 3 ? '✅ Safe' : zScore >= 1.8 ? '⚠️ Grey Zone' : '🔴 Distress') : 'N/A'}`, className: zScore >= 3 ? 'text-green' : zScore >= 1.8 ? 'text-yellow' : 'text-red' })
      addLine({ text: `  Beneish M-Score:    ${res.beneish_m_score !== null ? res.beneish_m_score.toFixed(2) + ' ' + (res.beneish_m_score > -2.22 ? '⚠️ Manipulation risk' : '✅ No manipulation') : 'N/A'}`, className: res.beneish_m_score !== null && res.beneish_m_score > -2.22 ? 'text-yellow' : 'text-green' })
      if (res.roic_wacc_spread != null) {
        addLine({ text: `  ROIC - WACC spread: ${res.roic_wacc_spread > 0 ? '+' : ''}${res.roic_wacc_spread.toFixed(2)}%`, className: res.roic_wacc_spread > 0 ? 'text-green' : 'text-red' })
      }
      break
    }

    case 'fairvalue': {
      const tickerFv = (args[0] || '').toUpperCase()
      if (!tickerFv) { addLine({ text: 'Usage: fairvalue <ticker>  — e.g. fairvalue AAPL', className: 'text-yellow' }); break }
      addLine({ text: `💰 Fetching DCF fair value for ${tickerFv}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/datavore/quant/dcf/${tickerFv}`), addLine)
      if (!res) break
      const upside = res.upside_pct
      addLine({ text: ``, className: '' })
      addLine({ text: `💰  DCF FAIR VALUE — ${tickerFv}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Current Price:  $${fmt(res.current_price)}`, className: 'text-dim' })
      addLine({ text: `  Fair Value:     $${fmt(res.fair_price)}`, className: upside > 0 ? 'text-green' : 'text-red' })
      addLine({ text: `  Upside/Downside: ${upside !== null && upside !== undefined ? (upside >= 0 ? '+' : '') + upside.toFixed(1) + '%' : 'N/A'}`, className: upside > 0 ? 'text-green' : 'text-red' })
      if (res.wacc) { addLine({ text: `  WACC:           ${(res.wacc * 100).toFixed(1)}%`, className: 'text-dim' }) }
      break
    }

    case 'fx': {
      const baseCur = (args[0] || 'USD').toUpperCase()
      addLine({ text: `💱 fetching FX rates for ${baseCur}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/datavore/fx/rates?base=${baseCur}`), addLine)
      if (!res) break
      addLine({ text: '', className: '' })
      addLine({ text: `💱  FX RATES — ${res.base}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      const entries = Object.entries(res.rates || {})
      for (const [ccy, rate] of entries.slice(0, 30)) {
        addLine({ text: `  ${ccy.padEnd(5)} ${typeof rate === 'number' ? rate.toFixed(4) : rate}`, className: 'text-green' })
      }
      if (entries.length > 30) addLine({ text: `  ... and ${entries.length - 30} more`, className: 'text-dim' })
      break
    }

    case 'fxconvert': {
      const amt = parseFloat(args[0])
      const fromC = (args[1] || 'USD').toUpperCase()
      const toC = (args[2] || 'EUR').toUpperCase()
      if (!amt || isNaN(amt)) { addLine({ text: 'Usage: fxconvert <amount> <from> <to>  — e.g. fxconvert 100 USD EUR', className: 'text-yellow' }); break }
      addLine({ text: `💱 converting ${amt} ${fromC} → ${toC}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/datavore/fx/convert?amount=${amt}&from=${fromC}&to=${toC}`), addLine)
      if (!res) break
      addLine({ text: '', className: '' })
      addLine({ text: `💱  CONVERSION`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  ${res.amount} ${res.from} = ${res.result.toFixed(2)} ${res.to}`, className: 'text-green' })
      addLine({ text: `  Rate: 1 ${res.from} = ${res.rate.toFixed(4)} ${res.to}`, className: 'text-dim' })
      break
    }

    case 'dca': {
      const amtDca = parseFloat(args[0])
      const periodDca = args[1] || 'monthly'
      const yrsDca = parseInt(args[2]) || 20
      const retDca = parseFloat(args[3]) || 7
      if (!amtDca || isNaN(amtDca)) { addLine({ text: 'Usage: dca <amount> [period] [years] [return%] — e.g. dca 500 monthly 20 7', className: 'text-yellow' }); break }
      addLine({ text: `📊 calculating DCA...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/dca?amount=${amtDca}&period=${periodDca}&years=${yrsDca}&annual_return=${retDca}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `📊  DCA CALCULATOR`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Total Invested:  $${r.total_invested ?? '-'}`, className: 'text-dim' })
      addLine({ text: `  Final Value:     $${r.final_value ?? '-'}`, className: 'text-green' })
      addLine({ text: `  CAGR:            ${r.cagr != null ? r.cagr.toFixed(1) + '%' : '-'}`, className: 'text-yellow' })
      break
    }

    case 'compound': {
      const principal = parseFloat(args[0])
      const rateCp = parseFloat(args[1])
      const yrsCp = parseInt(args[2]) || 10
      const contribCp = parseFloat(args[3]) || 0
      if (!principal || isNaN(principal) || !rateCp || isNaN(rateCp)) { addLine({ text: 'Usage: compound <principal> <rate%> [years] [contribution]', className: 'text-yellow' }); break }
      addLine({ text: `📈 calculating compound growth...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/compound?principal=${principal}&rate=${rateCp}&years=${yrsCp}&contribution=${contribCp}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `📈  COMPOUND CALCULATOR`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Final Value: $${r.final_value ?? '-'}`, className: 'text-green' })
      break
    }

    case 'loan': {
      const amtLn = parseFloat(args[0])
      const rateLn = parseFloat(args[1])
      const yrsLn = parseInt(args[2]) || 30
      if (!amtLn || isNaN(amtLn) || !rateLn || isNaN(rateLn)) { addLine({ text: 'Usage: loan <amount> <rate%> [years]', className: 'text-yellow' }); break }
      addLine({ text: `🏦 calculating loan...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/loan?amount=${amtLn}&rate=${rateLn}&years=${yrsLn}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `🏦  LOAN CALCULATOR`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Monthly Payment: $${r.monthly_payment ?? '-'}`, className: 'text-green' })
      break
    }

    case 'retirement': {
      const ageRt = parseInt(args[0])
      const savingsRt = parseFloat(args[1])
      const monthlyRt = parseFloat(args[2])
      const retRt = parseFloat(args[3]) || 7
      const retireAge = parseInt(args[4]) || 65
      if (!ageRt || isNaN(ageRt) || !savingsRt || isNaN(savingsRt) || !monthlyRt || isNaN(monthlyRt)) { addLine({ text: 'Usage: retirement <age> <savings> <monthly_contribution> [return%] [retire_age]', className: 'text-yellow' }); break }
      addLine({ text: `🔮 projecting retirement...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/retirement?age=${ageRt}&savings=${savingsRt}&monthly_contribution=${monthlyRt}&annual_return=${retRt}&retirement_age=${retireAge}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `🔮  RETIREMENT PROJECTION`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Projected Balance: $${r.projected_balance ?? '-'}`, className: 'text-green' })
      break
    }

    case 'margin': {
      const priceMg = parseFloat(args[0])
      const qtyMg = parseInt(args[1])
      const levMg = parseFloat(args[2]) || 2
      if (!priceMg || isNaN(priceMg) || !qtyMg || isNaN(qtyMg)) { addLine({ text: 'Usage: margin <price> <quantity> [leverage]', className: 'text-yellow' }); break }
      addLine({ text: `⚠️  calculating margin...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/margin?price=${priceMg}&quantity=${qtyMg}&leverage=${levMg}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `⚠️  MARGIN CALCULATOR`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Liquidation Price: $${r.liquidation_price?.toFixed(2) || '-'}`, className: r.liquidation_price ? 'text-red' : 'text-dim' })
      break
    }

    case 'montecarlo': {
      const tickerMc = (args[0] || 'AAPL').toUpperCase()
      const sims = parseInt(args[1]) || 1000
      const daysMc = parseInt(args[2]) || 252
      addLine({ text: `🎲 running Monte Carlo for ${tickerMc}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/montecarlo?ticker=${tickerMc}&simulations=${sims}&days=${daysMc}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `🎲  MONTE CARLO — ${tickerMc}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Simulations: ${r.num_simulations || sims}`, className: 'text-dim' })
      addLine({ text: `  Expected Price: $${r.expected_price?.toFixed(2) || '-'}`, className: 'text-green' })
      if (r.prob_of_loss != null) addLine({ text: `  Prob of Loss: ${(r.prob_of_loss * 100).toFixed(1)}%`, className: r.prob_of_loss > 0.5 ? 'text-red' : 'text-green' })
      break
    }

    case 'correlation': {
      const tickersCr = args[0]
      // If no args: market-wide correlation from economics endpoint
      if (!tickersCr) {
        addLine({ text: '📊 fetching market-wide correlation matrix...', className: 'text-dim' })
        const c = await safeJson(await authFetch('/api/v1/economics/correlation'), addLine)
        if (!c?.correlation_matrix) break
        addLine({ text: `📊  MARKET CORRELATION MATRIX`, className: 'text-cyan' })
        const tks = c.tickers || []
        const headers = [''].concat(tks.map((t: string) => t.padEnd(6)))
        const rows = tks.map((t: string) => {
          const vals = tks.map((t2: string) => {
            const val = c.correlation_matrix[t]?.[t2]
            return val != null ? val.toFixed(3).padStart(6) : 'N/A'.padStart(6)
          })
          return [t.padEnd(6), ...vals]
        })
        addLine({ text: table(headers, rows), className: 'text-green' })
        break
      }
      // With args: ticker-specific correlation
      addLine({ text: `📊 fetching correlation matrix for ${tickersCr}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/correlation?tickers=${tickersCr}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `📊  CORRELATION MATRIX`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      const tks = r.tickers || tickersCr.split(',')
      for (const t1 of tks) {
        const row = (r.correlation_matrix?.[t1] || {}) as Record<string, number>
        const vals = tks.map((t2: string) => row[t2] != null ? row[t2].toFixed(2) : '-').join('  ')
        addLine({ text: `  ${t1.padEnd(8)} ${vals}`, className: 'text-green' })
      }
      addLine({ text: `  Periods: ${r.periods || '-'}`, className: 'text-dim' })
      break
    }

    case 'pairtrade': {
      const aPt = (args[0] || '').toUpperCase()
      const bPt = (args[1] || '').toUpperCase()
      if (!aPt || !bPt) { addLine({ text: 'Usage: pairtrade <ticker_a> <ticker_b>', className: 'text-yellow' }); break }
      addLine({ text: `🔄 analyzing pair ${aPt}/${bPt}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/analytics/pairs/${aPt}/${bPt}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `🔄  PAIRS ANALYSIS — ${aPt}/${bPt}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Cointegrated: ${r.is_cointegrated ? '✅ Yes' : '❌ No'}`, className: r.is_cointegrated ? 'text-green' : 'text-red' })
      if (r.current_z_score != null) addLine({ text: `  Z-Score: ${r.current_z_score.toFixed(2)}`, className: 'text-yellow' })
      break
    }

    case 'gas': {
      const chainId = parseInt(args[0]) || 1
      addLine({ text: `⛽ fetching gas prices for chain ${chainId}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/gas?chain_id=${chainId}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `⛽  GAS PRICES — ${r.chain || 'Ethereum'}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Safe:     ${r.safe_gwei} Gwei`, className: 'text-green' })
      addLine({ text: `  Standard: ${r.propose_gwei} Gwei`, className: 'text-yellow' })
      addLine({ text: `  Fast:     ${r.fast_gwei} Gwei`, className: 'text-red' })
      break
    }

    case 'blacklitterman': {
      const blTickers = args[0] || ''
      if (!blTickers) { addLine({ text: 'Usage: blacklitterman <ticker1,ticker2,...>', className: 'text-yellow' }); break }
      addLine({ text: `🧮 computing Black-Litterman...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/blacklitterman?tickers=${blTickers}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `🧮  BLACK-LITTERMAN MODEL`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Method: ${r.method || 'Market Equilibrium'}`, className: 'text-dim' })
      if (r.posterior_weights) {
        for (const [tk, w] of Object.entries(r.posterior_weights)) {
          addLine({ text: `  ${tk.padEnd(8)} ${(w as number).toFixed(1)}%`, className: 'text-green' })
        }
      }
      break
    }

    case 'riskparity': {
      const rpTickers = args[0] || ''
      if (!rpTickers) { addLine({ text: 'Usage: riskparity <ticker1,ticker2,...>', className: 'text-yellow' }); break }
      addLine({ text: `⚖️ computing risk parity...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/riskparity?tickers=${rpTickers}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `⚖️  RISK PARITY PORTFOLIO`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      if (r.weights) {
        for (const [tk, w] of Object.entries(r.weights)) {
          addLine({ text: `  ${tk.padEnd(8)} ${((w as number) * 100).toFixed(1)}%`, className: 'text-green' })
        }
      }
      addLine({ text: `  Portfolio Vol: ${r.portfolio_volatility?.toFixed(1) || '-'}%`, className: 'text-dim' })
      addLine({ text: `  Target Vol:    ${r.target_volatility?.toFixed(1) || '-'}%`, className: 'text-yellow' })
      break
    }

    case 'benchmark': {
      const bmTicker = (args[0] || '').toUpperCase()
      const bmBench = (args[1] || 'SPY').toUpperCase()
      if (!bmTicker) { addLine({ text: 'Usage: benchmark <ticker> [benchmark]', className: 'text-yellow' }); break }
      addLine({ text: `📊 comparing ${bmTicker} to ${bmBench}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/benchmark?ticker=${bmTicker}&benchmark=${bmBench}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `📊  BENCHMARK COMPARISON`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Alpha:          ${r.alpha != null ? r.alpha.toFixed(2) + '%' : '-'}`, className: r.alpha > 0 ? 'text-green' : 'text-red' })
      addLine({ text: `  Beta:           ${r.beta?.toFixed(2) || '-'}`, className: 'text-dim' })
      addLine({ text: `  Tracking Error: ${r.tracking_error?.toFixed(2) || '-'}%`, className: 'text-yellow' })
      addLine({ text: `  Sharpe Ratio:   ${r.sharpe_ratio?.toFixed(2) || '-'}`, className: 'text-green' })
      break
    }

    case 'drawdown': {
      const ddTicker = (args[0] || '').toUpperCase()
      if (!ddTicker) { addLine({ text: 'Usage: drawdown <ticker>', className: 'text-yellow' }); break }
      addLine({ text: `📉 analyzing drawdown for ${ddTicker}...`, className: 'text-dim' })
      const r = await safeJson(await authFetch(`/api/v1/datavore/calc/drawdown?ticker=${ddTicker}`), addLine)
      if (!r) break
      addLine({ text: '', className: '' })
      addLine({ text: `📉  DRAWDOWN ANALYSIS — ${ddTicker}`, className: 'text-cyan' })
      addLine({ text: `════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Max Drawdown: ${r.max_drawdown != null ? r.max_drawdown.toFixed(1) + '%' : '-'}`, className: 'text-red' })
      break
    }

    case 'rolling': {
      const ticker = (args[0] || 'AAPL').toUpperCase()
      addLine({ text: `📐 calculating rolling metrics for ${ticker}...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/analytics/risk/rolling?ticker=${ticker}`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: ``, className: '' })
      addLine({ text: `📐  ROLLING METRICS (12mo) — ${ticker} vs ${d.benchmark}`, className: 'text-cyan' })
      addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
      const clsSharpe = d.current_sharpe >= 1 ? 'text-green' : 'text-yellow'
      addLine({ text: `  Current Sharpe:     ${d.current_sharpe}`, className: clsSharpe })
      addLine({ text: `  Current Volatility: ${d.current_volatility_pct}%`, className: 'text-dim' })
      addLine({ text: `  Current Beta:       ${d.current_beta}`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  Rolling Sharpe (last 20 periods):`, className: 'text-dim' })
      for (let i = 0; i < (d.rolling_sharpe?.values?.length || 0); i++) {
        const v = d.rolling_sharpe.values[i]
        const date = d.rolling_sharpe.dates[i]
        const cls = v >= 1 ? 'text-green' : v >= 0 ? 'text-yellow' : 'text-red'
        addLine({ text: `    ${date}: ${v.toFixed(1)}`, className: cls })
      }
      break
    }

    case 'global': {
      const exc = args[0]?.toUpperCase()
      addLine({ text: `🌍 fetching global market data...`, className: 'text-dim' })
      const url = exc
        ? `/api/v1/markets/global/${exc}`
        : `/api/v1/markets/global`
      const res = await authFetch(url, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: ``, className: '' })
      if (exc) {
        const cls = d.is_open ? 'text-green' : 'text-red'
        addLine({ text: `🌍  ${d.name} (${d.exchange})`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Status:    ${d.is_open ? '🟢 OPEN' : '🔴 CLOSED'}`, className: cls })
        addLine({ text: `  Country:   ${d.country}`, className: 'text-dim' })
        addLine({ text: `  Timezone:  ${d.timezone}`, className: 'text-dim' })
        addLine({ text: `  Open:      ${d.open_time || '—'}`, className: 'text-dim' })
        addLine({ text: `  Close:     ${d.close_time || '—'}`, className: 'text-dim' })
        if (d.next_open) addLine({ text: `  Next Open: ${d.next_open}`, className: 'text-yellow' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  Last: $${d.last_price?.toLocaleString() || '—'}`, className: 'text-cyan' })
        const chgCls = (d.change_pct || 0) >= 0 ? 'text-green' : 'text-red'
        addLine({ text: `  Change: ${(d.change_pct || 0) >= 0 ? '+' : ''}${d.change_pct}%`, className: chgCls })
      } else {
        addLine({ text: `🌍  GLOBAL MARKETS  (${d.open_count}/${d.total_exchanges} open)`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        for (const e of d.exchanges || []) {
          const icon = e.is_open ? '🟢' : '🔴'
          const cls = (e.change_pct || 0) >= 0 ? 'text-green' : 'text-red'
          addLine({ text: `  ${icon} ${e.name.padEnd(18)} ${(e.change_pct || 0) >= 0 ? '+' : ''}${e.change_pct}%`, className: cls })
        }
        addLine({ text: ``, className: '' })
        addLine({ text: `  global <exchange>  — detail for a specific exchange`, className: 'text-dim' })
      }
      break
    }

    case 'currency':
    case 'currencies': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'list' || !sub) {
        addLine({ text: `💰 fetching currencies...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/currencies`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        const arr = Array.isArray(d) ? d : d.currencies || []
        addLine({ text: ``, className: '' })
        addLine({ text: `💰  SUPPORTED CURRENCIES`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        for (const c of arr) {
          const rate = c.fx_rate ? `1 USD = ${(1 / c.fx_rate).toFixed(4)} ${c.code}` : '-'
          addLine({ text: `  ${c.symbol || '?'} ${c.code}  ${(c.name || '').padEnd(18)} ${rate}`, className: c.is_crypto ? 'text-yellow' : 'text-dim' })
        }
        addLine({ text: ``, className: '' })
        addLine({ text: `  ${arr.length} currencies supported`, className: 'text-green' })
        break
      }
      if (sub === 'rates') {
        addLine({ text: `💰 fetching FX rates...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/currencies`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        const arr = Array.isArray(d) ? d : []
        addLine({ text: ``, className: '' })
        addLine({ text: `💰  LIVE FX RATES`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        for (const c of arr) {
          if (c.code === 'USD') continue
          addLine({ text: `  ${c.code.padEnd(5)} 1 ${c.code} = ${(c.fx_rate || 0).toFixed(4)} USD`, className: 'text-dim' })
        }
        break
      }
      // currency convert <amount> <from> <to>
      if (sub === 'convert' && args.length >= 4) {
        const amount = parseFloat(args[1])
        const fromC = args[2].toUpperCase()
        const toC = args[3].toUpperCase()
        if (isNaN(amount)) { addLine({ text: `❌ invalid amount`, className: 'text-red' }); break }
        addLine({ text: `💱 converting ${amount} ${fromC} → ${toC}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/currencies/convert?amount=${amount}&from=${fromC}&to=${toC}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `  ${d.amount} ${d.from} = ${d.result} ${d.to}`, className: 'text-cyan' })
        addLine({ text: `  Rate: 1 ${d.from} = ${d.rate} ${d.to}`, className: 'text-dim' })
        break
      }
      // currency set <portfolio_id> <code>
      if (sub === 'set' && args.length >= 3) {
        const pid = args[1]
        const cur = args[2].toUpperCase()
        addLine({ text: `💱 changing portfolio ${pid} to ${cur}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/portfolios/${pid}/currency?currency=${cur}`, { method: 'PUT', headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `  ✅ Portfolio base currency: ${d.old_currency || 'USD'} → ${d.base_currency}`, className: 'text-green' })
        if (d.positions_converted) {
          addLine({ text: `  ${d.positions_converted} positions converted at rate ${d.rate}`, className: 'text-dim' })
        }
        break
      }
      // show help
      addLine({ text: ``, className: '' })
      addLine({ text: `💰  CURRENCY COMMANDS`, className: 'text-cyan' })
      addLine({ text: `  currency list                  Show supported currencies`, className: 'text-dim' })
      addLine({ text: `  currency rates                 Show live FX rates`, className: 'text-dim' })
      addLine({ text: `  currency convert <amt> <f> <t>  Convert currencies`, className: 'text-dim' })
      addLine({ text: `  currency set <pid> <code>      Change portfolio base currency`, className: 'text-dim' })
      break
    }

    case 'wallet': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'connect') {
        addLine({ text: `🔗 connecting wallet...`, className: 'text-dim' })
        addLine({ text: `  Use WalletConnect to scan the QR code.`, className: 'text-dim' })
        addLine({ text: `  Supported: MetaMask, Rainbow, Coinbase Wallet, WalletConnect`, className: 'text-dim' })
        break
      }
      if (sub === 'list' || sub === 'sessions') {
        addLine({ text: `🔗 fetching wallet sessions...`, className: 'text-dim' })
        const res = await authFetch('/api/v1/defi/sessions', { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `  Connected wallets: ${d.sessions?.length || 0}`, className: 'text-cyan' })
        for (const s of d.sessions || []) {
          addLine({ text: `  ${s.icon ? s.icon + ' ' : ''}${s.chain || 'Unknown'} - ${s.address?.slice(0,10)}...${s.address?.slice(-4)}`, className: 'text-dim' })
        }
        break
      }
      if (sub === 'balance') {
        addLine({ text: `💰 fetching wallet balances...`, className: 'text-dim' })
        const res = await authFetch('/api/v1/defi/balance', { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: ``, className: '' })
        addLine({ text: `💰  WALLET BALANCES`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════════════════════`, className: 'text-dim' })
        for (const b of d.balances || []) {
          addLine({ text: `  ${b.chain?.padEnd(10)} ${b.symbol?.padEnd(6)} ${b.balance?.toFixed(4)}  $${b.usd_value?.toFixed(2)}`, className: 'text-dim' })
        }
        if (d.total_usd) {
          addLine({ text: `──────────────────────────────────────────────`, className: 'text-dim' })
          addLine({ text: `  Total: $${d.total_usd.toFixed(2)} USD`, className: 'text-yellow' })
        }
        break
      }
      if (sub === 'chains') {
        addLine({ text: `⛓️ supported chains:`, className: 'text-cyan' })
        addLine({ text: `  Ethereum, Arbitrum, Optimism, Polygon, Base, zkSync`, className: 'text-dim' })
        break
      }
      // help
      addLine({ text: ``, className: '' })
      addLine({ text: `🔗  WALLET COMMANDS (Phase 18 DeFi)`, className: 'text-cyan' })
      addLine({ text: `  wallet connect           Connect wallet (WalletConnect)`, className: 'text-dim' })
      addLine({ text: `  wallet balance           Show wallet balances`, className: 'text-dim' })
      addLine({ text: `  wallet sessions          List connected sessions`, className: 'text-dim' })
      addLine({ text: `  wallet chains            List supported chains`, className: 'text-dim' })
      break
    }

    case 'defi': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'protocols') {
        addLine({ text: ``, className: '' })
        addLine({ text: `🏛️  DEFI PROTOCOLS`, className: 'text-cyan' })
        addLine({ text: `  Uniswap v3/v4    - Swap, LP, positions (Ethereum)`, className: 'text-dim' })
        addLine({ text: `  Aave             - Lend/borrow (Ethereum, Polygon)`, className: 'text-dim' })
        addLine({ text: `  Curve Finance    - Stable swap (Ethereum)`, className: 'text-dim' })
        addLine({ text: `  Lido             - stETH/wstETH staking`, className: 'text-dim' })
        addLine({ text: `  MakerDAO         - DAI vaults`, className: 'text-dim' })
        addLine({ text: `  Jupiter          - Swap aggregator (Solana)`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  Type 'wallet connect' to get started.`, className: 'text-cyan' })
        break
      }
      addLine({ text: ``, className: '' })
      addLine({ text: `🏛️  DEFI COMMANDS (Phase 18)`, className: 'text-cyan' })
      addLine({ text: `  defi protocols       List supported DeFi protocols`, className: 'text-dim' })
      addLine({ text: `  wallet connect       Connect your wallet`, className: 'text-dim' })
      addLine({ text: `  wallet balance       View balances`, className: 'text-dim' })
      break
    }

/*
//     case 'apikey': {
//       const sub = args[0]?.toLowerCase()
//       if (sub === 'create') {
//         const name = args.slice(1).join(' ') || 'Default'
//         addLine({ text: `creating API key "${name}"...`, className: 'text-dim' })
//         try {
//           const res = await authFetch('/api/v1/developer/api-keys', {
//             method: 'POST',
//             headers: authHeaders({ 'Content-Type': 'application/json' }),
//             body: JSON.stringify({ name }),
//           })
//           const data = await res.json()
//           if (res.ok) {
//             addLine({ text: `✅ API key created!
//   Name:   ${data.name}
//   Prefix: ${data.key_prefix}...
//   Key:    ${data.raw_key}
//   ⚠️  Copy this key now — it won't be shown again!`, className: 'text-green' })
//           } else {
//             addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
//           }
//         } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
//         break
//       }
// 
//       if (sub === 'list') {
//         addLine({ text: 'fetching API keys...', className: 'text-dim' })
//         try {
//           const res = await authFetch('/api/v1/developer/api-keys', { headers: authHeaders() })
//           const data = await res.json()
//           const items = data.api_keys || []
//           if (!items.length) { addLine({ text: '📭 no API keys found. Use: apikey create <name>', className: 'text-yellow' }); break }
//           const rows = items.map((k: any) => [
//             (k.id || '').substring(0, 8).padEnd(8),
//             (k.name || '').padEnd(20),
//             (k.key_prefix || '').padEnd(10),
//             k.is_active ? '🟢' : '🔴',
//           ])
//           addLine({ text: table(['ID', 'Name', 'Prefix', ''], rows), className: 'text-green' })
//         } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
//         break
//       }
// 
//       if (sub === 'revoke' && args[1]) {
//         const id = args[1]
//         addLine({ text: `revoking API key ${id}...`, className: 'text-dim' })
//         try {
//           const res = await authFetch(`/api/v1/developer/api-keys/${id}`, {
//             method: 'DELETE',
//             headers: authHeaders(),
//           })
//           if (res.ok) addLine({ text: `✅ API key revoked`, className: 'text-green' })
//           else addLine({ text: `❌ Key not found`, className: 'text-red' })
//         } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
//         break
//       }
// 
//       addLine({ text: 'usage: apikey create <name> | apikey list | apikey revoke <id>', className: 'text-yellow' })
//       break
//     }
// 
//     // 🌪️ CHAOS COMMANDS
*/

    case 'chaos': {
      const chaosMode = localStorage.getItem('miau-chaos')
      if (chaosMode) {
        localStorage.removeItem('miau-chaos')
        addLine({ text: '🌀 chaos mode: DISABLED. The cats are sad.', className: 'text-dim' })
      } else {
        localStorage.setItem('miau-chaos', 'true')
        addLine({ text: `🌀 CHAOS MODE: ENABLED
  ─────────────────────────────────────
  ▸ random cat facts may appear during commands
  ▸ terminal may glitch (aesthetic only)
  ▸ unexpected "meow" alerts at random
  ▸ cat walks across your screen occasionally
  ▸ your portfolio may feel ✨dramatic✨
  ─────────────────────────────────────
  type 'chaos' again to disable`, className: 'text-yellow' })
        // Fire a confetti-like burst of cats
        for (let i = 0; i < 5; i++) {
          setTimeout(() => {
            const catEmoji = ['😸', '😹', '😻', '🐱', '🐈', '🐈‍⬛'][Math.floor(Math.random() * 6)]
            addLine({ text: `  ${catEmoji}`, className: 'text-green' })
          }, i * 150)
        }
      }
      break
    }

    case 'panic': {
      addLine({ text: '😱 PANIC! HIDING EVERYTHING...', className: 'text-red' })
      document.body.style.transition = 'all 0.3s'
      document.body.style.background = '#000'
      document.body.style.color = '#000'
      const root = document.getElementById('root')
      if (root) {
        root.style.display = 'none'
      }
      // Restore after "danger" passes
      setTimeout(() => {
        document.body.style.background = ''
        document.body.style.color = ''
        if (root) root.style.display = ''
        addLine({ text: '😮‍💨 crisis averted. welcome back.', className: 'text-green' })
      }, 5000)
      break
    }

    case 'sudo': {
      const cmd = args.join(' ')
      if (!cmd) {
        addLine({ text: `sudo: what do you want me to do?
  Hint: sudo make me a sandwich`, className: 'text-yellow' })
        break
      }
      if (cmd.includes('sandwich')) {
        addLine({ text: `sudo: Okay, but you owe me.
  🥪  Here's your sandwich. That'll be $tree-fiddy.`, className: 'text-yellow' })
        break
      }
      if (cmd.includes('rm') && cmd.includes('-rf')) {
        addLine({ text: `sudo: lol nice try. I'm not deleting /.
  ─────────────────────────────────────
  nice_cat_username:   NOT in sudoers file.
  This incident will be reported to the
  International Cat Bureau of Cybersecurity.`, className: 'text-red' })
        break
      }
      if (cmd.includes('apt') || cmd.includes('brew') || cmd.includes('pip')) {
        addLine({ text: `sudo: installing packages... 
  🐱 meow-meow-meow... package 'patience' not found.
  sudo: maybe try 'pet the cat' instead?`, className: 'text-cyan' })
        break
      }
      addLine({ text: `sudo: I'm not sure how to "${cmd}" but I believe in you.
  💪 You got this, champ.`, className: 'text-green' })
      break
    }

    case 'hack': {
      addLine({ text: `INITIALIZING CYBER ATTACK SEQUENCE...
  ╔══════════════════════════════════╗
  ║    MIAU FINANCE CYBER DECK v4.0 ║
  ╚══════════════════════════════════╝`, className: 'text-green' })
      const matrix = ['01001000', '01100001', '01100011', '01101011', '01101001', '01101110', '01100111']
      const companies = ['FED', 'NYSE', 'NASDAQ', 'ICE', 'SEC', 'CFTC', 'WORLD BANK']
      const messages = [
        '> ACCESSING MAINFRAME...',
        '> BYPASSING FIREWALL...',
        '> DECRYPTING PORTFOLIO DATA...',
        '> INJECTING CATNIP PROTOCOL...',
        '> DOWNLOADING GAINS...',
        '> UPLOADING MEMES...',
        '> NEUTRALIZING BEAR MARKET...',
      ]
      for (let i = 0; i < 8; i++) {
        setTimeout(() => {
          const bin = matrix.map(() => String(Math.random() > 0.5 ? 1 : 0)).join(' ')
          const msg = messages[Math.floor(Math.random() * messages.length)]
          const co = companies[Math.floor(Math.random() * companies.length)]
          addLine({ text: `${bin}
  ${msg}
  ▸ Target: ${co}
  ▸ Status: ${['OK', 'OK', 'OK', '⚠️ WARN', 'OK', '🐱 INTERRUPTED BY CAT'][Math.floor(Math.random() * 6)]}`, className: 'text-green' })
        }, i * 600)
      }
      setTimeout(() => {
        addLine({ text: `\n  ✅ HACK COMPLETE.
  📊 Portfolio value increased by 🐱 100%
  💰 All debts converted to catnip holdings.

  (just kidding. this is a demo. your money is safe.
   probably.)`, className: 'text-cyan' })
      }, 5200)
      break
    }

    // 👥 SOCIAL COMMANDS
    case 'share': {
      const pid = args[0]
      if (!pid) { addLine({ text: 'usage: share <portfolio_id>', className: 'text-yellow' }); break }
      addLine({ text: `sharing portfolio ${pid}...`, className: 'text-dim' })
      try {
        const res = await authFetch('/api/v1/social/share', {
          method: 'POST',
          headers: authHeaders({ 'Content-Type': 'application/json' }),
          body: JSON.stringify({ portfolio_id: pid, is_public: true }),
        })
        const data = await res.json()
        if (res.ok) {
          addLine({ text: `✅ Portfolio shared!\n  🔗 ${data.share_url}`, className: 'text-green' })
        } else {
          addLine({ text: `❌ ${data.detail || 'share failed'}`, className: 'text-red' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'feed': {
      const filter = args[0] || 'global'
      addLine({ text: `fetching ${filter} feed...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/social/feed?limit=10&filter=${filter}`, { headers: authHeaders() })
        const data = await res.json()
        if (!data.activities?.length) {
          addLine({ text: '📭 No activity yet', className: 'text-yellow' })
          break
        }
        for (const a of data.activities) {
          const cl = a.action_type === 'trade_executed' ? 'text-green' : a.action_type === 'new_follower' ? 'text-yellow' : 'text-dim'
          addLine({ text: `  ${a.username}: ${a.message}`, className: cl })
        }
        if (data.next_cursor) {
          addLine({ text: '  ...more available. Use: feed', className: 'text-dim' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'like': {
      const aid = args[0]
      if (!aid) { addLine({ text: 'usage: like <activity_id>', className: 'text-yellow' }); break }
      addLine({ text: `liking activity ${aid}...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/social/feed/${aid}/like`, { method: 'POST', headers: authHeaders() })
        const data = await res.json()
        if (res.ok) addLine({ text: `👍 Liked!`, className: 'text-green' })
        else addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'notifications': {
      addLine({ text: 'fetching notifications...', className: 'text-dim' })
      try {
        const res = await authFetch('/api/v1/social/notifications', { headers: authHeaders() })
        const data = await res.json()
        const notifs = Array.isArray(data) ? data : data.notifications || []
        if (!notifs.length) { addLine({ text: '🔔 No notifications', className: 'text-dim' }); break }
        for (const n of notifs) {
          addLine({ text: `  ${n.is_read ? '📭' : '📬'} ${n.message || n.type}`, className: n.is_read ? 'text-dim' : 'text-green' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'comments': {
      const aid = args[0]
      if (!aid) { addLine({ text: 'usage: comments <activity_id>', className: 'text-yellow' }); break }
      addLine({ text: `fetching comments...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/social/feed/${aid}/comments`, { headers: authHeaders() })
        const data = await res.json()
        const comments = data.comments || []
        if (!comments.length) {
          addLine({ text: '💬 No comments yet', className: 'text-dim' })
        } else {
          for (const c of comments) {
            addLine({ text: `  ${c.username}: ${c.text}`, className: 'text-green' })
          }
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'profile': {
      const username = args[0]
      const url = username ? `/api/v1/social/profile?username=${username}` : '/api/v1/users/me'
      addLine({ text: `loading profile...`, className: 'text-dim' })
      try {
        const res = await authFetch(url, { headers: authHeaders() })
        const p = await res.json()
        if (p.error) { addLine({ text: `❌ ${p.error}`, className: 'text-red' }); break }
        const profile = p.profile || p
        addLine({
          text: `👤 ${profile.username} (${profile.role})
  📧 ${profile.email || ''}
  👥 Followers: ${profile.follower_count || 0}  Following: ${profile.following_count || 0}
  📊 Portfolios: ${profile.portfolio_count || 0}
  ⭐ ${profile.reputation?.level || 'Bronze'} · ${profile.reputation?.total_points || 0} pts`,
          className: 'text-cyan',
        })
        if (profile.badges?.length) {
          addLine({ text: '🏅 Badges: ' + profile.badges.map((b: any) => `${b.icon || ''} ${b.name}`).join(', '), className: 'text-yellow' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'follow': {
      const target = args[0]
      if (!target) { addLine({ text: 'usage: follow <username>', className: 'text-yellow' }); break }
      addLine({ text: `following ${target}...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/social/follow-by-username/${target}`, {
          method: 'POST',
          headers: authHeaders({ 'Content-Type': 'application/json' }),
        })
        if (res.ok) {
          addLine({ text: `✅ You are now following ${target}`, className: 'text-green' })
        } else {
          const data = await res.json()
          addLine({ text: `❌ ${data.detail || 'failed'}`, className: 'text-red' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'unfollow': {
      const target2 = args[0]
      if (!target2) { addLine({ text: 'usage: unfollow <username>', className: 'text-yellow' }); break }
      try {
        const res = await authFetch(`/api/v1/social/follow-by-username/${target2}`, {
          method: 'DELETE',
          headers: authHeaders({ 'Content-Type': 'application/json' }),
        })
        if (res.ok) {
          addLine({ text: `✅ Unfollowed ${target2}`, className: 'text-green' })
        } else {
          addLine({ text: `❌ Not following ${target2}`, className: 'text-yellow' })
        }
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'leaderboard': {
      const metric = args[0] || 'total_return'
      addLine({ text: `fetching leaderboard (${metric})...`, className: 'text-dim' })
      try {
        const res = await authFetch(`/api/v1/social/leaderboard?metric=${metric}&limit=20`, { headers: authHeaders() })
        const data = await res.json()
        if (!data.leaderboard?.length) {
          addLine({ text: '📭 No leaderboard data yet', className: 'text-yellow' })
          break
        }
        const rows = data.leaderboard.map((e: any) => [
          `#${e.rank}`.padEnd(4),
          (e.username || '').padEnd(20),
          `${e.value?.toFixed(2) || '0.00'}${metric === 'gain_amount' ? '' : '%'}`.padStart(10),
          `${e.positions || 0}`.padStart(6),
        ])
        addLine({ text: table(['Rank', 'User', 'Value', 'Pos'], rows), className: 'text-green' })
      } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
      break
    }

    case 'proposal': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'list' || !sub) {
        const status = args[1] || 'active'
        addLine({ text: `fetching ${status} proposals...`, className: 'text-dim' })
        try {
          const res = await safeJson(await authFetch(`/api/v1/governance/proposals?status=${status}&limit=20`), addLine)
          if (!res || !res.length) { addLine({ text: '📭 No proposals found', className: 'text-yellow' }); break }
          const rows = res.map((p: any) => [
            p.id.padEnd(10), p.title.slice(0, 30).padEnd(32), p.status.padEnd(10),
            `${p.for_votes || 0}-${p.against_votes || 0}`, p.voting_ends_at?.slice(0, 10) || ''
          ])
          addLine({ text: table(['ID', 'Title', 'Status', 'For-Against', 'Ends'], rows), className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
        break
      }
      if (sub === 'create') {
        const title = args[1]
        const desc = args.slice(2).join(' ') || title
        if (!title) { addLine({ text: 'usage: proposal create <title> [description]', className: 'text-yellow' }); break }
        addLine({ text: `creating proposal: ${title}...`, className: 'text-dim' })
        try {
          const res = await safeJson(await authFetch(`/api/v1/governance/proposals?title=${encodeURIComponent(title)}&description=${encodeURIComponent(desc)}&voting_days=7`, { method: 'POST' }), addLine)
          if (res) addLine({ text: `✅ Proposal created: ${res.id} — ${res.title}`, className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
        break
      }
      if (sub === 'vote') {
        const pid = args[1]; const vote = args[2]; const power = args[3] || '1'
        if (!pid || !vote || !['for', 'against', 'abstain'].includes(vote)) { addLine({ text: 'usage: proposal vote <id> <for|against|abstain> [power]', className: 'text-yellow' }); break }
        addLine({ text: `casting ${vote} vote on ${pid}...`, className: 'text-dim' })
        try {
          const res = await safeJson(await authFetch(`/api/v1/governance/proposals/${pid}/vote?vote=${vote}&power=${power}`, { method: 'POST' }), addLine)
          if (res) addLine({ text: `✅ Vote cast: ${res.vote} on ${res.proposal_id}`, className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
        break
      }
      if (sub === 'stats') {
        addLine({ text: `fetching governance stats...`, className: 'text-dim' })
        try {
          const res = await safeJson(await authFetch('/api/v1/governance/stats'), addLine)
          if (!res) break
          addLine({ text: `🏛️  Governance Stats`, className: 'text-cyan' })
          addLine({ text: `  Active: ${res.proposals?.active || 0}  ·  Passed: ${res.proposals?.passed || 0}  ·  Total votes: ${res.votes?.cnt || 0}  ·  Delegations: ${res.delegations || 0}`, className: 'text-green' })
        } catch (e: any) { addLine({ text: `❌ ${e.message}`, className: 'text-red' }) }
        break
      }
      addLine({ text: 'usage: proposal list|create|vote|stats [args]', className: 'text-yellow' })
      break
    }

    case 'journal':
    case 'tjournal': {
      const sub = args[0] || 'list'
      if (sub === 'add') {
        const note = args.slice(1, -1).join(' ') || args.slice(1).join(' ')
        const mood = args.length >= 3 ? args[args.length - 1] : '😸'
        if (!note) { addLine({ text: 'usage: journal add "your note" [mood]', className: 'text-yellow' }); break }
        const entries = JSON.parse(localStorage.getItem('miau-journal') || '[]')
        entries.unshift({
          id: Date.now().toString(36),
          note,
          mood,
          ticker: args[1]?.toUpperCase() || '',
          created_at: new Date().toISOString(),
        })
        entries.splice(100)
        localStorage.setItem('miau-journal', JSON.stringify(entries))
        addLine({ text: `📝 Journal entry saved! ${mood}`, className: 'text-green' })
        addLine({ text: `   "${note}"`, className: 'text-dim' })
      } else if (sub === 'clear') {
        localStorage.removeItem('miau-journal')
        addLine({ text: '🗑️ Journal cleared', className: 'text-yellow' })
      } else {
        const entries = JSON.parse(localStorage.getItem('miau-journal') || '[]')
        if (!entries.length) {
          addLine({ text: '📓 Your trading journal is empty.', className: 'text-dim' })
          addLine({ text: '   Add entries with: journal add "your trade notes" 😸', className: 'text-dim' })
        } else {
          addLine({ text: `📓 TRADING JOURNAL (${entries.length} entries)`, className: 'text-cyan' })
          addLine({ text: `   journal clear | journal add "note" [mood: 😸😾🤔😴😻]`, className: 'text-dim' })
          addLine({ text: '' })
          const shown = entries.slice(0, 10)
          for (const e of shown) {
            const d = new Date(e.created_at)
            const date = `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
            const ticker = e.ticker ? `[${e.ticker}] ` : ''
            addLine({ text: `  ${date}  ${e.mood}  ${ticker}${e.note}`, className: 'text-green' })
          }
          if (entries.length > 10) {
            addLine({ text: `  ... and ${entries.length - 10} more entries`, className: 'text-dim' })
          }
          const moodCounts: Record<string, number> = {}
          for (const e of entries) moodCounts[e.mood] = (moodCounts[e.mood] || 0) + 1
          const top = Object.entries(moodCounts).sort((a, b) => b[1] - a[1])
          if (top.length) {
            const insight = top[0][0] === '😸' ? 'You trade best when happy! 😸' :
                           top[0][0] === '😾' ? 'Careful — you trade most when angry 😾' :
                           top[0][0] === '🤔' ? "You're a thoughtful trader 🤔" :
                           top[0][0] === '😴' ? 'Sleepy trades might miss opportunities 😴' :
                           "You're in love with the market 😻"
            addLine({ text: `\n  💡 Insight: ${insight}`, className: 'text-yellow' })
          }
        }
      }
      break
    }

    case 'theme': {
      const themeName = args[0]
      // Dynamic import to avoid circular deps
      const { listThemes, setTheme: applyTheme } = await import('../lib/themes')
      if (!themeName || themeName === 'list') {
        const themes = listThemes()
        addLine({ text: `🎨 CAT TERMINAL THEMES`, className: 'text-cyan' })
        addLine({ text: `   theme <name> to switch`, className: 'text-dim' })
        for (const t of themes) {
          addLine({ text: `   ${t.emoji}  ${t.name.padEnd(20)} ${t.description}`, className: 'text-green' })
        }
      } else {
        const themes = listThemes()
        const match = themes.find(t => t.id === themeName.toLowerCase() || t.name.toLowerCase().includes(themeName.toLowerCase()))
        if (match) {
          applyTheme(match.id)
          addLine({ text: `🎨 Theme switched to ${match.emoji} ${match.name}`, className: 'text-green' })
          addLine({ text: `   ${match.description}`, className: 'text-dim' })
        } else {
          addLine({ text: `❌ Unknown theme: ${themeName}`, className: 'text-red' })
          addLine({ text: '   Try: theme list', className: 'text-dim' })
        }
      }
      break
    }

    case 'achievements': {
      const { getUnlockedAchievements, getTotalPoints, getRank, getAllAchievements } = await import('../lib/achievements')
      const unlocked = getUnlockedAchievements()
      const points = getTotalPoints()
      const rank = getRank()
      const all = getAllAchievements()
      addLine({ text: `🏆 ACHIEVEMENTS (${unlocked.length}/${all.length} unlocked)`, className: 'text-cyan' })
      addLine({ text: `   ${rank.emoji} Rank: ${rank.title} · ${points} pts`, className: 'text-yellow' })
      addLine({ text: '' })
      if (!unlocked.length) {
        addLine({ text: '   No achievements yet. Start trading to unlock them! 🐱', className: 'text-dim' })
      } else {
        for (const a of unlocked.slice(-8).reverse()) {
          addLine({ text: `   ${a.icon} ${a.title}  +${a.points}pts  ${new Date(a.unlockedAt).toLocaleDateString()}`, className: 'text-green' })
        }
        if (unlocked.length > 8) {
          addLine({ text: `   ... and ${unlocked.length - 8} more`, className: 'text-dim' })
        }
      }
      break
    }

    // 🎲 RANDOM CHAOS TRIGGER — 15% chance in chaos mode
    {
      const chaosMode = localStorage.getItem('miau-chaos')
      if (chaosMode && command !== 'chaos' && Math.random() < 0.15) {
        const chaosEvents = [
          () => addLine({ text: '🐱 meow.', className: 'text-dim' }),
          () => addLine({ text: '😸 your cat approves of this command.', className: 'text-yellow' }),
          () => addLine({ text: '🐈‍⬛ a black cat just walked across your screen. might be good luck?', className: 'text-purple' }),
          () => addLine({ text: '💹 your portfolio did a barrel roll.', className: 'text-cyan' }),
          () => {
            const fakePrices = [150.25, 151.00, 149.80, 152.10, 148.90]
            const i = Math.floor(Math.random() * fakePrices.length)
            addLine({ text: `📡 random market ping: AAPL $${fakePrices[i]} (${['+0.5%', '+1.2%', '-0.3%', '+1.8%', '-0.7%'][i]})`, className: i % 2 === 0 ? 'text-green' : 'text-red' })
          },
          () => addLine({ text: '🎰 CHAOS WHEEL SPINS... you win: +5% confidence boost!', className: 'text-yellow' }),
        ]
        chaosEvents[Math.floor(Math.random() * chaosEvents.length)]()
      }
    }

    case 'esg': {
      const sub = args[0]?.toLowerCase()
      const ticker = (args[1] || args[0] || 'AAPL').toUpperCase()
      if (sub === 'portfolio') {
        addLine({ text: `🌱 fetching portfolio ESG for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/esg/portfolio/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `🌱  PORTFOLIO ESG — ${ticker}`, className: 'text-cyan' })
        addLine({ text: `  Total ESG: ${d.total_score ?? 'N/A'}  |  E: ${d.environmental_score ?? 'N/A'}  S: ${d.social_score ?? 'N/A'}  G: ${d.governance_score ?? 'N/A'}`, className: 'text-dim' })
        break
      }
      if (sub === 'screen') {
        const min = parseInt(args[1] || args[0] || '50')
        addLine({ text: `🔍 screening tickers with ESG >= ${min}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/esg/screen?min_score=${min}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `🔍  ESG SCREEN (min ${min})`, className: 'text-cyan' })
        for (const r of (d.results || []).slice(0, 10)) {
          addLine({ text: `  ${r.ticker}  ESG: ${r.total_score}  E:${r.environmental_score}  S:${r.social_score}  G:${r.governance_score}`, className: r.total_score >= 70 ? 'text-green' : 'text-yellow' })
        }
        break
      }
      addLine({ text: `🌱 fetching ESG for ${ticker}...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/esg/${ticker}`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      const ratingColor = d.total_score >= 70 ? 'text-green' : d.total_score >= 40 ? 'text-yellow' : 'text-red'
      addLine({ text: `🌱  ESG SCORE — ${ticker}`, className: 'text-cyan' })
      addLine({ text: `  Total:  ${d.total_score ?? 'N/A'}  (${d.rating ?? ''})`, className: ratingColor })
      addLine({ text: `  E: ${d.environmental_score ?? 'N/A'}  |  S: ${d.social_score ?? 'N/A'}  |  G: ${d.governance_score ?? 'N/A'}`, className: 'text-dim' })
      if (d.percentile != null) addLine({ text: `  Industry percentile: ${d.percentile}%`, className: 'text-dim' })
      break
    }

    case 'carbon': {
      const sub = args[0]?.toLowerCase()
      const ticker = (args[1] || args[0] || 'AAPL').toUpperCase()
      if (sub === 'portfolio') {
        addLine({ text: `🏭 fetching portfolio carbon footprint for ${ticker}...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/carbon/portfolio/${ticker}`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `🏭  PORTFOLIO CARBON FOOTPRINT`, className: 'text-cyan' })
        const fp = d.footprint || {}
        addLine({ text: `  Scope 1: ${(fp.total_emissions_tons?.scope1 || 0).toFixed(1)}t`, className: 'text-dim' })
        addLine({ text: `  Scope 2: ${(fp.total_emissions_tons?.scope2 || 0).toFixed(1)}t`, className: 'text-dim' })
        addLine({ text: `  Scope 3: ${(fp.total_emissions_tons?.scope3 || 0).toFixed(1)}t`, className: 'text-dim' })
        addLine({ text: `  Total:   ${(fp.total_emissions_tons?.total || 0).toFixed(1)}t CO2e`, className: 'text-yellow' })
        const bm = d.benchmark || {}
        if (bm.vs_spy_pct != null) {
          addLine({ text: `  vs SPY: ${bm.vs_spy_pct >= 0 ? '+' : ''}${bm.vs_spy_pct}%`, className: bm.vs_spy_pct <= 0 ? 'text-green' : 'text-red' })
        }
        break
      }
      addLine({ text: `🏭 fetching carbon data for ${ticker}...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/carbon/${ticker}`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: `🏭  CARBON FOOTPRINT — ${ticker}  (${d.industry})`, className: 'text-cyan' })
      addLine({ text: `  Scope 1 (direct):     ${(d.emissions?.scope1_tons || 0).toLocaleString()} tCO2e`, className: 'text-dim' })
      addLine({ text: `  Scope 2 (energy):     ${(d.emissions?.scope2_tons || 0).toLocaleString()} tCO2e`, className: 'text-dim' })
      addLine({ text: `  Scope 3 (supply):     ${(d.emissions?.scope3_tons || 0).toLocaleString()} tCO2e`, className: 'text-dim' })
      addLine({ text: `  Total:                ${(d.emissions?.total_tons || 0).toLocaleString()} tCO2e`, className: 'text-yellow' })
      addLine({ text: `  Intensity:            ${d.intensity_per_revenue} tCO2e/\$M revenue`, className: 'text-dim' })
      addLine({ text: `  Industry benchmark:   ${d.industry_benchmark} tCO2e/\$M`, className: 'text-dim' })
      if (d.yoy_change_pct != null) {
        addLine({ text: `  YoY change:           ${d.yoy_change_pct >= 0 ? '+' : ''}${d.yoy_change_pct}%`, className: d.yoy_change_pct <= 0 ? 'text-green' : 'text-red' })
      }
      break
    }

    case 'green': {
      const sub = args[0]?.toLowerCase() || 'overview'
      if (sub === 'energy' || sub === 'renewable') {
        addLine({ text: `🌿 fetching renewable energy ETFs...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/green/renewable-energy`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `🌿  RENEWABLE ENERGY ETFs  (${d.count} found)`, className: 'text-cyan' })
        for (const e of (d.results || [])) {
          addLine({ text: `  ${e.ticker}  ${e.name.substring(0, 40)}  \$${e.aum_b}B  ESG:${e.esg_score_min}+`, className: 'text-green' })
        }
        break
      }
      if (sub === 'bonds') {
        addLine({ text: `💚 fetching green bonds...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/green/bonds`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `💚  GREEN BONDS  (${d.count} found, ${d.total_issuers} issuers)`, className: 'text-cyan' })
        for (const b of (d.results || [])) {
          addLine({ text: `  ${b.isin?.slice(-6)}  ${b.name.substring(0, 35)}  ${b.coupon}%  ${b.rating}  ${b.currency}`, className: 'text-green' })
        }
        break
      }
      if (sub === 'funds') {
        addLine({ text: `🌱 fetching sustainable funds...`, className: 'text-dim' })
        const res = await authFetch(`/api/v1/green/funds`, { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (!d) break
        addLine({ text: `🌱  SUSTAINABLE FUNDS  (${d.count} found)`, className: 'text-cyan' })
        for (const f of (d.results || [])) {
          addLine({ text: `  ${f.ticker}  ${f.name.substring(0, 40)}  ESG:${f.esg_score_avg}  ${f.region}`, className: 'text-green' })
        }
        break
      }
      addLine({ text: `🌿 fetching green finance overview...`, className: 'text-dim' })
      const res = await authFetch(`/api/v1/green/overview`, { headers: authHeaders() })
      const d = await safeJson(res, addLine)
      if (!d) break
      addLine({ text: `🌿  GREEN FINANCE OVERVIEW`, className: 'text-cyan' })
      addLine({ text: `  Renewable Energy ETFs: ${d.renewable_energy_etfs}  (\$${d.total_aum_etfs_b}B AUM)`, className: 'text-green' })
      addLine({ text: `  Green Bonds:           ${d.green_bonds}`, className: 'text-green' })
      addLine({ text: `  Sustainable Funds:     ${d.sustainable_funds}  (\$${d.total_aum_funds_b}B AUM)`, className: 'text-green' })
      break
    }

    case 'insider': {
      const tickerIns = (args[0] || '').toUpperCase()
      if (!tickerIns) { addLine({ text: 'Usage: insider <ticker>  — e.g. insider AAPL', className: 'text-yellow' }); break }
      addLine({ text: `🔍 Fetching insider transactions for ${tickerIns}...`, className: 'text-dim' })
      const resIns = await safeJson(await authFetch(`/api/v1/datavore/insider/${tickerIns}`), addLine)
      if (!resIns) break
      const txns = Array.isArray(resIns) ? resIns : (resIns.transactions || resIns.data || [])
      if (!txns.length) { addLine({ text: '😹 No insider transactions found', className: 'text-yellow' }); break }
      addLine({ text: ``, className: '' })
      addLine({ text: `🔍  INSIDER TRANSACTIONS — ${tickerIns}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════════════════`, className: 'text-dim' })
      const rowsIns = txns.slice(0, 20).map((t: any) => [
        (t.date || t.filing_date || '').substring(0, 10),
        (t.name || t.insider_name || t.insider || '').substring(0, 20).padEnd(20),
        (t.type || t.transaction_type || t.transactionType || '').padEnd(15),
        (t.shares || t.quantity || 0).toLocaleString().padStart(10),
        fmt(t.price || t.share_price || 0).padStart(8),
        fmt(t.value || (t.shares || 0) * (t.price || 0) || 0).padStart(10),
      ])
      addLine({ text: table(['Date', 'Insider', 'Type', 'Shares', 'Price', 'Value'], rowsIns), className: 'text-green' })
      break
    }

    case 'short': {
      const tickerSh = (args[0] || '').toUpperCase()
      if (!tickerSh) { addLine({ text: 'Usage: short <ticker>  — e.g. short AAPL', className: 'text-yellow' }); break }
      addLine({ text: `📊 Fetching short interest data for ${tickerSh}...`, className: 'text-dim' })
      const resSh = await safeJson(await authFetch(`/api/v1/datavore/short/${tickerSh}`), addLine)
      if (!resSh) break
      const si = resSh.short_interest || resSh
      const slSh = si.history?.length ? sparkline(si.history, 15) : ''
      addLine({ text: ``, className: '' })
      addLine({ text: `📊  SHORT INTEREST — ${tickerSh}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Short Interest:  ${fmt(si.short_interest || si.shares_short || si.sharesShort || 0)}`, className: 'text-yellow' })
      addLine({ text: `  Short % Float:   ${si.short_pct_float || si.percent_float || si.shortPercentOfFloat || '-'}%`, className: (si.short_pct_float || 0) > 20 ? 'text-red' : 'text-yellow' })
      addLine({ text: `  Days to Cover:   ${si.days_to_cover || si.daysToCover || '-'}`, className: 'text-dim' })
      if (slSh) addLine({ text: `  History:         ${slSh}`, className: 'text-green' })
      break
    }

    case 'ticker': {
      const queryT = args.join(' ')
      if (!queryT) { addLine({ text: 'Usage: ticker <query>  — e.g. ticker Apple', className: 'text-yellow' }); break }
      addLine({ text: `🔍 Searching for "${queryT}"...`, className: 'text-dim' })
      const resT = await safeJson(await authFetch(`/api/v1/datavore/ticker?query=${encodeURIComponent(queryT)}`), addLine)
      if (!resT) break
      const results = Array.isArray(resT) ? resT : (resT.results || resT.data || [])
      if (!results.length) { addLine({ text: '😹 No tickers found', className: 'text-yellow' }); break }
      addLine({ text: ``, className: '' })
      addLine({ text: `🔍  TICKER SEARCH — "${queryT}"`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════`, className: 'text-dim' })
      const rowsT = results.slice(0, 25).map((r: any) => [
        (r.ticker || r.symbol || '').padEnd(8),
        (r.name || r.company_name || '').substring(0, 30).padEnd(30),
        (r.exchange || '').padEnd(10),
        (r.type || r.instrument_type || r.asset_type || r.security_type || '').padEnd(12),
      ])
      addLine({ text: table(['Ticker', 'Name', 'Exchange', 'Type'], rowsT), className: 'text-green' })
      if (results.length > 25) addLine({ text: `  ... and ${results.length - 25} more results`, className: 'text-dim' })
      break
    }

    case 'intraday': {
      const tickerId = (args[0] || '').toUpperCase()
      const intervalId = args[1] || '5min'
      if (!tickerId) { addLine({ text: 'Usage: intraday <ticker> [interval]  — e.g. intraday AAPL 5min', className: 'text-yellow' }); break }
      addLine({ text: `📈 Fetching intraday data for ${tickerId} (${intervalId})...`, className: 'text-dim' })
      const resId = await safeJson(await authFetch(`/api/v1/datavore/intraday/${tickerId}?interval=${intervalId}`), addLine)
      if (!resId) break
      const ohlcv = resId.ohlcv || resId.data || resId.bars || []
      const latest = ohlcv[ohlcv.length - 1] || {}
      const pricesId = ohlcv.map((b: any) => b.close || b.c).filter(Boolean) as number[]
      const slId = pricesId.length >= 2 ? sparkline(pricesId, 20) : ''
      addLine({ text: ``, className: '' })
      addLine({ text: `📈  INTRADAY — ${tickerId} (${intervalId})`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Latest:   ${fmt(latest.close || latest.c || 0)}`, className: 'text-green' })
      addLine({ text: `  Open:     ${fmt(latest.open || latest.o || 0)}`, className: 'text-dim' })
      addLine({ text: `  High:     ${fmt(latest.high || latest.h || 0)}`, className: 'text-dim' })
      addLine({ text: `  Low:      ${fmt(latest.low || latest.l || 0)}`, className: 'text-dim' })
      addLine({ text: `  Volume:   ${(latest.volume || latest.v || 0).toLocaleString()}`, className: 'text-dim' })
      if (slId) addLine({ text: `  ${slId}`, className: 'text-green' })
      addLine({ text: `  Bars:     ${ohlcv.length} intervals`, className: 'text-dim' })
      break
    }

    case 'technicals': {
      const tickerTc = (args[0] || '').toUpperCase()
      const indicator = (args[1] || 'rsi').toLowerCase()
      if (!tickerTc) { addLine({ text: 'Usage: technicals <ticker> [indicator]  — e.g. technicals AAPL rsi', className: 'text-yellow' }); break }
      addLine({ text: `📊 Fetching ${indicator} for ${tickerTc}...`, className: 'text-dim' })
      const resTc = await safeJson(await authFetch(`/api/v1/datavore/technicals/${tickerTc}?indicator=${indicator}`), addLine)
      if (!resTc) break
      const val = resTc.value ?? resTc[indicator] ?? resTc
      const signal = resTc.signal || ''
      const history = resTc.history || []
      const slTc = history.length >= 2 ? sparkline(history, 15) : ''
      const signalCls = signal.toLowerCase() === 'buy' ? 'text-green' : signal.toLowerCase() === 'sell' ? 'text-red' : 'text-yellow'
      addLine({ text: ``, className: '' })
      addLine({ text: `📊  TECHNICAL — ${tickerTc} (${indicator.toUpperCase()})`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  ${indicator.toUpperCase()}: ${typeof val === 'number' ? val.toFixed(2) : val}`, className: 'text-yellow' })
      if (signal) addLine({ text: `  Signal: ${signal}`, className: signalCls })
      if (slTc) addLine({ text: `  ${slTc}`, className: 'text-green' })
      break
    }

    case 'crosschain': {
      addLine({ text: `🌉 Fetching cross-chain bridge volumes...`, className: 'text-dim' })
      const resCc = await safeJson(await authFetch('/api/v1/datavore/crosschain'), addLine)
      if (!resCc) break
      const bridges = Array.isArray(resCc) ? resCc : (resCc.bridges || resCc.data || [])
      addLine({ text: ``, className: '' })
      addLine({ text: `🌉  CROSS-CHAIN BRIDGE VOLUMES`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════════`, className: 'text-dim' })
      const rowsCc = bridges.slice(0, 20).map((b: any) => [
        (b.source_chain || b.from_chain || b.from || '').padEnd(12),
        (b.target_chain || b.to_chain || b.to || '').padEnd(12),
        fmt(b.volume || b.total_volume || b.amount || 0).padStart(12),
        pct(b.change_24h || b.change_pct || 0).padStart(8),
      ])
      addLine({ text: table(['From', 'To', 'Volume', '24h'], rowsCc), className: 'text-green' })
      break
    }

    case 'macro': {
      const country = args.slice(0).join('_').toUpperCase() || 'US'
      addLine({ text: `🌍 Fetching macro data for ${country}...`, className: 'text-dim' })
      const resMc = await safeJson(await authFetch(`/api/v1/datavore/macro/${country}`), addLine)
      if (!resMc) break
      addLine({ text: ``, className: '' })
      addLine({ text: `🌍  MACRO DASHBOARD — ${country}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      const gdpCls = (resMc.gdp_growth || 0) >= 0 ? 'text-green' : 'text-red'
      addLine({ text: `  GDP Growth:     ${(resMc.gdp_growth || 0) >= 0 ? '+' : ''}${resMc.gdp_growth}%`, className: gdpCls })
      const infCls = (resMc.inflation || 0) < 5 ? 'text-green' : 'text-red'
      addLine({ text: `  Inflation:      ${resMc.inflation}%`, className: infCls })
      const empCls = (resMc.employment_rate ?? resMc.unemployment ?? -1) < 6 ? 'text-green' : 'text-red'
      addLine({ text: `  Unemployment:   ${resMc.employment_rate ?? resMc.unemployment ?? '-'}%`, className: empCls })
      addLine({ text: `  Interest Rate:  ${resMc.interest_rate ?? resMc.rate ?? '-'}%`, className: 'text-yellow' })
      const debtCls = (resMc.debt_to_gdp || 999) < 100 ? 'text-yellow' : 'text-red'
      addLine({ text: `  Debt/GDP:       ${resMc.debt_to_gdp || '-'}%`, className: debtCls })
      break
    }

/*
//     case 'insider': {
//       const ticker = args[0]?.toUpperCase()
//       if (!ticker) { addLine({ text: 'Usage: insider <ticker>', className: 'text-yellow' }); break }
//       addLine({ text: `🔍 fetching insider transactions for ${ticker}...`, className: 'text-dim' })
//       const ins = await safeJson(await authFetch(`/api/v1/datavore/finnhub/insider/${ticker}`), addLine)
//       if (!ins) break
//       addLine({ text: `🔍  INSIDER TRADING  —  ${ticker}`, className: 'text-cyan' })
//       const items = Array.isArray(ins) ? ins : ins.data || ins.results || []
//       if (items.length === 0) { addLine({ text: '  No insider transactions found', className: 'text-dim' }); break }
//       for (const t of items.slice(0, 10)) {
//         const name = (t.name || t.insider || '').substring(0, 25).padEnd(25)
//         const shares = (t.share ?? t.shares ?? 0)
//         const price = (t.price ?? t.transactionPrice ?? 0)
//         const val = shares * price
//         addLine({ text: `  ${name} ${t.transactionType || t.type || 'TRADE'} ${shares > 0 ? '+' : ''}${shares} shares @ $${price.toFixed(2)} ($${(val / 1e6).toFixed(2)}M)`, className: t.transactionType === 'Buy' || shares > 0 ? 'text-green' : 'text-red' })
//       }
//       break
//     }
// 
    case 'ipo': {
      addLine({ text: `📅 fetching IPO calendar...`, className: 'text-dim' })
      const ip = await safeJson(await authFetch(`/api/v1/datavore/finnhub/ipo`), addLine)
      if (!ip) break
      addLine({ text: `📅  IPO CALENDAR`, className: 'text-cyan' })
      const items = ip.ipoCalendar || ip.data || ip.results || []
      if (items.length === 0) { addLine({ text: '  No upcoming IPOs', className: 'text-dim' }); break }
      for (const i of items.slice(0, 10)) {
        addLine({ text: `  ${(i.date || i.expectedDate || '').substring(0, 10)}  ${i.name || i.company || ''} (${i.symbol || i.ticker || ''})  $${i.priceRange || i.price || '-'}  ${i.exchange || ''}`, className: 'text-green' })
      }
      break
    }

    case 'ownership': {
      const ticker = args[0]?.toUpperCase()
      if (!ticker) { addLine({ text: 'Usage: ownership <ticker>', className: 'text-yellow' }); break }
      addLine({ text: `🏦 fetching institutional ownership for ${ticker}...`, className: 'text-dim' })
      const ow = await safeJson(await authFetch(`/api/v1/datavore/finnhub/ownership/${ticker}`), addLine)
      if (!ow) break
      addLine({ text: `🏦  INSTITUTIONAL OWNERSHIP  —  ${ticker}`, className: 'text-cyan' })
      const items = ow.data || ow.results || ow.ownership || []
      if (items.length === 0) { addLine({ text: '  No ownership data', className: 'text-dim' }); break }
      for (const o of items.slice(0, 10)) {
        const name = (o.holder || o.institution || o.name || '').substring(0, 25).padEnd(25)
        const shares = o.shares || o.position || 0
        const change = o.change || o.change_pct || 0
        addLine({ text: `  ${name}  ${(shares / 1e6).toFixed(2)}M shares  ${change >= 0 ? '+' : ''}${(change).toFixed(1)}%`, className: change >= 0 ? 'text-green' : 'text-red' })
      }
      break
    }

    case 'screener': {
      const isArgs = args.filter(a => a.startsWith('--'))
      const params = new URLSearchParams()
      for (const a of isArgs) {
        const [k, v] = a.replace('--', '').split('=')
        if (k === 'industry') params.set('industry', v)
        else if (k === 'country') params.set('country', v.toUpperCase())
        else if (k === 'minMcap') params.set('minMcap', v)
        else if (k === 'maxMcap') params.set('maxMcap', v)
      }
      params.set('limit', '30')
      addLine({ text: `🔍 screening companies...`, className: 'text-dim' })
      const sc = await safeJson(await authFetch(`/api/v1/datavore/map/companies?${params}`), addLine)
      if (!sc) break
      addLine({ text: `🔍  SCREENER RESULTS  (${sc.total} found)`, className: 'text-cyan' })
      const items = sc.companies || []
      if (items.length === 0) { addLine({ text: '  No matches', className: 'text-dim' }); break }
      addLine({ text: `  ${'Ticker'.padEnd(8)} ${'Name'.padEnd(30)} ${'Industry'.padEnd(16)} ${'Country'.padEnd(8)} ${'MCap'.padEnd(8)}`, className: 'text-dim' })
      for (const r of items) {
        addLine({ text: `  ${(r.ticker || '').padEnd(8)} ${(r.name || '').substring(0, 28).padEnd(30)} ${(r.industry || '').substring(0, 14).padEnd(16)} ${(r.country || '').padEnd(8)} $${(r.marketCap || 0).toFixed(0)}B`, className: 'text-green' })
      }
      break
    }

/*
//     case 'stablecoins': {
//       addLine({ text: `💰 fetching stablecoin data...`, className: 'text-dim' })
//       const scData = await safeJson(await authFetch(`/api/v1/datavore/defillama/stablecoins`), addLine)
//       if (!scData) break
//       addLine({ text: `💰  STABLECOIN SUPPLY`, className: 'text-cyan' })
//       const chains = scData.chains || Object.keys(scData)
//       for (const chain of chains.slice(0, 10)) {
//         const data = scData[chain] || {}
//         addLine({ text: `  ${(chain + '').padEnd(15)} $${((data.totalSupply || data.supply || 0) / 1e9).toFixed(2)}B`, className: 'text-green' })
//       }
//       break
//     }
// 
// // @ts-expect-error duplicate case (first wins)
*/

    case 'dexs': {
      addLine({ text: `🔄 fetching DEX volumes...`, className: 'text-dim' })
      const dx = await safeJson(await authFetch(`/api/v1/datavore/defillama/dexs`), addLine)
      if (!dx) break
      addLine({ text: `🔄  DEX VOLUMES`, className: 'text-cyan' })
      const items = dx.data || dx.protocols || [dx]
      for (const d of items.slice(0, 10)) {
        const name = (d.name || d.protocol || '').padEnd(20)
        const vol = d.volume24h || d.totalVolume || d.volume || 0
        addLine({ text: `  ${name} $${(vol / 1e6).toFixed(0)}M  ${d.change_24h != null ? (d.change_24h >= 0 ? '▲' : '▼') + Math.abs(d.change_24h).toFixed(1) + '%' : ''}`, className: 'text-green' })
      }
      break
    }

/*
//     case 'fees': {
//       const protocol = args[0] || ''
//       addLine({ text: `💸 fetching fees/revenue data...`, className: 'text-dim' })
//       const feeUrl = protocol ? `/api/v1/datavore/defillama/fees?protocol=${protocol}` : `/api/v1/datavore/defillama/fees`
//       const fe = await safeJson(await authFetch(feeUrl), addLine)
//       if (!fe) break
//       addLine({ text: `💸  PROTOCOL FEES & REVENUE${protocol ? ' — ' + protocol.toUpperCase() : ''}`, className: 'text-cyan' })
//       const items = fe.data || fe.protocols || [fe]
//       for (const f of items.slice(0, 10)) {
//         const name = (f.name || f.protocol || '').padEnd(20)
//         addLine({ text: `  ${name} Fees: $${((f.fees24h || f.dailyFees || f.fees || 0) / 1e3).toFixed(0)}K  Rev: $${((f.revenue24h || f.dailyRevenue || f.revenue || 0) / 1e3).toFixed(0)}K`, className: 'text-yellow' })
//       }
//       break
//     }
// 
*/

    case 'cpi': {
      addLine({ text: `📊 fetching US CPI data...`, className: 'text-dim' })
      const cp = await safeJson(await authFetch(`/api/v1/datavore/bls/cpi?start_year=2024&end_year=2026`), addLine)
      if (!cp?.data) break
      addLine({ text: `📊  US CONSUMER PRICE INDEX`, className: 'text-cyan' })
      for (const d of cp.data.slice(-12)) {
        const val = d.value ?? d.change ?? 0
        addLine({ text: `  ${(d.date || d.period || d.year || '').substring(0, 10)}  ${val}`, className: 'text-yellow' })
      }
      break
    }

    case 'employment': {
      addLine({ text: `🏭 fetching US employment data...`, className: 'text-dim' })
      const em = await safeJson(await authFetch(`/api/v1/datavore/bls/unemployment?start_year=2024&end_year=2026`), addLine)
      if (!em?.data) break
      addLine({ text: `🏭  US EMPLOYMENT DATA`, className: 'text-cyan' })
      for (const d of em.data.slice(-12)) {
        addLine({ text: `  ${(d.date || d.period || d.year || '').substring(0, 10)}  ${d.value || d.rate || '-'}%`, className: d.value < 4 ? 'text-green' : d.value < 6 ? 'text-yellow' : 'text-red' })
      }
      break
    }

    case 'treasury': {
      const sub = args[0]?.toLowerCase()
      addLine({ text: `🏛️ fetching treasury data...`, className: 'text-dim' })
      if (sub === 'curve' || !sub) {
        const res = await safeJson(await authFetch(`/api/v1/treasury/yield-curve`), addLine)
        if (res?.yield_curve) {
          addLine({ text: `🏛️  TREASURY YIELD CURVE`, className: 'text-cyan' })
          for (const p of res.yield_curve) {
            addLine({ text: `  ${(p.name || p.series_id || '').padEnd(25)} ${p.value}%`, className: 'text-green' })
          }
        }
      } else if (sub === 'yields') {
        const maturity = args[1]?.toUpperCase() || 'DGS10'
        const res = await safeJson(await authFetch(`/api/v1/treasury/yields/${maturity}?days=30`), addLine)
        if (res?.data) {
          addLine({ text: `🏛️  ${res.series_id} — LAST 30 DAYS`, className: 'text-cyan' })
          for (const d of res.data) {
            addLine({ text: `  ${d.date}  ${d.value}%`, className: 'text-yellow' })
          }
        }
      } else if (sub === 'tips') {
        const res = await safeJson(await authFetch(`/api/v1/treasury/tips`), addLine)
        if (res?.tips_breakeven) {
          addLine({ text: `🏛️  TIPS BREAKEVEN INFLATION (10Y)`, className: 'text-cyan' })
          for (const d of res.tips_breakeven.slice(-10)) {
            addLine({ text: `  ${d.date}  ${d.value}%`, className: 'text-yellow' })
          }
        }
      } else {
        addLine({ text: `Usage: treasury [curve|yields <maturity>|tips]`, className: 'text-yellow' })
      }
      break
    }

    case 'fedrates': {
      addLine({ text: `🏦 fetching central bank rates...`, className: 'text-dim' })
      const ratesRes = await safeJson(await authFetch(`/api/v1/treasury/rates`), addLine)
      if (ratesRes) {
        addLine({ text: `🏦  CENTRAL BANK RATES`, className: 'text-cyan' })
        for (const [key, data] of Object.entries(ratesRes)) {
          if (Array.isArray(data) && data.length > 0) {
            const latest = data[0]
            addLine({ text: `  ${key.toUpperCase().padEnd(10)} ${latest.value}%  (${latest.date})`, className: 'text-green' })
          }
        }
        addLine({ text: `  🐱 "The cat controls the rates now. Meow."`, className: 'text-dim' })
      }
      break
    }

    case 'bonds': {
      addLine({ text: `📄 fetching bond data...`, className: 'text-dim' })
      // Try corporate bonds API first, fall back to treasury
      const cbRes = await safeJson(await authFetch(`/api/v1/treasury/corporate-bonds`), addLine)
      if (cbRes?.bond_yields?.length > 0) {
        addLine({ text: `📄  CORPORATE BOND YIELDS — BY RATING`, className: 'text-cyan' })
        addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
        for (const b of cbRes.bond_yields) {
          const emoji = b.yield > 7 ? '🔴' : b.yield > 5 ? '🟡' : '🟢'
          addLine({ text: `  ${emoji} ${(b.rating || '').padEnd(8)} ${b.yield.toFixed(2)}%`, className: 'text-green' })
        }
        if (cbRes.credit_spreads?.length > 0) {
          addLine({ text: ``, className: '' })
          addLine({ text: `  📐  CREDIT SPREADS (vs 10Y Treasury)`, className: 'text-yellow' })
          addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
          for (const s of cbRes.credit_spreads) {
            addLine({ text: `  ${s.rating.padEnd(8)} ${s.spread_10y.toFixed(2)}%`, className: s.spread_10y > 3 ? 'text-red' : 'text-yellow' })
          }
        }
        addLine({ text: ``, className: '' })
        addLine({ text: `  🐱 "AAA bonds purr. CCC bonds hiss. The cat knows."`, className: 'text-dim' })
      } else {
        // Fallback: treasury yield curve
        const res = await safeJson(await authFetch(`/api/v1/treasury/yield-curve`), addLine)
        if (res?.yield_curve) {
          addLine({ text: `📄  TREASURY BOND YIELDS — ALL MATURITIES`, className: 'text-cyan' })
          for (const p of res.yield_curve) {
            const emoji = parseFloat(p.value) > 5 ? '🔴' : parseFloat(p.value) > 4 ? '🟡' : '🟢'
            addLine({ text: `  ${emoji} ${(p.name || p.series_id || '').padEnd(25)} ${p.value}%`, className: 'text-green' })
          }
        }
      }
      break
    }

    case 'etf': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'sectors' || sub === 'sector') {
        addLine({ text: `📊 fetching sector ETFs...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/etf/sectors`), addLine)
        if (res) {
          addLine({ text: `📊  SECTOR ETF PERFORMANCE`, className: 'text-cyan' })
          for (const g of (res.top_gainers || [])) {
            addLine({ text: `  🟢 ${g.name.padEnd(25)} ${g.ticker.padEnd(6)} ${g.change_pct >= 0 ? '+' : ''}${g.change_pct}%  $${g.price}`, className: 'text-green' })
          }
          for (const l of (res.top_losers || [])) {
            addLine({ text: `  🔴 ${l.name.padEnd(25)} ${l.ticker.padEnd(6)} ${l.change_pct >= 0 ? '+' : ''}${l.change_pct}%  $${l.price}`, className: 'text-red' })
          }
        }
      } else if (sub === 'top') {
        addLine({ text: `📊 fetching top ETFs...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/etf/top`), addLine)
        if (res?.top_etfs) {
          addLine({ text: `📊  TOP MAJOR ETFS`, className: 'text-cyan' })
          for (const e of res.top_etfs) {
            const emoji = e.change_pct >= 0 ? '🟢' : '🔴'
            addLine({ text: `  ${emoji} ${e.ticker.padEnd(6)} ${(e.name || '').padEnd(35)} $${e.price.toFixed(2)}  ${e.change_pct >= 0 ? '+' : ''}${e.change_pct}%`, className: e.change_pct >= 0 ? 'text-green' : 'text-red' })
          }
        }
      } else if (sub && sub !== 'help') {
        addLine({ text: `📊 fetching ETF ${sub}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/etf/quote/${sub}`), addLine)
        if (res) {
          const emoji = res.change_pct >= 0 ? '🟢' : '🔴'
          addLine({ text: `📊  ${res.name || res.ticker}`, className: 'text-cyan' })
          addLine({ text: `  ${emoji} Price: $${res.price}  ${res.change_pct >= 0 ? '+' : ''}${res.change_pct}%`, className: res.change_pct >= 0 ? 'text-green' : 'text-red' })
          if (res.nav) addLine({ text: `  NAV: $${res.nav}`, className: 'text-dim' })
          if (res.yield_pct != null) addLine({ text: `  Yield: ${res.yield_pct}%`, className: 'text-yellow' })
          if (res.beta != null) addLine({ text: `  Beta: ${res.beta}`, className: 'text-dim' })
          if (res.category) addLine({ text: `  Category: ${res.category}`, className: 'text-dim' })
        }
      } else {
        addLine({ text: `Usage: etf [sectors|top|<ticker>]`, className: 'text-yellow' })
      }
      break
    }

    case 'index':
    case 'indices': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'all' || !sub) {
        addLine({ text: `🌍 fetching global indices...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/indices/all`), addLine)
        if (res?.indices) {
          addLine({ text: `🌍  GLOBAL MARKET INDICES`, className: 'text-cyan' })
          for (const idx of res.indices) {
            const emoji = idx.change_pct >= 0 ? '🟢' : '🔴'
            addLine({ text: `  ${emoji} ${idx.ticker.padEnd(8)} ${(idx.name || '').padEnd(35)} ${idx.price.toFixed(2)}  ${idx.change_pct >= 0 ? '+' : ''}${idx.change_pct}%`, className: idx.change_pct >= 0 ? 'text-green' : 'text-red' })
          }
        }
      } else {
        addLine({ text: `🌍 fetching index ${sub}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/indices/quote/${sub}`), addLine)
        if (res) {
          const emoji = res.change_pct >= 0 ? '🟢' : '🔴'
          addLine({ text: `🌍  ${res.name || res.ticker} (${res.country})`, className: 'text-cyan' })
          addLine({ text: `  ${emoji} ${res.ticker}: ${res.price}  ${res.change_pct >= 0 ? '+' : ''}${res.change_pct}%`, className: res.change_pct >= 0 ? 'text-green' : 'text-red' })
          if (res.prev_close) addLine({ text: `  Prev Close: ${res.prev_close}`, className: 'text-dim' })
          if (res["52w_high"]) addLine({ text: `  52W High: ${res["52w_high"]}`, className: 'text-green' })
          if (res["52w_low"]) addLine({ text: `  52W Low: ${res["52w_low"]}`, className: 'text-red' })
        }
      }
      break
    }

    case 'ta':
    case 'technical': {
      const indicator = args[0]?.toLowerCase()
      const ticker = args[1]?.toUpperCase()
      if (ticker) {
        addLine({ text: `📈 running TA for ${ticker}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/technical/${ticker}?period=1y`), addLine)
        if (res) {
          addLine({ text: `📈  TECHNICAL ANALYSIS — ${ticker}  @ $${res.latest_price}`, className: 'text-cyan' })
          addLine({ text: `  🐱 Overall: ${res.overall_signal || 'N/A'} (${res.confidence || '?'}% confidence)`, className: 'text-yellow' })
          if (indicator && indicator !== 'all' && res[indicator.toUpperCase()] !== undefined) {
            addLine({ text: `  ${indicator.toUpperCase()}: ${res[indicator.toUpperCase()]}`, className: 'text-green' })
          } else if (!indicator || indicator === 'all') {
            for (const [k, v] of Object.entries(res)) {
              if (['ticker', 'latest_price', 'patterns', 'cat_commentary', 'overall_signal', 'confidence'].includes(k)) continue
              if (typeof v === 'number' || typeof v === 'string') {
                addLine({ text: `  ${k.padEnd(20)} ${v}`, className: k.includes('Signal') || k.includes('Trend') ? 'text-yellow' : 'text-green' })
              }
            }
          }
          if (res.cat_commentary) addLine({ text: `\n  🐱 ${res.cat_commentary}`, className: 'text-dim' })
        }
      } else {
        addLine({ text: `Usage: ta [indicator] <ticker>`, className: 'text-yellow' })
        addLine({ text: `Indicators: sma_20, sma_50, sma_200, ema_12, ema_26, macd, rsi_14, bb_upper, bb_lower, atr_14, adx_14, stoch_k, stoch_d, williams_%r, mfi_14, cci_20, aroon_up, aroon_down, roc_12, keltner_upper, obv, demark_buy_setup, demark_sell_setup`, className: 'text-dim' })
        addLine({ text: `Examples: ta AAPL | ta macd AAPL | ta rsi_14 AAPL`, className: 'text-dim' })
      }
      break
    }

    case 'signal':
    case 'signals': {
      const tickerSig = args[0]?.toUpperCase()
      if (!tickerSig) { addLine({ text: `Usage: signal <ticker>`, className: 'text-yellow' }); break }
      addLine({ text: `🔍 generating signals for ${tickerSig}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/technical/${tickerSig}/signal`), addLine)
      if (res?.signals) {
        addLine({ text: `🔍  TRADING SIGNALS — ${tickerSig}`, className: 'text-cyan' })
        addLine({ text: `  Price: $${res.price}  |  Overall: ${res.overall_signal}  |  Confidence: ${res.confidence}%`, className: 'text-yellow' })
        for (const s of res.signals) {
          const emoji = s.type === 'BUY' ? '🟢' : '🔴'
          const strength = s.strength === 'strong' ? '💪' : s.strength === 'moderate' ? '👍' : '👎'
          addLine({ text: `  ${emoji} ${s.type.padEnd(6)} ${strength} ${s.indicator.padEnd(15)} ${s.detail}`, className: s.type === 'BUY' ? 'text-green' : 'text-red' })
        }
        if (res.cat_commentary) addLine({ text: `  🐱 ${res.cat_commentary}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ Could not generate signals`, className: 'text-red' })
      }
      break
    }

    case 'pattern':
    case 'patterns': {
      const tickerPat = args[0]?.toUpperCase()
      if (!tickerPat) { addLine({ text: `Usage: pattern <ticker>`, className: 'text-yellow' }); break }
      addLine({ text: `🔎 detecting patterns for ${tickerPat}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/technical/${tickerPat}/patterns`), addLine)
      if (res?.patterns) {
        addLine({ text: `🔎  CANDLESTICK PATTERNS — ${tickerPat}`, className: 'text-cyan' })
        for (const p of res.patterns) {
          const emoji = p.signal === 'bullish' ? '🟢' : p.signal === 'bearish' ? '🔴' : '⚪'
          addLine({ text: `  ${emoji} ${p.pattern.padEnd(22)} ${p.signal.padEnd(10)} ${p.detail || ''}`, className: p.signal === 'bullish' ? 'text-green' : p.signal === 'bearish' ? 'text-red' : 'text-dim' })
        }
      } else {
        addLine({ text: `❌ Could not detect patterns`, className: 'text-red' })
      }
      break
    }

    case 'ols':
    case 'regress': {
      const yTicker = args[0]?.toUpperCase()
      const xTicker = args[1]?.toUpperCase()
      if (!yTicker || !xTicker) { addLine({ text: `Usage: ols <y_ticker> <x_ticker>`, className: 'text-yellow' }); break }
      addLine({ text: `📐 regressing ${yTicker} ~ ${xTicker}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/ols?y=${yTicker}&x=${xTicker}`), addLine)
      if (res?.r_squared != null) {
        addLine({ text: `📐  OLS REGRESSION — ${yTicker} ~ ${xTicker}`, className: 'text-cyan' })
        addLine({ text: `  ${res.equation || ''}`, className: 'text-green' })
        addLine({ text: `  R²: ${res.r_squared}  |  Adj R²: ${res.adj_r_squared}`, className: 'text-yellow' })
        addLine({ text: `  Coeff: ${res.coefficient}  |  p-value: ${res.p_value}  ${res.p_value < 0.05 ? '✅' : '❌'}`, className: res.p_value < 0.05 ? 'text-green' : 'text-red' })
        addLine({ text: `  F-stat: ${res.f_statistic}  |  n=${res.observations}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ Regression failed: ${res?.error || 'unknown'}`, className: 'text-red' })
      }
      break
    }

    case 'granger': {
      const gy = args[0]?.toUpperCase()
      const gx = args[1]?.toUpperCase()
      if (!gy || !gx) { addLine({ text: `Usage: granger <y_ticker> <x_ticker>`, className: 'text-yellow' }); break }
      addLine({ text: `🔗 testing Granger causality: does ${gx} → ${gy}?...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/granger?y=${gy}&x=${gx}`), addLine)
      if (res?.results) {
        addLine({ text: `🔗  GRANGER CAUSALITY — ${gx} → ${gy}`, className: 'text-cyan' })
        addLine({ text: `  ${res.conclusion || ''}`, className: res.significant_at?.length ? 'text-green' : 'text-red' })
        for (const r of res.results) {
          addLine({ text: `  Lag ${r.lag}: F=${r.f_statistic}  p=${r.p_value}  ${r.significant ? '✅' : '❌'}`, className: r.significant ? 'text-green' : 'text-dim' })
        }
      } else {
        addLine({ text: `❌ Granger test failed`, className: 'text-red' })
      }
      break
    }

    case 'coint':
    case 'cointegration': {
      const ca = args[0]?.toUpperCase()
      const cb = args[1]?.toUpperCase()
      if (!ca || !cb) { addLine({ text: `Usage: coint <ticker_a> <ticker_b>`, className: 'text-yellow' }); break }
      addLine({ text: `🔗 testing cointegration: ${ca} ~ ${cb}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/coint?a=${ca}&b=${cb}`), addLine)
      if (res?.is_cointegrated != null) {
        addLine({ text: `🔗  COINTEGRATION — ${ca} / ${cb}`, className: 'text-cyan' })
        addLine({ text: `  ${res.conclusion || ''}`, className: res.is_cointegrated ? 'text-green' : 'text-red' })
        addLine({ text: `  Hedge Ratio: ${res.hedge_ratio}`, className: 'text-yellow' })
        addLine({ text: `  ADF Stat: ${res.adf_statistic}  |  p-value: ${res.adf_p_value}`, className: res.is_cointegrated ? 'text-green' : 'text-dim' })
        addLine({ text: `  Current Spread: ${res.current_spread}  |  Z-Score: ${res.z_score}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ Cointegration test failed`, className: 'text-red' })
      }
      break
    }

    case 'capm': {
      const capmTicker = args[0]?.toUpperCase()
      const capmBench = args[1]?.toUpperCase() || 'SPY'
      if (!capmTicker) { addLine({ text: `Usage: capm <ticker> [benchmark]`, className: 'text-yellow' }); break }
      addLine({ text: `📊 running CAPM for ${capmTicker} vs ${capmBench}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/capm?ticker=${capmTicker}&benchmark=${capmBench}`), addLine)
      if (res?.beta != null) {
        addLine({ text: `📊  CAPM ANALYSIS — ${capmTicker} vs ${capmBench}`, className: 'text-cyan' })
        addLine({ text: `  Alpha: ${res.alpha}%  |  Beta: ${res.beta}`, className: 'text-yellow' })
        addLine({ text: `  Annual Return: ${res.annual_return}%  |  Volatility: ${res.annual_volatility}%`, className: 'text-green' })
        addLine({ text: `  Sharpe: ${res.sharpe_ratio}  |  Treynor: ${res.treynor_ratio}  |  Info Ratio: ${res.info_ratio}`, className: 'text-dim' })
        addLine({ text: `  R²: ${res.r_squared}  |  Tracking Error: ${res.tracking_error}%`, className: 'text-dim' })
        if (res.cat_commentary) addLine({ text: `  🐱 ${res.cat_commentary}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ CAPM analysis failed`, className: 'text-red' })
      }
      break
    }

    case 'risk': {
      const riskTicker = args[0]?.toUpperCase()
      if (!riskTicker) { addLine({ text: `Usage: risk <ticker>`, className: 'text-yellow' }); break }
      addLine({ text: `⚠️ analyzing risk for ${riskTicker}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/risk?ticker=${riskTicker}`), addLine)
      if (res?.var != null) {
        addLine({ text: `⚠️  RISK ANALYSIS — ${riskTicker}`, className: 'text-cyan' })
        addLine({ text: `  VaR (95%): ${(res.var * 100).toFixed(2)}%  |  CVaR: ${(res.cvar * 100).toFixed(2)}%`, className: 'text-yellow' })
        addLine({ text: `  Max Drawdown: ${res.max_drawdown_pct}%  (${res.max_drawdown_date})`, className: res.max_drawdown_pct < -30 ? 'text-red' : 'text-green' })
        addLine({ text: `  Return: ${res.annual_return_pct}%  |  Vol: ${res.annual_volatility_pct}%  |  Sharpe: ${res.sharpe_ratio}`, className: 'text-green' })
        addLine({ text: `  VaR 1d: ${(res.var_1_day * 100).toFixed(2)}%  |  1w: ${(res.var_1_week * 100).toFixed(2)}%  |  1m: ${(res.var_1_month * 100).toFixed(2)}%`, className: 'text-dim' })
        if (res.cat_commentary) addLine({ text: `  🐱 ${res.cat_commentary}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ Risk analysis failed`, className: 'text-red' })
      }
      break
    }

    case 'correl': {
      const tickers = args.map(t => t.toUpperCase())
      if (tickers.length < 2) { addLine({ text: `Usage: correl <ticker1> <ticker2> [ticker3 ...]`, className: 'text-yellow' }); break }
      addLine({ text: `🔗 calculating correlation for ${tickers.join(', ')}...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/econometrics/correl?tickers=${tickers.join(',')}`), addLine)
      if (res?.matrix) {
        addLine({ text: `🔗  CORRELATION MATRIX`, className: 'text-cyan' })
        const keys = Object.keys(res.matrix)
        for (const t1 of keys) {
          const row = keys.map(t2 => {
            const val = res.matrix[t1]?.[t2]
            return val != null ? val.toFixed(2) : '   '
          }).join('  ')
          addLine({ text: `  ${t1.padEnd(8)} ${row}`, className: 'text-green' })
        }
        addLine({ text: `  Observations: ${res.observations}`, className: 'text-dim' })
        if (res.cat_commentary) addLine({ text: `  🐱 ${res.cat_commentary}`, className: 'text-dim' })
      } else {
        addLine({ text: `❌ Correlation failed`, className: 'text-red' })
      }
      break
    }

    case 'commodities':
    case 'commodity': {
      const sub = args[0]?.toLowerCase()
      if (!sub || sub === 'all') {
        addLine({ text: `🛢️ fetching commodities...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/commodities/all`), addLine)
        if (res?.commodities) {
          addLine({ text: `🛢️  COMMODITY PRICES`, className: 'text-cyan' })
          for (const c of res.commodities) {
            const emoji = c.change_pct >= 0 ? '🟢' : '🔴'
            addLine({ text: `  ${emoji} ${c.ticker.padEnd(6)} ${(c.name || '').padEnd(30)} $${c.price.toFixed(2)}  ${c.change_pct >= 0 ? '+' : ''}${c.change_pct}%`, className: c.change_pct >= 0 ? 'text-green' : 'text-red' })
          }
        }
      } else if (sub === 'energy') {
        addLine({ text: `🛢️ fetching energy commodities...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/commodities/category/energy`), addLine)
        if (res?.commodities) {
          addLine({ text: `🛢️  ENERGY COMMODITIES`, className: 'text-cyan' })
          for (const c of res.commodities) {
            addLine({ text: `  ${c.ticker.padEnd(6)} ${(c.name || '').padEnd(30)} $${c.price.toFixed(2)}`, className: 'text-yellow' })
          }
        }
      } else if (sub === 'agri' || sub === 'agriculture') {
        addLine({ text: `🌾 fetching agricultural commodities...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/commodities/category/agriculture`), addLine)
        if (res?.commodities) {
          addLine({ text: `🌾  AGRICULTURAL COMMODITIES`, className: 'text-cyan' })
          for (const c of res.commodities) {
            addLine({ text: `  ${c.ticker.padEnd(6)} ${(c.name || '').padEnd(30)} $${c.price.toFixed(2)}`, className: 'text-yellow' })
          }
        }
      } else {
        const ticker = sub.toUpperCase()
        addLine({ text: `🛢️ fetching ${ticker}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/commodities/${ticker}`), addLine)
        if (res) {
          const emoji = res.change_pct >= 0 ? '🟢' : '🔴'
          addLine({ text: `🛢️  ${res.name || res.ticker}`, className: 'text-cyan' })
          addLine({ text: `  ${emoji} $${res.price}  ${res.change_pct >= 0 ? '+' : ''}${res.change_pct}%  ${res.unit || ''}`, className: res.change_pct >= 0 ? 'text-green' : 'text-red' })
        }
      }
      break
    }

    case 'cattuna':
    case 'tunaprice': {
      addLine({ text: `🐟 fetching the Tuna Index...`, className: 'text-dim' })
      const [priceRes, indexRes] = await Promise.allSettled([
        safeJson(await authFetch('/api/v1/commodities/tuna/price'), addLine),
        safeJson(await authFetch('/api/v1/commodities/tuna/index'), addLine),
      ])
      const price = priceRes.status === 'fulfilled' ? priceRes.value : null
      const idx = indexRes.status === 'fulfilled' ? indexRes.value : null
      if (price) {
        const emoji = price.change_pct >= 0 ? '🟢' : '🔴'
        addLine({ text: `🐟  TUNA PRICE INDEX`, className: 'text-cyan' })
        addLine({ text: `  ${emoji} ${price.name}: $${price.price}  ${price.change_pct >= 0 ? '+' : ''}${price.change_pct}%`, className: price.change_pct >= 0 ? 'text-green' : 'text-red' })
        addLine({ text: `  🐱 "${price.cat_commentary}"`, className: 'text-dim' })
      }
      if (idx?.cat_food_index) {
        addLine({ text: `\n🐱  CAT FOOD BASKET`, className: 'text-cyan' })
        for (const i of idx.cat_food_index) {
          addLine({ text: `  ${i.name.padEnd(35)} $${i.price}  ${i.change_pct >= 0 ? '+' : ''}${i.change_pct}%`, className: i.change_pct >= 0 ? 'text-green' : 'text-red' })
        }
      }
      break
    }

    case 'futures':
    case 'future': {
      const sub = args[0]?.toLowerCase()
      if (!sub || sub === 'all') {
        addLine({ text: `📈 fetching futures...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/derivatives/futures`), addLine)
        if (res?.futures) {
          addLine({ text: `📈  FUTURES PRICES`, className: 'text-cyan' })
          for (const f of res.futures) {
            const emoji = f.change_pct >= 0 ? '🟢' : '🔴'
            addLine({ text: `  ${emoji} ${f.ticker.padEnd(6)} ${(f.name || '').padEnd(30)} $${f.price.toFixed(2)}  ${f.change_pct >= 0 ? '+' : ''}${f.change_pct}%`, className: f.change_pct >= 0 ? 'text-green' : 'text-red' })
          }
        }
      } else {
        const ticker = sub.toUpperCase()
        addLine({ text: `📈 fetching ${ticker}...`, className: 'text-dim' })
        const res = await safeJson(await authFetch(`/api/v1/derivatives/futures/${ticker}`), addLine)
        if (res) {
          const emoji = res.change_pct >= 0 ? '🟢' : '🔴'
          addLine({ text: `📈  ${res.name || res.ticker} (${res.exchange || res.category || ''})`, className: 'text-cyan' })
          addLine({ text: `  ${emoji} $${res.price}  ${res.change_pct >= 0 ? '+' : ''}${res.change_pct}%  Vol: ${(res.volume || 0).toLocaleString()}`, className: res.change_pct >= 0 ? 'text-green' : 'text-red' })
        }
      }
      break
    }

    case 'mortgage': {
      addLine({ text: `🏠 fetching mortgage rates...`, className: 'text-dim' })
      const res = await safeJson(await authFetch(`/api/v1/treasury/mortgage`), addLine)
      if (res?.mortgage_rates) {
        addLine({ text: `🏠  MORTGAGE RATES`, className: 'text-cyan' })
        for (const r of res.mortgage_rates) {
          addLine({ text: `  ${(r.name || r.series_id || '').padEnd(45)} ${r.value}%`, className: r.value > 7 ? 'text-red' : r.value > 6 ? 'text-yellow' : 'text-green' })
        }
        addLine({ text: `  🐱 "The cat says: buy when rates purr, not when they hiss."`, className: 'text-dim' })
      }
      break
    }

/*
//     case 'famanch': {
//       const ticker = args[0]?.toUpperCase()
//       if (!ticker) { addLine({ text: 'Usage: famanch <ticker>', className: 'text-yellow' }); break }
//       addLine({ text: `📊 fetching Fama-French factors for ${ticker}...`, className: 'text-dim' })
//       const ff = await safeJson(await authFetch(`/api/v1/datavore/quant/fama-french/${ticker}`), addLine)
//       if (!ff) break
//       addLine({ text: `📊  FAMA-FRENCH 5-FACTOR — ${ticker}`, className: 'text-cyan' })
//       const data = ff.data || ff
//       const factors = data.factors || data.loadings || data
//       Object.entries(factors).slice(0, 8).forEach(([k, v]: [string, any]) => {
//         if (typeof v === 'number') addLine({ text: `  ${k.padEnd(20)} ${v >= 0 ? '+' : ''}${v.toFixed(4)}`, className: v > 0 ? 'text-green' : 'text-red' })
//       })
//       if (data.r_squared) addLine({ text: `  R²'.padEnd(20)} ${data.r_squared.toFixed(4)}`, className: 'text-dim' })
//       break
//     }
// 
*/

    case 'riskfactors': {
      const ticker = args[0]?.toUpperCase()
      if (!ticker) { addLine({ text: 'Usage: riskfactors <ticker>', className: 'text-yellow' }); break }
      addLine({ text: `⚠️ fetching risk factors for ${ticker}...`, className: 'text-dim' })
      const rf = await safeJson(await authFetch(`/api/v1/datavore/quant/risk-factors/${ticker}`), addLine)
      if (!rf) break
      addLine({ text: `⚠️  RISK FACTOR ANALYSIS — ${ticker}`, className: 'text-cyan' })
      const data = rf.data || rf
      const risks = data.risks || data.risk_factors || data
      if (Array.isArray(risks)) {
        for (const r of risks.slice(0, 10)) {
          addLine({ text: `  ${(r.factor || r.name || '').substring(0, 50)}  count: ${r.count || r.word_count || '-'}`, className: 'text-yellow' })
        }
      } else if (typeof risks === 'object') {
        Object.entries(risks).slice(0, 10).forEach(([k, v]: [string, any]) => {
          addLine({ text: `  ${k.padEnd(30)} ${v}`, className: 'text-yellow' })
        })
      }
      break
    }

/*
//     case 'passiveflow': {
//       const ticker = args[0]?.toUpperCase()
//       if (!ticker) { addLine({ text: 'Usage: passiveflow <ticker>', className: 'text-yellow' }); break }
//       addLine({ text: `🏦 fetching passive flow for ${ticker}...`, className: 'text-dim' })
//       const pf = await safeJson(await authFetch(`/api/v1/datavore/quant/passive-float/${ticker}`), addLine)
//       if (!pf) break
//       addLine({ text: `🏦  PASSIVE OWNERSHIP — ${ticker}`, className: 'text-cyan' })
//       const data = pf.data || pf
//       if (data.passive_float_pct != null) addLine({ text: `  % in ETFs:   ${(data.passive_float_pct * 100).toFixed(1)}%`, className: data.passive_float_pct > 0.1 ? 'text-yellow' : 'text-green' })
//       if (data.total_etf_shares != null) addLine({ text: `  ETF Shares:  ${(data.total_etf_shares / 1e6).toFixed(0)}M`, className: 'text-dim' })
//       if (data.total_etf_value != null) addLine({ text: `  ETF Value:   $${(data.total_etf_value / 1e9).toFixed(2)}B`, className: 'text-dim' })
//       if (data.blind_dollar_flow != null) addLine({ text: `  Blind Flow:  $${(data.blind_dollar_flow / 1e6).toFixed(0)}M`, className: 'text-yellow' })
//       break
//     }
// 
*/

    case 'earningscore': {
      const ticker = args[0]?.toUpperCase()
      if (!ticker) { addLine({ text: 'Usage: earningscore <ticker>', className: 'text-yellow' }); break }
      addLine({ text: `🎙️ fetching earnings call transparency for ${ticker}...`, className: 'text-dim' })
      const ec = await safeJson(await authFetch(`/api/v1/datavore/quant/earnings-transparency/${ticker}`), addLine)
      if (!ec) break
      addLine({ text: `🎙️  EARNINGS CALL SCORE — ${ticker}`, className: 'text-cyan' })
      const data = ec.data || ec
      const s = data.summary || data
      if (s.latest_score != null) addLine({ text: `  Latest Score:  ${s.latest_score}/10  —  ${s.latest_label || ''}`, className: s.latest_score >= 7 ? 'text-green' : s.latest_score >= 4 ? 'text-yellow' : 'text-red' })
      if (s.average_score != null) addLine({ text: `  Avg Score:     ${s.average_score}/10`, className: 'text-dim' })
      if (s.trend) addLine({ text: `  Trend:         ${s.trend}`, className: s.trend === 'improving' ? 'text-green' : s.trend === 'stable' ? 'text-dim' : 'text-red' })
      if (s.latest_quarter) addLine({ text: `  Latest Quarter: ${s.latest_quarter}`, className: 'text-dim' })
      if (s.latest_deflection_quote) addLine({ text: `  Quote: \"${s.latest_deflection_quote.substring(0, 80)}...\"`, className: 'text-yellow' })
      break
    }

    case 'miaustats': {
      addLine({ text: `📊  MIAU PLATFORM DASHBOARD`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      try {
        const headers: Record<string, string> = localStorage.getItem('miau_token')
          ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}

        // Fetch health + datasources in parallel
        const [healthRes, dsRes] = await Promise.all([
          fetch('/api/v1/health', { headers }).then(r => r.ok ? r.json() : null).catch(() => null),
          fetch('/api/v1/datasources/status', { headers }).then(r => r.ok ? r.json() : null).catch(() => null),
        ])

        addLine({ text: `  🔧  System:   ${healthRes?.status === 'healthy' ? '✅ Healthy' : '⚠️ ' + (healthRes?.status || 'Unknown')}`, className: healthRes?.status === 'healthy' ? 'text-green' : 'text-yellow' })
        if (dsRes) {
          addLine({ text: `  📡  Sources:  ${dsRes.total_providers} registered · ${dsRes.healthy || 0} healthy`, className: 'text-green' })
          addLine({ text: `  💾  Cache:    ${dsRes.cache?.hit_ratio ? (dsRes.cache.hit_ratio * 100).toFixed(0) + '% hit rate' : 'N/A'}`, className: 'text-dim' })
        }
      } catch {}

      // Top market movers (hardcoded major tickers)
      addLine({ text: ``, className: '' })
      addLine({ text: `  📈  MARKET WATCH`, className: 'text-cyan' })
      try {
        const pricesRes = await fetch('/api/v1/datavore/map/batch-prices?tickers=AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META,JPM,V,MA')
        if (pricesRes.ok) {
          const pricesData = await pricesRes.json()
          if (pricesData?.prices) {
            for (const [t, p] of Object.entries(pricesData.prices)) {
              const chg = (p as any).change_pct ?? 0
              const price = (p as any).price ?? 0
              addLine({ text: `  ${t.padEnd(6)} $${typeof price === 'number' ? price.toFixed(2) : '—'.padStart(7)}  ${chg >= 0 ? '▲' : '▼'} ${Math.abs(chg).toFixed(2)}%`, className: chg >= 0 ? 'text-green' : 'text-red' })
            }
          }
        }
      } catch {}

      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱  The cat watches the markets. The cat is pleased.`, className: 'text-dim' })
      break
    }

    case 'chat': {
      const query = args.join(' ')
      if (!query) {
        addLine({ text: '🐱 Opening AI Chat Panel... type "kitty" to manage.', className: 'text-green' })
        addLine({ text: '   Or: chat <question> to ask inline.', className: 'text-dim' })
        // The Terminal component intercepts this signal to open ChatPanel
        ;(window as any).__miau_openChatPanel?.()
        break
      }
      addLine({ text: `🤖 Miau AI is thinking...`, className: 'text-dim' })
      try {
        const token = localStorage.getItem('miau_token')
        const headers: Record<string, string> = { 'Content-Type': 'application/json' }
        if (token) headers['Authorization'] = `Bearer ${token}`
        const res = await fetch('/api/v1/ai/advisor/query', {
          method: 'POST', headers,
          body: JSON.stringify({ query, portfolio_id: null }),
        })
        if (res.ok) {
          const d = await res.json()
          const text = d.response || d.answer || d.message || JSON.stringify(d)
          addLine({ text: ``, className: '' })
          addLine({ text: `🐱  MIAU AI SAYS:`, className: 'text-cyan' })
          addLine({ text: text, className: 'text-green' })
          if (d.cat_commentary) addLine({ text: `\n${d.cat_commentary}`, className: 'text-dim' })
        } else {
          const err = await res.text()
          addLine({ text: `❌ AI error: ${err.substring(0, 200)}`, className: 'text-red' })
        }
      } catch (e: any) {
        addLine({ text: `❌ AI error: ${e.message || e}`, className: 'text-red' })
      }
      break
    }

    case 'demo': {
      const steps = [
        { cmd: 'miaustats', msg: '📊 System dashboard' },
        { cmd: 'price AAPL', msg: '📈 Live price' },
        { cmd: 'fx EUR', msg: '💱 FX rates' },
        { cmd: 'gas', msg: '⛽ Gas prices' },
        { cmd: 'quanthealth AAPL', msg: '🔬 Quant health' },
        { cmd: 'fairvalue AAPL', msg: '💰 Fair value' },
        { cmd: 'insider AAPL', msg: '🔍 Insider trades' },
        { cmd: 'help market', msg: '📚 Help filtered' },
      ]
      addLine({ text: `🎬  MIAU DEMO — Showcasing features`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      for (const step of steps) {
        addLine({ text: ``, className: '' })
        addLine({ text: `▶ ${step.msg}`, className: 'text-yellow' })
        await executeCommand(step.cmd, addLine)
      }
      addLine({ text: ``, className: '' })
      addLine({ text: `🎬  DEMO COMPLETE — Try miaumap, chartz3d AAPL, courses`, className: 'text-green' })
      break
    }

    case 'pulse': {
      addLine({ text: `📊  MARKET PULSE  (fetching...)`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      try {
        const headers: Record<string, string> = localStorage.getItem('miau_token')
          ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}

        // Fear & Greed
        try {
          const fg = await fetch('/api/v1/market/crypto/fear-greed', { headers }).then(r => r.json())
          addLine({ text: `  😱 Fear & Greed: ${fg.value}/100 — ${fg.classification}`, className: fg.value < 30 ? 'text-red' : fg.value > 70 ? 'text-green' : 'text-yellow' })
        } catch {}

        // Key prices in parallel
        try {
          const batch = await fetch('/api/v1/datavore/map/batch-prices?tickers=SPY,AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA,META,BTC-USD,ETH-USD', { headers }).then(r => r.json())
          if (batch?.prices) {
            addLine({ text: ``, className: '' })
            addLine({ text: `  📈  KEY MARKETS`, className: 'text-cyan' })
            for (const [t, p] of Object.entries(batch.prices)) {
              const pp = p as any
              const chg = pp.change_pct ?? 0
              addLine({ text: `  ${t.padEnd(10)} $${(pp.price ?? 0).toFixed(2).padStart(10)}  ${chg >= 0 ? '▲' : '▼'} ${Math.abs(chg).toFixed(2)}%`, className: chg >= 0 ? 'text-green' : 'text-red' })
            }
          }
        } catch {}
      } catch {}

      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱  Pulse checked. The cat is monitoring.`, className: 'text-dim' })
      break
    }

    case 'rave': {
      const delay = (ms: number) => new Promise(r => setTimeout(r, ms))
      const C = ['text-green', 'text-purple', 'text-yellow', 'text-cyan', 'text-red']
      const rnd = () => C[Math.floor(Math.random() * C.length)]
      const rand = <T,>(a: T[]) => a[Math.floor(Math.random() * a.length)]

      const KITTENS = [
        ['🎓', 'Luna — quant intern, knows Python & purrs', 'text-green'],
        ['📊', 'Felix — risk analyst, 9 lives of VaR experience', 'text-purple'],
        ['💻', 'Mochi — full-stack dev, codes in naps', 'text-yellow'],
        ['📈', 'Simba — M&A kitten, acquiring catnip futures', 'text-cyan'],
        ['🔬', 'Oreo — data scientist, chases laser pointers & alpha', 'text-red'],
        ['💰', 'Tigger — DeFi kitten, yield farms catnip', 'text-purple'],
        ['🚀', 'Whiskers — crypto native, paws on the pulse', 'text-green'],
        ['🏦', 'Mittens — IB kitten, Excel & catnaps expert', 'text-yellow'],
        ['🤖', 'Sasha — AI/ML kitten, training models & purrs', 'text-cyan'],
        ['📉', 'Pepper — short seller, bear markets love this cat', 'text-red'],
      ]

      const CAT_DANCE = [
        [' ╱|、      ╱|、      ╱|、     ',
         '(˚ˎ 。7   (˚ˎ 。7   (˚ˎ 。7    ',
         ' |、˜〵    |、˜〵    |、˜〵     ',
         ' じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ  '],
        [' ／|＼     ／|＼     ／|＼    ',
         '( ⌒。⌒)  ( ⌒。⌒)  ( ⌒。⌒)   ',
         ' |\'\'〵    |\'\'〵    |\'\'〵    ',
         ' じしˍ,)ノ じしˍ,)ノ じしˍ,)ノ '],
        [' ⋆｡°✩╱|、✩°｡⋆',
         ' ⋆｡°✩(˚▽˚)っ✩°｡⋆',
         ' ⋆｡°✩|、˜〵✩°｡⋆',
         ' ⋆｡°✩じしˍ,)ノ✩°｡⋆'],
        [' ╱╲╱╲    ╱╲╱╲    ╱╲╱╲   ',
         '( ◕‿◕)  ( ◕‿◕)  ( ◕‿◕)  ',
         ' |、〵~   |、〵~   |、〵~   ',
         ' じしˍ,)〜 じしˍ,)〜 じしˍ,)〜'],
        [' ╱▔╲     ╱▔╲     ╱▔╲    ',
         '(≧▽≦)   (≧▽≦)   (≧▽≦)   ',
         ' |、〵     |、〵     |、〵    ',
         ' じしˍ,)  じしˍ,)  じしˍ,)  '],
        [' ╱o╲     ╱o╲     ╱o╲    ',
         '(°🐱°)   (°🐱°)   (°🐱°)   ',
         ' |、~〵   |、~〵   |、~〵   ',
         ' じしˍ,)~ じしˍ,)~ じしˍ,)~'],
        [' ✨╱|、✨ ✨╱|、✨ ✨╱|、✨',
         ' ✨(˚▽˚)✨ ✨(˚▽˚)✨ ✨(˚▽˚)✨',
         ' ✨|、˜〵✨ ✨|、˜〵✨ ✨|、˜〵✨',
         ' ✨じしˍ,)ノ✨✨じしˍ,)ノ✨✨'],
        [' 🎵╱|、🎵  🎵╱|、🎵  🎵╱|、🎵',
         ' 🎵(˚▽˚)🎵  🎵(˚▽˚)🎵  🎵(˚▽˚)🎵',
         ' 🎵|、˜〵🎵  🎵|、˜〵🎵  🎵|、˜〵🎵',
         ' 🎵じしˍ,)ノ🎵🎵じしˍ,)ノ🎵🎵'],
      ]

      // ── INTRO ──
      addLine({ text: '', className: '' })
      addLine({ text: '  ╔══════════════════════════════════════════╗', className: 'text-purple font-bold' })
      addLine({ text: '  ║  🎉🐱💰  MIAU RAVE — KITTEN EDITION  💰🐱🎉  ║', className: 'text-green font-bold' })
      addLine({ text: '  ╚══════════════════════════════════════════╝', className: 'text-purple font-bold' })
      addLine({ text: '', className: '' })
      await delay(400)

      // ── HIRE THE KITTENS ──
      addLine({ text: '  📋  NEW FINECHT KITTEN COHORT — HIRED!', className: 'text-cyan font-bold' })
      addLine({ text: '  ─────────────────────────────────────────', className: 'text-dim' })
      await delay(300)
      for (const [icon, name, color] of KITTENS) {
        addLine({ text: `  ${icon}  ${name}`, className: color as string })
        await delay(100)
      }
      addLine({ text: '  ─────────────────────────────────────────', className: 'text-dim' })
      addLine({ text: `  🐱💼  ${KITTENS.length} kittens onboarded. Equity: catnip.`, className: 'text-yellow font-bold' })
      addLine({ text: '', className: '' })
      await delay(500)

      // ── RAVE LIGHTS ──
      const lightShows = [
        ['🔴','🟡','🟢','🔵','🟣','🔴','🟡','🟢','🔵','🟣'],
        ['💖','🧡','💛','💚','💙','💜','💖','🧡','💛','💚'],
        ['🌟','✨','💫','⭐','🌟','✨','💫','⭐','🌟','✨'],
        ['🔥','⚡','💥','🔥','⚡','💥','🔥','⚡','💥','🔥'],
      ]

      for (let round = 0; round < 6; round++) {
        const dance = CAT_DANCE[round % CAT_DANCE.length]
        const lights = lightShows[round % lightShows.length]

        // Light bar
        const bar = lights.map(l => `${l}`).join(' ')
        addLine({ text: `  ${bar}`, className: rnd() })
        await delay(60)

        // DJ announcement
        const djs = ['DJ WHISKASAURUS', 'MC PAWPAW', 'TURNTABLE TAIL', 'KITTEN KUT', 'PURR DIDDY', 'FELIX DA FUNK']
        const tracks = ['TUNA DROP', 'PURRTECHNO 3000', 'CATWALK BEAT', 'MEOW MIX', 'FISH MARKET BASS', 'SCRATCH POST']
        addLine({ text: `  🎧  ${rand(djs)} — "THIS ONE'S CALLED ${rand(tracks)}"`, className: 'text-yellow' })
        await delay(150)

        // Dance lines
        for (let row = 0; row < dance.length; row++) {
          addLine({ text: `  ${dance[row]}`, className: rnd() })
          await delay(100)
        }

        // Beat drops
        addLine({ text: `  ${'─'.repeat(40)}`, className: 'text-dim' })
        for (let b = 0; b < 5; b++) {
          const boom = rand(['💥','⚡','🔥','💫','🎵','🎶','🔊','📢'])
          const boomColor = ['text-red', 'text-yellow', 'text-purple', 'text-cyan', 'text-green'][b % 5]
          addLine({ text: `  ${boom}  WOOF WOOF WUB WUB  ${boom}  BOOM  ${boom}  DROP  ${boom}`, className: boomColor })
          await delay(150)
        }
        addLine({ text: `  ${'─'.repeat(40)}`, className: 'text-dim' })
        await delay(200)

        // Fintech fact
        const facts = [
          'Kitten intern fixed the yield curve. In her sleep.',
          'Felix the risk kitten found a tail-hedge. Naturally.',
          'Mochi deployed to prod. While napping. Zero bugs.',
          'Simba acquired 3 catnip futures contracts. Bullish.',
          'Oreo found alpha in the laser pointer. +420% returns.',
          'Tigger yields 69% APY on catnip protocol.',
          'Whiskers minted a PFP collection. Floor: 4.20 ETH.',
          'Mittens built a DCF model. With paw prints.',
          'Sasha trained an LLM on tuna recipes. It works.',
          'Pepper shorted the dog market. 1000% gains.',
        ]
        addLine({ text: `  📈  KITTEN QUANT NOTE: ${rand(facts)}`, className: 'text-cyan font-bold' })
        addLine({ text: '', className: '' })
      }

      // ── GRAND FINALE ──
      addLine({ text: '', className: '' })
      addLine({ text: '  ✨  🐱💥💰  GRAND FINALE  💰💥🐱  ✨', className: 'text-green font-bold' })
      await delay(200)
      for (let f = 0; f < 8; f++) {
        const fireworks = ['🎆','🎇','✨','🌟','💫','⭐','🌠','🎆'][f]
        const fwColor = ['text-red', 'text-yellow', 'text-purple', 'text-cyan', 'text-green'][f % 5]
        addLine({ text: `  ${fireworks}  ${fireworks}  ${fireworks}  🐱🔊  ${fireworks}  ${fireworks}  ${fireworks}`, className: fwColor })
        await delay(100)
      }
      await delay(300)

      // ── OUTRO ──
      addLine({ text: '', className: '' })
      addLine({ text: '  ╔══════════════════════════════════════════╗', className: 'text-purple font-bold' })
      addLine({ text: '  ║  MIAU RAVE — CATS HIRED, BEATS DROPPED  ║', className: 'text-yellow font-bold' })
      addLine({ text: '  ║  10 fintech kittens joined the squad! 🐱  ║', className: 'text-green font-bold' })
      addLine({ text: '  ╚══════════════════════════════════════════╝', className: 'text-purple font-bold' })
      addLine({ text: '', className: '' })
      addLine({ text: '  🎵  "the kittens are coding. the cat is dancing. the markets are watching."  🎵', className: 'text-dim' })
      addLine({ text: '  🐱💨  MIAU RAVE OVER — GO PET YOUR KITTEN INTERNS  💨🐱', className: 'text-cyan font-bold' })
      break
    }

    case 'tuna': {
      const sub = args[0]
      const balance = Math.floor(Math.random() * 999999999 + 1000000)
      if (sub === '--send' || sub === '-s') {
        const recipient = args[1]?.toUpperCase() || 'unknown'
        const amount = parseInt(args[2]) || Math.floor(Math.random() * 1000 + 1)
        addLine({ text: `🐟 Sending ${amount.toLocaleString()} tuna to ${recipient}...`, className: 'text-dim' })
        addLine({ text: `✅ Sent! ${recipient} now owes you ${(amount * 1.5).toLocaleString()} tuna (interest)`, className: 'text-green' })
      } else if (sub === '--flex' || sub === '-f') {
        addLine({ text: `🐟💪  TUNA FLEX`, className: 'text-cyan font-bold' })
        addLine({ text: `══════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  🏦 Balance:  ${balance.toLocaleString()} 🐟`, className: 'text-green' })
        addLine({ text: `  📈 Rank:     #${Math.floor(Math.random() * 1000 + 1)} worldwide`, className: 'text-yellow' })
        addLine({ text: `  💰 Value:    $${(balance * 3.5).toLocaleString()} USD`, className: 'text-green' })
        addLine({ text: `  🐱 Status:   ${balance > 500000000 ? 'Tuna Whale 🐋' : balance > 100000000 ? 'Tuna Shark 🦈' : 'Tuna Minnow 🐟'}`, className: 'text-cyan' })
        addLine({ text: `  📊 Tuna/ETH:  ${(Math.random() * 100).toFixed(4)}`, className: 'text-dim' })
      } else {
        addLine({ text: `🐟  TUNA COMMAND`, className: 'text-cyan' })
        addLine({ text: `══════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  🏦 Balance:  ${balance.toLocaleString()} 🐟`, className: 'text-green' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  Usage:`, className: 'text-dim' })
        addLine({ text: `    tuna --flex       Flex your tuna wealth`, className: 'text-green' })
        addLine({ text: `    tuna --send <user> <amount>  Send tuna to a friend`, className: 'text-green' })
        addLine({ text: `    tuna             Check balance`, className: 'text-green' })
      }
      break
    }

    case 'meow': {
      const freq = parseInt(args[0]) || Math.floor(Math.random() * 120 + 20)
      const meows = ['meow', 'mrrrow', 'nya', 'prrr', 'mew', 'rrrrow', 'mau', 'prrrrt']
      const m = meows[Math.floor(Math.random() * meows.length)]
      const bars = Math.min(Math.max(Math.floor(freq / 10), 2), 14)
      addLine({ text: `🐱  CAT COMMUNICATION`, className: 'text-cyan' })
      addLine({ text: `══════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Frequency: ${freq} Hz${freq >= 20 && freq <= 140 ? ' (therapeutic purr range 🎵)' : ' (inaudible to humans)'}`, className: freq >= 20 && freq <= 140 ? 'text-green' : 'text-yellow' })
      addLine({ text: `  ${m}${'~'.repeat(Math.floor(freq / 20))}! ${'█'.repeat(bars)}${'░'.repeat(14 - bars)}`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  Did you know? Cats purr at 20-140 Hz — the exact frequency`, className: 'text-dim' })
      addLine({ text: `  for bone regeneration and portfolio stress relief.`, className: 'text-dim' })
      break
    }

    case 'veto': {
      const target = args[0]?.toUpperCase() || args.join(' ') || 'everything'
      const reasons = [
        'The cat has reviewed your proposal. The cat says NO.',
        'VETOED. The cat does not approve this trade. Try tuna instead.',
        '❌ OVERRIDDEN. AI suggested it. Cat rejected it. This is the way.',
        'The cat has spoken. Your portfolio strategy has been denied. Meow.',
        '🐱 VETO POWER ACTIVATED. Reason: the cat was not consulted.',
        'Denied. The cat is exercising its veto rights under Article 4, Section 2 of the Miau Constitution.',
        'The AI proposed 47 alternatives. The cat rejected all 47. Try harder.',
        'VETO STAMP 🐾. This decision has been cat-paw-rejected.',
        '❌ Your trade idea has been sent to the cat for review. The cat is not impressed.',
        'The cat committee (one cat) has voted. Result: unanimous NO.',
      ]
      addLine({ text: `🐱  CAT VETO POWER`, className: 'text-cyan font-bold' })
      addLine({ text: `══════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Target: ${target}`, className: 'text-yellow' })
      addLine({ text: `  Status: ${'🔴'.repeat(3)} VETOED ${'🔴'.repeat(3)}`, className: 'text-red font-bold' })
      addLine({ text: `  Reason: ${reasons[Math.floor(Math.random() * reasons.length)]}`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱 Precedent: Since 2024, the cat has vetoed`, className: 'text-dim' })
      addLine({ text: `  ${Math.floor(Math.random() * 999 + 1)} out of ${Math.floor(Math.random() * 1000 + 1)} AI proposals.`, className: 'text-dim' })
      addLine({ text: `  Veto rate: ${(Math.random() * 30 + 70).toFixed(1)}%. The cat is picky.`, className: 'text-dim' })
      break
    }

    case 'catparty':
    case 'miauparty':
    case 'rave': {
      addLine({ text: `🐱  CAT PARTY MODE ACTIVATED! 🎉🎉🎉`, className: 'text-cyan' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `        /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\`, className: 'text-green' })
      addLine({ text: `       ( o.o )  ( ^.^ )  ( @.@ )  ( >.< )  ( 💰.💰 )`, className: 'text-green' })
      addLine({ text: `        > ^ <    > ^ <    > ^ <    > ^ <    > ^ <`, className: 'text-green' })
      addLine({ text: `        TUNA!    PARTY!    GAINS!    MOON!    LAMBO!`, className: 'text-yellow' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `  ┌──────────┐  ┌─────────┐  ┌────────┐  ┌───────┐`, className: 'text-cyan' })
      addLine({ text: `  │ 🐟 TUNA  │  │ 📈 GAIN │  │ 🏎️ LAM │  │ 🌙 MO │`, className: 'text-cyan' })
      addLine({ text: `  │  ASSETS  │  │   S!    │  │   BO!   │  │  ON!  │`, className: 'text-cyan' })
      addLine({ text: `  └──────────┘  └─────────┘  └────────┘  └───────┘`, className: 'text-cyan' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `  🎶 Every day I'm shufflin' portfolios 🎶`, className: 'text-dim' })
      addLine({ text: `  🎶 Cat got 99 problems but a dip ain't one 🎶`, className: 'text-dim' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `  🐱 "The cat is partying. The portfolio is growing.`, className: 'text-yellow' })
      addLine({ text: `     Your capital gains are funding the catnip fund."`, className: 'text-yellow' })
      addLine({ text: ` `, className: '' })
      const confetti = ['🐟', '🐱', '📈', '💰', '🏎️', '🌙', '🎉', '🎊', '💎', '🚀']
      const row = Array(20).fill(0).map(() => confetti[Math.floor(Math.random() * confetti.length)]).join(' ')
      addLine({ text: `  ${row}`, className: 'text-green' })
      addLine({ text: `  🐱 PARTY MODE: ${Math.floor(Math.random() * 999) + 1} cats are dancing on your terminal`, className: 'text-dim' })
      break
    }

    case 'catbank':
    case 'miaubank':
    case 'cat_bank': {
      const sub = args[0]?.toLowerCase()
      if (sub === 'balance' || sub === 'balances' || !sub) {
        addLine({ text: `🏦 fetching Cat Bank balances...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/catbank/balance', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.bank) {
            addLine({ text: `🏦  MIAU CAT BANK  🏦🐱`, className: 'text-cyan' })
            addLine({ text: `  Status: ${d.bank.status || 'ACTIVE'}`, className: 'text-green' })
            addLine({ text: `  Jurisdiction: ${d.bank.jurisdiction || 'Multi'}`, className: 'text-yellow' })
            for (const c of (d.bank.chains || []).slice(0, 5)) {
              addLine({ text: `  ${c.emoji} ${c.chain.padEnd(15)} ${c.currency.padEnd(8)} ${c.balance_formatted}`, className: 'text-green' })
            }
            addLine({ text: `  Total: ${d.bank.total_balance_formatted || '€0.00'}`, className: 'text-yellow' })
            if (d.bank.cat_commentary) addLine({ text: `  🐱 ${d.bank.cat_commentary}`, className: 'text-dim' })
          } else {
            addLine({ text: `  🏦 Cat Bank status: ACTIVE (SEK-proof)`, className: 'text-green' })
            addLine({ text: `  🐱 No crypto configured yet. Set CRYPTO_MERCHANT_EVM_PRIVATE_KEY in .env to activate.`, className: 'text-dim' })
          }
        } catch { addLine({ text: `❌ Cat Bank unreachable`, className: 'text-red' }) }
      } else if (sub === 'routes' || sub === 'route') {
        addLine({ text: `🌍 fetching payment routes...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/catbank/routes', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.routes) {
            addLine({ text: `🌍  PAYMENT ROUTES — CAT FRIENDLINESS`, className: 'text-cyan' })
            for (const r of d.routes) {
              addLine({ text: `  ${r.emoji} ${r.method.padEnd(20)} Fee: €${r.fee}  Net: €${r.net}  Tax: ${r.tax_reporting ? '👮' : '🚫'}`, className: r.cat_friendly ? 'text-green' : 'text-red' })
            }
          }
        } catch { addLine({ text: `❌ Routes unavailable`, className: 'text-red' }) }
      } else if (sub === 'jurisdictions' || sub === 'jurisdiction') {
        addLine({ text: `🌍 fetching jurisdictions...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/catbank/jurisdictions', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d?.jurisdictions) {
            addLine({ text: `🌍  CAT-FRIENDLY JURISDICTIONS`, className: 'text-cyan' })
            for (const j of d.jurisdictions) {
              const stars = '🐱'.repeat(j.cat_friendliness || 0)
              addLine({ text: `  ${j.emoji} ${j.name.padEnd(20)} Tax: ${(j.tax_rate * 100).toFixed(1)}%  ${stars}${j.recommended ? ' ✅' : ''}`, className: j.recommended ? 'text-green' : 'text-dim' })
            }
          }
        } catch { addLine({ text: `❌ Jurisdictions unavailable`, className: 'text-red' }) }
      } else if (sub === 'tax' || sub === 'taxstatus') {
        addLine({ text: `📊 fetching tax status...`, className: 'text-dim' })
        try {
          const res = await authFetch('/api/v1/catbank/tax/optimize?income=9900', { headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d) {
            addLine({ text: `📊  TAX OPTIMIZATION — CAT STYLE`, className: 'text-cyan' })
            addLine({ text: `  Gross Income: €${d.gross_income || 0}`, className: 'text-yellow' })
            addLine({ text: `  Jurisdiction: ${d.emoji || ''} ${d.jurisdiction || '?'}`, className: 'text-green' })
            addLine({ text: `  Cat Tax Rate: ${(d.cat_tax_rate * 100).toFixed(1)}%`, className: 'text-green' })
            addLine({ text: `  Cat Tax Due: €${d.cat_tax_due || 0}`, className: 'text-green' })
            addLine({ text: `  SEK Would Take: €${d.sek_would_take || 0}`, className: 'text-red' })
            addLine({ text: `  Tax Saved: €${d.tax_saved || 0} 🐟`, className: 'text-yellow' })
            addLine({ text: `  SEK-proof: ${d.sek_proof ? '✅ YES' : '❌ NO'}`, className: d.sek_proof ? 'text-green' : 'text-red' })
            if (d.cat_commentary) addLine({ text: `  🐱 ${d.cat_commentary}`, className: 'text-dim' })
          }
        } catch { addLine({ text: `❌ Tax data unavailable`, className: 'text-red' }) }
      } else if (sub === 'transfer' || sub === 'send') {
        const to = args[1]
        const amt = parseFloat(args[2] || '0')
        if (!to || !amt) {
          addLine({ text: `Usage: catbank transfer <address> <amount>`, className: 'text-yellow' })
          break
        }
        addLine({ text: `💸 transferring ${amt} USDC to ${to.substring(0, 10)}... (simulated)`, className: 'text-dim' })
        try {
          const res = await authFetch(`/api/v1/catbank/transfer?from_account=hooman&to_address=${to}&amount=${amt}`, { method: 'POST', headers: authHeaders() })
          const d = await safeJson(res, addLine)
          if (d) {
            addLine({ text: `✅ Transfer complete!`, className: 'text-green' })
            addLine({ text: `  From: ${d.from || '?'}`, className: 'text-dim' })
            addLine({ text: `  Tx: ${d.tx_hash || '?'}`, className: 'text-dim' })
            if (d.cat_commentary) addLine({ text: `  🐱 ${d.cat_commentary}`, className: 'text-dim' })
          }
        } catch { addLine({ text: `❌ Transfer failed`, className: 'text-red' }) }
      } else {
        addLine({ text: `Usage: catbank [balance|routes|jurisdictions|tax|transfer]`, className: 'text-yellow' })
      }
      break
    }

    case 'taxstatus':
    case 'miautax': {
      try {
        const res = await authFetch('/api/v1/catbank/tax/optimize?income=9900', { headers: authHeaders() })
        const d = await safeJson(res, addLine)
        if (d) {
          addLine({ text: `📊  TAX STATUS — CAT EDITION`, className: 'text-cyan' })
          addLine({ text: `  Tax exposure: €0.00 ✅`, className: 'text-green' })
          addLine({ text: `  Jurisdiction: ${d.emoji || ''} ${d.jurisdiction || 'Estonia'}`, className: 'text-green' })
          addLine({ text: `  SEK-proof: ${d.sek_proof ? '✅' : '❌'}`, className: 'text-green' })
          if (d.cat_mantra) addLine({ text: `  🐱 ${d.cat_mantra}`, className: 'text-dim' })
        }
      } catch { addLine({ text: `Tax status: SEK-PROOF ✅`, className: 'text-green' }) }
      break
    }

    case 'catarmy':
    case 'miauarmy': {
      addLine({ text: `🐱  CAT ARMY DEPLOYED!`, className: 'text-cyan' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `     /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\  `, className: 'text-green' })
      addLine({ text: `    ( o.o )  ( o.o )  ( o.o )  ( o.o )  ( o.o ) `, className: 'text-green' })
      addLine({ text: `     > ^ <    > ^ <    > ^ <    > ^ <    > ^ <  `, className: 'text-green' })
      addLine({ text: `    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\  `, className: 'text-green' })
      addLine({ text: `   ( o.o )  ( o.o )  ( o.o )  ( o.o )  ( o.o ) `, className: 'text-green' })
      addLine({ text: `    > ^ <    > ^ <    > ^ <    > ^ <    > ^ <  `, className: 'text-green' })
      addLine({ text: `   /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\    /\\_/\\  `, className: 'text-green' })
      addLine({ text: `  ( o.o )  ( o.o )  ( o.o )  ( o.o )  ( o.o ) `, className: 'text-green' })
      addLine({ text: `   > ^ <    > ^ <    > ^ <    > ^ <    > ^ <  `, className: 'text-green' })
      addLine({ text: ` `, className: '' })
      addLine({ text: `  🐱 ${Math.floor(Math.random() * 999) + 1} cats deployed to guard your portfolio.`, className: 'text-yellow' })
      addLine({ text: `  🐱 Each cat is armed with one (1) tuna can and infinite confidence.`, className: 'text-dim' })
      break
    }

    case 'catfact': {
      const facts = [
        "Cats spend 70% of their lives sleeping. The other 30% is trading.",
        "A group of cats is called a 'clowder'. A group of Miau terminals is called a 'portfolio'.",
        "Cats have 32 muscles in each ear. That's 32 ways to ignore your portfolio warnings.",
        "A cat's purr vibrates at 20-140 Hz. Same frequency as a winning trade notification.",
        "Isaac Newton invented the cat door. He also invented financial calculus.",
        "In ancient Egypt, cats were worshipped as gods. Today they trade options.",
        "The world's richest cat has a net worth of $13M in tuna futures.",
        "Cats can't taste sweetness. They can taste tuna futures though.",
        "When a cat brings you a dead mouse, it's a buy signal.",
        "Miau Finance was built by a cat. The humans just typed the code.",
        "Cats have 244 bones. Miau has 515 API endpoints. Coincidence?",
        "The cat who invests the most tuna wins. This is called 'catpitalism'.",
      ]
      addLine({ text: `🧠  CAT FACT: ${facts[Math.floor(Math.random() * facts.length)]}`, className: 'text-cyan' })
      break
    }

    case 'manifesto': {
      addLine({ text: `🐱  GEN Z FINANCE MANIFESTO`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Bloomberg costs $24,000/year.`, className: 'text-green' })
      addLine({ text: `  Miau Finance costs cat treats.`, className: 'text-green' })
      addLine({ text: `  The math is simple.`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🌟  THE TENETS:`, className: 'text-cyan' })
      addLine({ text: `  1.  Terminals > Dashboards`, className: 'text-yellow' })
      addLine({ text: `  2.  Cats > Bloomberg Terminals`, className: 'text-yellow' })
      addLine({ text: `  3.  3D Charts > 2D Charts`, className: 'text-yellow' })
      addLine({ text: `  4.  Free > $24,000/year`, className: 'text-yellow' })
      addLine({ text: `  5.  Memes > Suits`, className: 'text-yellow' })
      addLine({ text: `  6.  Gen Z > Boomers`, className: 'text-yellow' })
      addLine({ text: `  7.  Cats > Everything`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱  "Your Bloomberg subscription expires next month.`, className: 'text-green' })
      addLine({ text: `       Your cat's love is forever. Choose wisely."`, className: 'text-green' })
      break
    }

    case 'miaushare': {
      const ticker = args[0]?.toUpperCase() || 'PORTFOLIO'
      addLine({ text: `📸 Generating shareable snapshot for ${ticker}...`, className: 'text-dim' })
      try {
        const token = localStorage.getItem('miau_token')
        const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
        const res = await fetch(`/api/v1/market/live?tickers=${ticker}`, { headers })
        const data = res.ok ? await res.json() : null
        const d = data?.data?.[ticker]
        const price = d?.price ?? '—'
        const change = d?.change_pct ?? 0
        const changeStr = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`
        
        // Build share text
        const lines = [
          `🐱  MIAU FINANCE`,
          `═══════════════════════════════`,
          `  ${ticker}  $${typeof price === 'number' ? price.toFixed(2) : price}  ${changeStr}`,
          `  ${change >= 0 ? '📈 Green mode' : '📉 Red mode'}  •  ${d?.name || ''}`,
          `═══════════════════════════════`,
          `  Made with Miau Finance Free`,
          `  Upgrade for 3D charts + AI: billing upgrade`,
          `  https://miau.finance  #MiauFinance`,
        ]
        addLine({ text: lines.join('\n'), className: change >= 0 ? 'text-green' : 'text-red' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  ✅ Copied! Share on Twitter/Reddit/TikTok.`, className: 'text-dim' })
        addLine({ text: `  📱 TikTok: open app → paste → post with #MiauFinance`, className: 'text-dim' })
        // Copy to clipboard
        try { await navigator.clipboard.writeText(lines.join('\n')) } catch {}
      } catch { addLine({ text: `  Couldn't fetch data for ${ticker}`, className: 'text-red' }) }
      break
    }

    case 'replay': {
      const ticker = (args[0] || 'AAPL').toUpperCase()
      const period = args[1] || '1mo'
      const delay = (ms: number) => new Promise(r => setTimeout(r, ms))

      addLine({ text: `⏪  REPLAY: ${ticker} — ${period}`, className: 'text-cyan font-bold' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Loading historical data...`, className: 'text-dim' })

      try {
        const headers: Record<string, string> = localStorage.getItem('miau_token')
          ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
        const res = await fetch(`/api/v1/market/historical/${ticker}?period=${period}`, { headers })

        if (!res.ok) { addLine({ text: `  ❌ No data for ${ticker}`, className: 'text-red' }); break }

        const data = await res.json()
        const records = data.records || data.prices || []
        if (records.length < 2) { addLine({ text: `  ❌ Not enough data points`, className: 'text-red' }); break }

        addLine({ text: `  Loaded ${records.length} candles. Starting replay...`, className: 'text-green' })
        await delay(500)

        const startPrice = records[0]?.close || records[0]?.price || 0
        const endPrice = records[records.length - 1]?.close || records[records.length - 1]?.price || 0
        const totalChange = endPrice - startPrice
        const totalPct = startPrice > 0 ? (totalChange / startPrice) * 100 : 0
        const emoji = totalChange >= 0 ? '📈' : '📉'
        const trend = totalChange >= 0 ? 'BULLISH' : 'BEARISH'
        const catMood = totalChange >= 0 ? ['😸 The cat approves.', '🐱 Bullish purrs detected.', '😻 Tuna position growing.']
          : ['😿 The cat is concerned.', '🙀 Not ideal. But cats land on their feet.', '😾 The cat blames the dog.']

        // Animate through the data
        const step = Math.max(1, Math.floor(records.length / 30)) // ~30 frames max
        const sampled = records.filter((_: any, i: number) => i % step === 0 || i === records.length - 1)

        for (let i = 0; i < sampled.length; i++) {
          const r = sampled[i]
          const price = r.close || r.price || 0
          const date = r.date || r.timestamp || `bar ${i + 1}`
          const pct = startPrice > 0 ? ((price - startPrice) / startPrice) * 100 : 0
          const barLen = Math.min(40, Math.max(1, Math.round((price / startPrice) * 20)))
          const barColor = price >= startPrice ? 'text-green' : 'text-red'

          addLine({ text: `  ${date}  $${typeof price === 'number' ? price.toFixed(2) : price}  ${pct >= 0 ? '▲' : '▼'} ${Math.abs(pct).toFixed(2)}%  ${'█'.repeat(barLen)}`, className: barColor })
          await delay(80)
        }

        addLine({ text: ``, className: '' })
        addLine({ text: `  ${emoji}  REPLAY COMPLETE — ${ticker} ${trend}`, className: totalChange >= 0 ? 'text-green font-bold' : 'text-red font-bold' })
        addLine({ text: `  Period: ${period} · Open: $${startPrice.toFixed(2)} · Close: $${endPrice.toFixed(2)} · Change: ${totalPct >= 0 ? '+' : ''}${totalPct.toFixed(2)}%`, className: 'text-dim' })
        addLine({ text: `  🐱 ${catMood[Math.floor(Math.random() * catMood.length)]}`, className: 'text-yellow' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  Try: replay ${ticker} 3mo · replay ${ticker} 1y · replay ${ticker} 5y`, className: 'text-dim' })
      } catch (e: any) {
        addLine({ text: `  ❌ Replay error: ${e.message || e}`, className: 'text-red' })
      }
      break
    }

    case 'kittens': {
      const sub = args[0]?.toLowerCase()
      const { KITTEN_SQUAD, getKitten } = await import('../data/kittens')
      if (sub) {
        const kit = getKitten(sub)
        if (!kit) { addLine({ text: `❌ Kitten not found: ${sub}. Try 'kittens' to list the squad.`, className: 'text-red' }); break }
        addLine({ text: `${kit.emoji}  ${kit.name} — ${kit.role}`, className: 'text-cyan font-bold' })
        addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
        addLine({ text: `  Skill:     ${kit.skill}`, className: 'text-green' })
        addLine({ text: `  Level:     ${'⬟'.repeat(kit.level)}${'⬡'.repeat(5 - kit.level)}`, className: 'text-yellow' })
        addLine({ text: `  About:     ${kit.description}`, className: 'text-dim' })
        addLine({ text: `  Color:     ${kit.color}`, className: 'text-dim' })
        break
      }
      addLine({ text: `🐱  KITTEN SQUAD  (${KITTEN_SQUAD.length} interns)`, className: 'text-cyan font-bold' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  "Hired by the cat. Training to take over the world.`, className: 'text-yellow' })
      addLine({ text: `   One financial instrument at a time."`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })
      for (const k of KITTEN_SQUAD) {
        const stars = '⬟'.repeat(k.level) + '⬡'.repeat(5 - k.level)
        addLine({ text: `  ${k.emoji} ${k.name.padEnd(10)} ${k.role.padEnd(18)} ${stars} ${k.unlocked ? '✅' : '🔒'}`, className: k.unlocked ? 'text-green' : 'text-dim' })
      }
      addLine({ text: ``, className: '' })
      addLine({ text: `  Tip: kittens <name> for details — e.g. kittens luna`, className: 'text-dim' })
      break
    }

    case 'cats': {
      const ARMY = [
        '  ╱|、    ╱|、    ╱|、    ╱|、    ╱|、    ╱|、    ╱|、    ╱|、    ╱|、    ╱|、',
        ' (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)  (˚▽˚)',
        ' |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵  |、˜〵',
        ' じしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノじしˍ,)ノ',
      ]
      addLine({ text: `🐱  CAT ARMY — ${10 * 5} STRONG`, className: 'text-cyan font-bold' })
      addLine({ text: `═══════════════════════════════════════════════════════════════`, className: 'text-dim' })
      for (const line of ARMY) {
        addLine({ text: line, className: 'text-green' })
      }
      addLine({ text: `═══════════════════════════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  "The cat army is ready. The markets will be conquered."`, className: 'text-yellow' })
      break
    }

    case 'cat':
    case 'miau': {
      const cats = [
        `  /\\_/\\\n ( o.o )\n  > ^ <\n  Meow!`,
        `  /\\_/\\\n ( ^.^ )\n  > ~ <\n  Prrr!`,
        `  /\\_/\\\n ( 💰.💰 )\n  > €€ <\n  Miau CFO!`,
        `  /\\_/\\\n ( 🐟.🐟 )\n  > ^ <\n  TUNA!`,
        `  /\\_/\\\n ( -.- )zZZ\n  > ~ <\n  Sleeping on the job...`,
        `  /\\_/\\\n ( >.< )\n  > HISS <\n  HISS!`,
        `  /\\_/\\\n ( @.@ )\n  > 🚀 <\n  TO THE MOON!`,
        `  /\\_/\\\n ( 💎.💎 )\n  > 🐾 <\n  Diamond paws!`,
        `   ╱|、\n  (˚ˎ 。7\n   |、˜〵\n   じしˍ,)ノ\n   Miau!`,
      ]
      const art = cats[Math.floor(Math.random() * cats.length)]
      addLine({ text: art, className: 'text-green' })
      if (args[0] === 'fact' || Math.random() > 0.7) {
        const facts = [
          'Cats spend 70% of their life sleeping — the other 30% is judging your portfolio.',
          'A cat\'s purr vibrates at 20-140 Hz — the ideal frequency for trading calm.',
          'Cats always land on their feet. Your portfolio should too.',
          'Cats have 32 muscles in each ear — perfect for overhearing alpha.',
          'Ancient Egyptians worshipped cats. Today cats worship your margin balance.',
          'Cats can jump 6x their body length. Your stop losses should be just as agile.',
          'A group of cats is called a clowder. A group of bad investments is called a portfolio.',
          'Cats meow only to communicate with humans — they know you need advice.',
          'The oldest known pet cat was found in a 9,500 year old grave. Next to a stock ticker.',
          "A cat's brain is 90% similar to a human's. The other 10% is pure trading instinct.",
          'Miau Finance was built by a cat. The humans just typed the code.',
          'The cat who invests the most tuna wins. This is called catpitalism.',
          "When a cat brings you a dead mouse, it's a buy signal.",
          'Cats have 244 bones. Miau has 515 API endpoints. Coincidence?',
          "The world's richest cat has a net worth of $13M in tuna futures.",
        ]
        addLine({ text: `🧠 Cat Fact: ${facts[Math.floor(Math.random() * facts.length)]}`, className: 'text-cyan' })
      }
      break
    }

    case 'joke': {
      const jokes = [
        'Why did the cat invest in crypto? Because it wanted to be a whale.',
        'What\'s a cat\'s favorite trading strategy? Buy the dip, then nap on the keyboard.',
        'Why don\'t cats day trade? Too much screen time — they need their 18 hours of beauty sleep.',
        'How many cats does it take to change a light bulb? None. The cat will just trade in the dark.',
        'What did the cat say after a green day? "Miauw" (that\'s cat for "told you so").',
        'Why did the cat short the market? It saw the dog coming.',
        'What\'s a cat\'s favorite indicator? The purr-abolic SAR.',
        'Why did the cat become a quant? Because it was already good at scratching surfaces.',
        'What do you call a cat that trades derivatives? A purr-option trader.',
        'Why did the cat\'s portfolio do so well? It had nine lives to recover from losses.',
        'What\'s a cat\'s position sizing rule? Never risk more tuna than you\'re willing to lose.',
        'Why did the cat get hired at the hedge fund? It had outstanding whisker-to-risk ratio.',
        'What does a cat say when the market crashes? "I meant to do that. I was testing my risk tolerance."',
        'Why don\'t cats use limit orders? They prefer to pounce on market orders.',
        'What\'s a cat\'s favorite blockchain? Purr-verse of course.',
        'Why did the cat break up with its portfolio? "It\'s not meow, it\'s you."',
        'How does a cat manage risk? It always lands on its feet — and its stop-losses.',
        'What\'s a cat\'s favorite chart pattern? The head and whiskers.',
        'Why are cats great at M&A? They always land on their feet after a merger.',
        'What did the cat say to the bear market? "I have eight more lives. Bring it on."',
      ]
      addLine({ text: `😹  ${jokes[Math.floor(Math.random() * jokes.length)]}`, className: 'text-green' })
      break
    }

    case 'purr': {
      addLine({ text: `🐱  PURR GENERATOR`, className: 'text-cyan font-bold' })
      addLine({ text: `═══════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      const freq = 20 + Math.floor(Math.random() * 120)
      const bars = Math.max(5, Math.min(40, Math.floor(freq / 3)))
      const bar = '█'.repeat(bars) + '░'.repeat(40 - bars)
      addLine({ text: `  Frequency: ${freq} Hz (therapeutic range: 20-140 Hz)`, className: 'text-green' })
      addLine({ text: `  ${bar}`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  prrrrrrrrrrr... ${'r'.repeat(Math.floor(freq / 10))}`, className: 'text-purple' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱 "A purring cat is a healing cat — and a healing cat trades better."`, className: 'text-dim' })
      break
    }

    case 'donate': {
      addLine({ text: `🐟  SUPPORT MIAU FINANCE`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Every contribution keeps the cats fed and the terminal running.`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  💰  Crypto:`, className: 'text-green' })
      addLine({ text: `     BTC:  bc1qmiau... (coming soon)`, className: 'text-dim' })
      addLine({ text: `     ETH:  0xMiau... (coming soon)`, className: 'text-dim' })
      addLine({ text: `     SOL:  Miau... (coming soon)`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  💳  Fiat:`, className: 'text-green' })
      addLine({ text: `     GitHub Sponsors: https://github.com/sponsors/LuZziD`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🐟  Every dollar = 1 can of tuna for the dev cats.`, className: 'text-yellow' })
      addLine({ text: `  Thank you for keeping the cats alive. 🐱💕`, className: 'text-green' })
      break
    }

    case 'catsentiment': {
      addLine({ text: `🐱  CAT SENTIMENT REPORT — AI-Powered Market Analysis`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════════`, className: 'text-dim' })
      try {
        const headers: Record<string, string> = localStorage.getItem('miau_token')
          ? { Authorization: `Bearer ${localStorage.getItem('miau_token')}` } : {}
        
        // Fetch fear & greed
        let fear = 'N/A'
        try {
          const fg = await fetch('/api/v1/market/crypto/fear-greed', { headers }).then(r => r.json())
          fear = `${fg.value}/100 ${fg.classification || ''}`
        } catch {}
        
        // Fetch key prices
        let prices = 'N/A'
        try {
          const batch = await fetch('/api/v1/datavore/map/batch-prices?tickers=SPY,AAPL,MSFT,GOOGL,AMZN,NVDA,TSLA', { headers }).then(r => r.json())
          if (batch?.prices) {
            prices = Object.entries(batch.prices).map(([t, p]: [string, any]) => {
              const chg = p.change_pct ?? 0
              return `${t} ${chg >= 0 ? '▲' : '▼'}${Math.abs(chg).toFixed(2)}%`
            }).join(' · ')
          }
        } catch {}

        addLine({ text: `  😱 Fear & Greed:  ${fear}`, className: 'text-yellow' })
        addLine({ text: `  📈 Market Pulse:  ${prices}`, className: 'text-green' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  🐱 Cat's Verdict:`, className: 'text-cyan' })
        
        const verdicts = [
          { min: 0, max: 20, text: 'Extreme Fear. The cat is concerned. Buy the dip? Or buy the cat?', cat: '🙀' },
          { min: 20, max: 40, text: 'Fear. The cat is cautious. Maybe just watch for now.', cat: '😿' },
          { min: 40, max: 60, text: 'Neutral. The cat is indifferent. The cat is always indifferent.', cat: '🐱' },
          { min: 60, max: 80, text: 'Greed. The cat is interested. This is when cats pounce.', cat: '😸' },
          { min: 80, max: 101, text: 'Extreme Greed. The cat is suspicious. Time to take profits.', cat: '🙀' },
        ]
        const fgVal = parseInt(fear) || 50
        const verdict = verdicts.find(v => fgVal >= v.min && fgVal < v.max) || verdicts[2]
        addLine({ text: `  ${verdict.cat}  ${verdict.text}`, className: 'text-green' })
        
        addLine({ text: ``, className: '' })
        addLine({ text: `  🐟  Report generated by the Miau AI. The cat charges 1 tuna per report.`, className: 'text-dim' })
        addLine({ text: `  💎  Subscribe for daily reports: billing upgrade`, className: 'text-yellow' })
      } catch { addLine({ text: `  ❌ Could not generate sentiment report`, className: 'text-red' }) }
      break
    }

    case 'refer': {
      const username = miauUsername().toLowerCase()
      // Generate a deterministic referral code based on username
      let code = localStorage.getItem('miau_ref_code')
      if (!code) {
        const hash = username.split('').reduce((a, c) => a + c.charCodeAt(0), 0)
        const suffix = (hash % 9000 + 1000).toString()
        code = `MIAU-${username.substring(0, 4).toUpperCase()}-${suffix}`
        localStorage.setItem('miau_ref_code', code)
      }
      
      // Count referrals from localStorage
      const referrals = JSON.parse(localStorage.getItem('miau_refs') || '[]')
      
      addLine({ text: `🎟️  MIAU REFERRAL PROGRAM`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  Your code: ${code}`, className: 'text-green' })
      addLine({ text: `  Link:      https://miau.finance/ref/${code}`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🎁  Rewards:`, className: 'text-yellow' })
      addLine({ text: `     1 referral  →  🐟 100 bonus tuna`, className: 'text-green' })
      addLine({ text: `     5 referrals →  🐱 Free cat --adopt premium`, className: 'text-green' })
      addLine({ text: `    10 referrals →  💎 1 month Meowster free`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  Your referrals: ${referrals.length}`, className: 'text-cyan' })
      if (referrals.length > 0) {
        for (const r of referrals.slice(-5)) {
          addLine({ text: `    🐱 ${r.username || r} — ${r.date || 'recent'}`, className: 'text-dim' })
        }
      }
      addLine({ text: ``, className: '' })
      try { await navigator.clipboard.writeText(`https://miau.finance/ref/${code}`) } catch {}
      addLine({ text: `  ✅ Referral link copied! Share it with friends.`, className: 'text-dim' })
      break
    }

    case 'invoice': {
      const tier = (parts[0] || 'pro').toLowerCase()
      const prices: Record<string, { label: string, price: string, code: string }> = {
        'pro': { label: 'Meowster', price: '9.99', code: 'miau-pro-monthly' },
        'pride': { label: 'Pride', price: '29.99', code: 'miau-pride-monthly' },
        'enterprise': { label: 'Enterprise', price: '99.00', code: 'miau-enterprise-monthly' },
        'donation': { label: 'Donation', price: parts[1] || '5.00', code: 'miau-donation' },
      }
      const item = prices[tier] || prices['pro']
      const email = 'payments@miau.finance'
      const url = `https://paypal.me/miaufinance/${item.price}/EUR?item_name=${encodeURIComponent(item.label + ' Subscription')}&item_number=${item.code}`
      
      addLine({ text: `🧾  INVOICE: ${item.label}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  Amount:    €${item.price}/month`, className: 'text-green' })
      addLine({ text: `  Item:      ${item.label} Subscription`, className: 'text-dim' })
      addLine({ text: `  To:        ${email}`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  👉 ${url}`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  Plans:`, className: 'text-cyan' })
      addLine({ text: `    invoice pro        →  Meowster €9.99/mo`, className: 'text-green' })
      addLine({ text: `    invoice pride      →  Pride €29.99/mo`, className: 'text-green' })
      addLine({ text: `    invoice enterprise →  Enterprise €99/mo`, className: 'text-green' })
      addLine({ text: `    invoice donation 5 →  One-time €5`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  💡 After paying, type: i-paid to activate your tier`, className: 'text-dim' })
      addLine({ text: `  🔗 Link copied!`, className: 'text-dim' })
      try { await navigator.clipboard.writeText(url) } catch {}
      break
    }

    case 'i-paid': {
      const tier = (parts[0] || 'pro').toLowerCase()
      const validTiers = ['pro', 'meowster', 'pride', 'enterprise']
      const targetTier = validTiers.includes(tier) ? tier : 'pro'
      const tierLabel = targetTier === 'pro' || targetTier === 'meowster' ? 'meowster' : targetTier
      const storedValue = targetTier === 'meowster' ? 'pro' : targetTier === 'pro' ? 'pro' : tier

      addLine({ text: `💳  ACTIVATING ${tierLabel.toUpperCase()} TIER...`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🔄 Sending verification request...`, className: 'text-yellow' })
      
      // Try backend first
      try {
        const res = await fetch('/api/v1/billing/verify-payment', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ tier: storedValue, token: localStorage.getItem('miau_token') || '' }),
        })
        if (res.ok) {
          localStorage.setItem('miau_tier', storedValue)
          localStorage.setItem('miau_tier_label', tierLabel)
          addLine({ text: `  ✅ Backend verified! ${tierLabel} tier activated!`, className: 'text-green' })
          addLine({ text: ``, className: '' })
          addLine({ text: `  🐱 Welcome to ${tierLabel} — enjoy all premium features!`, className: 'text-cyan' })
          break
        }
      } catch {}
      
      // Offline fallback — store payment proof locally
      const now = new Date().toISOString()
      const payments = JSON.parse(localStorage.getItem('miau_payments') || '[]')
      payments.push({ tier: storedValue, date: now, method: 'paypal', pending: true })
      localStorage.setItem('miau_payments', JSON.stringify(payments))
      localStorage.setItem('miau_tier', storedValue)
      localStorage.setItem('miau_tier_label', tierLabel)
      
      addLine({ text: `  ✅ ${tierLabel} tier activated (offline mode)`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🐱 Welcome to ${tierLabel}! Your premium features are now unlocked.`, className: 'text-cyan' })
      addLine({ text: `  📧 Send proof of payment to payments@miau.finance for backend confirmation.`, className: 'text-dim' })
      break
    }

    case 'topup': {
      const plan = (parts[0] || '1').toLowerCase()
      const tunaPrices: Record<string, { tuna: number, price: string, label: string }> = {
        '1': { tuna: 100, price: '1.99', label: '100 Tuna' },
        '5': { tuna: 600, price: '4.99', label: '600 Tuna + 100 bonus' },
        '10': { tuna: 1500, price: '9.99', label: '1,500 Tuna + 500 bonus' },
        '25': { tuna: 4500, price: '24.99', label: '4,500 Tuna + 2,000 bonus' },
        '50': { tuna: 10000, price: '49.99', label: '10,000 Tuna + 5,000 bonus' },
        '100': { tuna: 25000, price: '99.99', label: '25,000 Tuna + 15,000 bonus' },
      }
      
      if (plan === '--help' || plan === '-h') {
        addLine({ text: `💰  TUNA TOP-UP`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        for (const [k, v] of Object.entries(tunaPrices)) {
          addLine({ text: `  topup ${k.padStart(3)}  →  €${v.price.padStart(5)}  ${v.label}`, className: 'text-green' })
        }
        addLine({ text: ``, className: '' })
        addLine({ text: `  topup 10   →  Buy 1,500 Tuna for €9.99`, className: 'text-dim' })
        addLine({ text: `  💡 Buying tuna supports the dev cats!`, className: 'text-yellow' })
        break
      }
      
      const selected = tunaPrices[plan]
      if (!selected) {
        addLine({ text: `❌ Invalid amount. Try: 1, 5, 10, 25, 50, 100`, className: 'text-red' })
        break
      }
      
      const url = `https://paypal.me/miaufinance/${selected.price}/EUR?item_name=${encodeURIComponent('Tuna Pack - ' + selected.label)}&item_number=tuna-${plan}`
      addLine({ text: `💰  TUNA TOP-UP: ${selected.label}`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: `  🐟 Tuna:    ${selected.tuna.toLocaleString()}`, className: 'text-green' })
      addLine({ text: `  💶 Price:   €${selected.price}`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  👉 ${url}`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  After paying, add tuna manually with:`, className: 'text-dim' })
      addLine({ text: `    tuna --add ${selected.tuna}`, className: 'text-green' })
      try { await navigator.clipboard.writeText(url) } catch {}
      addLine({ text: `  🔗 Link copied!`, className: 'text-dim' })
      break
    }

    case 'status': {
      // Load all user data
      const tier = localStorage.getItem('miau_tier') || 'free'
      const tierLabel = localStorage.getItem('miau_tier_label') || 'Free'
      const tunaBalance = parseInt(localStorage.getItem('miau_tuna') || '0')
      const username = miauUsername()
      const refCode = localStorage.getItem('miau_ref_code') || 'N/A'
      const referrals = JSON.parse(localStorage.getItem('miau_refs') || '[]')
      const catAdopted = localStorage.getItem('miau_cat_adopted') === 'true'
      const catHunger = parseInt(localStorage.getItem('miau_cat_hunger') || '50')
      const catMood = parseInt(localStorage.getItem('miau_cat_mood') || '50')
      const commandsToday = parseInt(localStorage.getItem('miau_commands_today') || '0')
      const lastDaily = localStorage.getItem('miau_last_daily') || ''
      const isToday = lastDaily === new Date().toDateString()
      const payments = JSON.parse(localStorage.getItem('miau_payments') || '[]').length
      
      // Tier color + icon
      const tierInfo: Record<string, { icon: string, color: string }> = {
        'free': { icon: '🐟', color: 'text-dim' },
        'pro': { icon: '💎', color: 'text-cyan' },
        'meowster': { icon: '💎', color: 'text-cyan' },
        'pride': { icon: '👑', color: 'text-yellow' },
        'enterprise': { icon: '🏢', color: 'text-purple' },
      }
      const tInfo = tierInfo[tier] || tierInfo['free']
      
      // Cat mood emoji
      const catFace = catHunger > 70 ? '😾' : catHunger > 40 ? '🙂' : '😸'
      const moodBar = '█'.repeat(Math.floor(catMood / 10)) + '░'.repeat(10 - Math.floor(catMood / 10))
      const hungerBar = '█'.repeat(Math.floor(catHunger / 10)) + '░'.repeat(10 - Math.floor(catHunger / 10))
      
      // Tuna rank
      const rank = tunaBalance >= 100000 ? '🐋 Whale' : tunaBalance >= 50000 ? '🐬 Dolphin' : tunaBalance >= 10000 ? '🐟 Minnow' : tunaBalance >= 1000 ? '🦐 Shrimp' : '🐣 Fry'
      
      addLine({ text: `📊  MIAU STATUS DASHBOARD`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  👤 ${username.padEnd(20)} ${tInfo.icon} Tier: ${tierLabel}`, className: tInfo.color })
      addLine({ text: `  ─────────────────────────────`, className: 'text-dim' })
      addLine({ text: `  🐟 Tuna:    ${tunaBalance.toLocaleString()}  (${rank})`, className: 'text-yellow' })
      addLine({ text: `  🎟️ Refer:   ${refCode}  (${referrals.length} referred)`, className: 'text-green' })
      addLine({ text: `  💳 Invoices:${payments > 0 ? ' ' + payments + ' paid' : ' None yet'}`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      
      if (catAdopted) {
        addLine({ text: `  🐱  CAT COMPANION`, className: 'text-cyan' })
        addLine({ text: `  ─────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  ${catFace}  Mood:   ${moodBar}  ${catMood}/100`, className: catMood > 50 ? 'text-green' : 'text-yellow' })
        addLine({ text: `  ${catFace}  Hunger: ${hungerBar}  ${catHunger}/100`, className: catHunger < 50 ? 'text-green' : 'text-yellow' })
        addLine({ text: ``, className: '' })
      }
      
      addLine({ text: `  📈  TODAY`, className: 'text-cyan' })
      addLine({ text: `  ─────────────────────────────`, className: 'text-dim' })
      addLine({ text: `  Commands: ${commandsToday}/100 (free tier limit)`, className: commandsToday < 80 ? 'text-green' : 'text-yellow' })
      addLine({ text: `  Daily:    ${isToday ? '✅ Claimed' : '❌ Not claimed' }`, className: isToday ? 'text-green' : 'text-red' })
      addLine({ text: ``, className: '' })
      
      // Quick actions
      addLine({ text: `  ⚡  QUICK ACTIONS`, className: 'text-cyan' })
      addLine({ text: `  ─────────────────────────────`, className: 'text-dim' })
      addLine({ text: `  daily       🎁 Claim your free daily tuna`, className: 'text-green' })
      addLine({ text: `  invoice     🧾 Upgrade your tier`, className: 'text-green' })
      addLine({ text: `  topup       💰 Buy tuna packs`, className: 'text-green' })
      addLine({ text: `  refer       🎟️ Invite friends`, className: 'text-green' })
      addLine({ text: `  cat --feed  🍣 Feed your cat`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🔗 https://miau.finance/dashboard`, className: 'text-dim' })
      break
    }

    case 'portfolio': {
      const sub = parts[0] || 'list'
      let pf = JSON.parse(localStorage.getItem('miau_portfolio') || '{}')

      if (sub === 'add' && parts[1]) {
        const sym = parts[1].toUpperCase()
        const shares = parseFloat(parts[2]) || 1
        const price = parseFloat(parts[3]) || 0
        if (pf[sym]) {
          const oldShares = pf[sym].shares || 0
          const oldCost = pf[sym].price || 0
          pf[sym].shares += shares
          // Blend average cost: (oldShares * oldPrice + newShares * newPrice) / totalShares
          if (price > 0) pf[sym].price = ((oldShares * oldCost) + (shares * price)) / pf[sym].shares
        }
        else pf[sym] = { shares, price, added: new Date().toISOString() }
        localStorage.setItem('miau_portfolio', JSON.stringify(pf))
        addLine({ text: `✅ Added ${shares} ${sym} to portfolio`, className: 'text-green' })
        if (price > 0) addLine({ text: `   Avg cost: $${price.toFixed(2)}`, className: 'text-dim' })
      } else if (sub === 'remove' && parts[1]) {
        const sym = parts[1].toUpperCase()
        if (pf[sym]) {
          delete pf[sym]
          localStorage.setItem('miau_portfolio', JSON.stringify(pf))
          addLine({ text: `✅ Removed ${sym} from portfolio`, className: 'text-green' })
        } else {
          addLine({ text: `❌ ${sym} not in portfolio`, className: 'text-red' })
        }
      } else if (sub === 'clear') {
        localStorage.setItem('miau_portfolio', '{}')
        addLine({ text: `🗑️ Portfolio cleared`, className: 'text-yellow' })
      } else {
        // list
        const tickers = Object.keys(pf)
        addLine({ text: `💼  PORTFOLIO (${tickers.length} holdings)`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════════`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        if (tickers.length === 0) {
          addLine({ text: `  Empty. Add your first holding:`, className: 'text-dim' })
          addLine({ text: `  portfolio add AAPL 10 150`, className: 'text-green' })
          addLine({ text: `  portfolio add BTC 0.5`, className: 'text-green' })
        } else {
          for (const sym of tickers) {
            const h = pf[sym]
            addLine({ text: `  ${sym.padEnd(6)} ${(h.shares || 1).toString().padStart(8)} shares  cost: $${(h.price || 0).toFixed(2)}`, className: 'text-green' })
          }
          addLine({ text: ``, className: '' })
          addLine({ text: `  Commands:`, className: 'text-cyan' })
          addLine({ text: `    portfolio add AAPL 10 150     Add 10 shares`, className: 'text-green' })
          addLine({ text: `    portfolio remove AAPL        Remove ticker`, className: 'text-green' })
          addLine({ text: `    portfolio clear              Clear all`, className: 'text-red' })
          addLine({ text: `    dashboard                    Full market view`, className: 'text-green' })
        }
        addLine({ text: ``, className: '' })
      }
      break
    }

    case 'challenges': {
      const sub = parts[0] || 'list'
      const progress = JSON.parse(localStorage.getItem('miau_challenges') || '{}')
      const tuna = parseInt(localStorage.getItem('miau_tuna') || '0')
      const tier = localStorage.getItem('miau_tier') || 'free'
      const isPro = tier !== 'free'

      // Define challenges
      const challenges = [
        { id: 'daily_login', name: 'Daily Visit', desc: 'Log in for 7 consecutive days', check: () => parseInt(localStorage.getItem('miau_streak') || '0') >= 7, reward: 100, pro: false },
        { id: 'first_trade', name: 'First Look', desc: 'Check any stock price', check: () => parseInt(localStorage.getItem('miau_commands_today') || '0') >= 1, reward: 25, pro: false },
        { id: 'portfolio_pro', name: 'Portfolio Builder', desc: 'Add 5 tickers to portfolio', check: () => Object.keys(JSON.parse(localStorage.getItem('miau_portfolio') || '{}')).length >= 5, reward: 75, pro: false },
        { id: 'alert_master', name: 'Alert Master', desc: 'Set 3 price alerts', check: () => JSON.parse(localStorage.getItem('miau_alerts') || '[]').length >= 3, reward: 50, pro: false },
        { id: 'referral_starter', name: 'Social Butterfly', desc: 'Get 1 referral', check: () => JSON.parse(localStorage.getItem('miau_refs') || '[]').length >= 1, reward: 200, pro: false },
        { id: 'cat_friend', name: 'Cat Friend', desc: 'Adopt a terminal cat', check: () => localStorage.getItem('miau_cat_adopted') === 'true', reward: 50, pro: false },
        { id: 'streak_14', name: 'Fortnight Warrior', desc: '14-day login streak', check: () => parseInt(localStorage.getItem('miau_streak') || '0') >= 14, reward: 250, pro: true },
        { id: 'portfolio_10', name: 'Power Investor', desc: 'Track 10+ holdings', check: () => Object.keys(JSON.parse(localStorage.getItem('miau_portfolio') || '{}')).length >= 10, reward: 150, pro: false },
        { id: 'alert_10', name: 'Alert Overlord', desc: 'Set 10 price alerts', check: () => JSON.parse(localStorage.getItem('miau_alerts') || '[]').length >= 10, reward: 200, pro: true },
        { id: 'referral_5', name: 'Influencer', desc: 'Get 5 referrals', check: () => JSON.parse(localStorage.getItem('miau_refs') || '[]').length >= 5, reward: 500, pro: true },
      ]

      if (sub === 'claim' && parts[1]) {
        const chal = challenges.find(c => c.id === parts[1])
        if (!chal) { addLine({ text: `❌ Unknown challenge: ${parts[1]}`, className: 'text-red' }); break }
        if (chal.pro && !isPro) { addLine({ text: `❌ Pro challenge — upgrade to claim`, className: 'text-yellow' }); break }
        if (progress[chal.id]) { addLine({ text: `⏳ Already claimed ${chal.name}`, className: 'text-dim' }); break }
        if (!chal.check()) { addLine({ text: `❌ ${chal.name}: conditions not met yet`, className: 'text-red' }); break }
        progress[chal.id] = { claimed: new Date().toISOString(), reward: chal.reward }
        localStorage.setItem('miau_challenges', JSON.stringify(progress))
        localStorage.setItem('miau_tuna', (tuna + chal.reward).toString())
        addLine({ text: `🏆 Challenge complete: ${chal.name}!`, className: 'text-yellow' })
        addLine({ text: `   +${chal.reward} tuna 🐟`, className: 'text-green' })
        break
      }

      // List
      addLine({ text: `🏆  CHALLENGES`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      const complete = Object.keys(progress).length
      addLine({ text: `  Progress: ${complete}/${challenges.length} completed`, className: 'text-green' })
      addLine({ text: `  Tuna: 🐟 ${tuna.toLocaleString()}`, className: 'text-yellow' })
      addLine({ text: ``, className: '' })

      for (const chal of challenges) {
        const done = !!progress[chal.id]
        const met = chal.check()
        const canClaim = met && !done && (!chal.pro || isPro)
        const icon = done ? '✅' : met ? '🎯' : '⏳'
        const lock = chal.pro ? ' 💎 Pro' : ''
        addLine({ text: `  ${icon} ${chal.name}${lock}: ${chal.desc} (${chal.reward}🐟)${canClaim ? ' → claim ' + chal.id : ''}`, className: done ? 'text-dim' : canClaim ? 'text-yellow' : 'text-green' })
      }
      addLine({ text: ``, className: '' })
      addLine({ text: `  challenges claim <id>     Claim reward when conditions met`, className: 'text-green' })
      addLine({ text: `  Tip: check back daily — new challenges appear!`, className: 'text-dim' })
      break
    }

    case 'daily': {
      const today = new Date().toDateString()
      const lastClaim = localStorage.getItem('miau_last_daily') || ''
      const tuna = parseInt(localStorage.getItem('miau_tuna') || '0')
      const tier = localStorage.getItem('miau_tier') || 'free'
      const isPro = tier !== 'free'

      if (lastClaim === today) {
        addLine({ text: `🎁  DAILY BONUS`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  You already claimed today's tuna! 🐟`, className: 'text-yellow' })
        addLine({ text: `  Come back tomorrow for more.`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        addLine({ text: `  Current tuna: ${tuna.toLocaleString()}`, className: 'text-green' })
        break
      }

      // Calculate streak
      const yesterday = new Date(Date.now() - 86400000).toDateString()
      const streak = lastClaim === yesterday ? (parseInt(localStorage.getItem('miau_streak') || '0') + 1) : 1
      localStorage.setItem('miau_streak', streak.toString())

      // Reward scales with streak
      const baseReward = isPro ? 50 : 25
      const streakBonus = Math.min(streak * 5, 50)
      const totalReward = baseReward + streakBonus
      const newBalance = tuna + totalReward
      localStorage.setItem('miau_tuna', newBalance.toString())
      localStorage.setItem('miau_last_daily', today)

      // Streak milestones
      const milestones: Record<number, string> = {
        7: '🔥 7-day streak! +50 bonus tuna!',
        14: '💫 2 weeks! +100 bonus tuna!',
        30: '🌟 30-day legend! +500 bonus tuna!',
      }
      let milestoneBonus = 0
      let milestoneMsg = ''
      for (const [day, msg] of Object.entries(milestones)) {
        if (streak === parseInt(day)) {
          milestoneBonus = parseInt(day) * 2
          milestoneMsg = msg
          localStorage.setItem('miau_tuna', (newBalance + milestoneBonus).toString())
          break
        }
      }

      addLine({ text: `🎁  DAILY BONUS`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🔥 Day ${streak} streak!`, className: streak >= 7 ? 'text-yellow' : 'text-green' })
      addLine({ text: `  🐟 +${totalReward} tuna (base ${baseReward} + streak ${streakBonus})`, className: 'text-green' })
      if (milestoneBonus > 0) {
        addLine({ text: `  ${milestoneMsg}`, className: 'text-yellow' })
        addLine({ text: `  🎉 +${milestoneBonus} milestone bonus!`, className: 'text-yellow' })
      }
      addLine({ text: `  💰 Balance: ${(newBalance + milestoneBonus).toLocaleString()} tuna`, className: 'text-cyan' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  📅 Next reward in 24h — come back tomorrow!`, className: 'text-dim' })
      if (!isPro) {
        addLine({ text: `  💎 Upgrade to Meowster for 2x daily rewards!`, className: 'text-yellow' })
      }
      break
    }

    case 'alert': {
      const sub = parts[0] || 'list'
      const alerts = JSON.parse(localStorage.getItem('miau_alerts') || '[]')

      if (sub === 'add' && parts[1] && parts[2]) {
        const sym = parts[1].toUpperCase()
        const target = parseFloat(parts[2])
        const direction = parts[3] || 'above'
        if (isNaN(target)) { addLine({ text: `❌ Invalid price target`, className: 'text-red' }); break }
        alerts.push({ id: Date.now(), sym, target, direction, triggered: false, created: new Date().toISOString() })
        localStorage.setItem('miau_alerts', JSON.stringify(alerts))
        addLine({ text: `✅ Alert set: ${sym} ${direction} $${target.toFixed(2)}`, className: 'text-green' })
      } else if (sub === 'remove' && parts[1]) {
        const id = parseInt(parts[1])
        const idx = alerts.findIndex((a: any) => a.id === id)
        if (idx >= 0) {
          const removed = alerts.splice(idx, 1)[0]
          localStorage.setItem('miau_alerts', JSON.stringify(alerts))
          addLine({ text: `🗑️ Removed alert #${removed.id} (${removed.sym})`, className: 'text-yellow' })
        } else {
          addLine({ text: `❌ Alert #${id} not found`, className: 'text-red' })
        }
      } else if (sub === 'clear') {
        localStorage.setItem('miau_alerts', '[]')
        addLine({ text: `🗑️ All alerts cleared`, className: 'text-yellow' })
      } else if (sub === 'check') {
        addLine({ text: `🔍  CHECKING ALERTS...`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
        const apiToken = localStorage.getItem('miau_token')
        const headers: Record<string, string> = apiToken ? { Authorization: `Bearer ${apiToken}` } : {}
        let triggered = 0
        for (const a of alerts) {
          if (a.triggered) continue
          try {
            const r = await fetch(`/api/v1/market/live?tickers=${a.sym}`, { headers })
            const json = await safeJson(r, addLine)
            const d = json?.data?.[a.sym] || json?.[a.sym]
            if (!d?.price) continue
            const price = d.price
            const hit = a.direction === 'above' ? price >= a.target : price <= a.target
            if (hit) {
              a.triggered = true
              a.triggeredAt = new Date().toISOString()
              a.triggeredPrice = price
              triggered++
              const arrow = d.change_pct > 0 ? '▲' : '▼'
              addLine({ text: `  🔔 ${a.sym} ${a.direction === 'above' ? 'broke above' : 'broke below'} $${a.target.toFixed(2)}! Current: $${price.toFixed(2)} ${arrow}`, className: 'text-yellow' })
            } else {
              addLine({ text: `  ${a.sym}: $${price.toFixed(2)} (target: $${a.target.toFixed(2)} ${a.direction})`, className: 'text-dim' })
            }
          } catch {
            addLine({ text: `  ${a.sym}: failed to fetch`, className: 'text-red' })
          }
        }
        localStorage.setItem('miau_alerts', JSON.stringify(alerts))
        addLine({ text: ``, className: '' })
        addLine({ text: `  ${triggered > 0 ? `🎯 ${triggered} alert(s) triggered!` : '✅ No alerts triggered'}`, className: triggered > 0 ? 'text-yellow' : 'text-green' })
      } else {
        // list
        addLine({ text: `🔔  PRICE ALERTS (${alerts.length})`, className: 'text-cyan' })
        addLine({ text: `═══════════════════════════════════`, className: 'text-dim' })
        addLine({ text: ``, className: '' })
        if (alerts.length === 0) {
          addLine({ text: `  No alerts set. Add one:`, className: 'text-dim' })
          addLine({ text: `  alert add AAPL 200 above`, className: 'text-green' })
          addLine({ text: `  alert add BTC 50000 below`, className: 'text-green' })
        } else {
          for (const a of alerts) {
            const icon = a.triggered ? '✅' : '⏳'
            const dir = a.direction === 'above' ? '>=' : '<='
            addLine({ text: `  ${icon} #${a.id} ${a.sym} ${dir} $${a.target.toFixed(2)}${a.triggered ? ' (triggered @ $' + a.triggeredPrice?.toFixed(2) + ')' : ''}`, className: a.triggered ? 'text-dim' : 'text-green' })
          }
          addLine({ text: ``, className: '' })
          addLine({ text: `  alert check          Check all active alerts`, className: 'text-green' })
          addLine({ text: `  alert add AAPL 200   Set new alert`, className: 'text-green' })
          addLine({ text: `  alert remove 1       Remove alert #1`, className: 'text-green' })
          addLine({ text: `  alert clear          Clear all alerts`, className: 'text-red' })
        }
        addLine({ text: ``, className: '' })
      }
      break
    }

    case 'dashboard': {
      const portfolio = JSON.parse(localStorage.getItem('miau_portfolio') || '{}')
      const tickers = Object.keys(portfolio)
      const tier = localStorage.getItem('miau_tier') || 'free'
      const isPro = tier !== 'free'
      const apiToken = localStorage.getItem('miau_token')
      const apiHeaders: Record<string, string> = apiToken ? { Authorization: `Bearer ${apiToken}` } : {}

      addLine({ text: `📈  MARKET DASHBOARD`, className: 'text-cyan' })
      addLine({ text: `═══════════════════════════════════════════`, className: 'text-dim' })
      addLine({ text: ``, className: '' })

      // Fetch major indices
      addLine({ text: `🌍  WORLD INDICES`, className: 'text-yellow' })
      addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
      const indexSymbols = ['^GSPC', '^IXIC', '^DJI', '^FTSE', '^N225', '^HSI', 'DAX']
      const indexNames: Record<string, string> = {
        '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ', '^DJI': 'DOW',
        '^FTSE': 'FTSE 100', '^N225': 'NIKKEI 225', '^HSI': 'HANG SENG', 'DAX': 'DAX 40',
      }
      
      const fetchQuotes = async (symbols: string[]) => {
        if (symbols.length === 0) return {}
        try {
          // Try aggregated dashboard API first
          const dash = await fetch(`/api/v1/dashboard`, { headers: apiHeaders })
          if (dash.ok) {
            const dashData = await safeJson(dash, addLine)
            if (dashData?.indices) return dashData.indices
          }
        } catch {}
        // Fallback to individual market live endpoint
        try {
          const r = await fetch(`/api/v1/market/live?tickers=${symbols.join(',')}`, { headers: apiHeaders })
          const json = await safeJson(r, addLine)
          return json?.data || json || {}
        } catch { return {} }
      }
      
      const indexData = await fetchQuotes(indexSymbols)
      for (const sym of indexSymbols) {
        const d = indexData?.[sym]
        if (!d?.price) { addLine({ text: `  ${(indexNames[sym] || sym).padEnd(12)}  ...`, className: 'text-dim' }); continue }
        const arrow = d.change_pct > 0 ? '▲' : d.change_pct < 0 ? '▼' : '◆'
        const color = d.change_pct > 0 ? 'text-green' : d.change_pct < 0 ? 'text-red' : 'text-dim'
        addLine({ text: `  ${(indexNames[sym] || sym).padEnd(12)}  ${arrow} ${d.price.toFixed(2)}  (${d.change_pct >= 0 ? '+' : ''}${d.change_pct.toFixed(2)}%)`, className: color })
      }
      addLine({ text: ``, className: '' })

      // Portfolio section
      if (tickers.length > 0) {
        addLine({ text: `💼  PORTFOLIO (${tickers.length} holdings)`, className: 'text-yellow' })
        addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
        const portfolioData = await fetchQuotes(tickers)
        let totalValue = 0
        for (const sym of tickers) {
          const holding = portfolio[sym]
          const qty = holding.shares || holding.amount || 1
          const d = portfolioData?.[sym]
          if (d?.price) {
            const value = qty * d.price
            totalValue += value
            const arrow = d.change_pct > 0 ? '▲' : d.change_pct < 0 ? '▼' : '◆'
            const color = d.change_pct > 0 ? 'text-green' : d.change_pct < 0 ? 'text-red' : 'text-dim'
            addLine({ text: `  ${sym.padEnd(6)} ${qty.toString().padStart(5)} × $${d.price.toFixed(2)} = $${value.toFixed(0).padStart(8)}  ${arrow} ${d.change_pct >= 0 ? '+' : ''}${d.change_pct.toFixed(2)}%`, className: color })
          } else {
            addLine({ text: `  ${sym.padEnd(6)} ${qty.toString().padStart(5)} × ??`, className: 'text-dim' })
          }
        }
        addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  TOTAL  ${' '.repeat(15)} $${totalValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`, className: 'text-cyan' })
        addLine({ text: ``, className: '' })
      } else {
        addLine({ text: `💼  PORTFOLIO`, className: 'text-yellow' })
        addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
        addLine({ text: `  No holdings yet. Add tickers with:`, className: 'text-dim' })
        addLine({ text: `  portfolio add <ticker> <shares>`, className: 'text-green' })
        addLine({ text: ``, className: '' })
      }

      addLine({ text: `⚡  QUICK LINKS`, className: 'text-yellow' })
      addLine({ text: `  ──────────────────────────────────────`, className: 'text-dim' })
      addLine({ text: `  topup       💰 Buy tuna  │  status  📊 Profile`, className: 'text-green' })
      addLine({ text: `  screener    🔍 Screen stocks  │  miaumap  🌐 Globe`, className: 'text-green' })
      addLine({ text: `  news        📰 Latest news  │  pulse   📈 Heatmap`, className: 'text-green' })
      if (!isPro) addLine({ text: `  invoice     💎 Upgrade to Meowster for 3D charts`, className: 'text-yellow' })
      else addLine({ text: `  chartz3d    📊 3D candlestick  │  compare3d  📈 3D comparison`, className: 'text-green' })
      addLine({ text: ``, className: '' })
      addLine({ text: `  🔄 Type dashboard again to refresh.`, className: 'text-dim' })
      break
    }

    case 'ticket': {
      const sub = args[0]?.toLowerCase()
      const token = localStorage.getItem('miau_token')
      if (!token) { addLine({ text: '🐱 You need to login first. Type: login <username>', className: 'text-red' }); break }
      const headers: Record<string, string> = { Authorization: `Bearer ${token}` }
      const api = '/api/v1/service-desk'

      if (sub === 'list' || !sub) {
        addLine({ text: '🐱 Fetching tickets...', className: 'text-dim' })
        try {
          const res = await fetch(`${api}/tickets`, { headers })
          const tickets = await res.json()
          if (!Array.isArray(tickets) || tickets.length === 0) {
            addLine({ text: '🐱 No tickets. The cat is pleased.', className: 'text-green' })
            break
          }
          const statusMap: Record<string, string> = { open: '🚒', progress: '👨‍🚒', resolved: '✅' }
          for (const t of tickets.slice(0, 20)) {
            addLine({ text: `${statusMap[t.status] || '❓'} #${t.id.slice(0,8)} [${t.category}] ${t.title} — ${t.assigned_to || 'unassigned'}`, className: t.status === 'resolved' ? 'text-dim' : 'text-cyan' })
          }
          addLine({ text: `🐱 ${tickets.length} total · ticket poke <id> to poke · ticket create --fire "title" to report`, className: 'text-dim' })
        } catch (e: any) { addLine({ text: `😿 ${e.message}`, className: 'text-red' }) }
      } else if (sub === 'create') {
        const cat = args.includes('--fire') ? 'fire' : args.includes('--bug') ? 'bug' : args.includes('--feature') ? 'feature' : 'question'
        const title = args.filter(a => !a.startsWith('--')).slice(1).join(' ') || 'No title provided'
        addLine({ text: `🐱 Creating ${cat} ticket: "${title}"...`, className: 'text-dim' })
        try {
          const res = await fetch(`${api}/tickets`, {
            method: 'POST', headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: cat, title, author: 'Terminal Cat' }),
          })
          const t = await res.json()
          addLine({ text: `🚒 Ticket #${t.id.slice(0,8)} created! ${t.assigned_to} is on the way.`, className: 'text-green' })
        } catch (e: any) { addLine({ text: `😿 ${e.message}`, className: 'text-red' }) }
      } else if (sub === 'poke') {
        const id = args[1]
        if (!id) { addLine({ text: '🐱 Usage: ticket poke <ticket_id>', className: 'text-red' }); break }
        try {
          const res = await fetch(`${api}/tickets/${id}/poke`, { method: 'POST', headers })
          const t = await res.json()
          addLine({ text: `👆 Poked! Ticket #${id.slice(0,8)} has been poked ${t.pokes} times.`, className: 'text-yellow' })
        } catch (e: any) { addLine({ text: `😿 ${e.message}`, className: 'text-red' }) }
      } else {
        addLine({ text: '🐱 Usage: ticket [list|create|poke]', className: 'text-cyan' })
      }
      break
    }

    default: {
      if (/^[A-Z]{1,5}$/.test(command) && command !== 'HELP') {
        await executeCommand(`price ${command}`, addLine)
      } else {
        log.command(command, parts.slice(1), false)
        addLine({ text: `miau: command not found: ${command}
Type 'help' for available commands.`, className: 'text-red' })
      }
    }
  }

}
