import type { Course } from '../lib/types'

export const wealthManagement: Course = {
  id: 'wealth-management',
  slug: 'wealth-management-private-banking',
  title: 'Wealth Management & Private Banking',
  description: 'Private banking, family office, and wealth planning for the ultra-high-net-worth cat — because even cats need a butler for their tuna portfolio.',
  category: 'Advanced Finance',
  difficulty: 'advanced',
  icon: '💰',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'private-banking-basics',
      slug: 'private-banking-basics',
      title: 'Private Banking Fundamentals',
      description: 'Understanding private banking services for HNWIs.',
      commands: ['wealth', 'private-bank'],
      steps: [
        { instruction: 'Explore private banking services: `private-bank --services --min-balance 1000000`', command: 'private-bank --services --min-balance 1000000', expectedOutput: 'Private banking services: Wealth management, portfolio advisory, tax planning, concierge banking — minimum $1M AUM' },
        { instruction: 'Private banks offer personalized financial solutions beyond retail banking.' },
        { instruction: 'The cat opened a private banking account — the minimum balance was 500 cans of tuna.' },
        { instruction: 'Check your wealth tier: `wealth --tier --net-worth 5000000`', command: 'wealth --tier --net-worth 5000000', expectedOutput: 'Client tier: Platinum — dedicated relationship manager, priority lending, exclusive investment opportunities' },
      ],
      quiz: [
        { question: 'What is the typical minimum asset threshold for private banking services?', options: ['$1 million in investable assets', '$100,000', '$10 million', 'No minimum required'], correctIndex: 0, explanation: 'Private banking typically requires $1 million or more in investable assets for dedicated relationship management.' },
      ],
    },
    {
      id: 'family-office',
      slug: 'family-office-services',
      title: 'Family Office Services',
      description: 'Multi-family and single-family office structures.',
      commands: ['family-office', 'wealth'],
      steps: [
        { instruction: 'Explore family office setup: `family-office --setup --type single --net-worth 100000000`', command: 'family-office --setup --type single --net-worth 100000000', expectedOutput: 'Single Family Office structure: Dedicated team of 8, annual cost $1.2M, services include investment management, estate planning, tax, philanthropy' },
        { instruction: 'Family offices manage the financial affairs of wealthy families under one roof.' },
        { instruction: 'A cat family office manages the tuna inheritance across generations.' },
        { instruction: 'Compare family office types: `family-office --compare --types single,multi`', command: 'family-office --compare --types single,multi', expectedOutput: 'Single F.O.: Fully customized, $5M+ annual cost. Multi F.O.: Shared services, $500K+ annual cost, minimum $20M AUM' },
      ],
      quiz: [
        { question: 'What distinguishes a single-family office from a multi-family office?', options: ['Single-family office serves one family with full customization; multi-family shares resources across families', 'Single-family office is cheaper', 'Multi-family office only serves non-profits', 'There is no difference'], correctIndex: 0, explanation: 'A single-family office is dedicated to one wealthy family, while a multi-family office pools resources across multiple families for cost efficiency.' },
      ],
    },
    {
      id: 'wealth-planning',
      slug: 'wealth-planning-strategies',
      title: 'Wealth Planning Strategies',
      description: 'Comprehensive wealth planning for multi-generational wealth.',
      commands: ['wealth-plan', 'wealth'],
      steps: [
        { instruction: 'Create a wealth plan: `wealth-plan --create --goal "multi-generational" --timeframe 50-years`', command: 'wealth-plan --create --goal "multi-generational" --timeframe 50-years', expectedOutput: 'Wealth plan created: Multi-generational strategy, 50-year horizon, 5.5% target return, 25% tax efficiency, $200M projected in 50 years' },
        { instruction: 'Wealth planning covers investment, tax, estate, and philanthropic strategies.' },
        { instruction: 'The cat\'s wealth plan includes a dynasty trust for future generations of napping.' },
      ],
      quiz: [
        { question: 'Which of the following is a key component of comprehensive wealth planning?', options: ['Investment management, tax optimization, estate planning, and philanthropy', 'Only stock trading', 'Budgeting and coupon clipping', 'Day trading strategies'], correctIndex: 0, explanation: 'Wealth planning integrates investment, tax, estate, and philanthropic strategies to preserve and grow wealth across generations.' },
      ],
    },
    {
      id: 'uhnw-services',
      slug: 'ultra-high-net-worth-services',
      title: 'Ultra-High-Net-Worth Services',
      description: 'Specialized services for UHNW clients with $30M+.',
      commands: ['private-bank', 'wealth'],
      steps: [
        { instruction: 'Explore UHNW services: `private-bank --uhnw --services --threshold 30000000`', command: 'private-bank --uhnw --services --threshold 30000000', expectedOutput: 'UHNW Services ($30M+): Direct private equity, art advisory, aircraft finance, philanthropy structuring, family governance' },
        { instruction: 'UHNW clients require bespoke solutions across asset classes and jurisdictions.' },
        { instruction: 'A UHNW cat has a butler for its butler. That\'s how cat knows they made it.' },
      ],
      quiz: [
        { question: 'What additional services are typically offered to UHNW clients beyond standard private banking?', options: ['Direct PE, art advisory, aviation finance, and family governance', 'Free checking accounts', 'Higher credit card limits', 'Priority customer service hotline'], correctIndex: 0, explanation: 'UHNW clients receive bespoke services like direct private equity access, art advisory, aircraft finance, and family governance consulting.' },
      ],
    },
  ],
}
