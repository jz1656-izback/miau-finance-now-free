import type { Course } from '../lib/types'

export const marketDataAdvanced: Course = {
  id: 'market-data-advanced',
  slug: 'market-data-advanced',
  title: 'Market Data — Advanced',
  description: 'Sector analysis, movers, market news, instruments, and search.',
  category: 'Markets',
  difficulty: 'intermediate',
  icon: '📊',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'mda-sectors',
      slug: 'sectors',
      title: 'Sector Performance',
      description: 'Track which sectors are winning and losing.',
      commands: ['sectors', 'sectorslist', 'sectorsexposure'],
      steps: [
        { instruction: 'View sector performance: `sectors`', command: 'sectors', expectedOutput: 'All 11 GICS sectors with % changes' },
        { instruction: 'List available sectors: `sectorslist`', command: 'sectorslist', expectedOutput: 'Full list of sector identifiers' },
        { instruction: 'Check factor exposure: `sectorsexposure AAPL`', command: 'sectorsexposure MSFT', expectedOutput: 'Sector factor loadings' },
      ],
      quiz: [
        { question: 'How many GICS sectors are tracked?', options: ['11', '8', '15', '20'], correctIndex: 0, explanation: 'The platform tracks all 11 GICS sectors.' },
      ],
    },
    {
      id: 'mda-movers',
      slug: 'movers',
      title: 'Market Movers',
      description: 'Find the biggest gainers and losers.',
      commands: ['movers', 'marketnews', 'news', 'newsbatch'],
      steps: [
        { instruction: 'View top movers: `movers`', command: 'movers', expectedOutput: 'Top gainers and losers listed' },
        { instruction: 'Market news: `marketnews`', command: 'marketnews', expectedOutput: 'Latest market headlines' },
        { instruction: 'Stock-specific news: `news AAPL`', command: 'news TSLA', expectedOutput: 'Recent news for the ticker' },
        { instruction: 'Batch news: `newsbatch AAPL MSFT`', command: 'newsbatch GOOGL AMZN', expectedOutput: 'News for multiple tickers' },
      ],
      quiz: [
        { question: 'Which command shows news for multiple stocks?', options: ['newsbatch', 'marketnews', 'news', 'movers'], correctIndex: 0, explanation: '`newsbatch ticker1 ticker2 ...` gets news for multiple stocks at once.' },
      ],
    },
    {
      id: 'mda-search',
      slug: 'search',
      title: 'Search & Instruments',
      description: 'Find any financial instrument in the database.',
      commands: ['search', 'instruments', 'instypes'],
      steps: [
        { instruction: 'Search for a stock: `search microsoft`', command: 'search apple', expectedOutput: 'Matching instruments displayed' },
        { instruction: 'List all instruments: `instruments`', command: 'instruments', expectedOutput: 'Instrument catalog' },
        { instruction: 'Types of instruments: `instypes`', command: 'instypes', expectedOutput: 'Stock, ETF, crypto, forex, index...' },
      ],
      quiz: [
        { question: 'How do you find a stock by name?', options: ['search', 'find', 'lookup', 'query'], correctIndex: 0, explanation: '`search <query>` searches the instrument database by name or ticker.' },
      ],
    },
    {
      id: 'mda-all',
      slug: 'aggregate',
      title: 'Aggregate Market View',
      description: 'See everything at once.',
      commands: ['all'],
      steps: [
        { instruction: 'Aggregate all market data: `all`', command: 'all', expectedOutput: 'Multi-panel market overview with indices, crypto, forex, sectors, and more' },
        { instruction: 'This is your daily market dashboard in one command.' },
      ],
      quiz: [
        { question: 'What does `all` display?', options: ['Complete market overview', 'Your portfolio', 'AI analysis', 'Nothing useful'], correctIndex: 0, explanation: '`all` shows an aggregated view of all market data — indices, crypto, forex, sectors, etc.' },
      ],
    },
  ],
}
