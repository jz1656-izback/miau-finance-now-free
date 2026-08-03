import type { Course } from '../lib/types'

export const globalMarkets: Course = {
  id: 'global-markets',
  slug: 'global-markets',
  title: 'Global Markets',
  description: 'Track exchanges worldwide, convert currencies, and trade across borders.',
  category: 'Markets',
  difficulty: 'intermediate',
  icon: '🌍',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'gm-global',
      slug: 'global',
      title: 'Global Market Overview',
      description: 'See what markets are open and how they are performing.',
      commands: ['global'],
      steps: [
        { instruction: 'Global overview: `global`', command: 'global', expectedOutput: 'Markets by region: Americas, Europe, Asia Pacific' },
        { instruction: 'Shows open/closed status, index values, and regional summaries.' },
        { instruction: 'Filter by region: `global Asia`' },
      ],
      quiz: [
        { question: 'What does the `global` command display?', options: ['Markets by region with status', 'Only US markets', 'Cryptocurrency data', 'Your portfolio'], correctIndex: 0, explanation: '`global` shows a region-by-region overview of global markets.' },
      ],
    },
    {
      id: 'gm-exchange',
      slug: 'exchange',
      title: 'Exchange Details',
      description: 'Zoom into a specific exchange.',
      commands: ['global <exchange>'],
      steps: [
        { instruction: 'View an exchange: `global NYSE`', command: 'global NYSE', expectedOutput: 'Exchange details with hours, indices, and key stocks' },
        { instruction: 'Try international exchanges: `global TSE` (Tokyo), `global LSE` (London).' },
      ],
      quiz: [
        { question: 'How do you view details for the Tokyo Stock Exchange?', options: ['global TSE', 'global tokyo', 'exchange TSE', 'market japan'], correctIndex: 0, explanation: '`global <exchange_code>` shows details for any exchange.' },
      ],
    },
    {
      id: 'gm-currency',
      slug: 'currency',
      title: 'Currency Management',
      description: 'Convert currencies and set base currency for portfolios.',
      commands: ['currency list', 'currency rates', 'currency convert', 'currency set'],
      steps: [
        { instruction: 'List currencies: `currency list`', command: 'currency list', expectedOutput: 'Supported currencies (20+ codes)' },
        { instruction: 'FX rates: `currency rates`', command: 'currency rates', expectedOutput: 'Live exchange rates vs USD' },
        { instruction: 'Convert: `currency convert 1000 EUR USD`', command: 'currency convert 1000 EUR USD', expectedOutput: 'Converted amount displayed' },
        { instruction: 'Set portfolio base: `currency set 1 EUR`', command: 'currency set 1 EUR', expectedOutput: 'Portfolio base currency changed' },
      ],
      quiz: [
        { question: 'How do you convert 500 USD to EUR?', options: ['currency convert 500 USD EUR', 'convert 500 usd eur', 'forex 500 USD EUR', 'exchange 500 USD EUR'], correctIndex: 0, explanation: '`currency convert <amt> <from> <to>` performs the conversion.' },
      ],
    },
    {
      id: 'gm-hours',
      slug: 'hours',
      title: 'Market Hours',
      description: 'Know when markets open and close.',
      commands: ['global'],
      steps: [
        { instruction: 'The `global` command shows which markets are currently open (green) and closed (dimmed).' },
        { instruction: 'Market hours account for daylight saving time and local holidays.' },
        { instruction: '19 global exchanges are tracked with real-time open/close status.' },
      ],
      quiz: [
        { question: 'How many global exchanges are tracked?', options: ['19', '5', '50', '100'], correctIndex: 0, explanation: 'The platform tracks 19 major exchanges worldwide with DST and holiday handling.' },
      ],
    },
  ],
}
