import type { Course } from '../lib/types'

export const behavioralFinance: Course = {
  id: 'behavioral-finance',
  slug: 'behavioral-finance',
  title: 'Behavioral Finance & Psychology',
  description: 'Cognitive biases, emotional discipline, and the psychology of money — the cat analyzes your brain.',
  category: 'Psychology',
  difficulty: 'beginner',
  icon: '🧠',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'bf-biases',
      slug: 'cognitive-biases',
      title: 'Cognitive Biases in Investing',
      description: 'Recognize the mental traps that cost you money.',
      commands: ['psychology', 'psychology biases'],
      steps: [
        { instruction: 'List common biases: `psychology biases`', command: 'psychology biases', expectedOutput: 'List of 20+ cognitive biases with descriptions' },
        { instruction: 'Confirmation bias = you seek info that confirms your existing beliefs. You ignore contradictory evidence.' },
        { instruction: 'Recency bias = you overweight recent events. A stock that went up yesterday feels like it will go up today.' },
      ],
      quiz: [
        { question: 'What is confirmation bias?', options: ['Seeking info that confirms existing beliefs', 'Overweighting recent events', 'Selling winners too early', 'Buying high and selling low'], correctIndex: 0, explanation: 'Confirmation bias is the tendency to seek, interpret, and remember information that confirms pre-existing beliefs.' },
      ],
    },
    {
      id: 'bf-emotions',
      slug: 'emotional-discipline',
      title: 'Emotional Discipline',
      description: 'Fear, greed, FOMO, and panic — master your emotions to master your portfolio.',
      commands: ['psychology check', 'psychology journal'],
      steps: [
        { instruction: 'Run a psychology check: `psychology check`', command: 'psychology check', expectedOutput: 'Emotional state assessment with recommendations' },
        { instruction: 'Fear and greed index: `psychology fear-greed`', command: 'psychology fear-greed', expectedOutput: 'Current market fear/greed level' },
        { instruction: 'Keep a trading journal: `psychology journal --entry "I sold because I panicked"`' },
      ],
      quiz: [
        { question: 'What is FOMO in trading?', options: ['Fear Of Missing Out — buying because others are', 'A risk management strategy', 'A technical indicator', 'A type of option spread'], correctIndex: 0, explanation: 'FOMO (Fear Of Missing Out) drives impulsive buying when you see others profiting.' },
      ],
    },
    {
      id: 'bf-heuristics',
      slug: 'heuristics',
      title: 'Mental Heuristics & Shortcuts',
      description: 'Your brain takes shortcuts. Learn when they help and when they hurt.',
      commands: ['psychology heuristics'],
      steps: [
        { instruction: 'Learn about heuristics: `psychology heuristics`', command: 'psychology heuristics', expectedOutput: 'Overview of mental shortcuts in financial decision-making' },
        { instruction: 'Anchoring = you fixate on a reference price (e.g., "it was $100 last week, now $80 is cheap").' },
        { instruction: 'Availability heuristic = you overestimate probability of events that are easy to recall (e.g., a recent crash).' },
      ],
      quiz: [
        { question: 'What is anchoring?', options: ['Fixating on a reference price', 'Ignoring reference points', 'Following the crowd', 'Taking profits too early'], correctIndex: 0, explanation: 'Anchoring is when you rely too heavily on the first piece of information (the anchor) when making decisions.' },
      ],
    },
    {
      id: 'bf-system',
      slug: 'build-your-system',
      title: 'Building Your Trading System',
      description: 'Create rules, checklists, and systems to beat your own brain.',
      commands: ['psychology plan', 'psychology checklist'],
      steps: [
        { instruction: 'Create a trading plan: `psychology plan --create`', command: 'psychology plan --create', expectedOutput: 'Trading plan template' },
        { instruction: 'A trading plan removes emotion. You decide entry, exit, position size, and risk BEFORE the trade.' },
        { instruction: 'Build a pre-trade checklist: `psychology checklist --build`' },
      ],
      quiz: [
        { question: 'Why use a pre-trade checklist?', options: ['To remove emotion from decisions', 'To slow down execution', 'To impress clients', 'To comply with regulations'], correctIndex: 0, explanation: 'A pre-trade checklist forces you to verify your strategy before emotion takes over.' },
      ],
    },
  ],
}
