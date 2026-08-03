import type { Course } from '../lib/types'

export const time_series_forecasting: Course = {
  id: 'time-series-forecasting',
  slug: 'time-series-forecasting',
  title: 'Time Series Forecasting',
  description: 'Cat-themed course on Time Series Forecasting.',
  category: 'Data Science',
  difficulty: 'advanced',
  icon: '📈',
  lessonCount: 4,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'time-series-forecasting-1', slug: 'time-series-forecasting-1', title: 'Getting Started',
      description: 'Introduction to Time Series Forecasting.',
      commands: ['help'],
      steps: [
        { instruction: 'Explore Time Series Forecasting in the terminal. Type help for available commands.' },
        { instruction: 'The cat recommends starting slowly and building up your knowledge.' },
      ],
      quiz: [{ question: 'Ready to learn Time Series Forecasting?', options: ['Yes', 'No', 'Maybe', 'Ask the cat'], correctIndex: 0, explanation: 'Learning is a journey. The cat is proud of you.' }],
    },
    {
      id: 'time-series-forecasting-2', slug: 'time-series-forecasting-2', title: 'Core Concepts',
      description: 'Key concepts in Time Series Forecasting.',
      commands: ['help'],
      steps: [
        { instruction: 'Understanding the core concepts is essential for mastery.' },
        { instruction: 'The cat mastered these concepts napping.' },
      ],
      quiz: [{ question: 'What is the most important concept?', options: ['Risk management', 'Getting rich quick', 'Ignoring losses', 'Following the herd'], correctIndex: 0, explanation: 'Risk management is the foundation of all successful trading and investing.' }],
    },
    {
      id: 'time-series-forecasting-3', slug: 'time-series-forecasting-3', title: 'Practical Applications',
      description: 'Applying Time Series Forecasting in real markets.',
      commands: ['help'],
      steps: [
        { instruction: 'Apply what you have learned in the terminal with real data.' },
        { instruction: 'The cat applies its knowledge daily. It is very profitable. Meow.' },
      ],
      quiz: [{ question: 'What should you do after learning a new concept?', options: ['Practice with small positions first', 'Go all in immediately', 'Forget it immediately', 'Tell everyone on social media'], correctIndex: 0, explanation: 'Always practice new strategies with small positions before scaling up.' }],
    },
  ],
}
