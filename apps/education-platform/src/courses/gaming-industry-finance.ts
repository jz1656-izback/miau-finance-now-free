import type { Course } from '../lib/types'

export const gaming_industry_finance: Course = {
  id: 'gaming-industry-finance', slug: 'gaming-industry-finance', title: 'Gaming Industry Finance',
  description: 'A comprehensive cat-themed guide to Gaming Industry Finance. Learn how to analyze and invest in this sector.',
  category: 'Industry Analysis', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'gaming-industry-finance-1', slug: 'gaming-industry-finance-1', title: 'Sector Overview', description: 'Understanding the Gaming Industry Finance sector.',
      commands: ['help'], steps: [
        { instruction: 'Explore the Gaming Industry Finance sector and its key players.' },
        { instruction: 'The cat follows this sector closely. The fish are surprisingly knowledgeable.' },
      ], quiz: [{ question: 'Why is sector analysis important?', options: ['Different sectors have unique drivers and risks', 'All sectors behave the same', 'Sectors do not matter', 'Only technical analysis works'], correctIndex: 0, explanation: 'Each sector responds differently to economic conditions, requiring specialized analysis approaches.' }] },
    { id: 'gaming-industry-finance-2', slug: 'gaming-industry-finance-2', title: 'Key Metrics', description: 'Important metrics for Gaming Industry Finance.',
      commands: ['help'], steps: [
        { instruction: 'Learn the key financial metrics specific to this sector.' },
        { instruction: 'The cat tracks these metrics daily. It has a very detailed spreadsheet.' },
      ], quiz: [{ question: 'What is the most important metric in this sector?', options: ['Revenue growth and margins', 'Twitter followers', 'Office color scheme', 'CEO zodiac sign'], correctIndex: 0, explanation: 'Revenue growth and profit margins are fundamental metrics across all sectors.' }] },
    { id: 'gaming-industry-finance-3', slug: 'gaming-industry-finance-3', title: 'Investment Strategies', description: 'Strategies for Gaming Industry Finance investing.',
      commands: ['help'], steps: [
        { instruction: 'Apply sector-specific strategies to your portfolio.' },
        { instruction: 'The cats strategy: buy when others are fearful, sell when the tuna runs out.' },
      ], quiz: [{ question: 'How should you approach investing in this sector?', options: ['Diversify within the sector and focus on fundamentals', 'Invest everything in one company', 'Ignore the sector entirely', 'Follow social media hype'], correctIndex: 0, explanation: 'Even within a sector, diversification across multiple companies reduces single-stock risk.' }] },
  ],
}
