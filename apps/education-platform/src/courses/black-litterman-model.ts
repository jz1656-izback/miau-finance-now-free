import type { Course } from '../lib/types'

export const blackLittermanModel: Course = {
  id: 'black-litterman-model',
  slug: 'black-litterman-model',
  title: 'Black-Litterman Portfolio Model',
  description: 'Combine market equilibrium with your own views to build optimized portfolios — the cat balances market wisdom with gut instinct.',
  category: 'Quantitative',
  difficulty: 'advanced',
  icon: '🧮',
  lessonCount: 3,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'bl-intro',
      slug: 'bl-intro',
      title: 'Introduction to Black-Litterman',
      description: 'How the model combines prior beliefs with market data.',
      commands: ['blacklitterman SPY,TLT,GLD'],
      steps: [
        { instruction: 'Run basic Black-Litterman: `blacklitterman SPY,TLT,GLD`', command: 'blacklitterman SPY,TLT,GLD', expectedOutput: 'Prior returns, posterior weights, covariance matrix' },
        { instruction: 'The model starts with market-cap weights (equilibrium) and adjusts based on your views.' },
        { instruction: 'The cat believes tuna will outperform salmon by 5%. Black-Litterman quantifies this belief.' },
      ],
      quiz: [
        { question: 'What is the starting point of the Black-Litterman model?', options: ['Market equilibrium (CAPM-based returns)', 'Equal weights', 'Random weights', 'Last year returns'], correctIndex: 0, explanation: 'Black-Litterman starts with market-capitalization weights as the neutral prior, then adjusts for investor views.' },
      ],
    },
    {
      id: 'bl-views',
      slug: 'bl-views',
      title: 'Incorporating Investor Views',
      description: 'Express your market opinions quantitatively.',
      commands: ['blacklitterman SPY,TLT,GLD,GLD,IAU'],
      steps: [
        { instruction: 'Run with more assets: `blacklitterman SPY,TLT,GLD,GLD,IAU`', command: 'blacklitterman SPY,TLT,GLD,GLD,IAU', expectedOutput: 'Posterior weights for each asset' },
        { instruction: 'Add view tickers and expected returns to tilt the model toward your convictions.' },
        { instruction: 'The cats view: tuna will outperform (confidence: high, based on extensive tasting).' },
      ],
      quiz: [
        { question: 'What happens when you express a high-confidence bullish view on an asset?', options: ['The model increases its weight in the posterior portfolio', 'The model ignores it as noise', 'The asset is removed from the portfolio', 'The view is applied to all assets'], correctIndex: 0, explanation: 'High-confidence views shift portfolio weights toward the expressed direction, while low-confidence views are tempered by the prior.' },
      ],
    },
    {
      id: 'bl-practical',
      slug: 'bl-practical',
      title: 'Practical Portfolio Applications',
      description: 'Use Black-Litterman for real portfolio decisions.',
      commands: ['riskparity SPY,TLT,GLD'],
      steps: [
        { instruction: 'Compare with risk parity: `riskparity SPY,TLT,GLD`', command: 'riskparity SPY,TLT,GLD', expectedOutput: 'Equal risk contribution weights vs Black-Litterman' },
        { instruction: 'Black-Litterman produces more stable and intuitive portfolios than pure mean-variance optimization.' },
        { instruction: 'The cat uses Black-Litterman to decide how much tuna vs salmon to hold. The prior is 50/50.' },
      ],
      quiz: [
        { question: 'Why does Black-Litterman often produce more intuitive portfolios than Markowitz?', options: ['It starts from market equilibrium and tilts only as much as confidence warrants', 'It ignores correlations', 'It uses equal weights', 'It only invests in one asset'], correctIndex: 0, explanation: 'Pure mean-variance optimization often produces extreme weights. Black-Litterman starts from reasonable market-cap weights and only deviates based on expressed views.' },
      ],
    },
  ],
}
