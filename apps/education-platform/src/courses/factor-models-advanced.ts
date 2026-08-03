import type { Course } from '../lib/types'

export const factor_models_advanced: Course = {
  id: 'factor-models-advanced',
  slug: 'factor-models-advanced',
  title: 'Advanced Factor Models',
  description: 'Cat-themed course on Advanced Factor Models.',
  category: 'Quantitative',
  difficulty: 'advanced',
  icon: '📊',
  lessonCount: 4,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'factor-models-advanced-1', slug: 'factor-models-advanced-1', title: 'Getting Started',
      description: 'Introduction to Advanced Factor Models.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Advanced Factor Models in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Advanced Factor Models?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'factor-models-advanced-2', slug: 'factor-models-advanced-2', title: 'Core Concepts',
      description: 'Key concepts in Advanced Factor Models.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'factor-models-advanced-3', slug: 'factor-models-advanced-3', title: 'Practical Applications',
      description: 'Applying Advanced Factor Models in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
