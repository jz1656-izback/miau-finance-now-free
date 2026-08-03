import type { Course } from '../lib/types'

export const miau_portfolio_optimizer: Course = {
  id: 'miau-portfolio-optimizer', slug: 'miau-portfolio-optimizer', title: 'Miau Portfolio Optimizer',
  description: 'Learn to use the Miau Portfolio Optimizer feature in the Miau Finance ecosystem.',
  category: 'Portfolio', difficulty: 'beginner', icon: '🐱', lessonCount: 3, estimatedMinutes: 15,
  lessons: [
    { id: 'miau-portfolio-optimizer-1', slug: 'miau-portfolio-optimizer-1', title: 'Getting Started', description: 'Introduction to Miau Portfolio Optimizer.', commands: ['help'], steps: [
      { instruction: 'Learn how to access and use Miau Portfolio Optimizer.' },
      { instruction: 'The cat uses this feature daily. It is very efficient.' },
    ], quiz: [{ question: 'How do you access this feature?', options: ['Through the terminal or the dedicated interface', 'It is not accessible', 'Only admins can use it', 'It costs extra'], correctIndex: 0, explanation: 'Miau Finance features are accessible through the terminal commands or dedicated interfaces.' }] },
    { id: 'miau-portfolio-optimizer-2', slug: 'miau-portfolio-optimizer-2', title: 'Core Features', description: 'Key functionality.', commands: ['help'], steps: [
      { instruction: 'Explore the main features and capabilities.' },
      { instruction: 'The cat discovered a hidden feature by accident. It was very pleased.' },
    ], quiz: [{ question: 'What makes this feature useful?', options: ['It saves time and provides better insights', 'It looks cool', 'Everyone else uses it', 'The cat said so'], correctIndex: 0, explanation: 'Miau Finance features are designed to save time and provide actionable insights.' }] },
    { id: 'miau-portfolio-optimizer-3', slug: 'miau-portfolio-optimizer-3', title: 'Advanced Tips', description: 'Power user tips.', commands: ['help'], steps: [
      { instruction: 'Learn advanced tips and tricks for Miau Portfolio Optimizer.' },
      { instruction: 'The cat knows all the shortcuts. It is a power user.' },
    ], quiz: [{ question: 'How can you get the most out of this feature?', options: ['Explore all options and read the documentation', 'Use the default settings only', 'Ignore advanced features', 'Ask the cat'], correctIndex: 0, explanation: 'Exploring all options and reading documentation helps you leverage the full power of each feature.' }] },
  ],
}
