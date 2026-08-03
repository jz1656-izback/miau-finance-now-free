import type { Course } from '../lib/types'

export const cryptoDerivatives: Course = {
  id: 'crypto-derivatives',
  slug: 'crypto-derivatives-trading',
  title: 'Crypto Derivatives',
  description: 'Perpetual swaps, crypto options, funding rates, and basis trading — the cat trades crypto derivatives with 9x leverage (one life per x).',
  category: 'Crypto & Web3',
  difficulty: 'advanced',
  icon: '📉',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'perpetual-swaps',
      slug: 'perpetual-swaps-fundamentals',
      title: 'Perpetual Swap Fundamentals',
      description: 'Understanding perpetual futures contracts.',
      commands: ['perp', 'funding', 'basis'],
      steps: [
        { instruction: 'Analyze a perpetual swap: `perp --analyze --pair BTC/USD --mark-price 65000 --funding-rate 0.0001 --open-interest 5B`', command: 'perp --analyze --pair BTC/USD --mark-price 65000 --funding-rate 0.0001 --open-interest 5B', expectedOutput: 'BTC-PERP: Mark $65,000, Index $64,800, Funding 0.01% (8hr), OI $5B. Longs paying shorts. Basis: +$200 (+0.31%). Next funding in 4 hours' },
        { instruction: 'Perpetual swaps are futures contracts with no expiration date.' },
        { instruction: 'The cat checked the funding rate — longs are paying shorts, so the cat went short and purred.' },
      ],
      quiz: [
        { question: 'How do perpetual swaps maintain price alignment with the spot market?', options: ['Through funding rates that periodic payments between long and short positions', 'Through mandatory settlement every 24 hours', 'Through government intervention', 'Through exchange price manipulation'], correctIndex: 0, explanation: 'Funding rates are periodic payments between long and short traders that incentivize price convergence between the perpetual contract and the underlying spot price.' },
      ],
    },
    {
      id: 'funding-rates',
      slug: 'funding-rate-strategies',
      title: 'Funding Rate Strategies',
      description: 'Trading based on funding rate dynamics.',
      commands: ['funding', 'perp', 'basis'],
      steps: [
        { instruction: 'Analyze funding rate history: `funding --history --pair ETH/USD --period 30d`', command: 'funding --history --pair ETH/USD --period 30d', expectedOutput: 'ETH funding (30d): Average 0.015% (8hr), High 0.12%, Low -0.05%. Cumulative annualized: +22% long cost. Regime: Bullish (funding positive 22 of 30 days)' },
        { instruction: 'Positive funding rates mean longs pay shorts, indicating bullish sentiment.' },
        { instruction: 'The cat funding rate strategy collects premium in high-funding environments — passive tuna income.' },
      ],
      quiz: [
        { question: 'What does a consistently positive funding rate indicate?', options: ['Bullish sentiment with longs willing to pay to maintain positions', 'Bearish sentiment', 'Neutral market conditions', 'Low volatility environment'], correctIndex: 0, explanation: 'Positive funding rates indicate that long positions are paying shorts, suggesting strong bullish demand and potential overcrowding in long positions.' },
      ],
    },
    {
      id: 'basis-trading',
      slug: 'basis-trading-crypto',
      title: 'Basis Trading & Cash-and-Carry',
      description: 'Capturing the basis between futures and spot.',
      commands: ['basis', 'perp', 'funding'],
      steps: [
        { instruction: 'Calculate basis trade: `basis --cash-carry --spot 65000 --futures 66500 --expiry 30 --funding-cost 0.02`', command: 'basis --cash-carry --spot 65000 --futures 66500 --expiry 30 --funding-cost 0.02', expectedOutput: 'Basis trade: Buy spot $65K, sell futures $66.5K. Gross basis: $1,500 (2.31%). Funding cost 30d: 2% annualized (0.17% total). Net return: 2.14% over 30 days' },
        { instruction: 'Basis trading captures the price difference between spot and futures markets.' },
        { instruction: 'The cat basis trade yielded 2.14% in 30 days — better than the cat food bank interest rate.' },
      ],
      quiz: [
        { question: 'What is a cash-and-carry arbitrage in crypto?', options: ['Buying spot and selling futures to capture the basis spread with minimal risk', 'Carrying cash to the exchange', 'Arbitraging different stablecoins', 'Trading with cash only'], correctIndex: 0, explanation: 'Cash-and-carry involves simultaneously buying the spot asset and selling futures, locking in the basis spread as a nearly risk-free return.' },
      ],
    },
    {
      id: 'crypto-options',
      slug: 'crypto-options-strategies',
      title: 'Crypto Options Strategies',
      description: 'Options trading in cryptocurrency markets.',
      commands: ['crypto-options', 'basis', 'funding'],
      steps: [
        { instruction: 'Price a crypto option: `crypto-options --price --underlying BTC --strike 70000 --expiry 30 --type call --vol 0.55`', command: 'crypto-options --price --underlying BTC --strike 70000 --expiry 30 --type call --vol 0.55', expectedOutput: 'BTC $70K call, 30d expiry: Implied vol 55%, Delta 0.42, Premium $3,200. Skew: 25d put vol 65% vs call vol 50% (negative skew). Greeks: Gamma 0.00012, Vega $45' },
        { instruction: 'Crypto options have higher implied volatility than traditional markets due to higher spot volatility.' },
        { instruction: 'The cat bought a BTC call option — it is betting on a moon mission or a cat-astrophic loss.' },
      ],
      quiz: [
        { question: 'Why do crypto options typically have higher implied volatility than equity options?', options: ['Cryptocurrencies have higher realized volatility and market uncertainty', 'Crypto options are government-regulated', 'Crypto has less trading volume', 'Crypto exchanges charge higher fees'], correctIndex: 0, explanation: 'Higher underlying volatility and greater uncertainty in cryptocurrency markets lead to higher implied volatility levels in crypto options compared to traditional equity options.' },
      ],
    },
  ],
}
