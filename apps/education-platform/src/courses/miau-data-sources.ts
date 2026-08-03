import type { Course } from '../lib/types'

export const miauDataSources: Course = {
  id: 'miau-data-sources',
  slug: 'miau-data-sources',
  title: 'Miau Finance Data Sources',
  description: 'How the data vacuum cleaner works — 20+ APIs, automatic fallback chains, and zero-config no-key providers. The cat pulls data from everywhere.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '🔌',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'ds-architecture',
      slug: 'data-source-architecture',
      title: 'The Data Vacuum Cleaner',
      description: 'How Miau Finance pulls data from 20+ APIs seamlessly.',
      commands: ['health', 'datasources status'],
      steps: [
        { instruction: 'Check all active data sources: `datasources status`', command: 'datasources status', expectedOutput: 'List of all registered providers with health status' },
        { instruction: 'Miau Finance v3.0 integrates 20+ public APIs through a unified data source layer.' },
        { instruction: 'The cat\'s data vacuum runs 24/7. It never misses a data point. Unlike mice.' },
        { instruction: 'No-key providers load automatically. Key-based ones activate when you configure them in Settings.' },
      ],
      quiz: [
        { question: 'How does Miau Finance handle failing data sources?', options: ['Automatic fallback chain — if one provider fails, the next takes over', 'Shows an error message and stops', 'Retries 3 times then gives up', 'Only uses one provider at a time'], correctIndex: 0, explanation: 'The DataSourceManager uses a fallback chain: if Provider A fails (rate limit, outage), it automatically tries Provider B, then C, ensuring maximum uptime.' },
      ],
    },
    {
      id: 'ds-no-key',
      slug: 'no-key-providers',
      title: 'Zero-Config Providers',
      description: 'Data sources that work immediately with no API key needed.',
      commands: ['fx USD', 'defillama', 'gas 1'],
      steps: [
        { instruction: 'Check FX rates for 200 currencies: `fx USD` — uses Frankfurter, no key needed', command: 'fx USD', expectedOutput: 'USD exchange rates for 200+ currencies' },
        { instruction: 'Frankfurter provides 200 currencies from 55 central banks with history back to 1948.' },
        { instruction: 'Check top DeFi protocols: `defillama` — uses DeFiLlama, 2400+ protocols', command: 'defillama', expectedOutput: 'Top DeFi protocols ranked by TVL' },
        { instruction: 'Check Ethereum gas prices: `gas 1` — uses Blocknative', command: 'gas 1', expectedOutput: 'Safe/Normal/Fast gas prices in gwei' },
        { instruction: 'The cat loves no-key APIs because they require zero effort. Just like a cat.' },
      ],
      quiz: [
        { question: 'Which data provider handles 200+ currency FX rates with no API key?', options: ['Frankfurter', 'Finnhub', 'Alpha Vantage', 'CoinGecko'], correctIndex: 0, explanation: 'Frankfurter.app provides free FX rates for 200+ currencies from 55 central banks with historical data back to 1948 — no key required.' },
      ],
    },
    {
      id: 'ds-key-providers',
      slug: 'key-based-providers',
      title: 'Key-Based Providers',
      description: 'Unlock premium data sources by adding API keys in Settings.',
      commands: ['profile AAPL', 'technicals AAPL'],
      steps: [
        { instruction: 'Configure API keys in Settings → Data Sources. Add your Finnhub, Twelve Data, and CoinPaprika keys.' },
        { instruction: 'Once configured, premium commands activate: `profile AAPL` for company profiles, `technicals AAPL` for RSI/MACD.' },
        { instruction: 'The cat recommends getting a Finnhub key first — it unlocks 12+ commands including insider trading and IPO data.' },
        { instruction: 'Key-based providers are never stored in logs or error messages. Your keys are safe with the cat.' },
      ],
      quiz: [
        { question: 'Which single API key unlocks the most commands in Miau Finance?', options: ['Finnhub (12+ commands: insider, IPO, short, ownership, earnings, recommendations, SEC filings)', 'Twelve Data (technical indicators)', 'BLS (macro/CPI data)', 'Etherscan (gas tracker)'], correctIndex: 0, explanation: 'Finnhub provides quotes, history, financials, company news, SEC filings, insider transactions, short interest, IPO calendar, institutional ownership, earnings, recommendations, price targets, and market news.' },
      ],
    },
    {
      id: 'ds-commands',
      slug: 'data-source-commands',
      title: 'All Data Source Commands',
      description: 'A tour of every command powered by the new data layer.',
      commands: ['fx', 'defillama', 'yields 5', 'gas', 'quanthealth AAPL', 'fairvalue AAPL', 'passiveflow AAPL', 'etfanalyzer SPY'],
      steps: [
        { instruction: 'Quant health: `quanthealth AAPL` — Piotroski F-Score, Altman Z', command: 'quanthealth AAPL', expectedOutput: 'Piotroski score, Altman Z, Beneish M' },
        { instruction: 'Fair value: `fairvalue AAPL` — DCF valuation', command: 'fairvalue AAPL', expectedOutput: 'Current price vs fair value' },
        { instruction: 'Passive flow: `passiveflow AAPL` — ETF ownership', command: 'passiveflow AAPL', expectedOutput: 'Passive ownership percentage' },
        { instruction: 'Run `help` to see all 30+ data-powered commands. The cat built all of them just for you.' },
      ],
      quiz: [
        { question: 'What does the quanthealth command show?', options: ['Piotroski F-Score, Altman Z-Score, and Beneish M-Score for fundamental health', 'Stock price and volume', 'Technical indicators like RSI and MACD', 'Company earnings history'], correctIndex: 0, explanation: 'quanthealth aggregates three key forensic accounting scores: Piotroski F-Score (financial strength 0-9), Altman Z-Score (bankruptcy risk), and Beneish M-Score (earnings manipulation detection).' },
      ],
    },
  ],
}
