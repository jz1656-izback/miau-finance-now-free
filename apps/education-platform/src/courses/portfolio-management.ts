import type { Course } from '../lib/types'

export const portfolioManagement: Course = {
  id: 'portfolio-management',
  slug: 'portfolio-management',
  title: 'Portfolio Management',
  description: 'View, analyze, and export your portfolios.',
  category: 'Portfolio',
  difficulty: 'intermediate',
  icon: '💼',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'pm-list',
      slug: 'list',
      title: 'Listing Portfolios',
      description: 'See all your portfolios at a glance.',
      commands: ['portfolios', 'ls', 'df'],
      steps: [
        { instruction: 'List all portfolios: `portfolios`', command: 'portfolios', expectedOutput: 'Table of portfolios with IDs and values' },
        { instruction: 'Same thing with shortcuts: `ls` or `df`', command: 'ls', expectedOutput: 'Same output, shorter command' },
        { instruction: 'Note the portfolio IDs — you will need them.' },
      ],
      quiz: [
        { question: 'What is a shortcut for `portfolios`?', options: ['ls', 'pf', 'list', 'show'], correctIndex: 0, explanation: '`ls` and `df` are aliases for `portfolios`.' },
      ],
    },
    {
      id: 'pm-detail',
      slug: 'detail',
      title: 'Portfolio Details',
      description: 'Dive deep into a specific portfolio.',
      commands: ['portfolio', 'rm', 'positions'],
      steps: [
        { instruction: 'View portfolio details: `portfolio <id>`', command: 'portfolio 1', expectedOutput: 'Portfolio summary, value, returns' },
        { instruction: 'Check positions: `positions <id>`', command: 'positions 1', expectedOutput: 'Individual holdings with weight and P&L' },
      ],
      quiz: [
        { question: 'How do you see individual holdings within a portfolio?', options: ['positions <id>', 'portfolio <id>', 'holdings <id>', 'assets <id>'], correctIndex: 0, explanation: '`positions <id>` shows a breakdown of individual holdings.' },
      ],
    },
    {
      id: 'pm-export',
      slug: 'export',
      title: 'Exporting Portfolios',
      description: 'Download your data in CSV, JSON, or PDF.',
      commands: ['export'],
      steps: [
        { instruction: 'Export as CSV: `export <id> csv`', command: 'export 1 csv', expectedOutput: 'Download triggered' },
        { instruction: 'Try JSON format: `export <id> json`', command: 'export 1 json', expectedOutput: 'JSON download' },
        { instruction: 'PDF format for reports: `export <id> pdf`' },
      ],
      quiz: [
        { question: 'Which formats does `export` support?', options: ['CSV, JSON, PDF', 'Only CSV', 'Only JSON', 'Excel and PDF'], correctIndex: 0, explanation: '`export` supports CSV, JSON, and PDF export formats.' },
      ],
    },
    {
      id: 'pm-pnl',
      slug: 'pnl',
      title: 'Profit & Loss',
      description: 'Track your gains and losses over time.',
      commands: ['pnl', 'summary', 'ping'],
      steps: [
        { instruction: 'View P&L timeseries: `pnl`', command: 'pnl', expectedOutput: 'P&L over time displayed' },
        { instruction: 'Platform summary: `summary` or `ping`', command: 'summary', expectedOutput: 'API status, user count, system health' },
      ],
      quiz: [
        { question: 'What does `pnl` show?', options: ['Profit & Loss timeseries', 'People & Logistics', 'Price & Liquidity', 'Nothing'], correctIndex: 0, explanation: '`pnl` displays your Profit & Loss over time.' },
      ],
    },
  ],
}
