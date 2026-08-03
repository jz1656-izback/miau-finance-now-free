import type { Course } from '../lib/types'

export const careerInFinance: Course = {
  id: 'career-in-finance',
  slug: 'career-in-finance',
  title: 'Career in Finance',
  description: 'Career paths, interviews, networking, and certifications — the cat landed a job at meow-gan Stanley.',
  category: 'Career',
  difficulty: 'beginner',
  icon: '🚀',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'career-paths',
      slug: 'finance-career-paths',
      title: 'Finance Career Paths',
      description: 'IB, S&T, AM, research, quant.',
      commands: ['career', 'career explore'],
      steps: [
        { instruction: 'Explore finance career paths: `career explore --interest quantitative`', command: 'career explore --interest quantitative', expectedOutput: 'Career matches: quant analyst, quant developer, quant researcher, risk quant' },
        { instruction: 'Finance offers diverse paths from investment banking to quantitative research.' },
        { instruction: 'The cat chose "feline wealth management" — high touch, high purr.' },
      ],
      quiz: [
        { question: 'Which finance role focuses on building mathematical models for trading?', options: ['Quantitative analyst', 'Investment banker', 'Equity researcher', 'Portfolio manager'], correctIndex: 0, explanation: 'Quants develop mathematical and statistical models for pricing derivatives, risk management, and trading strategies.' },
      ],
    },
    {
      id: 'career-interviews',
      slug: 'interview-preparation',
      title: 'Interview Preparation',
      description: 'Technical and behavioral interviews.',
      commands: ['interview', 'interview practice'],
      steps: [
        { instruction: 'Practice a technical interview: `interview practice --type quant --difficulty medium`', command: 'interview practice --type quant --difficulty medium', expectedOutput: 'Quant interview question: "What is the expected value of rolling two dice?"' },
        { instruction: 'Behavioral questions test fit — prepare your stories using the STAR method.' },
        { instruction: 'The cat\'s interview answer: "I consistently deliver results — mice, that is."' },
      ],
      quiz: [
        { question: 'What is the STAR method for interviews?', options: ['Situation, Task, Action, Result — a structured storytelling framework', 'Strategy, Timing, Analysis, Risk — a trading framework', 'Speed, Tenacity, Agility, Reach — a cat framework', 'Simple, Transparent, Accurate, Reliable — a data framework'], correctIndex: 0, explanation: 'STAR is a structured method for answering behavioral questions by describing the Situation, Task, Action, and Result.' },
      ],
    },
    {
      id: 'career-networking',
      slug: 'networking-skills',
      title: 'Networking & Personal Brand',
      description: 'Building relationships in finance.',
      commands: ['network', 'network connect'],
      steps: [
        { instruction: 'Find finance professionals to network with: `network connect --industry finance --role quant --location london`', command: 'network connect --industry finance --role quant --location london', expectedOutput: '15 quant professionals found in London — connect requests sent to 5' },
        { instruction: 'LinkedIn is your digital resume — keep it updated and professional.' },
        { instruction: 'The cat networks at the local fish market — very niche, very effective.' },
      ],
      quiz: [
        { question: 'What is the most effective way to network?', options: ['Provide value first, build genuine relationships over time', 'Ask everyone for a job immediately', 'Connect with everyone on LinkedIn blindly', 'Attend every event regardless of relevance'], correctIndex: 0, explanation: 'Effective networking focuses on building genuine relationships by offering value before asking for help.' },
      ],
    },
    {
      id: 'career-certifications',
      slug: 'certifications-licenses',
      title: 'Certifications & Licenses',
      description: 'CFA, FRM, CAIA, Series exams.',
      commands: ['resume', 'resume optimize'],
      steps: [
        { instruction: 'Optimize your resume for a quant role: `resume optimize --target quant --file resume.pdf`', command: 'resume optimize --target quant --file resume.pdf', expectedOutput: 'Resume optimized: keywords added, quant skills highlighted, ATS score improved to 85%' },
        { instruction: 'CFA is valuable for investment roles, FRM for risk, CAIA for alternatives.' },
        { instruction: 'The cat is pursuing a CAIA — Chartered Alternative Investment Analyst. It is very serious.' },
      ],
      quiz: [
        { question: 'Which certification is most relevant for risk management careers?', options: ['FRM (Financial Risk Manager)', 'CFA (Chartered Financial Analyst)', 'CAIA (Chartered Alternative Investment Analyst)', 'CPA (Certified Public Accountant)'], correctIndex: 0, explanation: 'The FRM certification specializes in risk management including market, credit, operational, and liquidity risk.' },
      ],
    },
  ],
}
