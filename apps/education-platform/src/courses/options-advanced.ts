import type { Course } from '../lib/types'

export const optionsAdvanced: Course = {
  id: 'options-advanced',
  slug: 'options-advanced',
  title: 'Options Advanced',
  description: 'Vol surface, exotic options, vol arbitrage, and skew — the cat has options on tuna futures.',
  category: 'Derivatives',
  difficulty: 'advanced',
  icon: '📐',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'opt-volsurface',
      slug: 'volatility-surface',
      title: 'Volatility Surface',
      description: '3D mapping of implied volatility.',
      commands: ['vol-surface', 'vol-surface plot'],
      steps: [
        { instruction: 'Plot the volatility surface: `vol-surface plot --ticker SPX --expiry 30,60,90 --strikes otm,atm,itm`', command: 'vol-surface plot --ticker SPX --expiry 30,60,90 --strikes otm,atm,itm', expectedOutput: 'Volatility surface for SPX: smirk pattern detected, skew steep on puts' },
        { instruction: 'The vol surface shows how implied volatility varies by strike and expiration.' },
        { instruction: 'The cat can read a vol surface better than it reads ingredients labels.' },
      ],
      quiz: [
        { question: 'What does a steep put skew on the volatility surface indicate?', options: ['Market is pricing higher tail risk on the downside', 'Puts are cheaper than calls', 'Volatility is low across strikes', 'The market expects a rally'], correctIndex: 0, explanation: 'A steep put skew means deep out-of-the-money puts have higher implied vol, indicating investors hedge against a crash.' },
      ],
    },
    {
      id: 'opt-exotic',
      slug: 'exotic-options',
      title: 'Exotic Options',
      description: 'Barrier, Asian, lookback, and digital options.',
      commands: ['exotic', 'exotic price'],
      steps: [
        { instruction: 'Price a barrier option: `exotic price --type knock-out --barrier 150 --spot 140 --strike 145 --expiry 30`', command: 'exotic price --type knock-out --barrier 150 --spot 140 --strike 145 --expiry 30', expectedOutput: 'Knock-out call price: $3.45 — barrier at $150, 65% probability of knockout' },
        { instruction: 'Exotic options have non-standard payoff structures.' },
        { instruction: 'The cat created an exotic option: if tuna price hits $50, exercise — otherwise, nap.' },
      ],
      quiz: [
        { question: 'What is an Asian option?', options: ['Its payoff depends on the average price over a period', 'It can only be traded in Asia', 'It is priced in yen', 'It has an Asian-style settlement'], correctIndex: 0, explanation: 'Asian options use the average underlying price over the option\'s life rather than the price at a single point in time.' },
      ],
    },
    {
      id: 'opt-varbs',
      slug: 'volatility-arbitrage',
      title: 'Volatility Arbitrage',
      description: 'Trading realized vs implied volatility.',
      commands: ['vol-arb', 'vol-arb trade'],
      steps: [
        { instruction: 'Find vol arbitrage opportunities: `vol-arb trade --ticker SPX --compare realized,implied`', command: 'vol-arb trade --ticker SPX --compare realized,implied', expectedOutput: 'Vol arbitrage signal: implied vol 22%, realized vol 18% — sell vol (short straddle)' },
        { instruction: 'Vol arbitrage profits when implied and realized volatility diverge.' },
        { instruction: 'The cat\'s vol arb: nap implied = 8h, nap realized = 12h — long naps.' },
      ],
      quiz: [
        { question: 'How do you profit from vol arbitrage?', options: ['Buy when implied vol is low relative to realized; sell when high', 'Always buy options at the ask price', 'Trade only at market open', 'Hedge with futures continuously'], correctIndex: 0, explanation: 'Vol arbitrage involves buying options when implied volatility is cheap vs realized, and selling when it is expensive.' },
      ],
    },
    {
      id: 'opt-skew',
      slug: 'volatility-skew',
      title: 'Volatility Skew & Smile',
      description: 'Understanding market sentiment.',
      commands: ['skew', 'skew analyze'],
      steps: [
        { instruction: 'Analyze volatility skew: `skew analyze --ticker SPX --maturity 1m --strikes 90,95,100,105,110`', command: 'skew analyze --ticker SPX --maturity 1m --strikes 90,95,100,105,110', expectedOutput: 'Skew analysis: 25-delta put vol 28%, 25-delta call vol 18% — risk reversal -10%' },
        { instruction: 'Skew measures the difference in implied volatility between puts and calls.' },
        { instruction: 'The cat\'s risk reversal: long purr, short hiss.' },
      ],
      quiz: [
        { question: 'What does a negative risk reversal indicate?', options: ['Puts are more expensive than calls, suggesting bearish sentiment', 'Calls are more expensive than puts', 'The market is neutral', 'Volatility is symmetric'], correctIndex: 0, explanation: 'Risk reversal (call vol minus put vol) being negative means puts cost more — investors are hedging downside risk.' },
      ],
    },
  ],
}
