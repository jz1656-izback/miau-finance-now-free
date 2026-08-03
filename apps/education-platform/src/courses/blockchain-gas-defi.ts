import type { Course } from '../lib/types'

export const blockchainGasDefi: Course = {
  id: 'blockchain-gas-defi',
  slug: 'blockchain-gas-defi',
  title: 'Blockchain Gas & DeFi Tools',
  description: 'Understand Ethereum gas fees, DeFi protocols, and on-chain analytics — the cat validates transactions on the blockchain meowork.',
  category: 'DeFi',
  difficulty: 'intermediate',
  icon: '⛽',
  lessonCount: 3,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'gas-basics', slug: 'gas-basics', title: 'Gas Fees Explained',
      description: 'What gas is and how to read gas prices.',
      commands: ['gas 1', 'gas 137'],
      steps: [
        { instruction: 'Check Ethereum gas: `gas 1`', command: 'gas 1', expectedOutput: 'Safe, standard, and fast gas prices in Gwei' },
        { instruction: 'Gas is measured in Gwei (1 ETH = 1 billion Gwei). Higher gas = faster confirmation.' },
        { instruction: 'The cat waits for low gas to move its tuna NFTs. Patience is a virtue.' },
        { instruction: 'Check Polygon: `gas 137`', command: 'gas 137', expectedOutput: 'Lower gas fees on L2' },
      ],
      quiz: [{ question: 'Why would you choose "fast" gas over "safe" gas?', options: ['Your transaction confirms faster during network congestion', 'It is cheaper', 'It guarantees success', 'It uses less energy'], correctIndex: 0, explanation: 'Fast gas pays a higher priority fee, incentivizing validators to include your transaction sooner.' }],
    },
    {
      id: 'defi-protocols', slug: 'defi-protocols', title: 'DeFi Protocol Overview',
      description: 'Major DeFi protocols and their use cases.',
      commands: ['defi protocols'],
      steps: [
        { instruction: 'List DeFi protocols: `defi protocols`', command: 'defi protocols', expectedOutput: 'Supported protocols with chain and TVL' },
        { instruction: 'DeFi protocols offer lending, borrowing, trading, and yield without intermediaries.' },
        { instruction: 'The cat provides liquidity to the Tuna-ETH pool. The APR is measured in fish.' },
      ],
      quiz: [{ question: 'What is Total Value Locked (TVL) in DeFi?', options: ['The total amount of assets deposited in a protocol', 'The market cap of the protocol token', 'The daily trading volume', 'The number of users'], correctIndex: 0, explanation: 'TVL measures the total value of crypto assets locked in a protocols smart contracts, indicating its scale and usage.' }],
    },
    {
      id: 'gas-optimization', slug: 'gas-optimization', title: 'Gas Optimization Strategies',
      description: 'Save on transaction fees.',
      commands: ['gas 1', 'gas 10'],
      steps: [
        { instruction: 'Compare chains: `gas 1` vs `gas 10` (Optimism)', command: 'gas 1', expectedOutput: 'Ethereum mainnet gas prices' },
        { instruction: 'L2 solutions like Optimism and Arbitrum offer significantly lower fees.' },
        { instruction: 'The cat batches its tuna trades to save on gas. Efficiency is key.' },
      ],
      quiz: [{ question: 'What is the best way to reduce gas costs?', options: ['Use L2 solutions or trade during low congestion periods', 'Always use fast gas', 'Trade only on weekends', 'Avoid DeFi entirely'], correctIndex: 0, explanation: 'L2 solutions have lower fees by design, and trading during off-peak hours reduces priority fees.' }],
    },
  ],
}
