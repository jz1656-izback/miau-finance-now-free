import type { Course } from '../lib/types'

export const tailRisk: Course = {
  id: 'tail-risk',
  slug: 'tail-risk-hedging',
  title: 'Tail Risk Hedging',
  description: 'Black swans, tail hedging, put options, VIX, and crisis alpha — the cat prepares for the day the tuna market crashes.',
  category: 'Risk Management',
  difficulty: 'advanced',
  icon: '🛡️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'black-swans',
      slug: 'black-swan-events',
      title: 'Black Swan Events',
      description: 'Understanding rare and unpredictable events.',
      commands: ['black-swan', 'tail-risk', 'vix'],
      steps: [
        { instruction: 'Identify historical black swans: `black-swan --history --list`', command: 'black-swan --history --list', expectedOutput: 'Black swan events: 1987 Crash (-22.6% in one day), 2008 Financial Crisis (-38.5%), 2020 COVID (-33.9%), 2022 Inflation shock (-19.4%)' },
        { instruction: 'A black swan is an unpredictable event with severe consequences beyond normal expectations.' },
        { instruction: 'The cat remembers the Great Tuna Shortage of 2020 — a true black swan event in feline history.' },
      ],
      quiz: [
        { question: 'What characterizes a black swan event?', options: ['It is rare, has severe impact, and is rationalized in hindsight as predictable', 'It happens every year', 'It has no market impact', 'It is always positive for markets'], correctIndex: 0, explanation: 'Black swan events are rare, consequential outliers that seem predictable only after they occur, making them nearly impossible to anticipate.' },
      ],
    },
    {
      id: 'tail-hedging',
      slug: 'tail-hedging-strategies',
      title: 'Tail Hedging Strategies',
      description: 'Protecting portfolios against extreme downside.',
      commands: ['tail-risk', 'vix'],
      steps: [
        { instruction: 'Construct a tail hedge: `tail-risk --hedge --portfolio-value 10000000 --protection 0.95 --cost-budget 0.02`', command: 'tail-risk --hedge --portfolio-value 10000000 --protection 0.95 --cost-budget 0.02', expectedOutput: 'Tail hedge: Buy 3-month 5% OTM SPX puts, rolling monthly. Cost: 2% annually ($200K). Protection: Portfolio floor at 85% of value ($8.5M). Max drawdown reduction: -50% to -15%' },
        { instruction: 'Tail hedging uses out-of-the-money options to protect against extreme market moves.' },
        { instruction: 'The cat tail hedge involves buying put options on the tuna market and sleeping soundly.' },
        { instruction: 'Evaluate hedge effectiveness: `tail-risk --evaluate --period 2020 --hedge-type puts`', command: 'tail-risk --evaluate --period 2020 --hedge-type puts', expectedOutput: '2020 COVID crash: Tail hedge paid +450% in March. Net portfolio impact: -8% vs -34% unhedged. Hedge cost: 2% annualized. Benefit-cost ratio: 22:1' },
      ],
      quiz: [
        { question: 'What is the typical cost of a tail hedging program as a percentage of portfolio value?', options: ['1-3% annually for meaningful downside protection', '0.1% annually', '10-15% annually', 'Tail hedging costs nothing'], correctIndex: 0, explanation: 'Tail hedging programs typically cost 1-3% of portfolio value per year, acting as an insurance premium against extreme market events.' },
      ],
    },
    {
      id: 'vix-trading',
      slug: 'vix-volatility-trading',
      title: 'VIX & Volatility Trading',
      description: 'Using the VIX for hedging and speculation.',
      commands: ['vix', 'tail-risk'],
      steps: [
        { instruction: 'Analyze VIX term structure: `vix --term-structure --date 2025-05-19`', command: 'vix --term-structure --date 2025-05-19', expectedOutput: 'VIX term structure: Spot 14.2, M1 16.8, M2 18.5, M3 19.2, M4 19.8, M5 20.1, M6 20.3 — contango. VIX futures premium: 2.6 points' },
        { instruction: 'The VIX measures implied volatility of S&P 500 options over the next 30 days.' },
        { instruction: 'When the VIX spikes, the cat hides under the bed — it is a volatility risk-off signal.' },
      ],
      quiz: [
        { question: 'What does the VIX index measure?', options: ['The implied volatility of S&P 500 index options over the next 30 days', 'The price of gold', 'The number of stocks trading up', 'The volume on the NYSE'], correctIndex: 0, explanation: 'The CBOE Volatility Index (VIX) measures the market expectation of 30-day forward S&P 500 volatility through option prices.' },
      ],
    },
    {
      id: 'crisis-alpha',
      slug: 'crisis-alpha-strategies',
      title: 'Crisis Alpha Strategies',
      description: 'Strategies that perform well during market crises.',
      commands: ['crisis-alpha', 'tail-risk', 'vix'],
      steps: [
        { instruction: 'Screen for crisis alpha strategies: `crisis-alpha --screen --period 2008,2020,2022`', command: 'crisis-alpha --screen --period 2008,2020,2022', expectedOutput: 'Crisis alpha: Long Treasuries (+15% in 2008, +11% in 2020, -13% in 2022), Gold (+5%, +8%, +0%), Trend following (+21%, +18%, +24%)' },
        { instruction: 'Crisis alpha refers to strategies that generate positive returns during market crises.' },
        { instruction: 'The cat crisis alpha strategy: hide under the bed until volatility subsides, then emerge victorious.' },
      ],
      quiz: [
        { question: 'What is crisis alpha?', options: ['Positive returns generated during market crises from strategies that thrive in volatility', 'Alpha generated by crisis management firms', 'Returns from distressed debt', 'Alpha from merger arbitrage'], correctIndex: 0, explanation: 'Crisis alpha refers to the positive returns that certain strategies like trend following and long volatility produce during periods of market stress.' },
      ],
    },
  ],
}
