import type { Course } from '../lib/types'

export const defiAdvanced: Course = {
  id: 'defi-advanced-protocols',
  slug: 'defi-advanced-protocols',
  title: 'DeFi Advanced Protocols',
  description: 'AMMs, lending, yield optimization, and composability — the cat yields more than a farm in summer.',
  category: 'Web3',
  difficulty: 'advanced',
  icon: '🔗',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'defi-amm',
      slug: 'automated-market-makers',
      title: 'Automated Market Makers',
      description: 'How AMMs like Uniswap work.',
      commands: ['defi-swap', 'defi-swap quote'],
      steps: [
        { instruction: 'Get a swap quote: `defi-swap quote --from ETH --to USDC --amount 10 --slippage 0.5`', command: 'defi-swap quote --from ETH --to USDC --amount 10 --slippage 0.5', expectedOutput: 'Swap quote: 10 ETH → 32,450 USDC, price impact 0.3%, fee $12.50' },
        { instruction: 'AMMs use the constant product formula x * y = k to determine prices.' },
        { instruction: 'The cat provides liquidity to the ETH/TUNA pool — deep liquidity, delicious returns.' },
      ],
      quiz: [
        { question: 'What determines the price in a constant product AMM?', options: ['The ratio of reserves in the liquidity pool', 'An oracle price feed', 'External market price', 'The protocol governance vote'], correctIndex: 0, explanation: 'AMMs like Uniswap price assets based on the relative size of each token in the pool via the constant product formula.' },
      ],
    },
    {
      id: 'defi-lending',
      slug: 'defi-lending-borrowing',
      title: 'Lending & Borrowing',
      description: 'Supply assets, earn interest, borrow against collateral.',
      commands: ['defi-lend', 'defi-lend supply'],
      steps: [
        { instruction: 'Supply assets to a lending pool: `defi-lend supply --asset USDC --amount 50000 --protocol aave`', command: 'defi-lend supply --asset USDC --amount 50000 --protocol aave', expectedOutput: 'Supplied 50,000 USDC to Aave — APY 4.5%, health factor N/A (no borrow)' },
        { instruction: 'Over-collateralization ensures lending protocols remain solvent.' },
        { instruction: 'The cat supplies tuna to the pantry pool — daily interest: one fish.' },
      ],
      quiz: [
        { question: 'What happens when a borrower\'s health factor drops below 1?', options: ['The position is liquidated to repay the loan', 'The interest rate increases', 'The borrower must add more collateral', 'The loan is forgiven'], correctIndex: 0, explanation: 'If collateral value falls below the loan threshold (health factor < 1), liquidators repay the loan and seize collateral.' },
      ],
    },
    {
      id: 'defi-yield',
      slug: 'yield-optimization-strategies',
      title: 'Yield Optimization Strategies',
      description: 'Farming, compounding, and yield aggregation.',
      commands: ['yield', 'yield optimize'],
      steps: [
        { instruction: 'Optimize yield across protocols: `yield optimize --asset USDC --amount 100000 --risk low`', command: 'yield optimize --asset USDC --amount 100000 --risk low', expectedOutput: 'Optimized yield strategy: 60% Aave (4.5%), 30% Compound (4.2%), 10% Curve (5.8%) — blended APY 4.6%' },
        { instruction: 'Yield aggregators auto-compound rewards for maximum returns.' },
        { instruction: 'The cat\'s yield optimization: rotate between sun spots for optimal warmth.' },
      ],
      quiz: [
        { question: 'What is impermanent loss in liquidity provision?', options: ['Temporary loss when pool token prices diverge relative to holding', 'Permanent loss of deposited funds', 'Loss due to smart contract bugs', 'Loss from withdrawal fees'], correctIndex: 0, explanation: 'Impermanent loss occurs when the price ratio of pooled tokens changes, making the value of LP shares less than simply holding the tokens.' },
      ],
    },
    {
      id: 'defi-composability',
      slug: 'defi-composability-lego',
      title: 'Composability & DeFi Legos',
      description: 'Combining protocols like building blocks.',
      commands: ['compound', 'compound strategy'],
      steps: [
        { instruction: 'Create a composed DeFi strategy: `compound strategy --name "Lend-Borrow-Farm" --steps supply,borrow,stake`', command: 'compound strategy --name "Lend-Borrow-Farm" --steps supply,borrow,stake', expectedOutput: 'DeFi strategy "Lend-Borrow-Farm" created: deposit ETH, borrow USDC, stake LP tokens' },
        { instruction: 'Composability lets you stack protocols for enhanced risk and return.' },
        { instruction: 'The cat built a DeFi strategy using yarn, a cardboard box, and nine lives.' },
      ],
      quiz: [
        { question: 'What makes DeFi composable?', options: ['Smart contracts that can interact freely like open APIs', 'All protocols being built by the same team', 'Government regulation of DeFi', 'Centralized coordination by developers'], correctIndex: 0, explanation: 'DeFi protocols expose public smart contract interfaces that any other protocol can integrate with permissionlessly.' },
      ],
    },
  ],
}
