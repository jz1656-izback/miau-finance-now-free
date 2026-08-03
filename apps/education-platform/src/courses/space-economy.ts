import type { Course } from '../lib/types'

export const spaceEconomy: Course = {
  id: 'space-economy',
  slug: 'space-economy-investing',
  title: 'Space Economy',
  description: 'Satellite, launch, space tourism, and space mining — the cat invests in the final frontier because Earth ran out of tuna.',
  category: 'Emerging Industries',
  difficulty: 'advanced',
  icon: '🚀',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'satellite-economics',
      slug: 'satellite-economics',
      title: 'Satellite Economics',
      description: 'The business of satellite communications and imaging.',
      commands: ['satellite', 'space', 'launch'],
      steps: [
        { instruction: 'Analyze satellite constellation economics: `satellite --economics --constellation starlink --users 3000000 --arfpu 120`', command: 'satellite --economics --constellation starlink --users 3000000 --arfpu 120', expectedOutput: 'Starlink economics: 3M subs x $120/mo = $4.32B annual revenue. Satellite cost: $500K each. 4,500 satellites = $2.25B. Breakeven: 18 months. Margin: 60%+ at scale' },
        { instruction: 'Satellite constellations provide internet, Earth observation, and navigation services.' },
        { instruction: 'The cat uses satellite internet to watch bird videos from space — truly global entertainment.' },
      ],
      quiz: [
        { question: 'What is the primary revenue model for satellite internet constellations?', options: ['Monthly subscription fees from end-users for broadband internet access', 'Selling satellite hardware', 'Government grants only', 'Advertising revenue'], correctIndex: 0, explanation: 'Satellite internet constellations like Starlink generate recurring revenue primarily through monthly subscription fees paid by end-users.' },
      ],
    },
    {
      id: 'launch-industry',
      slug: 'launch-industry-economics',
      title: 'Launch Industry Economics',
      description: 'The business of rocket launches.',
      commands: ['launch', 'space', 'satellite'],
      steps: [
        { instruction: 'Compare launch costs: `launch --costs --vehicle "Falcon 9,Starship,ULA Vulcan"`', command: 'launch --costs --vehicle "Falcon 9,Starship,ULA Vulcan"', expectedOutput: 'Launch costs per kg: Falcon 9 $2,700 (reusable), Starship $1,000 (target), Vulcan $6,500 (expendable). Market: 250+ launches in 2025, $15B launch services market' },
        { instruction: 'Reusable rockets have dramatically reduced the cost of space access.' },
        { instruction: 'The cat calculated the cost per kilo of tuna delivered to orbit — still cheaper than the cat food aisle.' },
      ],
      quiz: [
        { question: 'How have reusable rockets changed space economics?', options: ['They reduced launch costs by 10x, enabling new business models and more frequent launches', 'They increased costs due to refurbishment', 'They made space travel slower', 'They had no significant impact'], correctIndex: 0, explanation: 'Reusable rocket technology has dramatically lowered per-launch costs, opening space access to more commercial applications.' },
      ],
    },
    {
      id: 'space-tourism',
      slug: 'space-tourism-business',
      title: 'Space Tourism & Human Spaceflight',
      description: 'The emerging space tourism industry.',
      commands: ['space-tourism', 'space', 'launch'],
      steps: [
        { instruction: 'Analyze space tourism market: `space-tourism --market --year 2025 --projection 2030`', command: 'space-tourism --market --year 2025 --projection 2030', expectedOutput: 'Space tourism market 2025: $1.5B. Projected 2030: $8B (35% CAGR). Suborbital ($250K/ticket), Orbital ($55M/ticket). TAM: 15M high-net-worth individuals' },
        { instruction: 'Space tourism ranges from suborbital flights to orbital stays on the ISS or private stations.' },
        { instruction: 'The cat booked a suborbital flight — it wants to see the Earth from space and knock over a moon rock.' },
      ],
      quiz: [
        { question: 'What is the approximate cost of a suborbital space tourism flight as of 2025?', options: ['$250,000 to $500,000 per seat', '$10,000 per seat', '$10 million per seat', '$5,000 per seat'], correctIndex: 0, explanation: 'Suborbital space tourism flights on vehicles like Blue Origin New Shepard and Virgin Galactic cost approximately $250K-$500K per seat.' },
      ],
    },
    {
      id: 'space-mining',
      slug: 'space-mining-resources',
      title: 'Space Mining & Resources',
      description: 'The future of asteroid and lunar resource extraction.',
      commands: ['space', 'space-tourism'],
      steps: [
        { instruction: 'Evaluate asteroid mining potential: `space --mining --asteroid "Psyche" --metal-content platinum --concentration 0.0001`', command: 'space --mining --asteroid "Psyche" --metal-content platinum --concentration 0.0001', expectedOutput: 'Asteroid Psyche: Estimated $10,000 quadrillion in metals. Recovery cost: $100B+ infrastructure. Timeline: 20-30 years. Legal framework: Outer Space Treaty uncertainties' },
        { instruction: 'Asteroid mining remains speculative but could unlock enormous natural resources.' },
        { instruction: 'The cat invested in space mining — it dreams of platinum-lined litter boxes on Mars.' },
      ],
      quiz: [
        { question: 'What is the primary legal challenge facing asteroid mining?', options: ['Ambiguity in the Outer Space Treaty regarding property rights for extracted resources', 'No rockets available', 'Too much competition', 'Asteroids are protected by international law'], correctIndex: 0, explanation: 'The Outer Space Treaty of 1967 does not clearly address property rights for resources extracted from celestial bodies, creating legal uncertainty.' },
      ],
    },
  ],
}
