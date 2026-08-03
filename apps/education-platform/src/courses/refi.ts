import type { Course } from '../lib/types'

export const regenerativeFinance: Course = {
  id: 'regenerative-finance',
  slug: 'regenerative-finance-refi',
  title: 'Regenerative Finance (ReFi)',
  description: 'Carbon credits, ecological assets, and circular economy — the cat regenerates the planet one pawprint at a time.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '🌿',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'refi-intro',
      slug: 'regenerative-finance-basics',
      title: 'Regenerative Finance Basics',
      description: 'Moving beyond sustainable to regenerative.',
      commands: ['refi', 'refi overview'],
      steps: [
        { instruction: 'Get a ReFi ecosystem overview: `refi overview --sector carbon,biodiversity,oceans`', command: 'refi overview --sector carbon,biodiversity,oceans', expectedOutput: 'ReFi landscape: 45 protocols, $2.1B total value locked, 12M tons carbon credits issued' },
        { instruction: 'ReFi goes beyond "do no harm" to actively regenerate ecosystems.' },
        { instruction: 'The cat practices ReFi by regenerating its cardboard box empire.' },
      ],
      quiz: [
        { question: 'How does ReFi differ from traditional ESG investing?', options: ['ReFi actively restores ecosystems rather than just reducing harm', 'ReFi ignores environmental issues', 'ReFi only focuses on social impact', 'ReFi is the same as impact investing'], correctIndex: 0, explanation: 'Regenerative finance aims to create net-positive environmental outcomes by restoring degraded ecosystems.' },
      ],
    },
    {
      id: 'refi-carbon',
      slug: 'carbon-credits-markets',
      title: 'Carbon Credits & Markets',
      description: 'Tokenized carbon offsets on-chain.',
      commands: ['carbon', 'carbon credit'],
      steps: [
        { instruction: 'Buy tokenized carbon credits: `carbon credit --buy --amount 100 --project "Amazon Reforestation"`', command: 'carbon credit --buy --amount 100 --project "Amazon Reforestation"', expectedOutput: '100 carbon credits purchased: 100 tons CO2 offset, credits retired on-chain, certificate generated' },
        { instruction: 'Carbon credits represent one ton of CO2 removed or avoided.' },
        { instruction: 'The cat offsets its carbon paw print by planting virtual catnip.' },
      ],
      quiz: [
        { question: 'What does a tokenized carbon credit represent?', options: ['Verified removal or avoidance of one metric ton of CO2', 'A share in a carbon trading company', 'A cryptocurrency mined with renewable energy', 'A donation to environmental charities'], correctIndex: 0, explanation: 'Each carbon credit represents one metric ton of CO2 equivalent that has been verified as removed or avoided.' },
      ],
    },
    {
      id: 'refi-offset',
      slug: 'offsetting-biodiversity',
      title: 'Offsetting & Biodiversity',
      description: 'Beyond carbon to ecological assets.',
      commands: ['offset', 'offset portfolio'],
      steps: [
        { instruction: 'Offset your portfolio\'s carbon footprint: `offset portfolio --portfolio my-investments --scope 1,2,3`', command: 'offset portfolio --portfolio my-investments --scope 1,2,3', expectedOutput: 'Portfolio carbon footprint: 245 tons CO2e — offset cost: $3,675 (100 credits at $36.75)' },
        { instruction: 'Biodiversity credits are an emerging asset class in ReFi.' },
        { instruction: 'The cat\'s portfolio is carbon neutral — it breathes in CO2 and purrs out oxygen.' },
      ],
      quiz: [
        { question: 'What is a biodiversity credit?', options: ['A financial instrument that funds ecosystem restoration and species protection', 'A credit card for buying plants', 'A government tax credit for gardeners', 'A discount at pet stores'], correctIndex: 0, explanation: 'Biodiversity credits generate funding for conservation projects that protect species and restore natural habitats.' },
      ],
    },
    {
      id: 'refi-circular',
      slug: 'circular-economy-finance',
      title: 'Circular Economy & Finance',
      description: 'Financing a waste-free future.',
      commands: ['circular', 'circular analyze'],
      steps: [
        { instruction: 'Analyze circular economy impact: `circular analyze --company XYZ --metrics waste_reduction,recycled_content,product_lifespan`', command: 'circular analyze --company XYZ --metrics waste_reduction,recycled_content,product_lifespan', expectedOutput: 'Circular economy score: 72/100 — waste -34%, recycled inputs 45%, product lifespan +2.1y' },
        { instruction: 'The circular economy eliminates waste by keeping materials in use.' },
        { instruction: 'The cat practices circular economy: cardboard box → scratching post → recycle → new box.' },
      ],
      quiz: [
        { question: 'What is the circular economy?', options: ['An economic system focused on eliminating waste through reuse and recycling', 'A roundabout way of trading stocks', 'An economic theory about business cycles', 'A circular flow of money in the economy'], correctIndex: 0, explanation: 'The circular economy designs out waste by keeping products and materials in use through reuse, repair, and recycling.' },
      ],
    },
  ],
}
