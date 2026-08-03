import type { Course } from '../lib/types'

export const mergersAndAcquisitions: Course = {
  id: 'mergers-and-acquisitions',
  slug: 'mergers-and-acquisitions',
  title: 'Mergers & Acquisitions',
  description: 'M&A process, accretion/dilution, and deal types — the cat advises on deals.',
  category: 'Investment Banking',
  difficulty: 'advanced',
  icon: '🤝',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ma-process',
      slug: 'ma-process',
      title: 'The M&A Process',
      description: 'Understand how a deal comes together from start to finish.',
      commands: ['ma', 'ma process'],
      steps: [
        { instruction: 'Walk through the M&A process: `ma process`', command: 'ma process', expectedOutput: 'Step-by-step M&A process timeline' },
        { instruction: 'Phases: strategy → targeting → due diligence → valuation → negotiation → closing → integration.' },
        { instruction: 'Investment banks typically advise both buyers and sellers in M&A transactions.' },
      ],
      quiz: [
        { question: 'What comes after due diligence in the M&A process?', options: ['Valuation', 'Targeting', 'Integration', 'Closing'], correctIndex: 0, explanation: 'After due diligence comes valuation, then negotiation, then closing, and finally integration.' },
      ],
    },
    {
      id: 'ma-accretion',
      slug: 'accretion-dilution',
      title: 'Accretion & Dilution Analysis',
      description: 'Determine if a deal adds or subtracts value per share.',
      commands: ['merger', 'merger accretion'],
      steps: [
        { instruction: 'Run accretion/dilution analysis: `merger accretion --acquirer AAPL --target XYZ --premium 20`', command: 'merger accretion --acquirer AAPL --target XYZ --premium 20', expectedOutput: 'Accretion/dilution analysis with EPS impact' },
        { instruction: 'Accretive = the deal increases EPS. Dilutive = it decreases EPS.' },
        { instruction: 'Management typically wants accretive deals, but strategic value matters too.' },
      ],
      quiz: [
        { question: 'What does an accretive merger mean?', options: ['The deal increases earnings per share', 'The deal decreases earnings per share', 'The deal has no impact on earnings', 'The deal is tax-free'], correctIndex: 0, explanation: 'An accretive merger increases the combined company\'s earnings per share compared to the acquirer\'s standalone EPS.' },
      ],
    },
    {
      id: 'ma-deal-types',
      slug: 'deal-types',
      title: 'Types of M&A Deals',
      description: 'Horizontal, vertical, conglomerate, and more.',
      commands: ['ma types', 'ma examples'],
      steps: [
        { instruction: 'List deal types: `ma types`', command: 'ma types', expectedOutput: 'Descriptions of horizontal, vertical, conglomerate, and concentric mergers' },
        { instruction: 'Horizontal = competitors in the same industry. Vertical = buyer and seller in the same supply chain.' },
        { instruction: 'Conglomerate = unrelated businesses combining for diversification.' },
      ],
      quiz: [
        { question: 'What is a horizontal merger?', options: ['Two competitors in the same industry merge', 'A company acquires its supplier', 'A company acquires its distributor', 'Two unrelated companies merge'], correctIndex: 0, explanation: 'A horizontal merger involves two companies that operate in the same industry and are direct competitors.' },
      ],
    },
    {
      id: 'ma-financing',
      slug: 'deal-financing',
      title: 'Financing M&A Deals',
      description: 'Cash, stock, debt, and earnouts — how deals get funded.',
      commands: ['dilution', 'dilution calc'],
      steps: [
        { instruction: 'Calculate deal financing impact: `dilution calc --cash 1B --stock 0.5B --debt 0.5B`', command: 'dilution calc --cash 1B --stock 0.5B --debt 0.5B', expectedOutput: 'Financing structure with EPS impact breakdown' },
        { instruction: 'Cash deals are simple but deplete the balance sheet. Stock deals dilute existing shareholders.' },
        { instruction: 'Earnouts tie part of the purchase price to future performance targets.' },
      ],
      quiz: [
        { question: 'What is an earnout in M&A?', options: ['Additional payment based on future performance', 'A type of debt financing', 'The initial cash payment', 'A regulatory fee'], correctIndex: 0, explanation: 'An earnout is a contractual provision where the seller receives additional compensation if the business achieves specified future targets.' },
      ],
    },
  ],
}
