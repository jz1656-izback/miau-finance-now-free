import type { Course } from '../lib/types'

export const smart_contract_development: Course = {
  id: 'smart-contract-development', slug: 'smart-contract-development', title: 'Smart Contract Development',
  description: 'A cat-friendly guide to Smart Contract Development. The cat explores Web3 one paw at a time.',
  category: 'Programming', difficulty: 'advanced', icon: '🔗', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'smart-contract-development-1', slug: 'smart-contract-development-1', title: 'Core Concepts', description: 'Understanding Smart Contract Development.', commands: ['defi protocols'], steps: [
      { instruction: 'Learn the fundamentals of Smart Contract Development.' },
      { instruction: 'The cat was an early adopter. It bought tuna at /usr/bin/bash.01.' },
    ], quiz: [{ question: 'Why does this matter in Web3?', options: ['It is a fundamental building block of decentralized finance', 'It is not important', 'Only developers need to know', 'It is already obsolete'], correctIndex: 0, explanation: 'Understanding core Web3 concepts is essential for navigating the decentralized finance landscape.' }] },
    { id: 'smart-contract-development-2', slug: 'smart-contract-development-2', title: 'Practical Applications', description: 'Using Smart Contract Development in practice.', commands: ['gas 1'], steps: [
      { instruction: 'Apply your knowledge with real transactions on-chain.' },
      { instruction: 'The cat has a hardware wallet shaped like a fish. It is very secure.' },
    ], quiz: [{ question: 'What is the main risk in this area?', options: ['Smart contract bugs and market volatility', 'The cat stealing your tuna', 'Too many options', 'Not enough users'], correctIndex: 0, explanation: 'Smart contract vulnerabilities and market volatility are the primary risks in DeFi and Web3.' }] },
    { id: 'smart-contract-development-3', slug: 'smart-contract-development-3', title: 'Security Best Practices', description: 'Staying safe.', commands: ['gas 1'], steps: [
      { instruction: 'Learn security best practices for protecting your assets.' },
      { instruction: 'The cat uses a multisig wallet. One key is hidden under the cat bed.' },
    ], quiz: [{ question: 'How can you protect your Web3 assets?', options: ['Use hardware wallets and verify all transactions', 'Store everything on exchanges', 'Share your seed phrase with trusted friends', 'Use the same password everywhere'], correctIndex: 0, explanation: 'Hardware wallets provide the best security by keeping private keys offline. Always verify transaction details before signing.' }] },
  ],
}
