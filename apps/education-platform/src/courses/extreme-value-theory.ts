import type { Course } from '../lib/types'

export const extreme_value_theory: Course = {
  id: 'extreme-value-theory', slug: 'extreme-value-theory', title: 'Extreme Value Theory in Finance',
  description: 'A comprehensive cat-themed course on Extreme Value Theory in Finance.',
  category: 'Risk Management', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'extreme-value-theory-1', slug: 'extreme-value-theory-1', title: 'Overview', description: 'Introduction to Extreme Value Theory in Finance.', commands: ['help'],
      steps: [{ instruction: 'Learn the fundamentals of Extreme Value Theory in Finance.' },
        { instruction: 'The cat recommends paying close attention to this topic.' }],
      quiz: [{ question: 'Why is this topic important?', options: ['It builds foundational knowledge', 'It is not important', 'Only experts need it', 'It will be obsolete soon'], correctIndex: 0, explanation: 'Foundational knowledge is essential for advanced understanding.' }] },
    { id: 'extreme-value-theory-2', slug: 'extreme-value-theory-2', title: 'Core Concepts', description: 'Key ideas.', commands: ['help'],
      steps: [{ instruction: 'Explore the core concepts of Extreme Value Theory in Finance.' },
        { instruction: 'The cat mastered these concepts through careful observation.' }],
      quiz: [{ question: 'What is the main takeaway?', options: ['Apply these concepts with proper risk management', 'Ignore everything', 'Only focus on gains', 'Follow trends blindly'], correctIndex: 0, explanation: 'All financial concepts should be applied with proper risk management.' }] },
    { id: 'extreme-value-theory-3', slug: 'extreme-value-theory-3', title: 'Practical Use', description: 'Real-world application.', commands: ['help'],
      steps: [{ instruction: 'Apply this knowledge in your trading and analysis.' },
        { instruction: 'The cat applies this daily. It is very successful. Meow.' }],
      quiz: [{ question: 'How should you practice?', options: ['Start small and scale up gradually', 'Go all in immediately', 'Only paper trade forever', 'Copy others'], correctIndex: 0, explanation: 'Gradual scaling with proper risk management is the safest approach.' }] },
  ],
}
