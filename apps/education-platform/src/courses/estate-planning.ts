import type { Course } from '../lib/types'

export const estatePlanning: Course = {
  id: 'estate-planning',
  slug: 'estate-planning-trusts',
  title: 'Estate Planning & Trusts',
  description: 'Trusts, wills, inheritance tax, and estate freezing — because the cat wants its tuna fortune to go to the right paws.',
  category: 'Wealth Management',
  difficulty: 'intermediate',
  icon: '📜',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'trust-fundamentals',
      slug: 'trust-fundamentals',
      title: 'Trust Fundamentals',
      description: 'Understanding trust structures and their uses.',
      commands: ['trust', 'estate'],
      steps: [
        { instruction: 'Explore trust types: `trust --types --jurisdiction US,UK,Offshore`', command: 'trust --types --jurisdiction US,UK,Offshore', expectedOutput: 'Trust types: Revocable (US), Irrevocable (US), Bare Trust (UK), Discretionary (UK), Offshore Purpose Trust' },
        { instruction: 'A trust is a fiduciary arrangement where a trustee holds assets for beneficiaries.' },
        { instruction: 'The cat set up a trust for its tuna — the trustee is a very serious golden retriever.' },
      ],
      quiz: [
        { question: 'What is a trust in estate planning?', options: ['A fiduciary arrangement where a trustee manages assets for beneficiaries', 'A type of investment account', 'A loan from a bank', 'A government program for retirees'], correctIndex: 0, explanation: 'A trust is a legal arrangement where a trustee holds and manages assets on behalf of designated beneficiaries.' },
      ],
    },
    {
      id: 'wills-probate',
      slug: 'wills-and-probate',
      title: 'Wills & Probate',
      description: 'Creating wills and navigating the probate process.',
      commands: ['will', 'estate'],
      steps: [
        { instruction: 'Draft a will: `will --draft --estate-value 5000000 --beneficiaries "spouse,children,charity"`', command: 'will --draft --estate-value 5000000 --beneficiaries "spouse,children,charity"', expectedOutput: 'Will drafted: $5M estate, 50% spouse, 30% children trust, 20% charity — executor appointed, guardianship clause included' },
        { instruction: 'A will outlines how assets are distributed after death and names guardians for minors.' },
        { instruction: 'The cat\'s will leaves all scratching posts to the neighborhood kittens.' },
        { instruction: 'Simulate probate: `will --probate --state California --estate 5000000`', command: 'will --probate --state California --estate 5000000', expectedOutput: 'Probate estimate: 12-18 months, legal fees ~$150K, executor fees ~$250K, estate tax due $0 (under federal exemption)' },
      ],
      quiz: [
        { question: 'What happens during probate?', options: ['A court validates the will, appoints an executor, and oversees asset distribution', 'The bank automatically distributes assets', 'The government takes all assets', 'Beneficiaries divide assets without oversight'], correctIndex: 0, explanation: 'Probate is the court-supervised process of validating a will and overseeing the proper distribution of assets.' },
      ],
    },
    {
      id: 'inheritance-tax',
      slug: 'inheritance-tax-planning',
      title: 'Inheritance Tax Planning',
      description: 'Strategies to minimize inheritance and estate taxes.',
      commands: ['inheritance', 'estate'],
      steps: [
        { instruction: 'Calculate estate tax: `inheritance --tax --estate 15000000 --state New-York --year 2025`', command: 'inheritance --tax --estate 15000000 --state New-York --year 2025', expectedOutput: 'Federal estate tax: $0 (under $13.61M exemption). NY state estate tax: $1,240,000 (estate over exemption threshold)' },
        { instruction: 'Annual gift exclusion allows tax-free transfers of $18K per recipient per year.' },
        { instruction: 'The cat uses the annual gift exclusion to give tuna tax-free to its kittens.' },
      ],
      quiz: [
        { question: 'What is the annual gift tax exclusion amount for 2025?', options: ['$18,000 per recipient', '$10,000 per recipient', '$50,000 per recipient', '$100,000 total'], correctIndex: 0, explanation: 'The annual gift tax exclusion allows individuals to gift up to $18,000 per recipient per year without triggering gift tax.' },
      ],
    },
    {
      id: 'estate-freezing',
      slug: 'estate-freezing-techniques',
      title: 'Estate Freezing Techniques',
      description: 'Freezing asset values to minimize future estate taxes.',
      commands: ['estate', 'trust'],
      steps: [
        { instruction: 'Analyze estate freeze: `estate --freeze --type "corporate" --current-value 10000000 --growth-rate 0.07`', command: 'estate --freeze --type "corporate" --current-value 10000000 --growth-rate 0.07', expectedOutput: 'Estate freeze analysis: $10M current value frozen at $10M. Future growth of $43.2M over 20 years accrues to beneficiaries — tax savings ~$12.8M' },
        { instruction: 'Estate freezing fixes the value of an asset for tax purposes while future growth goes to heirs.' },
        { instruction: 'The cat froze its tuna empire — future catnip harvests go directly to the kittens tax-free.' },
      ],
      quiz: [
        { question: 'What is the primary purpose of an estate freeze?', options: ['To fix the current value of assets and shift future growth to beneficiaries tax-efficiently', 'To freeze assets so they cannot be sold', 'To prevent asset values from decreasing', 'To freeze estate taxes at current rates'], correctIndex: 0, explanation: 'An estate freeze locks in the current value for tax purposes, allowing future appreciation to pass to beneficiaries with reduced tax implications.' },
      ],
    },
  ],
}
