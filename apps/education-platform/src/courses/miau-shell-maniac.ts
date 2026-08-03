import type { Course } from '../lib/types'

export const miauShellManiac: Course = {
  id: 'miau-shell-maniac',
  slug: 'miau-shell-maniac',
  title: 'Miau Shell Maniac Certification 🏆',
  description: 'Better than an MBA (the cats said so). The ultimate terminal finance certification — master every command, model, and API. Graduate as a Certified Miau Shell Maniac (CMSM).',
  category: 'certification',
  difficulty: 'advanced',
  icon: '🎓',
  lessonCount: 7,
  estimatedMinutes: 520,
  lessons: [
    {
      id: 'cmsm-1',
      slug: 'terminal-weapon',
      title: 'Terminal as a Weapon: Speed-Finance',
      description: 'Execute market analysis faster than any Bloomberg user could dream.',
      commands: ['price AAPL MSFT GOOGL AMZN META', 'risk AAPL', 'beta TSLA', 'correlation'],
      steps: [
        { instruction: 'Get live prices for 5 mega-cap tech stocks in one command', command: 'price AAPL MSFT GOOGL AMZN META', expectedOutput: 'AAPL...', hint: 'Just list the tickers after price' },
        { instruction: 'Run comprehensive risk analysis', command: 'risk AAPL', expectedOutput: 'Risk Analytics', hint: 'risk <ticker>' },
        { instruction: 'Calculate beta for a stock', command: 'beta TSLA', expectedOutput: 'Beta:', hint: 'beta <ticker>' },
        { instruction: 'Open the correlation matrix heatmap', command: 'correlation AAPL,MSFT,GOOGL', expectedOutput: 'correlation', hint: 'comma-separated tickers' },
      ],
      quiz: [
        { question: 'How many clicks does a Bloomberg user need vs your keystrokes?', options: ['40-60 clicks vs 4-8 keystrokes', 'Same amount', '100 clicks vs 50 keystrokes', 'Cats click'], correctIndex: 0, explanation: 'Bloomberg requires 40-60 clicks to get price/risk data. Miau terminal needs 4-8 keystrokes — speed is the point.' },
        { question: 'Why are terminal commands faster than GUI clicks?', options: ['No context switching, direct input, scriptable', 'They look cooler', 'They are not faster', 'GUIs are deprecated'], correctIndex: 0, explanation: 'Terminal commands eliminate context switching between windows, accept direct keyboard input without mouse movement, and can be chained/scripted for complex workflows.' },
      ],
    },
    {
      id: 'cmsm-2',
      slug: 'world-map',
      title: 'World Map Mastery: Global Markets',
      description: 'Navigate the Leaflet-powered world map. Find every exchange. Master the tile layers.',
      commands: ['map'],
      steps: [
        { instruction: 'Open the map: type map in the terminal', command: 'map', expectedOutput: 'map', hint: 'Just type map' },
        { instruction: 'Search for BOVESPA', command: 'map', expectedOutput: 'BOVESPA', hint: 'Use the search bar on the map' },
        { instruction: 'Switch between Dark, Streets, and Satellite tile layers', command: 'map', hint: 'Bottom bar buttons' },
      ],
      quiz: [
        { question: 'How many exchanges are on the Miau Finance world map?', options: ['21', '10', '50', '5'], correctIndex: 0, explanation: 'The Miau Finance world map displays 21 global exchanges across North America, Europe, Asia, and Oceania.' },
        { question: 'Which tile layer shows satellite imagery?', options: ['Satellite', 'Dark', 'Streets', 'None'], correctIndex: 0, explanation: 'The Satellite tile layer uses real satellite imagery for a geographic view of exchanges and trading hubs.' },
      ],
    },
    {
      id: 'cmsm-3',
      slug: 'valuation-models',
      title: 'Valuation: DCF, WACC, Comps, LBO',
      description: 'Run all four investment banking valuation models. An MBA takes 4 hours. You take 4 seconds.',
      commands: ['sheetz miau -dcf AAPL', 'sheetz miau -wacc AAPL', 'sheetz miau -comps AAPL', 'sheetz miau -lbo AAPL', 'sheetz miau -all AAPL'],
      steps: [
        { instruction: 'Run a DCF valuation on AAPL', command: 'sheetz miau -dcf AAPL', expectedOutput: 'DCF Valuation', hint: 'sheet miau -dcf <ticker>' },
        { instruction: 'Calculate WACC for AAPL', command: 'sheetz miau -wacc AAPL', expectedOutput: 'WACC', hint: 'sheet miau -wacc <ticker>' },
        { instruction: 'Run comparable company analysis', command: 'sheetz miau -comps AAPL', expectedOutput: 'Comparable', hint: 'sheet miau -comps <ticker>' },
        { instruction: 'Run an LBO model', command: 'sheetz miau -lbo AAPL', expectedOutput: 'LBO', hint: 'sheet miau -lbo <ticker>' },
        { instruction: 'Run all 4 models at once with the -all flag', command: 'sheetz miau -all AAPL', expectedOutput: 'DCF...WACC...Comps...LBO', hint: 'sheet miau -all <ticker>' },
      ],
      quiz: [
        { question: 'What does the -all flag do?', options: ['Runs DCF, WACC, Comps, and LBO at once', 'Shows all stocks', 'Runs in slow mode', 'Prints all cat names'], correctIndex: 0, explanation: 'The -all flag runs all four IB valuation models (DCF, WACC, Comps, LBO) in a single command — an MBA takes 4 hours, you take 4 seconds.' },
      ],
    },
    {
      id: 'cmsm-4',
      slug: 'defi-protocols',
      title: 'DeFi Protocol Mastery',
      description: 'Navigate 8 DeFi protocols. Find the best yields. Trade across chains.',
      commands: ['defi yield', 'defi protocols'],
      steps: [
        { instruction: 'Check DeFi yields across all protocols', command: 'defi yield', expectedOutput: 'yield', hint: 'defi yield' },
        { instruction: 'List available DeFi protocols', command: 'defi protocols', expectedOutput: 'Uniswap, Aave, Curve', hint: 'defi protocols' },
      ],
      quiz: [
        { question: 'Which DeFi protocol handles stable swaps with low slippage?', options: ['Curve', 'Uniswap', 'Aave', 'Lido'], correctIndex: 0, explanation: 'Curve specializes in stablecoin and correlated asset swaps with minimal slippage using its concentrated liquidity model.' },
        { question: 'Which Solana DEX does Miau Finance integrate with?', options: ['Jupiter and Raydium', 'OpenSea', 'Blur', 'None'], correctIndex: 0, explanation: 'Miau Finance integrates with Jupiter and Raydium, the two largest Solana DEX aggregators for Solana-based token swaps.' },
      ],
    },
    {
      id: 'cmsm-5',
      slug: 'developer-platform',
      title: 'API Keys & Developer Platform',
      description: 'Master API key management, webhooks, and the developer console.',
      commands: ['devconsole', 'apikey create', 'apikey list'],
      steps: [
        { instruction: 'Open the developer console dashboard', command: 'devconsole', expectedOutput: 'Developer Console', hint: 'devconsole' },
        { instruction: 'Create a new API key with scopes', command: 'apikey create "My Bot" --scopes market:read,orders:create', expectedOutput: 'miau_', hint: 'apikey create <name>' },
        { instruction: 'List your active API keys', command: 'apikey list', expectedOutput: 'api_keys', hint: 'apikey list' },
      ],
      quiz: [
        { question: 'How many scoped permissions does the plugin system have?', options: ['16', '5', '100', 'Unlimited'], correctIndex: 0, explanation: 'The Miau Finance plugin sandbox has 16 granular scoped permissions covering market data, orders, account info, and admin functions.' },
        { question: 'What modules are blocked in the plugin sandbox?', options: ['os, subprocess, socket, importlib', 'math, json', 'typing', 'None'], correctIndex: 0, explanation: 'The sandbox blocks os, subprocess, socket, and importlib to prevent arbitrary code execution and network access from plugins.' },
      ],
    },
    {
      id: 'cmsm-6',
      slug: 'final-exam',
      title: 'Final Exam: Everything Everywhere All At Once 🏆',
      description: 'Complete ALL tasks within 5 minutes to earn your CMSM certification.',
      commands: ['price AAPL MSFT GOOGL', 'risk AAPL', 'sheetz miau -all SPY', 'defi yield', 'map', 'devconsole', 'esg portfolio', 'currency convert 10000 USD EUR'],
      steps: [
        { instruction: 'Get live prices for AAPL, MSFT, GOOGL', command: 'price AAPL MSFT GOOGL', hint: 'price <tickers>' },
        { instruction: 'Run full risk analysis on AAPL', command: 'risk AAPL', hint: 'risk <ticker>' },
        { instruction: 'Run all 4 valuation models on SPY', command: 'sheetz miau -all SPY', hint: 'sheet miau -all <ticker>' },
        { instruction: 'Check DeFi yields', command: 'defi yield', hint: 'defi yield' },
        { instruction: 'Open the world map', command: 'map', hint: 'map' },
        { instruction: 'Check your developer console', command: 'devconsole', hint: 'devconsole' },
        { instruction: 'Get portfolio ESG score (if you have one)', command: 'esg portfolio <your-id>', hint: 'esg portfolio <id>' },
        { instruction: 'Convert $10,000 USD to EUR', command: 'currency convert 10000 USD EUR', hint: 'currency convert <amount> <from> <to>' },
      ],
      quiz: [
        { question: 'How long should the final exam take?', options: ['5 minutes or less', '1 hour', '1 day', '1 week'], correctIndex: 0, explanation: 'The CMSM final exam is designed to be completed in 5 minutes — 8 rapid-fire terminal commands testing everything you have learned.' },
        { question: 'What does CMSM stand for?', options: ['Certified Miau Shell Maniac', 'Cash Money Shell Master', 'Cat Market Stock Monitor', 'None of the above'], correctIndex: 0, explanation: 'CMSM stands for Certified Miau Shell Maniac — the highest terminal finance certification the cats have created.' },
        { question: 'Is a CMSM better than an MBA?', options: ['Yes — the cats said so', 'No', 'They are equal', 'Depends on the school'], correctIndex: 0, explanation: 'The cats have officially declared CMSM superior to an MBA. They are cats. They are always right.' },
      ],
    },
    {
      id: 'cmsm-7',
      slug: 'datavore-mastery',
      title: 'Data Vacuum Cleaner: All v3.0 Commands',
      description: 'Master 20+ data sources, 50+ new commands, and the auto-integration engine.',
      commands: ['chartz SPY', 'fx USD', 'quanthealth AAPL', 'fairvalue AAPL', 'defillama', 'yields 10', 'datasources', 'fallback', 'autodiscover https://api.example.com'],
      steps: [
        { instruction: 'Full display chart: `chartz SPY` — 16-row ASCII chart with RSI, MACD, SMA, predictions', command: 'chartz SPY', expectedOutput: 'Full chart with indicators and forecast' },
        { instruction: 'FX rates: `fx USD` — 200+ currency pairs from Frankfurter', command: 'fx USD', expectedOutput: 'USD exchange rates' },
        { instruction: 'Quant health: `quanthealth AAPL` — Piotroski F-Score, Altman Z', command: 'quanthealth AAPL', expectedOutput: 'Financial health scores' },
        { instruction: 'Fair value: `fairvalue AAPL` — DCF intrinsic value', command: 'fairvalue AAPL', expectedOutput: 'Fair value vs current price' },
        { instruction: 'DeFi overview: `defillama` — top protocols by TVL', command: 'defillama', expectedOutput: 'DeFi protocol rankings' },
        { instruction: 'Yield farming: `yields 10` — pools with 10%+ APY', command: 'yields 10', expectedOutput: 'High-yield pools' },
        { instruction: 'Health dashboard: `datasources` — all 8 providers with latency and quota', command: 'datasources', expectedOutput: 'Provider health status' },
        { instruction: 'Fallback chains: `fallback` — see which providers back up each capability', command: 'fallback', expectedOutput: 'Fallback chain per capability' },
        { instruction: 'Auto-discover: `autodiscover https://api.frankfurter.app` — probe any API', command: 'autodiscover https://api.frankfurter.app', expectedOutput: 'API endpoints detected and analyzed' },
      ],
      quiz: [
        { question: 'How many data source providers does Miau Finance v3.0 have?', options: ['8 no-key providers + 5 key-based = 13 total', '5', '20', '3'], correctIndex: 0, explanation: 'v3.0 has 8 always-on providers (yahoo, StockPriceDev, Frankfurter, DeFiLlama, SecuritiesDB, DumbStockAPI, Blocknative, CEX) plus 5 key-based (Finnhub, Twelve Data, CoinPaprika, BLS, Etherscan).' },
        { question: 'What happens when a data source fails in v3.0?', options: ['The fallback chain automatically tries the next provider in line', 'The command shows an error', 'The system crashes', 'You have to manually switch sources'], correctIndex: 0, explanation: 'The DataSourceManager tries providers in priority order. If the first provider fails, it falls through to the next. For example, if Finnhub is down for quotes, Yahoo and StockPriceDev take over.' },
      ],
    },
  ],
}

export default miauShellManiac
