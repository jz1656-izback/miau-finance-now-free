import type { Course } from '../lib/types'

export const monte_carlo_deep: Course = {
  id: 'monte-carlo-deep',
  slug: 'monte-carlo-deep',
  title: 'Monte Carlo Simulation Deep Dive',
  description: 'Cat-themed course on Monte Carlo Simulation Deep Dive.',
  category: 'Quantitative',
  difficulty: 'advanced',
  icon: '🎲',
  lessonCount: 4,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'monte-carlo-deep-1', slug: 'monte-carlo-deep-1', title: 'Getting Started',
      description: 'Introduction to Monte Carlo Simulation Deep Dive.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Monte Carlo Simulation Deep Dive in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Monte Carlo Simulation Deep Dive?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'monte-carlo-deep-2', slug: 'monte-carlo-deep-2', title: 'Core Concepts',
      description: 'Key concepts in Monte Carlo Simulation Deep Dive.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'monte-carlo-deep-3', slug: 'monte-carlo-deep-3', title: 'Practical Applications',
      description: 'Applying Monte Carlo Simulation Deep Dive in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
