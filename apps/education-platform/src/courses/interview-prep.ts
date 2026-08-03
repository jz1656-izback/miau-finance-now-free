import type { Course } from '../lib/types'

export const interviewPrep: Course = {
  id: 'interview-prep',
  slug: 'finance-interview-preparation',
  title: 'Finance Interview Prep',
  description: 'Investment banking interviews, case studies, and technical questions — the cat prepares for finance interviews with purr-fect composure.',
  category: 'Career Development',
  difficulty: 'beginner',
  icon: '💼',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'ib-interview',
      slug: 'investment-banking-interview',
      title: 'Investment Banking Interview Basics',
      description: 'Preparing for IB interview questions.',
      commands: ['interview', 'technical', 'fit'],
      steps: [
        { instruction: 'Practice the "tell me about yourself" pitch: `interview --pitch --role "Investment Banking Analyst" --background "Finance major, 2 internships"`', command: 'interview --pitch --role "Investment Banking Analyst" --background "Finance major, 2 internships"', expectedOutput: 'Pitch structure: 1) Current role/school (15s), 2) Relevant experience (30s), 3) Why banking (15s), 4) Why this firm (15s). Total: 75 seconds. Memorize and practice' },
        { instruction: 'The "tell me about yourself" answer should be 60-90 seconds and tell a coherent story.' },
        { instruction: 'The cat practiced its pitch: "I am a detail-oriented feline with experience knocking things off desks."' },
      ],
      quiz: [
        { question: 'How long should your "tell me about yourself" response be in an investment banking interview?', options: ['60-90 seconds covering background, experience, and interest in the role', '30 seconds maximum', '3-5 minutes', 'As long as the interviewer wants'], correctIndex: 0, explanation: 'A concise 60-90 second response that covers your background, relevant experience, and interest in banking is the standard expectation.' },
      ],
    },
    {
      id: 'technical-questions',
      slug: 'finance-technical-questions',
      title: 'Technical Finance Questions',
      description: 'Common technical interview questions and answers.',
      commands: ['technical', 'interview', 'case-study'],
      steps: [
        { instruction: 'Practice a DCF question: `technical --dcf --question "Walk me through a DCF"`', command: 'technical --dcf --question "Walk me through a DCF"', expectedOutput: 'DCF steps: 1) Project FCFs 5-10yr, 2) Calculate terminal value (exit multiple/Gordon growth), 3) Discount at WACC, 4) Sum PV to get enterprise value, 5) Adjust for net debt to get equity value' },
        { instruction: 'The DCF question is the most common technical question in finance interviews.' },
        { instruction: 'The cat explained a DCF model to the interviewer — the interviewer was impressed and offered tuna.' },
        { instruction: 'Practice valuation: `technical --valuation --method comps --ticker AAPL`', command: 'technical --valuation --method comps --ticker AAPL', expectedOutput: 'AAPL comps: P/E 28x, EV/EBITDA 22x, P/S 7.5x. vs peers MSFT (32x, 24x, 10x), GOOGL (21x, 16x, 5x). AAPL trades at a discount to MSFT, premium to GOOGL' },
      ],
      quiz: [
        { question: 'What is Enterprise Value (EV) equal to?', options: ['Equity value + total debt - cash and cash equivalents', 'Equity value only', 'Market capitalization only', 'Total assets minus total liabilities'], correctIndex: 0, explanation: 'Enterprise Value = Market Capitalization + Total Debt + Preferred Stock + Minority Interest - Cash and Cash Equivalents.' },
      ],
    },
    {
      id: 'case-studies',
      slug: 'case-study-preparation',
      title: 'Case Study Preparation',
      description: 'Tackling finance case studies in interviews.',
      commands: ['case-study', 'technical', 'interview'],
      steps: [
        { instruction: 'Work through a case study: `case-study --type "M&A" --scenario "Target EV $500M, Synergies $50M, Premium 20%"`', command: 'case-study --type "M&A" --scenario "Target EV $500M, Synergies $50M, Premium 20%"', expectedOutput: 'M&A case: Target $500M EV, 20% premium ($600M purchase price). Synergies $50M pre-tax ($37.5M after-tax at 25%). Accretion: $0.45/share or +8%. Breakeven: 3.2 years' },
        { instruction: 'Case studies test your analytical thinking and ability to work through problems under pressure.' },
        { instruction: 'The cat solved the M&A case — it recommended buying the tuna company for strategic synergies.' },
      ],
      quiz: [
        { question: 'In an M&A case study, what does accretion/dilution analysis determine?', options: ['Whether the acquisition will increase or decrease the acquirer earnings per share', 'The physical size of the merged company', 'Whether the merger is legal', 'The number of employees to lay off'], correctIndex: 0, explanation: 'Accretion/dilution analysis measures whether a proposed acquisition will increase (accretive) or decrease (dilutive) the acquirer earnings per share.' },
      ],
    },
    {
      id: 'fit-questions',
      slug: 'behavioral-fit-questions',
      title: 'Behavioral & Fit Questions',
      description: 'Answering behavioral questions effectively.',
      commands: ['fit', 'interview'],
      steps: [
        { instruction: 'Prepare for "Why investment banking?": `fit --why-banking --reason "deals,learning,exit-ops"`', command: 'fit --why-banking --reason "deals,learning,exit-ops"', expectedOutput: 'Recommended answer: 1) Passion for transactions and deal-making, 2) Unmatched learning environment and training, 3) Strong foundation/career acceleration for future goals' },
        { instruction: 'Use the STAR method (Situation, Task, Action, Result) for behavioral questions.' },
        { instruction: 'The cat used the STAR method to describe how it caught a mouse — Situation: mouse in kitchen, Task: protect food, Action: pounced, Result: mouse relocated outside.' },
      ],
      quiz: [
        { question: 'What does the STAR method stand for in behavioral interviews?', options: ['Situation, Task, Action, Result', 'Strategy, Tactics, Action, Review', 'Strengths, Talents, Aspirations, Results', 'Skills, Training, Abilities, Resources'], correctIndex: 0, explanation: 'STAR stands for Situation, Task, Action, Result — a structured method for answering behavioral interview questions with concrete examples.' },
      ],
    },
  ],
}
