import type { Course } from '../lib/types'

export const portfolio_construction_advanced: Course = {
  id: 'portfolio-construction-advanced', slug: 'portfolio-construction-advanced', title: 'Advanced Portfolio Construction',
  description: 'A comprehensive cat-themed course on Advanced Portfolio Construction.',
  category: 'Portfolio Management', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'portfolio-construction-advanced-1', slug: 'portfolio-construction-advanced-1', title: 'Overview', description: 'Introduction to Advanced Portfolio Construction.', commands: ['help'],
      steps: [{ instruction: 'Learn the fundamentals of Advanced Portfolio Construction.' },
        { instruction: 'The cat recommends paying close attention to this topic.' }],
      quiz: [{ question: 'Why is this topic important?', options: ['It builds foundational knowledge', 'It is not important', 'Only experts need it', 'It will be obsolete soon'], correctIndex: 0, explanation: 'Foundational knowledge is essential for advanced understanding.' }] },
    { id: 'portfolio-construction-advanced-2', slug: 'portfolio-construction-advanced-2', title: 'Core Concepts', description: 'Key ideas.', commands: ['help'],
      steps: [{ instruction: 'Explore the core concepts of Advanced Portfolio Construction.' },
        { instruction: 'The cat mastered these concepts through careful observation.' }],
      quiz: [{ question: 'What is the main takeaway?', options: ['Apply these concepts with proper risk management', 'Ignore everything', 'Only focus on gains', 'Follow trends blindly'], correctIndex: 0, explanation: 'All financial concepts should be applied with proper risk management.' }] },
    { id: 'portfolio-construction-advanced-3', slug: 'portfolio-construction-advanced-3', title: 'Practical Use', description: 'Real-world application.', commands: ['help'],
      steps: [{ instruction: 'Apply this knowledge in your trading and analysis.' },
        { instruction: 'The cat applies this daily. It is very successful. Meow.' }],
      quiz: [{ question: 'How should you practice?', options: ['Start small and scale up gradually', 'Go all in immediately', 'Only paper trade forever', 'Copy others'], correctIndex: 0, explanation: 'Gradual scaling with proper risk management is the safest approach.' }] },
  ],
}
