import type { Course } from '../lib/types'

export const sustainableInvesting: Course = {
  id: 'sustainable-investing',
  slug: 'sustainable-and-impact-investing',
  title: 'Sustainable & Impact Investing',
  description: 'Impact investing, green funds, SDGs, and community investing — the cat invests with a clear conscience and a green paw.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '🌱',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'si-intro',
      slug: 'impact-investing-basics',
      title: 'Impact Investing Basics',
      description: 'Putting money to work for good.',
      commands: ['impact', 'impact score'],
      steps: [
        { instruction: 'Check impact score of a fund: `impact score --fund "Global Impact Fund"`', command: 'impact score --fund "Global Impact Fund"', expectedOutput: 'Impact score: 85/100 — aligned with SDG 7, 13, 15' },
        { instruction: 'Impact investing seeks both financial return and measurable positive impact.' },
        { instruction: 'The cat\'s impact: one less mouse in the house per quarter.' },
      ],
      quiz: [
        { question: 'What distinguishes impact investing from traditional investing?', options: ['Intentional measurement of positive social or environmental outcomes', 'Higher returns guaranteed', 'Lower risk profile', 'Exclusive to institutional investors'], correctIndex: 0, explanation: 'Impact investing explicitly aims to generate measurable social or environmental benefits alongside financial returns.' },
      ],
    },
    {
      id: 'si-green',
      slug: 'green-funds-sustainable',
      title: 'Green Funds & Sustainable Finance',
      description: 'Evaluating environmentally friendly funds.',
      commands: ['sustainable', 'sustainable fund'],
      steps: [
        { instruction: 'Find top sustainable funds: `sustainable fund --category equity --region global --min-score 70`', command: 'sustainable fund --category equity --region global --min-score 70', expectedOutput: '6 sustainable funds found — highest ESG score: 92 (Eco-Growth Equity Fund)' },
        { instruction: 'Green funds invest in companies with strong environmental practices.' },
        { instruction: 'The cat prefers funds that invest in renewable catnip farms.' },
      ],
      quiz: [
        { question: 'What is greenwashing?', options: ['Misleading claims about environmental benefits of investments', 'Painting fund documents green', 'Investing in tree-planting companies', 'A legitimate sustainability certification'], correctIndex: 0, explanation: 'Greenwashing is when companies or funds overstate their environmental credentials to attract impact-conscious investors.' },
      ],
    },
    {
      id: 'si-sdg',
      slug: 'sdg-alignment',
      title: 'SDG Alignment',
      description: 'Mapping investments to UN goals.',
      commands: ['green-fund', 'green-fund compare'],
      steps: [
        { instruction: 'Compare green funds by ESG rating: `green-fund compare --funds fund-a, fund-b, fund-c`', command: 'green-fund compare --funds fund-a, fund-b, fund-c', expectedOutput: 'ESG comparison: fund-a (AA), fund-b (A), fund-c (BBB) — trailing returns, expense ratios' },
        { instruction: 'The 17 UN SDGs provide a framework for impact measurement.' },
        { instruction: 'The cat aligns with SDG 2 (Zero Hunger) and SDG 15 (Life on Land).' },
      ],
      quiz: [
        { question: 'How do investors use SDGs?', options: ['As a framework to align investments with global sustainability goals', 'As a tax reporting requirement', 'As a stock screening tool only', 'As a replacement for financial analysis'], correctIndex: 0, explanation: 'The UN Sustainable Development Goals help investors categorize and measure the societal impact of their investments.' },
      ],
    },
    {
      id: 'si-community',
      slug: 'community-investing',
      title: 'Community Investing',
      description: 'Local and community-focused finance.',
      commands: ['sdg', 'sdg track'],
      steps: [
        { instruction: 'Track SDG alignment of your portfolio: `sdg track --portfolio my-portfolio`', command: 'sdg track --portfolio my-portfolio', expectedOutput: 'Portfolio SDG alignment: SDG 7 (Clean Energy) 35%, SDG 13 (Climate) 25%, other SDGs 40%' },
        { instruction: 'Community investing directs capital to underserved local economies.' },
        { instruction: 'The cat invests in the local petting zoo — strong community vibes.' },
      ],
      quiz: [
        { question: 'What is community investing?', options: ['Directing capital to underserved communities and local development', 'Investing in community social media platforms', 'Funding neighborhood block parties', 'Local stock exchange investing'], correctIndex: 0, explanation: 'Community investing channels capital to low-income communities and underserved areas to promote economic development.' },
      ],
    },
  ],
}
