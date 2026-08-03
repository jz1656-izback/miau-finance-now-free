import type { Course } from '../lib/types'

export const miaubook_social: Course = {
  id: 'miaubook-social',
  slug: 'miaubook-social',
  title: 'MiauBook Social Trading',
  description: 'Cat-themed course on MiauBook Social Trading.',
  category: 'Social',
  difficulty: 'beginner',
  icon: '📘',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'miaubook-social-1', slug: 'miaubook-social-1', title: 'Getting Started',
      description: 'Introduction to MiauBook Social Trading.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore MiauBook Social Trading in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn MiauBook Social Trading?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'miaubook-social-2', slug: 'miaubook-social-2', title: 'Core Concepts',
      description: 'Key concepts in MiauBook Social Trading.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'miaubook-social-3', slug: 'miaubook-social-3', title: 'Practical Applications',
      description: 'Applying MiauBook Social Trading in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
