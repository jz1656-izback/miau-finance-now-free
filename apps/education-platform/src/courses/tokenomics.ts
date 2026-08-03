import type { Course } from '../lib/types'

export const tokenomics: Course = {
  id: 'tokenomics',
  slug: 'tokenomics-token-design',
  title: 'Tokenomics & Token Design',
  description: 'Token models, incentives, vesting, and token velocity — the cat designs a token that can be earned through purring and spent on catnip.',
  category: 'Crypto & Web3',
  difficulty: 'advanced',
  icon: '🪙',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'token-models',
      slug: 'token-model-design',
      title: 'Token Model Design',
      description: 'Different token models and their economic properties.',
      commands: ['tokenomics', 'token', 'incentive'],
      steps: [
        { instruction: 'Design a token model: `tokenomics --design --type utility --supply 1000000000 --initial-distribution "public:40,team:20,treasury:20,community:20"`', command: 'tokenomics --design --type utility --supply 1000000000 --initial-distribution "public:40,team:20,treasury:20,community:20"', expectedOutput: 'Utility token: 1B supply. Distribution: public sale 40%, team (4yr vest) 20%, treasury 20%, community rewards 20%. Initial market cap at $0.10: $100M' },
        { instruction: 'Token models define supply, distribution, and utility within a protocol ecosystem.' },
        { instruction: 'The cat designed a PUR token — 1 billion supply, 50% reserved for treats.' },
      ],
      quiz: [
        { question: 'What is a utility token?', options: ['A token that provides access to a product or service within a blockchain ecosystem', 'A token representing company shares', 'A stablecoin pegged to gold', 'A token used only for governance'], correctIndex: 0, explanation: 'Utility tokens grant holders access to specific products, services, or functions within a blockchain-based platform.' },
      ],
    },
    {
      id: 'incentive-design',
      slug: 'incentive-design-tokens',
      title: 'Incentive Design & Mechanisms',
      description: 'Aligning incentives through token rewards.',
      commands: ['incentive', 'tokenomics', 'token'],
      steps: [
        { instruction: 'Model incentive emissions: `incentive --emissions --total-supply 1B --annual-emission-rate 0.10 --halving-period 4`', command: 'incentive --emissions --total-supply 1B --annual-emission-rate 0.10 --halving-period 4', expectedOutput: 'Emission schedule: Year 1 emit 100M (10%), Year 2 emit 50M (halved), Year 3 emit 25M. Cumulative after 4yr: 187.5M (18.75% of total). Inflation rate decreasing' },
        { instruction: 'Token incentives align protocol participants through carefully designed reward schedules.' },
        { instruction: 'The cat proposed an incentive model where purring earns PUR tokens — the cats are highly motivated.' },
      ],
      quiz: [
        { question: 'Why do token projects implement halving schedules for emissions?', options: ['To control inflation and create scarcity over time, rewarding early participants', 'To make tokens cheaper', 'To increase transaction speed', 'To comply with regulations'], correctIndex: 0, explanation: 'Halving schedules reduce token emission rates over time, creating scarcity and potentially increasing value for existing holders.' },
      ],
    },
    {
      id: 'vesting',
      slug: 'token-vesting-schedules',
      title: 'Token Vesting & Lockups',
      description: 'Designing vesting schedules for token distributions.',
      commands: ['vesting', 'tokenomics', 'token'],
      steps: [
        { instruction: 'Design a vesting schedule: `vesting --schedule --team-allocation 20% --cliff 12 --linear-vest 36`', command: 'vesting --schedule --team-allocation 20% --cliff 12 --linear-vest 36', expectedOutput: 'Vesting: 12-month cliff (no tokens), then 36-month linear vest. Team unlocks 2M tokens/month after cliff. Fully vested at 48 months. 1yr cliff reduces dump risk' },
        { instruction: 'Vesting schedules prevent early stakeholders from dumping tokens immediately after listing.' },
        { instruction: 'The cat team tokens have a 4-year vest — the cat plans to be around that long, probably.' },
      ],
      quiz: [
        { question: 'Why do token projects use cliffs in vesting schedules?', options: ['To prevent early team members from selling immediately if they leave the project early', 'To make the project look more professional', 'To comply with exchange requirements only', 'To reduce the total token supply'], correctIndex: 0, explanation: 'A cliff period (typically 6-12 months) ensures that team members must stay with the project for a minimum period before any tokens unlock.' },
      ],
    },
    {
      id: 'token-velocity',
      slug: 'token-velocity-economics',
      title: 'Token Velocity & Economics',
      description: 'Managing token velocity to maintain value.',
      commands: ['tokenomics', 'token'],
      steps: [
        { instruction: 'Calculate token velocity: `tokenomics --velocity --transaction-volume 500M --average-token-balance 100M`', command: 'tokenomics --velocity --transaction-volume 500M --average-token-balance 100M', expectedOutput: 'Token velocity: 5x (annual trading volume / average balance). High velocity (>10) indicates low holding incentive. Target: 3-8x for healthy ecosystem economy' },
        { instruction: 'Token velocity measures how frequently tokens change hands in the ecosystem.' },
        { instruction: 'The cat token velocity is low — cats hoard their PUR tokens like they hoard cardboard boxes.' },
      ],
      quiz: [
        { question: 'Why is high token velocity often a concern for token designers?', options: ['High velocity means tokens are spent quickly rather than held, potentially depressing price', 'High velocity means the blockchain is fast', 'High velocity attracts hackers', 'High velocity is always good'], correctIndex: 0, explanation: 'High token velocity indicates low holding demand, which can create selling pressure and make it difficult for the token to appreciate in value.' },
      ],
    },
  ],
}
