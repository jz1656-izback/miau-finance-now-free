import type { Course } from '../lib/types'

export const catTradingPsychology: Course = {
  id: 'cat-trading-psychology',
  slug: 'cat-trading-psychology',
  title: 'Cat Trading Psychology',
  description: 'What cats can teach us about trading discipline, patience, and emotional control.',
  category: 'Psychology',
  difficulty: 'beginner',
  icon: '😸',
  lessonCount: 3,
  estimatedMinutes: 15,
  lessons: [
    {
      id: 'ctp-1', slug: 'ctp-1', title: 'The Cats Mind', description: 'Trading psychology basics.',
      commands: ['cat', 'scorecard'],
      steps: [
        { instruction: 'Pet the cat and center yourself: type cat --pet', command: 'cat --pet', expectedOutput: 'The cat purrs happily' },
        { instruction: 'Cats are patient hunters. They wait for the perfect moment to pounce, just like good traders.' },
      ],
      quiz: [{ question: 'What trading trait do cats exemplify?', options: ['Patience and discipline', 'Impulsiveness', 'Revenge trading', 'Panic selling'], correctIndex: 0, explanation: 'Cats are naturally patient and disciplined hunters, waiting for the right moment to act.' }],
    },
    {
      id: 'ctp-2', slug: 'ctp-2', title: 'Emotional Control', description: 'Managing fear and greed.',
      commands: ['scorecard'],
      steps: [
        { instruction: 'Check your scorecard: type scorecard', command: 'scorecard', expectedOutput: 'Your trading stats' },
        { instruction: 'Cats do not panic. When a cat misses a jump, it lands gracefully and tries again.' },
      ],
      quiz: [{ question: 'How do cats handle failure?', options: ['They adapt and try again without emotional distress', 'They give up', 'They get angry', 'They blame others'], correctIndex: 0, explanation: 'Cats are resilient creatures. They accept failure, learn, and move on without emotional baggage.' }],
    },
    {
      id: 'ctp-3', slug: 'ctp-3', title: 'The Pounce', description: 'Executing at the right time.',
      commands: ['price AAPL'],
      steps: [
        { instruction: 'Check a stocks price: type price AAPL', command: 'price AAPL', expectedOutput: 'Current price and change' },
        { instruction: 'A cat waits, observes, and strikes when the timing is perfect. Your trades should follow the same principle.' },
      ],
      quiz: [{ question: 'When should you enter a trade according to cat wisdom?', options: ['When your analysis confirms the setup and risk is managed', 'As soon as you hear about it', 'When everyone else is buying', 'Randomly'], correctIndex: 0, explanation: 'Like a cat waiting to pounce, enter trades only when your analysis and risk management align.' }],
    },
  ],
}
