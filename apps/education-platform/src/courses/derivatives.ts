import type { Course } from '../lib/types'

export const derivatives: Course = {
  id: 'derivatives',
  slug: 'derivatives',
  title: 'Options & Derivatives',
  description: 'Options chains, Greeks, futures, and structured products — the cat hedges its tuna.',
  category: 'Analytics',
  difficulty: 'advanced',
  icon: '📐',
  lessonCount: 5,
  estimatedMinutes: 35,
  lessons: [
    {
      id: 'der-options-basics',
      slug: 'options-basics',
      title: 'Options Fundamentals',
      description: 'Calls, puts, strikes, and expiration — the building blocks.',
      commands: ['options', 'options chain'],
      steps: [
        { instruction: 'View the options chain: `options AAPL`', command: 'options AAPL', expectedOutput: 'Full options chain with strikes, IV, open interest' },
        { instruction: 'Calls give the right to buy. Puts give the right to sell. Both have an expiration date.' },
        { instruction: 'Open interest shows liquidity. Volume shows activity. Focus on high-volume strikes.' },
      ],
      quiz: [
        { question: 'What does a call option give you?', options: ['Right to buy', 'Right to sell', 'Obligation to buy', 'Obligation to sell'], correctIndex: 0, explanation: 'A call gives the right (not obligation) to buy the underlying at the strike price.' },
      ],
    },
    {
      id: 'der-greeks',
      slug: 'greeks',
      title: 'The Greeks',
      description: 'Delta, gamma, theta, vega, rho — measure option sensitivity.',
      commands: ['options greeks', 'options risk'],
      steps: [
        { instruction: 'Analyze Greeks: `options greeks AAPL`', command: 'options greeks AAPL', expectedOutput: 'Delta, Gamma, Theta, Vega, Rho for each strike' },
        { instruction: 'Delta = how much option price moves per $1 stock move. At-the-money ≈ 0.50.' },
        { instruction: 'Theta = time decay. Options lose value every day. Theta is negative for long positions.' },
        { instruction: 'Vega = sensitivity to implied volatility. High vega = big moves when IV changes.' },
      ],
      quiz: [
        { question: 'Which Greek measures time decay?', options: ['Theta', 'Delta', 'Gamma', 'Vega'], correctIndex: 0, explanation: 'Theta measures time decay — how much option value is lost per day.' },
      ],
    },
    {
      id: 'der-strategies',
      slug: 'option-strategies',
      title: 'Option Strategies',
      description: 'Spreads, straddles, strangles, iron condors — build them step by step.',
      commands: ['options strategy', 'options analyze'],
      steps: [
        { instruction: 'Analyze a strategy: `options strategy AAPL --bull-put-spread`', command: 'options strategy AAPL --bull-put-spread', expectedOutput: 'Max profit, max loss, breakeven, probability of profit' },
        { instruction: 'Bull put spread = sell a put, buy a lower strike put. Credit received = max profit.' },
        { instruction: 'Straddle = buy a call and put at same strike. Profits from big moves either direction.' },
      ],
      quiz: [
        { question: 'What is a bull put spread?', options: ['Credit spread that profits from upward moves', 'Debit spread that profits from downward moves', 'A single put option', 'A futures contract'], correctIndex: 0, explanation: 'Bull put spread is a credit spread — you sell a put and buy a lower strike put, collecting premium.' },
      ],
    },
    {
      id: 'der-futures',
      slug: 'futures',
      title: 'Futures & Forwards',
      description: 'Futures contracts, margin, basis, and roll yield.',
      commands: ['futures', 'futures chain'],
      steps: [
        { instruction: 'View futures: `futures ES`', command: 'futures ES', expectedOutput: 'S&P 500 futures chain with prices and open interest' },
        { instruction: 'Futures are standardized contracts traded on exchanges. Margin requirements vary.' },
        { instruction: 'Contango = futures price > spot. Backwardation = futures price < spot.' },
      ],
      quiz: [
        { question: 'What is contango?', options: ['Futures price above spot price', 'Futures price below spot price', 'No difference', 'Inverse relationship'], correctIndex: 0, explanation: 'Contango is when futures trade above the spot price, common in equity index futures.' },
      ],
    },
    {
      id: 'der-risk',
      slug: 'derivatives-risk',
      title: 'Derivatives Risk Management',
      description: 'Portfolio hedging, tail risk, and position sizing for derivatives.',
      commands: ['risk greeks', 'risk var', 'hedge'],
      steps: [
        { instruction: 'Check portfolio Greeks: `risk greeks`', command: 'risk greeks', expectedOutput: 'Aggregate delta, gamma, theta, vega for your portfolio' },
        { instruction: 'Value at Risk: `risk var --95`', command: 'risk var --95', expectedOutput: '95% VaR in USD' },
        { instruction: 'Hedge delta exposure: `hedge --delta-neutral`', command: 'hedge --delta-neutral', expectedOutput: 'Recommended hedge trades' },
      ],
      quiz: [
        { question: 'What does delta-neutral mean?', options: ['Portfolio has zero net delta exposure', 'Portfolio has maximum delta', 'No options in portfolio', 'All positions are hedged'], correctIndex: 0, explanation: 'Delta-neutral means the portfolio\'s net delta is zero — no directional exposure to the underlying.' },
      ],
    },
  ],
}
