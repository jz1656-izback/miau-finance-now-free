import type { Course } from '../lib/types'

export const miau_sdk_python: Course = {
  id: 'miau-sdk-python', slug: 'miau-sdk-python', title: 'Miau Python SDK',
  description: 'Learn to use the Miau Python SDK feature in the Miau Finance ecosystem.',
  category: 'Programming', difficulty: 'beginner', icon: '🐱', lessonCount: 3, estimatedMinutes: 15,
  lessons: [
    { id: 'miau-sdk-python-1', slug: 'miau-sdk-python-1', title: 'Getting Started', description: 'Introduction to Miau Python SDK.', commands: ['help'], steps: [
      { instruction: 'Learn how to access and use Miau Python SDK.' },
      { instruction: 'The cat uses this feature daily. It is very efficient.' },
    ], quiz: [{ question: 'How do you access this feature?', options: ['Through the terminal or the dedicated interface', 'It is not accessible', 'Only admins can use it', 'It costs extra'], correctIndex: 0, explanation: 'Miau Finance features are accessible through the terminal commands or dedicated interfaces.' }] },
    { id: 'miau-sdk-python-2', slug: 'miau-sdk-python-2', title: 'Core Features', description: 'Key functionality.', commands: ['help'], steps: [
      { instruction: 'Explore the main features and capabilities.' },
      { instruction: 'The cat discovered a hidden feature by accident. It was very pleased.' },
    ], quiz: [{ question: 'What makes this feature useful?', options: ['It saves time and provides better insights', 'It looks cool', 'Everyone else uses it', 'The cat said so'], correctIndex: 0, explanation: 'Miau Finance features are designed to save time and provide actionable insights.' }] },
    { id: 'miau-sdk-python-3', slug: 'miau-sdk-python-3', title: 'Advanced Tips', description: 'Power user tips.', commands: ['help'], steps: [
      { instruction: 'Learn advanced tips and tricks for Miau Python SDK.' },
      { instruction: 'The cat knows all the shortcuts. It is a power user.' },
    ], quiz: [{ question: 'How can you get the most out of this feature?', options: ['Explore all options and read the documentation', 'Use the default settings only', 'Ignore advanced features', 'Ask the cat'], correctIndex: 0, explanation: 'Exploring all options and reading documentation helps you leverage the full power of each feature.' }] },
  ],
}
