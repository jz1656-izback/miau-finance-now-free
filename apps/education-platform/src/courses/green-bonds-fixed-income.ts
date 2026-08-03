import type { Course } from '../lib/types'

export const green_bonds_fixed_income: Course = {
  id: 'green-bonds-fixed-income', slug: 'green-bonds-fixed-income', title: 'Green Bonds & Fixed Income',
  description: 'A comprehensive cat-themed guide to Green Bonds & Fixed Income. Learn how to analyze and invest in this sector.',
  category: 'Fixed Income', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'green-bonds-fixed-income-1', slug: 'green-bonds-fixed-income-1', title: 'Sector Overview', description: 'Understanding the Green Bonds & Fixed Income sector.',
      commands: ['help'], steps: [
        { instruction: 'Explore the Green Bonds & Fixed Income sector and its key players.' },
        { instruction: 'The cat follows this sector closely. The fish are surprisingly knowledgeable.' },
      ], quiz: [{ question: 'Why is sector analysis important?', options: ['Different sectors have unique drivers and risks', 'All sectors behave the same', 'Sectors do not matter', 'Only technical analysis works'], correctIndex: 0, explanation: 'Each sector responds differently to economic conditions, requiring specialized analysis approaches.' }] },
    { id: 'green-bonds-fixed-income-2', slug: 'green-bonds-fixed-income-2', title: 'Key Metrics', description: 'Important metrics for Green Bonds & Fixed Income.',
      commands: ['help'], steps: [
        { instruction: 'Learn the key financial metrics specific to this sector.' },
        { instruction: 'The cat tracks these metrics daily. It has a very detailed spreadsheet.' },
      ], quiz: [{ question: 'What is the most important metric in this sector?', options: ['Revenue growth and margins', 'Twitter followers', 'Office color scheme', 'CEO zodiac sign'], correctIndex: 0, explanation: 'Revenue growth and profit margins are fundamental metrics across all sectors.' }] },
    { id: 'green-bonds-fixed-income-3', slug: 'green-bonds-fixed-income-3', title: 'Investment Strategies', description: 'Strategies for Green Bonds & Fixed Income investing.',
      commands: ['help'], steps: [
        { instruction: 'Apply sector-specific strategies to your portfolio.' },
        { instruction: 'The cats strategy: buy when others are fearful, sell when the tuna runs out.' },
      ], quiz: [{ question: 'How should you approach investing in this sector?', options: ['Diversify within the sector and focus on fundamentals', 'Invest everything in one company', 'Ignore the sector entirely', 'Follow social media hype'], correctIndex: 0, explanation: 'Even within a sector, diversification across multiple companies reduces single-stock risk.' }] },
  ],
}
