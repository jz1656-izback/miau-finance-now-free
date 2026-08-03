import type { Course } from '../lib/types'

export const fundamentals: Course = {
  id: 'fundamentals',
  slug: 'fundamentals',
  title: 'Fundamental Analysis',
  description: 'Company financials, earnings, and deep dive research.',
  category: 'Research',
  difficulty: 'intermediate',
  icon: '📑',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'fa-financials',
      slug: 'financials',
      title: 'Company Financials',
      description: 'View income statements, balance sheets, and cash flows.',
      commands: ['fundamentals'],
      steps: [
        { instruction: 'Get fundamentals: `fundamentals AAPL`', command: 'fundamentals AAPL', expectedOutput: 'Revenue, earnings, margins, ratios displayed' },
        { instruction: 'Shows key metrics: P/E, ROE, debt/equity, profit margins, and growth rates.' },
      ],
      quiz: [
        { question: 'What does `fundamentals` display?', options: ['Key financial ratios and metrics', 'Stock price only', 'News articles', 'Technical indicators'], correctIndex: 0, explanation: '`fundamentals` shows key financial data including ratios, margins, and growth metrics.' },
      ],
    },
    {
      id: 'fa-earnings',
      slug: 'earnings',
      title: 'Earnings Calendar',
      description: 'Track upcoming and past earnings reports.',
      commands: ['earnings'],
      steps: [
        { instruction: 'Earnings calendar: `earnings AAPL`', command: 'earnings AAPL', expectedOutput: 'Upcoming earnings dates and estimates' },
        { instruction: 'Shows expected EPS, revenue, and historical surprise data.' },
      ],
      quiz: [
        { question: 'What does `earnings` show?', options: ['Earnings dates and estimates', 'Stock price', 'Dividend yield', 'Company news'], correctIndex: 0, explanation: '`earnings` displays upcoming earnings dates with EPS and revenue estimates.' },
      ],
    },
    {
      id: 'fa-pipeline',
      slug: 'pipeline',
      title: 'Data Pipeline & Analysis',
      description: 'Monitor data pipeline runs and performance metrics.',
      commands: ['pipelines', 'calc pnl', 'optperf', 'performance'],
      steps: [
        { instruction: 'Check pipeline runs: `pipelines`', command: 'pipelines', expectedOutput: 'Recent pipeline jobs and status' },
        { instruction: 'Instrument performance: `performance AAPL`', command: 'performance AAPL', expectedOutput: 'Performance metrics breakdown' },
        { instruction: 'Optimizer performance: `optperf`', command: 'optperf', expectedOutput: 'Backend optimizer efficiency stats' },
      ],
      quiz: [
        { question: 'What does `pipelines` monitor?', options: ['Data pipeline job status', 'Stock prices', 'Trading orders', 'News feeds'], correctIndex: 0, explanation: '`pipelines` shows the status of data pipeline jobs.' },
      ],
    },
  ],
}
