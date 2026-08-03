import type { Course } from '../lib/types'

export const catberg_terminal: Course = {
  id: 'catberg-terminal',
  slug: 'catberg-terminal',
  title: 'Catberg Bloomberg Terminal',
  description: 'Cat-themed course on Catberg Bloomberg Terminal.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '📺',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'catberg-terminal-1', slug: 'catberg-terminal-1', title: 'Getting Started',
      description: 'Introduction to Catberg Bloomberg Terminal.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Catberg Bloomberg Terminal in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Catberg Bloomberg Terminal?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'catberg-terminal-2', slug: 'catberg-terminal-2', title: 'Core Concepts',
      description: 'Key concepts in Catberg Bloomberg Terminal.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'catberg-terminal-3', slug: 'catberg-terminal-3', title: 'Practical Applications',
      description: 'Applying Catberg Bloomberg Terminal in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
