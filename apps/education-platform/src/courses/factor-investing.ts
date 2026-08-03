import type { Course } from '../lib/types'

export const factorInvesting: Course = {
  id: 'factor-investing',
  slug: 'factor-investing-smart-beta',
  title: 'Factor Investing & Smart Beta',
  description: 'Value, momentum, size, quality, and low volatility factors — the cat factors its returns like a quantitative feline.',
  category: 'Investment Strategies',
  difficulty: 'advanced',
  icon: '📐',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'factor-basics',
      slug: 'factor-investing-fundamentals',
      title: 'Factor Investing Fundamentals',
      description: 'Understanding investment factors and their premiums.',
      commands: ['factor', 'smart-beta'],
      steps: [
        { instruction: 'Explore factor definitions: `factor --list --premiums`', command: 'factor --list --premiums', expectedOutput: 'Factors: Value (HML) +4.2%, Momentum (WML) +8.1%, Size (SMB) +2.5%, Quality (QMJ) +3.8%, Low Vol (BAB) +5.3% — annualized premiums since 1963' },
        { instruction: 'Factors are persistent characteristics that explain differences in asset returns.' },
        { instruction: 'The cat loaded its factor zoo — now it has more factors than it has whiskers.' },
      ],
      quiz: [
        { question: 'What are factor premiums in investing?', options: ['Persistent, long-term excess returns associated with specific stock characteristics', 'Premium prices paid for popular stocks', 'Fees charged by factor-based funds', 'Short-term trading profits'], correctIndex: 0, explanation: 'Factor premiums are the long-term excess returns that certain stock characteristics (like value or momentum) have historically delivered over the market.' },
      ],
    },
    {
      id: 'value-momentum',
      slug: 'value-and-momentum-factors',
      title: 'Value & Momentum Factors',
      description: 'Deep dive into the two most established factors.',
      commands: ['value-factor', 'momentum', 'factor'],
      steps: [
        { instruction: 'Analyze value factor performance: `value-factor --performance --period 2020-2025`', command: 'value-factor --performance --period 2020-2025', expectedOutput: 'Value factor (HML): 2020: -12%, 2021: +8%, 2022: +22%, 2023: +5%, 2024: +3%, 2025 YTD: +2% — 5yr cumulative: +26%' },
        { instruction: 'The value factor buys cheap stocks; the momentum factor buys stocks with strong recent returns.' },
        { instruction: 'The cat\'s value factor is purring — it found a cheap tuna stock with a 10% margin of safety.' },
        { instruction: 'Check momentum: `momentum --screen --top-20 --period 6mo`', command: 'momentum --screen --top-20 --period 6mo', expectedOutput: 'Top momentum stocks: NVDA +145%, PLTR +89%, MSTR +67%, TSLA +42%, META +35% — 6-month return momentum factor' },
      ],
      quiz: [
        { question: 'What is the basic premise of the momentum factor?', options: ['Stocks that have performed well recently tend to continue performing well in the near term', 'Stocks that have gone down will rebound', 'Momentum stocks have low volatility', 'Momentum guarantees positive returns'], correctIndex: 0, explanation: 'The momentum factor captures the tendency of stocks with strong recent performance to continue outperforming over the following months.' },
      ],
    },
    {
      id: 'smart-beta',
      slug: 'smart-beta-strategies',
      title: 'Smart Beta Strategies',
      description: 'Building factor-based investment strategies.',
      commands: ['smart-beta', 'factor'],
      steps: [
        { instruction: 'Construct a smart beta portfolio: `smart-beta --construct --factors "value,momentum,quality" --tilt 0.3 --universe SP500`', command: 'smart-beta --construct --factors "value,momentum,quality" --tilt 0.3 --universe SP500', expectedOutput: 'Smart beta portfolio: Multi-factor (value 30%, momentum 30%, quality 30%, market 10%). Expected tracking error 2.5%, information ratio 0.6' },
        { instruction: 'Smart beta strategies weight securities based on factor exposures rather than market cap.' },
        { instruction: 'The cat\'s smart beta strategy is smarter than the average bear — it factors in nap time.' },
      ],
      quiz: [
        { question: 'How do smart beta strategies differ from traditional cap-weighted indexing?', options: ['Smart beta weights securities based on factor exposures rather than market capitalization', 'Smart beta is always actively managed', 'Smart beta uses leverage', 'Smart beta only invests in growth stocks'], correctIndex: 0, explanation: 'Smart beta strategies apply alternative weighting schemes based on factors like value, momentum, or low volatility, deviating from traditional market-cap weighting.' },
      ],
    },
    {
      id: 'factor-timing',
      slug: 'factor-timing-strategies',
      title: 'Factor Timing & Implementation',
      description: 'Timing factor exposures and implementing factor strategies.',
      commands: ['factor', 'momentum'],
      steps: [
        { instruction: 'Analyze factor timing signals: `factor --timing --signal "value-vs-growth" --current-regime`', command: 'factor --timing --signal "value-vs-growth" --current-regime', expectedOutput: 'Current regime: Late-cycle (yield curve inverted for 14mo). Factor recommendation: Overweight quality, underweight value, neutral momentum' },
        { instruction: 'Factor timing attempts to adjust factor exposures based on economic conditions.' },
        { instruction: 'The cat\'s factor timing model says overweight quality — the cat is nothing if not high quality.' },
      ],
      quiz: [
        { question: 'Why is factor timing considered challenging?', options: ['Factors can have long periods of underperformance and regime changes are hard to predict', 'Factors never change', 'Factor timing is illegal', 'Factor correlations are perfectly stable'], correctIndex: 0, explanation: 'Factor timing is difficult because factors can underperform for extended periods and economic regime changes are notoriously hard to predict.' },
      ],
    },
  ],
}
