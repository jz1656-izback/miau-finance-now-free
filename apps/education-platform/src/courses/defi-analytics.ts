import type { Course } from '../lib/types'

export const defiAnalytics: Course = {
  id: 'defi-analytics',
  slug: 'defi-analytics',
  title: 'DeFi Analytics with DeFiLlama',
  description: 'TVL, yields, stablecoins, DEX volumes, gas prices, and chain analysis — the cat tracks 2400+ protocols across 180+ chains.',
  category: 'Web3',
  difficulty: 'intermediate',
  icon: '⛓️',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'defi-tvl',
      slug: 'defi-tvl-overview',
      title: 'DeFi TVL Overview',
      description: 'Track total value locked across all protocols.',
      commands: ['defillama', 'tvl aave', 'chain ethereum'],
      steps: [
        { instruction: 'See top DeFi protocols: `defillama` — ranked by TVL', command: 'defillama', expectedOutput: 'Top protocols with TVL in B/M' },
        { instruction: 'Check a specific protocol: `tvl aave` — Aave TVL and details', command: 'tvl aave', expectedOutput: 'Aave TVL, chain, category, 24h change' },
        { instruction: 'Explore a chain: `chain ethereum` — all protocols on Ethereum', command: 'chain ethereum', expectedOutput: 'Ethereum chain overview with protocol list' },
        { instruction: 'The cat\'s TVL is 100% tuna. It is very liquid.' },
      ],
      quiz: [
        { question: 'What does TVL (Total Value Locked) measure in DeFi?', options: ['The total value of assets deposited in a protocol smart contracts', 'The market cap of a protocol token', 'The daily trading volume', 'The total revenue generated'], correctIndex: 0, explanation: 'TVL measures the total value of all assets deposited in a protocol smart contracts. It is the primary metric for DeFi protocol adoption and usage.' },
      ],
    },
    {
      id: 'defi-yields',
      slug: 'defi-yield-farming',
      title: 'Yield Pools & Farming',
      description: 'Find the best APY across 2400+ protocols.',
      commands: ['yields 10', 'yields 5'],
      steps: [
        { instruction: 'Find high-yield pools: `yields 10` — pools with 10%+ APY', command: 'yields 10', expectedOutput: 'Yield pools sorted by APY with TVL' },
        { instruction: 'Higher APY usually means higher risk. Check the pool TVL to see if it is legit.' },
        { instruction: 'Filter for safer yields: `yields 3` — for 3%+ APY', command: 'yields 3', expectedOutput: 'Lower yield, higher TVL pools' },
        { instruction: 'The cat yields 100% returns on its tuna farming. It is the most successful yield farmer.' },
      ],
      quiz: [
        { question: 'What is the primary risk when chasing high DeFi yields?', options: ['Impermanent loss, smart contract risk, and potential rug pulls — high APY often means higher risk', 'The yield is always guaranteed', 'Only large investors can participate', 'There is no risk in established protocols'], correctIndex: 0, explanation: 'High DeFi yields come with significant risks including impermanent loss (in AMM pools), smart contract bugs/hacks, and malicious protocols (rug pulls). Always check TVL and audit reports.' },
      ],
    },
    {
      id: 'defi-stablecoins-gas',
      slug: 'stablecoins-gas',
      title: 'Stablecoins & Gas Analysis',
      description: 'Monitor stablecoin supply and chain gas prices.',
      commands: ['stablecoins', 'gas 1', 'gas 137'],
      steps: [
        { instruction: 'Check stablecoin market: `stablecoins` — supply across chains', command: 'stablecoins', expectedOutput: 'Stablecoin list with supply amounts' },
        { instruction: 'Check Ethereum gas: `gas 1` — Safe/Normal/Fast prices', command: 'gas 1', expectedOutput: 'Ethereum gas prices in gwei' },
        { instruction: 'Check Polygon gas: `gas 137` — much cheaper than Ethereum', command: 'gas 137', expectedOutput: 'Polygon gas prices' },
        { instruction: 'The cat uses Polygon because the gas fees are measured in cans of tuna, not barrels.' },
      ],
      quiz: [
        { question: 'Why would you check gas prices before making a DeFi transaction?', options: ['To time your transaction for lower fees — gas prices vary significantly by time of day and network congestion', 'Gas prices are always the same', 'To see if the network is down', 'Gas only matters for Bitcoin transactions'], correctIndex: 0, explanation: 'Gas prices fluctuate based on network demand. Checking gas helps you time transactions during low-congestion periods (typically weekends or late night UTC) to save on fees.' },
      ],
    },
    {
      id: 'defi-dexs-fees',
      slug: 'dex-fees-revenue',
      title: 'DEXs, Fees & Protocol Revenue',
      description: 'Track DEX volumes and protocol earnings.',
      commands: ['dexs', 'fees', 'tvl uniswap'],
      steps: [
        { instruction: 'See DEX volumes: `dexs` — top decentralized exchanges by volume', command: 'dexs', expectedOutput: 'DEX volume overview' },
        { instruction: 'Check protocol fees: `fees` — which protocols earn the most', command: 'fees', expectedOutput: 'Protocol fee/revenue data' },
        { instruction: 'Cross-reference with TVL: `tvl uniswap` — compare fees to TVL', command: 'tvl uniswap', expectedOutput: 'Uniswap TVL and details' },
        { instruction: 'The cat earns fees from its DeFi protocol "MeowSwap." Total fees: infinite treats.' },
      ],
      quiz: [
        { question: 'What is the relationship between DEX trading volume and protocol fees?', options: ['Higher trading volume typically generates more fee revenue for the protocol and liquidity providers', 'Volume and fees are unrelated', 'Fees decrease as volume increases', 'Only stakers earn fees'], correctIndex: 0, explanation: 'DEXs earn a percentage of every trade. Higher trading volume directly translates to more fee revenue distributed to liquidity providers and the protocol treasury.' },
      ],
    },
  ],
}
