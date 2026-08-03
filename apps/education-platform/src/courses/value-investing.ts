import type { Course } from '../lib/types'

export const valueInvesting: Course = {
  id: 'value-investing',
  slug: 'value-investing-graham-dodd',
  title: 'Value Investing',
  description: 'Graham & Dodd, Buffett, margin of safety, intrinsic value, and circle of competence — the cat buys undervalued tuna while others chase sardines.',
  category: 'Investment Strategies',
  difficulty: 'intermediate',
  icon: '🧐',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'graham-dodd',
      slug: 'graham-and-dodd-philosophy',
      title: 'Graham & Dodd Philosophy',
      description: 'The founding principles of value investing.',
      commands: ['value', 'graham', 'intrinsic'],
      steps: [
        { instruction: 'Apply the Graham number: `value --graham --eps 5 --book-value 40`', command: 'value --graham --eps 5 --book-value 40', expectedOutput: 'Graham Number: sqrt(22.5 × 5 × 40) = $67.08. Current price: $85 — stock is OVERVALUED (trading above Graham Number)' },
        { instruction: 'Benjamin Graham is the father of value investing — he taught Warren Buffett.' },
        { instruction: 'The cat read "The Intelligent Investor" — it was mostly about intelligent cat investing.' },
      ],
      quiz: [
        { question: 'What is the Graham Number?', options: ['A formula estimating the fair value of a stock based on EPS and book value', 'The number of Graham\'s books sold', 'A type of moving average', 'A portfolio allocation metric'], correctIndex: 0, explanation: 'The Graham Number calculates a stock\'s maximum fair price as the square root of (22.5 × earnings per share × book value per share).' },
      ],
    },
    {
      id: 'margin-of-safety',
      slug: 'margin-of-safety-principle',
      title: 'Margin of Safety',
      description: 'The cornerstone of value investing risk management.',
      commands: ['margin-safety', 'value', 'intrinsic'],
      steps: [
        { instruction: 'Calculate margin of safety: `margin-safety --calculate --intrinsic 100 --current-price 70`', command: 'margin-safety --calculate --intrinsic 100 --current-price 70', expectedOutput: 'Margin of safety: 30% (($100 - $70) / $100). Risk assessment: ADEQUATE (target >25%). Buy zone: YES' },
        { instruction: 'Margin of safety is the difference between intrinsic value and market price.' },
        { instruction: 'The cat insists on a 50% margin of safety — it wants to be very safe about its tuna investments.' },
      ],
      quiz: [
        { question: 'What does a 30% margin of safety mean?', options: ['The stock is trading 30% below its estimated intrinsic value', 'The stock is 30% overvalued', 'The stock has 30% less risk than the market', 'The stock pays a 30% dividend'], correctIndex: 0, explanation: 'A margin of safety of 30% means the stock price is 30% below the estimated intrinsic value, providing a cushion against errors in valuation.' },
      ],
    },
    {
      id: 'intrinsic-value',
      slug: 'intrinsic-value-valuation',
      title: 'Intrinsic Value & DCF',
      description: 'Calculating intrinsic value using DCF analysis.',
      commands: ['intrinsic', 'value'],
      steps: [
        { instruction: 'Run a DCF valuation: `intrinsic --dcf --ticker AAPL --growth-5yr 0.08 --terminal-growth 0.03 --wacc 0.10`', command: 'intrinsic --dcf --ticker AAPL --growth-5yr 0.08 --terminal-growth 0.03 --wacc 0.10', expectedOutput: 'AAPL intrinsic value: $198/share. Current price: $175. Margin of safety: 13.2%. DCF assumptions: 5yr growth 8%, terminal 3%, WACC 10%' },
        { instruction: 'Discounted Cash Flow (DCF) estimates intrinsic value by projecting future cash flows.' },
        { instruction: 'The cat built a DCF model — the terminal value is mostly tuna-based cash flows.' },
      ],
      quiz: [
        { question: 'What is the key assumption that most impacts a DCF valuation?', options: ['The terminal growth rate assumption', 'The stock price', 'The dividend yield', 'The market capitalization'], correctIndex: 0, explanation: 'The terminal growth rate has an outsized impact on DCF valuations because it determines the value of cash flows beyond the projection period.' },
      ],
    },
    {
      id: 'circle-of-competence',
      slug: 'circle-of-competence-investing',
      title: 'Circle of Competence',
      description: 'Staying within your circle of competence.',
      commands: ['value', 'graham'],
      steps: [
        { instruction: 'Define your circle of competence: `value --circle --industries "technology,consumer-goods,healthcare"`', command: 'value --circle --industries "technology,consumer-goods,healthcare"', expectedOutput: 'Circle of competence: Technology (strong), Consumer goods (moderate), Healthcare (basic). Recommendation: Focus on tech and consumer goods' },
        { instruction: 'The circle of competence means only investing in businesses you truly understand.' },
        { instruction: 'The cat\'s circle of competence: tuna, salmon, catnip, and scratching post manufacturers.' },
      ],
      quiz: [
        { question: 'What is Buffett\'s "circle of competence" concept?', options: ['Only invest in businesses and industries you can thoroughly understand and analyze', 'Invest in everything equally', 'Only invest in companies you worked for', 'Invest only in circular economy companies'], correctIndex: 0, explanation: 'The circle of competence advises investors to stay within industries and business models they deeply understand to avoid costly mistakes.' },
      ],
    },
  ],
}
