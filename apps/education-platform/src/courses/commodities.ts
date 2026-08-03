import type { Course } from '../lib/types'

export const commodities: Course = {
  id: 'commodities',
  slug: 'commodities',
  title: 'Commodities Trading',
  description: 'Gold, oil, agriculture, commodity ETFs, and futures — the cat trades raw materials.',
  category: 'Commodities',
  difficulty: 'intermediate',
  icon: '🛢️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'com-overview',
      slug: 'commodities-overview',
      title: 'Commodities Overview',
      description: 'Types of commodities and how they trade.',
      commands: ['commodities', 'commodities list'],
      steps: [
        { instruction: 'List all commodities: `commodities list`', command: 'commodities list', expectedOutput: 'Categories: energy, metals, agriculture, livestock with current prices' },
        { instruction: 'Hard commodities are mined or extracted (gold, oil). Soft commodities are grown (wheat, coffee).' },
        { instruction: 'Commodities are typically traded via futures contracts on exchanges.' },
      ],
      quiz: [
        { question: 'Which is a soft commodity?', options: ['Wheat', 'Gold', 'Crude oil', 'Copper'], correctIndex: 0, explanation: 'Soft commodities are agricultural products that are grown, like wheat, coffee, and cotton.' },
      ],
    },
    {
      id: 'com-gold',
      slug: 'gold-trading',
      title: 'Gold & Precious Metals',
      description: 'Gold as a store of value, inflation hedge, and portfolio diversifier.',
      commands: ['commodity', 'commodity gold'],
      steps: [
        { instruction: 'Analyze gold: `commodity gold --chart`', command: 'commodity gold --chart', expectedOutput: 'Gold price chart with moving averages and key levels' },
        { instruction: 'Gold is considered a safe haven during market turmoil and economic uncertainty.' },
        { instruction: 'Gold has an inverse correlation with real interest rates and the US dollar.' },
      ],
      quiz: [
        { question: 'Why is gold considered a safe haven?', options: ['It tends to hold value during market stress', 'It pays high dividends', 'It is backed by governments', 'It has low volatility'], correctIndex: 0, explanation: 'Gold is viewed as a safe haven because it tends to retain or increase value during economic uncertainty and market turmoil.' },
      ],
    },
    {
      id: 'com-oil',
      slug: 'oil-energy',
      title: 'Oil & Energy Commodities',
      description: 'Crude oil, natural gas, and energy market dynamics.',
      commands: ['gold', 'gold chart'],
      steps: [
        { instruction: 'Analyze crude oil: `oil --chart --type WTI`', command: 'oil --chart --type WTI', expectedOutput: 'WTI crude oil chart with supply/demand data' },
        { instruction: 'Brent vs WTI — Brent is the global benchmark, WTI is the US benchmark.' },
        { instruction: 'OPEC+ production decisions significantly influence oil prices.' },
      ],
      quiz: [
        { question: 'Which is the global benchmark for crude oil?', options: ['Brent Crude', 'WTI', 'Dubai Crude', 'Oman Crude'], correctIndex: 0, explanation: 'Brent Crude is the global benchmark for oil prices, while WTI is the primary US benchmark.' },
      ],
    },
    {
      id: 'com-futures',
      slug: 'commodity-futures',
      title: 'Commodity Futures & ETFs',
      description: 'Trade commodities through futures and ETFs.',
      commands: ['oil', 'oil analysis'],
      steps: [
        { instruction: 'View commodity ETFs: `commodities etf --list`', command: 'commodities etf --list', expectedOutput: 'List of commodity ETFs with expense ratios and holdings' },
        { instruction: 'Futures contracts have expiration dates — you must roll positions or take delivery.' },
        { instruction: 'Commodity ETFs offer easier access than futures but have tracking errors and expense ratios.' },
      ],
      quiz: [
        { question: 'What is contango in commodity futures?', options: ['Future prices are higher than spot prices', 'Spot prices are higher than futures prices', 'Prices are flat across months', 'The market is closed'], correctIndex: 0, explanation: 'Contango is when futures prices are higher than the current spot price, often due to storage costs.' },
      ],
    },
  ],
}
