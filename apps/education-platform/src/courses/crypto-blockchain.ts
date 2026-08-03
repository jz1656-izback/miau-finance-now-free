import type { Course } from '../lib/types'

export const cryptoBlockchain: Course = {
  id: 'crypto-blockchain',
  slug: 'crypto-blockchain',
  title: 'Crypto & Blockchain Markets',
  description: 'Bitcoin, altcoins, on-chain analysis, and crypto trading strategies.',
  category: 'Markets',
  difficulty: 'intermediate',
  icon: '₿',
  lessonCount: 5,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'cb-basics',
      slug: 'crypto-basics',
      title: 'Crypto Fundamentals',
      description: 'Blockchain, consensus mechanisms, and crypto market structure.',
      commands: ['crypto', 'crypto list'],
      steps: [
        { instruction: 'List crypto markets: `crypto list`', command: 'crypto list', expectedOutput: 'Top cryptocurrencies by market cap' },
        { instruction: 'View BTC details: `crypto BTC`', command: 'crypto BTC', expectedOutput: 'BTC price, volume, market cap, dominance' },
        { instruction: 'Bitcoin uses Proof of Work. Ethereum uses Proof of Stake. Each has trade-offs.' },
      ],
      quiz: [
        { question: 'What consensus mechanism does Bitcoin use?', options: ['Proof of Work', 'Proof of Stake', 'Delegated Proof of Stake', 'Proof of Authority'], correctIndex: 0, explanation: 'Bitcoin uses Proof of Work (PoW), where miners compete to solve cryptographic puzzles.' },
      ],
    },
    {
      id: 'cb-onchain',
      slug: 'on-chain-analysis',
      title: 'On-Chain Analysis',
      description: 'Read the blockchain like a book — wallet activity, exchange flows, and miner behavior.',
      commands: ['crypto onchain', 'crypto flows'],
      steps: [
        { instruction: 'Check exchange flows: `crypto flows BTC`', command: 'crypto flows BTC', expectedOutput: 'Exchange inflow/outflow for BTC' },
        { instruction: 'Exchange outflows = investors moving to cold storage (bullish). Inflows = selling pressure (bearish).' },
        { instruction: 'View active addresses: `crypto onchain BTC --active`', command: 'crypto onchain BTC --active', expectedOutput: 'Active addresses over time' },
      ],
      quiz: [
        { question: 'What do exchange outflows typically indicate?', options: ['Investors moving to cold storage (bullish)', 'Selling pressure (bearish)', 'Nothing significant', 'Market manipulation'], correctIndex: 0, explanation: 'Exchange outflows suggest investors are moving BTC to cold storage, indicating long-term holding sentiment.' },
      ],
    },
    {
      id: 'cb-trading',
      slug: 'crypto-trading',
      title: 'Crypto Trading Strategies',
      description: 'Spot, futures, perpetual swaps, and arbitrage in crypto markets.',
      commands: ['crypto book', 'crypto trade'],
      steps: [
        { instruction: 'View order book: `crypto book BTC-USDT`', command: 'crypto book BTC-USDT', expectedOutput: 'Bid/ask depth chart with order book' },
        { instruction: 'Perpetual swaps have no expiry — they use funding rates to track spot prices.' },
        { instruction: 'Positive funding = longs pay shorts. Negative = shorts pay longs.' },
      ],
      quiz: [
        { question: 'What keeps perpetual swap prices close to spot?', options: ['Funding rate mechanism', 'Expiration dates', 'Market makers', 'Arbitrage bots'], correctIndex: 0, explanation: 'The funding rate mechanism ensures perpetual swap prices stay close to spot by incentivizing the opposite side.' },
      ],
    },
    {
      id: 'cb-defi-crypto',
      slug: 'defi-crypto',
      title: 'DeFi & Crypto Integration',
      description: 'How DeFi protocols interact with crypto markets — lending, borrowing, staking.',
      commands: ['defi protocols', 'crypto yield'],
      steps: [
        { instruction: 'Check crypto yield opportunities: `crypto yield`', command: 'crypto yield', expectedOutput: 'Best yield opportunities across protocols' },
        { instruction: 'Staking = lock tokens to secure a network, earn rewards.' },
        { instruction: 'Liquidity mining = provide liquidity to a DEX, earn protocol tokens.' },
      ],
      quiz: [
        { question: 'What is staking?', options: ['Locking tokens to secure a network', 'Buying tokens at a discount', 'Selling tokens for profit', 'Trading tokens on an exchange'], correctIndex: 0, explanation: 'Staking involves locking tokens to help secure a proof-of-stake network in exchange for rewards.' },
      ],
    },
    {
      id: 'cb-risk',
      slug: 'crypto-risk',
      title: 'Crypto Risk Management',
      description: 'Volatility, rug pulls, smart contract risk, and portfolio allocation for crypto.',
      commands: ['risk crypto', 'crypto var'],
      steps: [
        { instruction: 'Crypto VaR: `risk crypto --95 BTC`', command: 'risk crypto --95 BTC', expectedOutput: '95% VaR for BTC position' },
        { instruction: 'Crypto volatility is 3-5x higher than equities. Position size accordingly.' },
        { instruction: 'Never invest more than you can afford to lose. This is not financial advice — it is survival advice.' },
      ],
      quiz: [
        { question: 'How does crypto volatility compare to equities?', options: ['3-5x higher', 'About the same', 'Lower', '2x lower'], correctIndex: 0, explanation: 'Crypto is typically 3-5x more volatile than equities, requiring smaller position sizes.' },
      ],
    },
  ],
}
