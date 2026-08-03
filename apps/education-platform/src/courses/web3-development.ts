import type { Course } from '../lib/types'

export const web3_development: Course = {
  id: 'web3-development', slug: 'web3-development', title: 'Web3 Development',
  description: 'A comprehensive cat-themed course on Web3 Development.',
  category: 'Programming', difficulty: 'intermediate', icon: '📘', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'web3-development-1', slug: 'web3-development-1', title: 'Overview', description: 'Introduction to Web3 Development.', commands: ['help'],
      steps: [{ instruction: 'Learn the fundamentals of Web3 Development.' },
        { instruction: 'The cat recommends paying close attention to this topic.' }],
      quiz: [{ question: 'Why is this topic important?', options: ['It builds foundational knowledge', 'It is not important', 'Only experts need it', 'It will be obsolete soon'], correctIndex: 0, explanation: 'Foundational knowledge is essential for advanced understanding.' }] },
    { id: 'web3-development-2', slug: 'web3-development-2', title: 'Core Concepts', description: 'Key ideas.', commands: ['help'],
      steps: [{ instruction: 'Explore the core concepts of Web3 Development.' },
        { instruction: 'The cat mastered these concepts through careful observation.' }],
      quiz: [{ question: 'What is the main takeaway?', options: ['Apply these concepts with proper risk management', 'Ignore everything', 'Only focus on gains', 'Follow trends blindly'], correctIndex: 0, explanation: 'All financial concepts should be applied with proper risk management.' }] },
    { id: 'web3-development-3', slug: 'web3-development-3', title: 'Practical Use', description: 'Real-world application.', commands: ['help'],
      steps: [{ instruction: 'Apply this knowledge in your trading and analysis.' },
        { instruction: 'The cat applies this daily. It is very successful. Meow.' }],
      quiz: [{ question: 'How should you practice?', options: ['Start small and scale up gradually', 'Go all in immediately', 'Only paper trade forever', 'Copy others'], correctIndex: 0, explanation: 'Gradual scaling with proper risk management is the safest approach.' }] },
  ],
}
