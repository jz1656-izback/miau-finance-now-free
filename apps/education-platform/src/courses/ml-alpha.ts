import type { Course } from '../lib/types'

export const ml_alpha: Course = {
  id: 'ml-alpha',
  slug: 'ml-alpha',
  title: 'Machine Learning for Alpha',
  description: 'Cat-themed course on Machine Learning for Alpha.',
  category: 'AI',
  difficulty: 'advanced',
  icon: '🤖',
  lessonCount: 4,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'ml-alpha-1', slug: 'ml-alpha-1', title: 'Getting Started',
      description: 'Introduction to Machine Learning for Alpha.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Machine Learning for Alpha in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Machine Learning for Alpha?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'ml-alpha-2', slug: 'ml-alpha-2', title: 'Core Concepts',
      description: 'Key concepts in Machine Learning for Alpha.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'ml-alpha-3', slug: 'ml-alpha-3', title: 'Practical Applications',
      description: 'Applying Machine Learning for Alpha in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
