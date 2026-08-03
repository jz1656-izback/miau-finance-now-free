import type { Course } from '../lib/types'

export const circularEconomy: Course = {
  id: 'circular-economy',
  slug: 'circular-economy',
  title: 'Circular Economy & Blue Finance',
  description: 'Waste-to-value, ocean finance, biodiversity, and nature-based solutions — Prof. Tuna swims in circular currents.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '♻️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ce-circular',
      slug: 'circular-economy-basics',
      title: 'Circular Economy Fundamentals',
      description: 'From linear take-make-waste to circular regenerate-restore.',
      commands: ['circular', 'circular metrics'],
      steps: [
        { instruction: 'View circular economy metrics: `circular AAPL`', command: 'circular AAPL', expectedOutput: 'Circular material use, waste diversion, recyclability' },
        { instruction: 'Linear economy = take, make, waste. Circular economy = reduce, reuse, recycle, regenerate.' },
        { instruction: 'Screen for circular companies: `circular screen 70`', command: 'circular screen 70', expectedOutput: 'Companies with circularity score >= 70' },
      ],
      quiz: [
        { question: 'What does a circular economy prioritize?', options: ['Reduce, reuse, recycle, regenerate', 'Maximum production', 'Single-use materials', 'Planned obsolescence'], correctIndex: 0, explanation: 'The circular economy prioritizes reducing waste, reusing materials, recycling, and regenerating natural systems.' },
      ],
    },
    {
      id: 'ce-blue',
      slug: 'blue-finance',
      title: 'Blue Finance & Ocean Economy',
      description: 'Sustainable ocean investing, blue bonds, and marine biodiversity.',
      commands: ['blue', 'blue bond', 'blue economy'],
      steps: [
        { instruction: 'Explore blue economy: `blue`', command: 'blue', expectedOutput: 'Blue finance dashboard: ocean health, sustainable seafood, blue bonds' },
        { instruction: 'Blue bonds fund sustainable ocean projects — marine protected areas, sustainable fisheries, coastal resilience.' },
        { instruction: 'Check blue bond listings: `blue bond list`', command: 'blue bond list', expectedOutput: 'Active blue bonds with use-of-proceeds' },
      ],
      quiz: [
        { question: 'What do blue bonds finance?', options: ['Sustainable ocean projects', 'Renewable energy', 'Green buildings', 'Electric vehicles'], correctIndex: 0, explanation: 'Blue bonds fund projects that support ocean health, sustainable fisheries, marine conservation, and coastal resilience.' },
      ],
    },
    {
      id: 'ce-biodiversity',
      slug: 'biodiversity',
      title: 'Biodiversity & Natural Capital',
      description: 'Nature-related risks, TNFD, and biodiversity metrics.',
      commands: ['biodiversity', 'biodiversity risk', 'tnfd'],
      steps: [
        { instruction: 'Check biodiversity risk: `biodiversity risk AAPL`', command: 'biodiversity risk AAPL', expectedOutput: 'Land use, water stress, species impact, deforestation risk' },
        { instruction: 'TNFD = Taskforce on Nature-related Financial Disclosures. The biodiversity equivalent of TCFD.' },
        { instruction: 'View TNFD framework: `tnfd`', command: 'tnfd', expectedOutput: 'TNFD disclosure framework' },
      ],
      quiz: [
        { question: 'What does TNFD stand for?', options: ['Taskforce on Nature-related Financial Disclosures', 'Total Net Financial Debt', 'Taxonomy of Natural Financial Data', 'Transparent Natural Fund Distribution'], correctIndex: 0, explanation: 'TNFD is the Taskforce on Nature-related Financial Disclosures, focusing on biodiversity and natural capital.' },
      ],
    },
    {
      id: 'ce-waste',
      slug: 'waste-to-value',
      title: 'Waste-to-Value & Recycling',
      description: 'Investing in waste management, recycling technology, and circular supply chains.',
      commands: ['circular waste', 'circular recycling', 'circular supply-chain'],
      steps: [
        { instruction: 'Analyze waste management sector: `circular waste`', command: 'circular waste', expectedOutput: 'Waste-to-energy and recycling company analysis' },
        { instruction: 'Extended Producer Responsibility (EPR) laws are driving growth in recycling infrastructure.' },
        { instruction: 'Circular supply chain screen: `circular supply-chain`', command: 'circular supply-chain', expectedOutput: 'Companies with circular supply chain initiatives' },
      ],
      quiz: [
        { question: 'What is Extended Producer Responsibility?', options: ['Producers responsible for product end-of-life', 'Extended warranties for consumers', 'Longer production cycles', 'Government subsidies for producers'], correctIndex: 0, explanation: 'EPR makes producers responsible for the entire lifecycle of their products, including end-of-life disposal and recycling.' },
      ],
    },
  ],
}
