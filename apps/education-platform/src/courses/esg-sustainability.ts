import type { Course } from '../lib/types'

export const esgSustainability: Course = {
  id: 'esg-sustainability',
  slug: 'esg-sustainability',
  title: 'ESG & Sustainability',
  description: 'Track ESG scores, carbon footprints, and green investments.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '🌱',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'esg-score',
      slug: 'score',
      title: 'ESG Scoring',
      description: 'View environmental, social, and governance scores.',
      commands: ['esg', 'esg portfolio', 'esg screen'],
      steps: [
        { instruction: 'Get ESG score: `esg AAPL`', command: 'esg AAPL', expectedOutput: 'E, S, G scores with total ESG rating' },
        { instruction: 'Portfolio ESG: `esg portfolio 1`', command: 'esg portfolio 1', expectedOutput: 'Weighted ESG score for your portfolio' },
        { instruction: 'Screen by ESG: `esg screen 70`', command: 'esg screen 60', expectedOutput: 'Only stocks with ESG >= 60' },
      ],
      quiz: [
        { question: 'What does the E in ESG stand for?', options: ['Environmental', 'Earnings', 'Equity', 'Efficiency'], correctIndex: 0, explanation: 'ESG = Environmental, Social, and Governance.' },
      ],
    },
    {
      id: 'esg-carbon',
      slug: 'carbon',
      title: 'Carbon Footprint',
      description: 'Measure and track carbon emissions.',
      commands: ['carbon', 'carbon portfolio'],
      steps: [
        { instruction: 'Stock carbon footprint: `carbon AAPL`', command: 'carbon AAPL', expectedOutput: 'Scope 1, 2, 3 emissions and carbon intensity' },
        { instruction: 'Portfolio carbon: `carbon portfolio 1`', command: 'carbon portfolio 1', expectedOutput: 'Total portfolio carbon footprint' },
        { instruction: 'Compare your portfolio emissions against benchmarks.' },
      ],
      quiz: [
        { question: 'How many carbon emission scopes are tracked?', options: ['3 (Scope 1, 2, 3)', '2', '5', '1'], correctIndex: 0, explanation: 'Three scopes are tracked: direct emissions (1), energy (2), and supply chain (3).' },
      ],
    },
    {
      id: 'esg-green',
      slug: 'green',
      title: 'Green Finance',
      description: 'Discover sustainable investment opportunities.',
      commands: ['green', 'green energy', 'green bonds', 'green funds'],
      steps: [
        { instruction: 'Green overview: `green`', command: 'green', expectedOutput: 'Sustainable finance dashboard' },
        { instruction: 'Renewable energy ETFs: `green energy`', command: 'green energy', expectedOutput: 'List of clean energy ETFs' },
        { instruction: 'Green bonds: `green bonds`', command: 'green bonds', expectedOutput: 'Green bond listings' },
        { instruction: 'Sustainable funds: `green funds`' },
      ],
      quiz: [
        { question: 'What does `green bonds` display?', options: ['Bonds funding environmental projects', 'Stock prices', 'Company bonds', 'Treasury bonds'], correctIndex: 0, explanation: '`green bonds` lists bonds that fund environmental and climate-related projects.' },
      ],
    },
    {
      id: 'esg-reporting',
      slug: 'reporting',
      title: 'Sustainability Reporting',
      description: 'Generate ESG reports and track temperature alignment.',
      commands: ['esg portfolio'],
      steps: [
        { instruction: 'Your portfolio ESG score includes temperature alignment — showing how your investments align with 1.5°C or 2°C climate goals.' },
        { instruction: 'Use `esg screen` to filter out fossil fuel companies or those below your minimum ESG threshold.' },
        { instruction: 'Regularly check `carbon portfolio` to monitor your financial carbon footprint.' },
      ],
      quiz: [
        { question: 'What does temperature alignment measure?', options: ['Portfolio alignment with climate goals', 'Stock price temperature', 'Market volatility', 'Trading volume'], correctIndex: 0, explanation: 'Temperature alignment shows how your portfolio aligns with Paris Agreement climate targets.' },
      ],
    },
  ],
}
