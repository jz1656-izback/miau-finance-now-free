import type { Course } from '../lib/types'

export const accountingForInvestors: Course = {
  id: 'accounting-for-investors',
  slug: 'accounting-for-investors',
  title: 'Accounting for Investors',
  description: 'Financial statements, ratios, and earnings quality — the cat reads the footnotes.',
  category: 'Accounting',
  difficulty: 'intermediate',
  icon: '📒',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'acct-statements',
      slug: 'financial-statements',
      title: 'Financial Statements',
      description: 'Read and interpret the three core financial statements.',
      commands: ['accounting', 'accounting statements'],
      steps: [
        { instruction: 'View company financials: `accounting statements --ticker AAPL`', command: 'accounting statements --ticker AAPL', expectedOutput: 'Income statement, balance sheet, and cash flow statement' },
        { instruction: 'The income statement shows revenue, expenses, and profit over a period.' },
        { instruction: 'The balance sheet shows assets, liabilities, and equity at a point in time.' },
      ],
      quiz: [
        { question: 'What does the balance sheet equation show?', options: ['Assets = Liabilities + Equity', 'Revenue - Expenses = Profit', 'Cash In - Cash Out = Net Cash', 'Assets = Revenue + Expenses'], correctIndex: 0, explanation: 'The accounting equation states that Assets = Liabilities + Shareholders\' Equity.' },
      ],
    },
    {
      id: 'acct-ratios',
      slug: 'financial-ratios',
      title: 'Financial Ratios',
      description: 'Use ratios to analyze company performance.',
      commands: ['financials', 'financials ratios'],
      steps: [
        { instruction: 'Calculate key ratios: `financials ratios --ticker AAPL`', command: 'financials ratios --ticker AAPL', expectedOutput: 'P/E, ROE, debt-to-equity, current ratio, and profit margin' },
        { instruction: 'ROE measures how efficiently a company generates profit from shareholder equity.' },
        { instruction: 'The current ratio (current assets / current liabilities) measures short-term liquidity.' },
      ],
      quiz: [
        { question: 'What does ROE measure?', options: ['Return on equity — profit generated per dollar of equity', 'Return on expenses', 'Rate of earnings', 'Revenue over equity'], correctIndex: 0, explanation: 'Return on Equity (ROE) measures net income as a percentage of shareholders\' equity, showing how well a company uses investor capital.' },
      ],
    },
    {
      id: 'acct-earnings',
      slug: 'earnings-quality',
      title: 'Earnings Quality',
      description: 'Detect accounting red flags and earnings manipulation.',
      commands: ['ratios', 'ratios analysis'],
      steps: [
        { instruction: 'Run earnings quality check: `accounting earnings-quality --ticker AAPL`', command: 'accounting earnings-quality --ticker AAPL', expectedOutput: 'Earnings quality score with accruals, revenue recognition, and red flags' },
        { instruction: 'High accruals relative to cash flow can signal earnings manipulation.' },
        { instruction: 'Watch for aggressive revenue recognition, changing depreciation methods, and one-time items.' },
      ],
      quiz: [
        { question: 'What is a red flag for earnings quality?', options: ['High accruals relative to operating cash flow', 'High profit margins', 'Consistent revenue growth', 'Low debt levels'], correctIndex: 0, explanation: 'High accruals (non-cash earnings) relative to operating cash flow can indicate aggressive accounting or earnings manipulation.' },
      ],
    },
    {
      id: 'acct-revenue',
      slug: 'revenue-recognition',
      title: 'Revenue Recognition',
      description: 'Understand when and how companies record revenue.',
      commands: ['earnings', 'earnings analysis'],
      steps: [
        { instruction: 'Analyze revenue recognition: `accounting revenue --ticker AAPL`', command: 'accounting revenue --ticker AAPL', expectedOutput: 'Revenue breakdown by segment and recognition method' },
        { instruction: 'ASC 606 requires revenue to be recognized when control of goods/services transfers to the customer.' },
        { instruction: 'Subscription revenue is recognized over time, not when cash is received.' },
      ],
      quiz: [
        { question: 'Under ASC 606, when is revenue recognized?', options: ['When control transfers to the customer', 'When cash is received', 'When the contract is signed', 'At the end of the fiscal year'], correctIndex: 0, explanation: 'ASC 606 requires revenue recognition when control of a good or service transfers to the customer, not necessarily when payment is received.' },
      ],
    },
  ],
}
