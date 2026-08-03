import type { Course } from '../lib/types'

export const south_american_markets_deep: Course = {
  id: 'south-american-markets-deep', slug: 'south-american-markets-deep', title: 'South American Markets Deep Dive',
  description: 'Explore South American Markets Deep Dive — the cat travels the world one market at a time.',
  category: 'Global Markets', difficulty: 'intermediate', icon: '🌍', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'south-american-markets-deep-1', slug: 'south-american-markets-deep-1', title: 'Market Overview', description: 'Understanding South American Markets Deep Dive.', commands: ['global'], steps: [
      { instruction: 'Explore South American Markets Deep Dive using the global markets command.' },
      { instruction: 'The cat has passports for all these markets. It is very well-traveled.' },
    ], quiz: [{ question: 'What is unique about this market?', options: ['It has distinct regulatory and cultural characteristics', 'It is exactly like all others', 'It does not matter', 'Only locals can trade'], correctIndex: 0, explanation: 'Each market has unique regulations, trading hours, settlement cycles, and cultural factors.' }] },
    { id: 'south-american-markets-deep-2', slug: 'south-american-markets-deep-2', title: 'Trading Mechanics', description: 'How to trade in this market.', commands: ['global'], steps: [
      { instruction: 'Learn the trading mechanics specific to this region.' },
      { instruction: 'The cat trades across all time zones. It naps strategically.' },
    ], quiz: [{ question: 'What should you check before trading in a new market?', options: ['Trading hours, settlement, currency, and regulations', 'The local food', 'The weather', 'The time zone only'], correctIndex: 0, explanation: 'Understanding trading hours, settlement cycles, currency risks, and local regulations is essential before trading in any market.' }] },
    { id: 'south-american-markets-deep-3', slug: 'south-american-markets-deep-3', title: 'Investment Opportunities', description: 'Opportunities in South American Markets Deep Dive.', commands: ['help'], steps: [
      { instruction: 'Identify unique opportunities in this market.' },
      { instruction: 'The cat found some excellent fish markets in this region.' },
    ], quiz: [{ question: 'How should you approach investing in this market?', options: ['Start with ETFs or ADRs before direct investment', 'Jump in immediately', 'Only invest locally', 'Ignore currency risk'], correctIndex: 0, explanation: 'ETFs and ADRs provide diversified exposure to foreign markets without the complexities of direct investment.' }] },
  ],
}
