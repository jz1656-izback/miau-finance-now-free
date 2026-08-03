import type { Course } from '../lib/types'

export const solana_ecosystem: Course = {
  id: 'solana-ecosystem', slug: 'solana-ecosystem', title: 'Solana Ecosystem',
  description: 'A cat-friendly guide to Solana Ecosystem. The cat explores Web3 one paw at a time.',
  category: 'Web3', difficulty: 'advanced', icon: '🔗', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'solana-ecosystem-1', slug: 'solana-ecosystem-1', title: 'Core Concepts', description: 'Understanding Solana Ecosystem.', commands: ['defi protocols'], steps: [
      { instruction: 'Learn the fundamentals of Solana Ecosystem.' },
      { instruction: 'The cat was an early adopter. It bought tuna at /usr/bin/bash.01.' },
    ], quiz: [{ question: 'Why does this matter in Web3?', options: ['It is a fundamental building block of decentralized finance', 'It is not important', 'Only developers need to know', 'It is already obsolete'], correctIndex: 0, explanation: 'Understanding core Web3 concepts is essential for navigating the decentralized finance landscape.' }] },
    { id: 'solana-ecosystem-2', slug: 'solana-ecosystem-2', title: 'Practical Applications', description: 'Using Solana Ecosystem in practice.', commands: ['gas 1'], steps: [
      { instruction: 'Apply your knowledge with real transactions on-chain.' },
      { instruction: 'The cat has a hardware wallet shaped like a fish. It is very secure.' },
    ], quiz: [{ question: 'What is the main risk in this area?', options: ['Smart contract bugs and market volatility', 'The cat stealing your tuna', 'Too many options', 'Not enough users'], correctIndex: 0, explanation: 'Smart contract vulnerabilities and market volatility are the primary risks in DeFi and Web3.' }] },
    { id: 'solana-ecosystem-3', slug: 'solana-ecosystem-3', title: 'Security Best Practices', description: 'Staying safe.', commands: ['gas 1'], steps: [
      { instruction: 'Learn security best practices for protecting your assets.' },
      { instruction: 'The cat uses a multisig wallet. One key is hidden under the cat bed.' },
    ], quiz: [{ question: 'How can you protect your Web3 assets?', options: ['Use hardware wallets and verify all transactions', 'Store everything on exchanges', 'Share your seed phrase with trusted friends', 'Use the same password everywhere'], correctIndex: 0, explanation: 'Hardware wallets provide the best security by keeping private keys offline. Always verify transaction details before signing.' }] },
  ],
}
