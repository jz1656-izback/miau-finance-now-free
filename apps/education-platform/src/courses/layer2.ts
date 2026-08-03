import type { Course } from '../lib/types'

export const layer2Scaling: Course = {
  id: 'layer2-scaling',
  slug: 'layer-2-and-scaling',
  title: 'Layer 2 & Scaling',
  description: 'Rollups, sidechains, gas optimization, and L2 bridges — the cat moves at purr-second speed.',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '⚡',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'l2-intro',
      slug: 'layer2-fundamentals',
      title: 'Layer 2 Fundamentals',
      description: 'Why L2 is needed for blockchain scaling.',
      commands: ['l2', 'l2 info'],
      steps: [
        { instruction: 'Get Layer 2 network info: `l2 info --network arbitrum`', command: 'l2 info --network arbitrum', expectedOutput: 'Arbitrum: TVL $3.2B, TPS 45, avg fee $0.12, finality 12m' },
        { instruction: 'L2s process transactions off-chain and post proofs to L1 for security.' },
        { instruction: 'The cat processes 9 lives in parallel — optimistic rollup style.' },
      ],
      quiz: [
        { question: 'Why are Layer 2 solutions needed?', options: ['Ethereum mainnet is congested and expensive — L2s scale throughput', 'L1 blockchains cannot support smart contracts', 'L2s are more secure than L1', 'L2s replace the need for Ethereum entirely'], correctIndex: 0, explanation: 'L2s handle transactions off the main chain, dramatically increasing throughput and reducing fees while inheriting L1 security.' },
      ],
    },
    {
      id: 'l2-rollups',
      slug: 'optimistic-zk-rollups',
      title: 'Optimistic & ZK Rollups',
      description: 'The two main rollup architectures.',
      commands: ['rollup', 'rollup compare'],
      steps: [
        { instruction: 'Compare rollup technologies: `rollup compare --types optimistic,zk`', command: 'rollup compare --types optimistic,zk', expectedOutput: 'Optimistic: 7-day challenge period, any validator can submit fraud proofs. ZK: instant finality via validity proofs, computationally intensive' },
        { instruction: 'Optimistic rollups assume validity unless challenged; ZK rollups prove validity mathematically.' },
        { instruction: 'The cat is optimistic about meals but uses zero-knowledge to hide the treat stash.' },
      ],
      quiz: [
        { question: 'What is the main trade-off between optimistic and ZK rollups?', options: ['Optimistic has withdrawal delay; ZK has high computational costs', 'Optimistic is centralized; ZK is decentralized', 'Optimistic supports fewer dApps; ZK supports more', 'Optimistic is newer; ZK is older technology'], correctIndex: 0, explanation: 'Optimistic rollups have a 7-day withdrawal window for fraud proofs, while ZK rollups need expensive off-chain computation.' },
      ],
    },
    {
      id: 'l2-bridges',
      slug: 'bridges-cross-chain',
      title: 'Bridges & Cross-Chain',
      description: 'Moving assets between layers.',
      commands: ['bridge', 'bridge transfer'],
      steps: [
        { instruction: 'Transfer assets across chains: `bridge transfer --amount 10 ETH --from ethereum --to arbitrum`', command: 'bridge transfer --amount 10 ETH --from ethereum --to arbitrum', expectedOutput: 'Bridge transfer initiated: 10 ETH locked on Ethereum, waiting for confirmation on Arbitrum (~15m)' },
        { instruction: 'Bridges lock tokens on one chain and mint representation on another.' },
        { instruction: 'The cat built a bridge between the sofa and the food bowl — high traffic, critical infrastructure.' },
      ],
      quiz: [
        { question: 'What is the main security risk with cross-chain bridges?', options: ['Smart contract vulnerabilities that can lead to fund theft', 'Bridges are always centralized', 'Bridges cannot handle large transactions', 'Bridges require government approval'], correctIndex: 0, explanation: 'Bridge contracts hold large amounts of locked value, making them prime targets for hacks and exploits.' },
      ],
    },
    {
      id: 'l2-gas',
      slug: 'gas-optimization',
      title: 'Gas Optimization',
      description: 'Minimizing transaction costs.',
      commands: ['gas', 'gas estimate'],
      steps: [
        { instruction: 'Estimate gas costs for a transaction: `gas estimate --tx-type swap --amount 10000 USDC`', command: 'gas estimate --tx-type swap --amount 10000 USDC', expectedOutput: 'Estimated gas: 210,000 units — total cost: $3.50 (L2) vs $45.00 (L1)' },
        { instruction: 'Batch transactions and use L2s to dramatically reduce gas costs.' },
        { instruction: 'The cat optimizes gas by napping through market volatility.' },
      ],
      quiz: [
        { question: 'What causes high gas fees on Ethereum?', options: ['Network congestion with more demand than block capacity', 'The price of ETH itself', 'The number of dApps deployed', 'The block time being too fast'], correctIndex: 0, explanation: 'When many users compete for block space, gas prices rise through a bidding mechanism for transaction inclusion.' },
      ],
    },
  ],
}
