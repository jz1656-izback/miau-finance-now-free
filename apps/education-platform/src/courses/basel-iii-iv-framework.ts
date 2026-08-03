import type { Course } from '../lib/types'

export const basel_iii_iv_framework: Course = {
  id: 'basel-iii-iv-framework', slug: 'basel-iii-iv-framework', title: 'Basel III/IV Framework',
  description: 'A cat-guided professional development course on Basel III/IV Framework. Sharpen your skills.',
  category: 'Regulation', difficulty: 'intermediate', icon: '💼', lessonCount: 3, estimatedMinutes: 20,
  lessons: [
    { id: 'basel-iii-iv-framework-1', slug: 'basel-iii-iv-framework-1', title: 'Fundamentals', description: 'Core principles of Basel III/IV Framework.', commands: ['help'], steps: [
      { instruction: 'Learn the fundamentals of Basel III/IV Framework.' },
      { instruction: 'The cat attended a seminar on this. It slept through most of it and still passed.' },
    ], quiz: [{ question: 'Why is this skill important in finance?', options: ['It directly impacts career progression and effectiveness', 'It is not important', 'Only managers need it', 'It is optional'], correctIndex: 0, explanation: 'Professional skills are critical for career advancement and effective performance in finance roles.' }] },
    { id: 'basel-iii-iv-framework-2', slug: 'basel-iii-iv-framework-2', title: 'Practical Application', description: 'Applying these skills.', commands: ['help'], steps: [
      { instruction: 'Practice applying these skills in real scenarios.' },
      { instruction: 'The cat practices its negotiation skills during tuna treat time.' },
    ], quiz: [{ question: 'How should you practice these skills?', options: ['Role-play scenarios and seek feedback', 'Read about them once', 'Watch videos only', 'Avoid practice until necessary'], correctIndex: 0, explanation: 'Active practice through role-play and real application with feedback is the most effective way to develop professional skills.' }] },
    { id: 'basel-iii-iv-framework-3', slug: 'basel-iii-iv-framework-3', title: 'Mastery', description: 'Advanced techniques.', commands: ['help'], steps: [
      { instruction: 'Master advanced techniques in Basel III/IV Framework.' },
      { instruction: 'The cat achieved mastery by teaching others. Teaching is the best way to learn.' },
    ], quiz: [{ question: 'What is the best way to master a professional skill?', options: ['Teach others and get real-world experience', 'Read one book', 'Attend one workshop', 'Watch tutorials'], correctIndex: 0, explanation: 'Teaching others and applying skills in real situations deepens understanding and reveals knowledge gaps.' }] },
  ],
}
