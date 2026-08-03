import type { Course } from '../lib/types'

export const businessCycles: Course = {
  id: 'business-cycles',
  slug: 'business-cycles',
  title: 'Business Cycles',
  description: 'Expansion, recession, leading indicators, and sector rotation — the cat knows when the economy needs a catnap.',
  category: 'Economics',
  difficulty: 'intermediate',
  icon: '🔄',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'cycle-phases',
      slug: 'business-cycle-phases',
      title: 'Business Cycle Phases',
      description: 'Expansion, peak, contraction, trough.',
      commands: ['cycle', 'cycle phase'],
      steps: [
        { instruction: 'Identify the current cycle phase: `cycle phase --country US --indicators gdp,employment,industrial`', command: 'cycle phase --country US --indicators gdp,employment,industrial', expectedOutput: 'Current phase: Late-cycle expansion — GDP growth 2.1%, unemployment 4.2%, capacity utilization 79%' },
        { instruction: 'The business cycle has four phases that repeat over years.' },
        { instruction: 'The cat\'s personal business cycle: eat, nap, zoomies, repeat.' },
      ],
      quiz: [
        { question: 'What typically characterizes a recession phase?', options: ['Two consecutive quarters of negative GDP growth', 'Rapid GDP growth and low unemployment', 'High inflation and rising wages', 'Stock market reaching all-time highs'], correctIndex: 0, explanation: 'A recession is broadly defined as two consecutive quarters of declining GDP, with rising unemployment and falling production.' },
      ],
    },
    {
      id: 'cycle-indicators',
      slug: 'leading-lagging-indicators',
      title: 'Leading & Lagging Indicators',
      description: 'Predicting where the cycle is headed.',
      commands: ['indicator', 'indicator list'],
      steps: [
        { instruction: 'List key economic indicators: `indicator list --type leading --country US`', command: 'indicator list --type leading --country US', expectedOutput: 'Leading indicators: yield curve (-0.4%), building permits (+2.1%), consumer confidence 98.5, M2 supply growth 3.2%' },
        { instruction: 'Leading indicators change before the economy, lagging indicators confirm trends.' },
        { instruction: 'The cat\'s leading indicator: tail position. Tail up = bullish, tail down = bearish.' },
      ],
      quiz: [
        { question: 'What is an example of a lagging economic indicator?', options: ['Unemployment rate — it rises after a recession has started', 'Stock market indices', 'Building permits', 'Consumer confidence'], correctIndex: 0, explanation: 'Unemployment is a lagging indicator because companies lay off workers after economic downturns are already underway.' },
      ],
    },
    {
      id: 'cycle-rotation',
      slug: 'sector-rotation-strategy',
      title: 'Sector Rotation Strategy',
      description: 'Moving capital through the cycle.',
      commands: ['rotation', 'rotation analyze'],
      steps: [
        { instruction: 'Analyze sector rotation opportunities: `rotation analyze --phase late-cycle --region US`', command: 'rotation analyze --phase late-cycle --region US', expectedOutput: 'Late-cycle sector picks: energy (+8.2%), healthcare (+5.1%), utilities (+4.5%) — avoid tech (-2.3%)' },
        { instruction: 'Different sectors perform best at different points in the business cycle.' },
        { instruction: 'The cat rotates between sunbeam spots throughout the day — same principle.' },
      ],
      quiz: [
        { question: 'Why do investors use sector rotation?', options: ['To allocate capital to sectors that historically outperform in the current cycle phase', 'To randomly pick winning stocks', 'To diversify across all sectors equally', 'To avoid stock market investing entirely'], correctIndex: 0, explanation: 'Sector rotation moves investments into sectors that tend to perform well during specific phases of the business cycle.' },
      ],
    },
    {
      id: 'cycle-recession',
      slug: 'recession-detection',
      title: 'Recession Detection & Preparation',
      description: 'Spotting and surviving downturns.',
      commands: ['recession', 'recession probability'],
      steps: [
        { instruction: 'Calculate recession probability: `recession probability --model yield-curve --spread -0.4`', command: 'recession probability --model yield-curve --spread -0.4', expectedOutput: 'Recession probability (12 months): 65% — yield curve inverted, leading indicators weakening' },
        { instruction: 'An inverted yield curve has preceded most US recessions.' },
        { instruction: 'The cat predicts recessions by observing hoomans stress-buying more tuna.' },
      ],
      quiz: [
        { question: 'What does an inverted yield curve suggest?', options: ['Short-term rates above long-term rates, signaling recession expectations', 'Long-term rates are significantly higher', 'The economy is growing rapidly', 'Inflation is well under control'], correctIndex: 0, explanation: 'An inverted yield curve (short rates > long rates) has historically been one of the most reliable recession predictors.' },
      ],
    },
  ],
}
