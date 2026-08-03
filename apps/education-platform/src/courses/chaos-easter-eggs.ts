import type { Course } from '../lib/types'

export const chaos_easter_eggs: Course = {
  id: 'chaos-easter-eggs',
  slug: 'chaos-easter-eggs',
  title: 'Chaos Mode & Easter Eggs',
  description: 'Cat-themed course on Chaos Mode & Easter Eggs.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '🎮',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'chaos-easter-eggs-1', slug: 'chaos-easter-eggs-1', title: 'Getting Started',
      description: 'Introduction to Chaos Mode & Easter Eggs.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Chaos Mode & Easter Eggs in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Chaos Mode & Easter Eggs?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'chaos-easter-eggs-2', slug: 'chaos-easter-eggs-2', title: 'Core Concepts',
      description: 'Key concepts in Chaos Mode & Easter Eggs.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'chaos-easter-eggs-3', slug: 'chaos-easter-eggs-3', title: 'Practical Applications',
      description: 'Applying Chaos Mode & Easter Eggs in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
