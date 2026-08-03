import type { Course } from '../lib/types'

export const marketDataBasics: Course = {
  id: 'market-data-basics',
  slug: 'market-data-basics',
  title: 'Market Data — Basics',
  description: 'Price checks, charts, sparklines, crypto, and fear & greed.',
  category: 'Markets',
  difficulty: 'beginner',
  icon: '📈',
  lessonCount: 5,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'mdb-price',
      slug: 'price',
      title: 'Checking Prices',
      description: 'Get live prices for stocks, ETFs, and indices.',
      commands: ['price'],
      steps: [
        { instruction: 'Check Apple price: `price AAPL`', command: 'price AAPL', expectedOutput: 'AAPL price and % change' },
        { instruction: 'Try an index: `price ^GSPC`', command: 'price ^GSPC', expectedOutput: 'S&P 500 price' },
        { instruction: 'You can just type a ticker directly: `NVDA`', command: 'NVDA', expectedOutput: 'NVIDIA price displayed' },
        { instruction: 'Try your favorite stock ticker.' },
      ],
      quiz: [
        { question: 'What happens if you just type a ticker like `AAPL`?', options: ['It runs `price AAPL`', 'It errors', 'It does nothing', 'It opens a chart'], correctIndex: 0, explanation: 'Any 1-5 letter uppercase input is forwarded to the `price` command.' },
      ],
    },
    {
      id: 'mdb-chart',
      slug: 'chart',
      title: 'ASCII Charts',
      description: 'View price charts right in the terminal.',
      commands: ['chart', 'sparkline'],
      steps: [
        { instruction: 'View a chart: `chart TSLA`', command: 'chart TSLA', expectedOutput: 'ASCII price chart displayed' },
        { instruction: 'Compact view with sparklines: `sparkline AAPL TSLA`', command: 'sparkline AAPL MSFT', expectedOutput: 'Mini sparkline for each ticker' },
        { instruction: 'Try multiple tickers in a sparkline.' },
      ],
      quiz: [
        { question: 'Which command shows a compact price trend line?', options: ['sparkline', 'chart', 'price', 'trend'], correctIndex: 0, explanation: '`sparkline` displays a compact, text-based price trend.' },
      ],
    },
    {
      id: 'mdb-crypto',
      slug: 'crypto',
      title: 'Cryptocurrency',
      description: 'Check Bitcoin and top crypto prices.',
      commands: ['crypto', 'btc', 'cryptomkt', 'cryptohist', 'cryptotop'],
      steps: [
        { instruction: 'Check Bitcoin: `btc` or `crypto`', command: 'crypto', expectedOutput: 'BTC and top crypto prices' },
        { instruction: 'Market overview: `cryptomkt`', command: 'cryptomkt', expectedOutput: 'Crypto market stats' },
        { instruction: 'Top cryptos by cap: `cryptotop 10`', command: 'cryptotop 5', expectedOutput: 'Top 5 cryptocurrencies' },
      ],
      quiz: [
        { question: 'Which command shows the top N cryptocurrencies?', options: ['cryptotop', 'cryptomkt', 'crypto', 'btc'], correctIndex: 0, explanation: '`cryptotop [n]` shows the top n cryptocurrencies by market cap.' },
      ],
    },
    {
      id: 'mdb-forex',
      slug: 'forex',
      title: 'Forex & Commodities',
      description: 'Track currency pairs and commodity prices.',
      commands: ['forex', 'commodities', 'treasury'],
      steps: [
        { instruction: 'View forex rates: `forex`', command: 'forex', expectedOutput: 'Major currency pairs displayed' },
        { instruction: 'Check commodities: `commodities`', command: 'commodities', expectedOutput: 'Gold, oil, silver, copper prices' },
        { instruction: 'Treasury yields: `treasury`', command: 'treasury', expectedOutput: '2Y, 5Y, 10Y, 30Y yields' },
      ],
      quiz: [
        { question: 'What does `treasury` display?', options: ['US bond yields', 'Company treasuries', 'Gold prices', 'Tax rates'], correctIndex: 0, explanation: '`treasury` shows US Treasury yields across maturities.' },
      ],
    },
    {
      id: 'mdb-fear',
      slug: 'fear',
      title: 'Market Sentiment',
      description: 'Fear & Greed index and market indicators.',
      commands: ['fear', 'breadth', 'indicators'],
      steps: [
        { instruction: 'Check market sentiment: `fear`', command: 'fear', expectedOutput: 'Fear & Greed index value and zone' },
        { instruction: 'Market breadth: `breadth`', command: 'breadth', expectedOutput: 'Advancers vs decliners' },
        { instruction: 'Key indicators: `indicators`', command: 'indicators', expectedOutput: 'VIX, put/call ratio, and more' },
      ],
      quiz: [
        { question: 'What does the `fear` command show?', options: ['Fear & Greed Index', 'Your anxiety level', 'Market volatility', 'News sentiment'], correctIndex: 0, explanation: '`fear` displays the Fear & Greed Index for market sentiment.' },
      ],
    },
  ],
}
