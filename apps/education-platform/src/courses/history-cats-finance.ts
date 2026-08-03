import type { Course } from '../lib/types'

export const history_cats_finance: Course = {
  id: 'history-cats-finance', slug: 'history-cats-finance', title: 'History of Cats in Finance',
  description: 'A comprehensive cat-themed course on History of Cats in Finance.',
  category: 'History', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'history-cats-finance-1', slug: 'history-cats-finance-1', title: 'Overview', description: 'Introduction to History of Cats in Finance.', commands: ['help'],
      steps: [{ instruction: 'Learn the fundamentals of History of Cats in Finance.' },
        { instruction: 'The cat recommends paying close attention to this topic.' }],
      quiz: [{ question: 'Why is this topic important?', options: ['It builds foundational knowledge', 'It is not important', 'Only experts need it', 'It will be obsolete soon'], correctIndex: 0, explanation: 'Foundational knowledge is essential for advanced understanding.' }] },
    { id: 'history-cats-finance-2', slug: 'history-cats-finance-2', title: 'Core Concepts', description: 'Key ideas.', commands: ['help'],
      steps: [{ instruction: 'Explore the core concepts of History of Cats in Finance.' },
        { instruction: 'The cat mastered these concepts through careful observation.' }],
      quiz: [{ question: 'What is the main takeaway?', options: ['Apply these concepts with proper risk management', 'Ignore everything', 'Only focus on gains', 'Follow trends blindly'], correctIndex: 0, explanation: 'All financial concepts should be applied with proper risk management.' }] },
    { id: 'history-cats-finance-3', slug: 'history-cats-finance-3', title: 'Practical Use', description: 'Real-world application.', commands: ['help'],
      steps: [{ instruction: 'Apply this knowledge in your trading and analysis.' },
        { instruction: 'The cat applies this daily. It is very successful. Meow.' }],
      quiz: [{ question: 'How should you practice?', options: ['Start small and scale up gradually', 'Go all in immediately', 'Only paper trade forever', 'Copy others'], correctIndex: 0, explanation: 'Gradual scaling with proper risk management is the safest approach.' }] },
  ],
}
