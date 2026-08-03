import type { Course } from '../lib/types'

export const climateRisk: Course = {
  id: 'climate-risk',
  slug: 'climate-risk',
  title: 'Climate Risk & Carbon Markets',
  description: 'Physical risk, transition risk, carbon credits, emissions trading — Prof. Tuna predicts a warming portfolio.',
  category: 'ESG',
  difficulty: 'advanced',
  icon: '🌍',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'cr-physical',
      slug: 'physical-risk',
      title: 'Physical Climate Risk',
      description: 'Assess how floods, fires, and storms impact your portfolio.',
      commands: ['climate risk', 'climate physical'],
      steps: [
        { instruction: 'Check physical risk for a stock: `climate risk AAPL --physical`', command: 'climate risk AAPL --physical', expectedOutput: 'Physical risk score: flood, wildfire, hurricane exposure' },
        { instruction: 'Physical risk = direct damage from climate events to assets, supply chains, and operations.' },
        { instruction: 'Screen portfolio for high physical risk: `climate risk portfolio 1 --physical`', command: 'climate risk portfolio 1 --physical', expectedOutput: 'Portfolio physical risk heatmap' },
      ],
      quiz: [
        { question: 'What does physical climate risk measure?', options: ['Direct damage from climate events', 'Regulatory change risk', 'Technology disruption risk', 'Market sentiment risk'], correctIndex: 0, explanation: 'Physical risk measures exposure to climate events like floods, wildfires, hurricanes, and sea-level rise.' },
      ],
    },
    {
      id: 'cr-transition',
      slug: 'transition-risk',
      title: 'Transition Risk',
      description: 'Policy changes, technology shifts, and market disruptions from the low-carbon transition.',
      commands: ['climate risk --transition', 'climate scenario'],
      steps: [
        { instruction: 'Check transition risk: `climate risk AAPL --transition`', command: 'climate risk AAPL --transition', expectedOutput: 'Transition risk score: policy, technology, market, reputation' },
        { instruction: 'Transition risk arises from the shift to a low-carbon economy — carbon taxes, regulation, changing consumer preferences.' },
        { instruction: 'Run a climate scenario: `climate scenario AAPL --2c`', command: 'climate scenario AAPL --2c', expectedOutput: 'Revenue at risk under 2°C scenario' },
      ],
      quiz: [
        { question: 'What is transition risk?', options: ['Risk from shifting to a low-carbon economy', 'Risk of extreme weather', 'Risk of sea-level rise', 'Risk of biodiversity loss'], correctIndex: 0, explanation: 'Transition risk stems from policy, technology, and market changes during the shift to a net-zero economy.' },
      ],
    },
    {
      id: 'cr-carbon-credits',
      slug: 'carbon-credits',
      title: 'Carbon Credits & Offsets',
      description: 'Understand carbon markets, credits, and offset quality.',
      commands: ['carbon market', 'carbon credit', 'carbon offset'],
      steps: [
        { instruction: 'View carbon markets: `carbon market`', command: 'carbon market', expectedOutput: 'EU ETS, voluntary carbon market prices' },
        { instruction: 'Check a carbon credit: `carbon credit BCT-2024`', command: 'carbon credit BCT-2024', expectedOutput: 'Credit type, vintage, registry, verification status' },
        { instruction: 'Voluntary carbon markets let companies offset emissions by buying credits from projects that reduce CO2.' },
      ],
      quiz: [
        { question: 'What are voluntary carbon markets?', options: ['Companies buy credits to offset emissions voluntarily', 'Government-mandated carbon trading', 'Stock market for green companies', 'Renewable energy subsidies'], correctIndex: 0, explanation: 'Voluntary carbon markets allow companies to voluntarily purchase carbon credits to offset their emissions.' },
      ],
    },
    {
      id: 'cr-paris',
      slug: 'paris-alignment',
      title: 'Paris Alignment & Net Zero',
      description: 'Measure portfolio temperature alignment and net-zero pathways.',
      commands: ['climate alignment', 'climate netzero', 'climate pathway'],
      steps: [
        { instruction: 'Check Paris alignment: `climate alignment AAPL`', command: 'climate alignment AAPL', expectedOutput: 'Temperature alignment score and benchmark' },
        { instruction: 'Net-zero pathway: `climate pathway portfolio 1 --netzero-2050`', command: 'climate pathway portfolio 1 --netzero-2050', expectedOutput: 'Year-by-year emission reduction pathway' },
        { instruction: 'The Paris Agreement aims to limit global warming to well below 2°C, pursuing 1.5°C.' },
      ],
      quiz: [
        { question: 'What temperature goal does the Paris Agreement pursue?', options: ['1.5°C above pre-industrial levels', '2.5°C above pre-industrial levels', '1.0°C above pre-industrial levels', '3.0°C above pre-industrial levels'], correctIndex: 0, explanation: 'The Paris Agreement aims to limit warming to well below 2°C, pursuing efforts to limit it to 1.5°C.' },
      ],
    },
  ],
}
