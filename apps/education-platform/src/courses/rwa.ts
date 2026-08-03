import type { Course } from '../lib/types'

export const realWorldAssets: Course = {
  id: 'real-world-assets',
  slug: 'real-world-assets-rwa',
  title: 'Real World Assets (RWA)',
  description: 'Tokenized assets, real estate tokens, and commodity tokens — the cat tokenizes its scratching post as an RWA.',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '🏗️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'rwa-intro',
      slug: 'rwa-fundamentals',
      title: 'RWA Fundamentals',
      description: 'What tokenized real-world assets are.',
      commands: ['rwa', 'rwa list'],
      steps: [
        { instruction: 'List available RWAs on-chain: `rwa list --chain ethereum --category all`', command: 'rwa list --chain ethereum --category all', expectedOutput: 'RWA protocols: 12 active — total TVL $4.2B, top: real-estate (45%), commodities (30%)' },
        { instruction: 'RWAs bring traditional assets like real estate and commodities onto blockchains.' },
        { instruction: 'The cat thinks everything should be tokenized — starting with tuna cans.' },
      ],
      quiz: [
        { question: 'What does RWA tokenization achieve?', options: ['Makes traditional assets tradeable on blockchain with fractional ownership', 'Creates new cryptocurrencies', 'Replaces all physical assets', 'Eliminates the need for legal ownership'], correctIndex: 0, explanation: 'RWA tokenization converts ownership rights of physical assets into digital tokens, enabling fractional trading on-chain.' },
      ],
    },
    {
      id: 'rwa-realestate',
      slug: 'real-estate-tokenization',
      title: 'Real Estate Tokenization',
      description: 'Buying buildings one token at a time.',
      commands: ['tokenize', 'tokenize property'],
      steps: [
        { instruction: 'Tokenize a real estate property: `tokenize property --address "123 Main St" --valuation 5000000 --tokens 5000`', command: 'tokenize property --address "123 Main St" --valuation 5000000 --tokens 5000', expectedOutput: 'Property tokenized: 5,000 tokens created at $1,000 each — rental yield 4.2% APR' },
        { instruction: 'Fractional ownership lets you invest in real estate with minimal capital.' },
        { instruction: 'The cat tokenized its cat tree — 100 shares, each entitled to 1% of nap time.' },
      ],
      quiz: [
        { question: 'What is the main benefit of tokenized real estate?', options: ['Fractional ownership and liquidity for an illiquid asset class', 'Guaranteed price appreciation', 'Elimination of property taxes', 'Anonymous property ownership'], correctIndex: 0, explanation: 'Tokenization divides property into many tokens, allowing small investors access to real estate with better liquidity.' },
      ],
    },
    {
      id: 'rwa-commodities',
      slug: 'commodity-tokens',
      title: 'Commodity Tokens',
      description: 'Gold, oil, and grain on-chain.',
      commands: ['asset', 'asset verify'],
      steps: [
        { instruction: 'Verify an asset-backed token: `asset verify --token GOLD --check-reserves`', command: 'asset verify --token GOLD --check-reserves', expectedOutput: 'GOLD token: 99.8% backed by physical gold in audited vaults — last audit 2026-05-18' },
        { instruction: 'Commodity tokens represent physical goods stored in verified vaults.' },
        { instruction: 'The cat issued a TUNA token — backed 1:1 by actual tuna in the pantry.' },
      ],
      quiz: [
        { question: 'What is the key risk with asset-backed tokens?', options: ['The custodian may not actually hold the promised reserves', 'They are always over-collateralized', 'Blockchain cannot track physical assets', 'They are illegal in most countries'], correctIndex: 0, explanation: 'Asset-backed tokens rely on custodians to hold reserves — if the custodian is fraudulent, the token may be worthless.' },
      ],
    },
    {
      id: 'rwa-stablecoins',
      slug: 'stablecoins-digital-dollars',
      title: 'Stablecoins & Digital Dollars',
      description: 'The backbone of on-chain finance.',
      commands: ['stable', 'stable mint'],
      steps: [
        { instruction: 'Mint stablecoins against collateral: `stable mint --collateral ETH --amount 10000 --ratio 150`', command: 'stable mint --collateral ETH --amount 10000 --ratio 150', expectedOutput: '10,000 stablecoins minted against 150% ETH collateral: liquidation price $1,250' },
        { instruction: 'Stablecoins maintain peg through collateralization or algorithmic mechanisms.' },
        { instruction: 'The cat prefers fully reserved stablecoins — backed by 100% fish.' },
      ],
      quiz: [
        { question: 'How do collateralized stablecoins maintain their peg?', options: ['Over-collateralization with volatile assets and liquidation mechanisms', 'Government backing and regulation', 'Algorithmic printing and burning of tokens', 'Fixed supply with market demand'], correctIndex: 0, explanation: 'Collateralized stablecoins require more collateral than stablecoins issued and liquidate positions if collateral value drops.' },
      ],
    },
  ],
}
