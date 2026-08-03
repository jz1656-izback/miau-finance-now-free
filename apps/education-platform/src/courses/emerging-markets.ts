import type { Course } from '../lib/types'

export const emergingMarkets: Course = {
  id: 'emerging-markets',
  slug: 'emerging-markets',
  title: 'Emerging Markets',
  description: 'BRICS, frontier markets, country risk, and FX risk — the cat goes global.',
  category: 'Global Markets',
  difficulty: 'advanced',
  icon: '🌏',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'em-brics',
      slug: 'brics-emerging',
      title: 'BRICS & Major Emerging Markets',
      description: 'Brazil, Russia, India, China, South Africa, and beyond.',
      commands: ['emerging', 'emerging brics'],
      steps: [
        { instruction: 'Analyze BRICS markets: `emerging brics --compare`', command: 'emerging brics --compare', expectedOutput: 'BRICS comparison: GDP growth, inflation, market returns, and demographics' },
        { instruction: 'BRICS account for over 30% of global GDP and 40% of the world population.' },
        { instruction: 'Each BRICS nation has unique risks — China faces property debt, India infrastructure gaps.' },
      ],
      quiz: [
        { question: 'Which countries make up BRICS?', options: ['Brazil, Russia, India, China, South Africa', 'Britain, Russia, India, Canada, Spain', 'Brazil, Romania, Indonesia, Chile, Singapore', 'Belgium, Russia, Iran, China, Sweden'], correctIndex: 0, explanation: 'BRICS refers to Brazil, Russia, India, China, and South Africa — major emerging economies.' },
      ],
    },
    {
      id: 'em-frontier',
      slug: 'frontier-markets',
      title: 'Frontier Markets',
      description: 'Vietnam, Nigeria, Bangladesh, and the next wave of growth.',
      commands: ['brics', 'brics analysis'],
      steps: [
        { instruction: 'List frontier markets: `emerging frontier --list`', command: 'emerging frontier --list', expectedOutput: 'Frontier market rankings with GDP growth, market cap, and accessibility' },
        { instruction: 'Frontier markets are less developed than emerging markets but offer higher growth potential.' },
        { instruction: 'Key frontier markets: Vietnam, Nigeria, Bangladesh, Kenya, Kazakhstan.' },
      ],
      quiz: [
        { question: 'What distinguishes frontier markets from emerging markets?', options: ['Smaller size and less developed capital markets', 'Higher GDP per capita', 'Full market accessibility', 'Lower growth potential'], correctIndex: 0, explanation: 'Frontier markets are smaller, less accessible, and have less developed capital markets than emerging markets.' },
      ],
    },
    {
      id: 'em-country-risk',
      slug: 'country-risk',
      title: 'Country Risk Analysis',
      description: 'Political, economic, and sovereign risk assessment.',
      commands: ['country-risk', 'country-risk analysis'],
      steps: [
        { instruction: 'Run country risk analysis: `country-risk analysis --country Argentina`', command: 'country-risk analysis --country Argentina', expectedOutput: 'Country risk score: political, economic, and sovereign risk breakdown' },
        { instruction: 'Sovereign risk = risk of government default. Credit ratings (S&P, Moody\'s, Fitch) assess this.' },
        { instruction: 'Political risk includes expropriation, currency controls, and policy changes.' },
      ],
      quiz: [
        { question: 'What does a sovereign credit rating assess?', options: ['A government\'s ability to repay its debt', 'A company\'s creditworthiness', 'Stock market volatility', 'Currency stability'], correctIndex: 0, explanation: 'Sovereign credit ratings assess the creditworthiness of a national government and its ability to repay debt.' },
      ],
    },
    {
      id: 'em-fx-risk',
      slug: 'emerging-market-fx',
      title: 'Emerging Market FX Risk',
      description: 'Currency risk in emerging market investments.',
      commands: ['frontier', 'frontier invest'],
      steps: [
        { instruction: 'Analyze FX risk: `emerging fx --portfolio`', command: 'emerging fx --portfolio', expectedOutput: 'Currency exposure analysis with hedging recommendations' },
        { instruction: 'Emerging market currencies are more volatile and can wipe out equity returns.' },
        { instruction: 'Hedging FX risk with forwards or options is possible but adds cost.' },
      ],
      quiz: [
        { question: 'Why is FX risk significant in emerging markets?', options: ['Currencies are more volatile and can sharply depreciate', 'FX risk does not exist in emerging markets', 'All emerging currencies are pegged to USD', 'Central banks eliminate FX risk'], correctIndex: 0, explanation: 'Emerging market currencies tend to be more volatile, and sudden depreciations can significantly reduce investment returns in USD terms.' },
      ],
    },
  ],
}
