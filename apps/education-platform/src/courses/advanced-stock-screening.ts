import type { Course } from '../lib/types'

export const advancedStockScreening: Course = {
  id: 'advanced-stock-screening',
  slug: 'advanced-stock-screening',
  title: 'Advanced Stock Screening & Quant Analysis',
  description: 'Piotroski F-Score, Altman Z, DCF fair value, ETF overlap, and passive flow — the cat analyzes stocks like a quant hedge fund.',
  category: 'Quantitative',
  difficulty: 'intermediate',
  icon: '🔬',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'quant-health',
      slug: 'quant-health-scores',
      title: 'Quant Health Scores',
      description: 'Piotroski, Altman Z, and Beneish M-Score.',
      commands: ['quanthealth AAPL', 'quanthealth TSLA'],
      steps: [
        { instruction: 'Run quant health: `quanthealth AAPL` — Piotroski F-Score, Altman Z, Beneish M', command: 'quanthealth AAPL', expectedOutput: 'Piotroski F-Score /9, Altman Z-Score, Beneish M-Score' },
        { instruction: 'The Piotroski F-Score (0-9) measures financial strength. 7+ is strong, 4-6 is mixed, 0-3 is weak.' },
        { instruction: 'Compare two tickers: `quanthealth JPM` and `quanthealth MS` to see which is healthier', command: 'quanthealth JPM', expectedOutput: 'Banking sector quant health comparison' },
        { instruction: 'The cat scored 9/9 on the Piotroski test. It has very strong financials. In tuna.' },
      ],
      quiz: [
        { question: 'What does an Altman Z-Score below 1.8 indicate?', options: ['High bankruptcy risk — the company is in the distress zone', 'Strong financial health', 'The stock is undervalued', 'The company has positive cash flow'], correctIndex: 0, explanation: 'Altman Z-Score below 1.8 indicates the company is in the distress zone with elevated bankruptcy risk. Above 3.0 is considered safe.' },
      ],
    },
    {
      id: 'dcf-valuation',
      slug: 'dcf-fair-value',
      title: 'DCF Fair Value',
      description: 'Calculate intrinsic value using discounted cash flow.',
      commands: ['fairvalue AAPL', 'fairvalue MSFT'],
      steps: [
        { instruction: 'Find fair value: `fairvalue AAPL` — see if Apple is over/undervalued', command: 'fairvalue AAPL', expectedOutput: 'Current price vs fair value with upside/downside %' },
        { instruction: 'DCF values a company by projecting future cash flows and discounting them back.' },
        { instruction: 'The cat valued a tuna company at $1B. It is currently trading at 3 cans of tuna.' },
        { instruction: 'Check a different ticker: `fairvalue TSLA` to compare valuations', command: 'fairvalue TSLA', expectedOutput: 'TSLA DCF fair value with upside %' },
      ],
      quiz: [
        { question: 'What does a positive upside % in fairvalue mean?', options: ['The stock appears undervalued — the DCF fair price is above the current market price', 'The stock is guaranteed to go up', 'The company has strong earnings', 'The market is inefficient'], correctIndex: 0, explanation: 'A positive upside means the DCF-calculated fair value exceeds the current market price, suggesting the stock may be undervalued relative to its intrinsic value.' },
      ],
    },
    {
      id: 'etf-analysis',
      slug: 'etf-overlap-analysis',
      title: 'ETF & Passive Flow Analysis',
      description: 'See ETF holdings, overlap, and passive ownership.',
      commands: ['etfanalyzer SPY', 'passiveflow AAPL'],
      steps: [
        { instruction: 'Analyze an ETF: `etfanalyzer SPY` — see top holdings', command: 'etfanalyzer SPY', expectedOutput: 'SPY top holdings with weights' },
        { instruction: 'Check passive ownership: `passiveflow AAPL` — what % is trapped in passive ETFs', command: 'passiveflow AAPL', expectedOutput: 'Passive ownership percentage and top ETF holders' },
        { instruction: 'The cat checked passive flow for its tuna stock. 100% of it is in the cat\'s bowl.' },
        { instruction: 'Compare two ETFs: `etfanalyzer QQQ` vs `etfanalyzer VOO`', command: 'etfanalyzer QQQ', expectedOutput: 'QQQ top holdings' },
      ],
      quiz: [
        { question: 'What is "passive flow" in stock analysis?', options: ['The percentage of a stock held by passive/index ETFs, indicating potential selling pressure from rebalancing', 'The flow of cash through a company', 'The trading volume of a stock', 'The dividend payment schedule'], correctIndex: 0, explanation: 'Passive flow measures how much of a stock is owned by passive/index ETFs. High passive ownership means more mechanical buying/selling from ETF rebalancing.' },
      ],
    },
    {
      id: 'screening-workflow',
      slug: 'screening-workflow',
      title: 'Full Screening Workflow',
      description: 'Put it all together — find quality stocks.',
      commands: ['quanthealth JPM', 'fairvalue JPM', 'passiveflow JPM'],
      steps: [
        { instruction: 'Full screening workflow for JPMorgan: 1) Check health: `quanthealth JPM`', command: 'quanthealth JPM', expectedOutput: 'JPM financial health scores' },
        { instruction: '2) Check valuation: `fairvalue JPM` — is it fairly priced?', command: 'fairvalue JPM', expectedOutput: 'JPM fair value' },
        { instruction: '3) Check passive ownership: `passiveflow JPM`', command: 'passiveflow JPM', expectedOutput: 'JPM passive flow' },
        { instruction: 'The cat screened 500 stocks and found the best one: tuna futures. Always invest in tuna.' },
      ],
      quiz: [
        { question: 'What is the recommended order for screening a stock?', options: ['Check quant health first (is it a good company?), then fair value (is it priced right?), then passive flow', 'Buy first, ask questions later', 'Only check the stock price', 'Read the news and guess'], correctIndex: 0, explanation: 'A systematic approach: 1) Financial health (can it survive?), 2) Valuation (is it priced fairly?), 3) Ownership structure (who else owns it?).' },
      ],
    },
  ],
}
