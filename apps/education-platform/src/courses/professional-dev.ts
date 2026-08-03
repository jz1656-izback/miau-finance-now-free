import type { Course } from '../lib/types'

export const professionalDev: Course = {
  id: 'professional-dev',
  slug: 'professional-dev',
  title: 'Professional Development & Ethics',
  description: 'Finance ethics, compliance, professional standards, and career growth — the cat has principles.',
  category: 'Professional',
  difficulty: 'beginner',
  icon: '⚖️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'pd-code',
      slug: 'code-of-conduct',
      title: 'Code of Conduct & Ethics',
      description: 'Standards of professional behavior in finance.',
      commands: ['help ethics', 'compliance'],
      steps: [
        { instruction: 'View the ethics guide: `help ethics`', command: 'help ethics', expectedOutput: 'Miau Finance Code of Ethics' },
        { instruction: 'Key principles: integrity, objectivity, confidentiality, professionalism, and putting clients first.' },
        { instruction: 'Check compliance status: `compliance status`', command: 'compliance status', expectedOutput: 'Your compliance checklist' },
      ],
      quiz: [
        { question: 'Which principle means putting client interests ahead of your own?', options: ['Fiduciary duty', 'Confidentiality', 'Objectivity', 'Professionalism'], correctIndex: 0, explanation: 'Fiduciary duty requires putting client interests first, ahead of personal gain.' },
      ],
    },
    {
      id: 'pd-compliance',
      slug: 'compliance-basics',
      title: 'Regulatory Compliance',
      description: 'Know your regulations — SEC, FINRA, MiFID II, and what they mean for your trading.',
      commands: ['compliance', 'compliance report'],
      steps: [
        { instruction: 'Run a compliance check: `compliance check --all`', command: 'compliance check --all', expectedOutput: 'Compliance status across all regulations' },
        { instruction: 'Pattern Day Trader rule: if you trade 4+ day trades in 5 days with a margin account under $25k, you get flagged.' },
        { instruction: 'Insider trading is illegal. Never trade on material non-public information.' },
      ],
      quiz: [
        { question: 'What is the PDT rule minimum equity?', options: ['$25,000', '$10,000', '$50,000', '$5,000'], correctIndex: 0, explanation: 'Pattern Day Trader rules require $25,000 minimum equity in margin accounts.' },
      ],
    },
    {
      id: 'pd-cv',
      slug: 'resume-building',
      title: 'Resume & Portfolio Building',
      description: 'Showcase your Miau Finance skills to employers and clients.',
      commands: ['certificate', 'profile'],
      steps: [
        { instruction: 'View your certificates: `certificate list`', command: 'certificate list', expectedOutput: 'Your earned certifications' },
        { instruction: 'Generate a shareable profile: `profile export`', command: 'profile export', expectedOutput: 'Shareable URL with your course history' },
      ],
      quiz: [
        { question: 'What does `certificate list` show?', options: ['Your earned certifications', 'Available courses', 'Course prices', 'Cat facts'], correctIndex: 0, explanation: '`certificate list` displays all certifications you have earned.' },
      ],
    },
    {
      id: 'pd-networking',
      slug: 'networking',
      title: 'Professional Networking',
      description: 'Connect with other analysts, share strategies, and build your reputation.',
      commands: ['social feed', 'follow', 'profile'],
      steps: [
        { instruction: 'Browse the professional feed: `social feed`', command: 'social feed', expectedOutput: 'Activity feed from other analysts' },
        { instruction: 'Follow top analysts: `follow @catcfaofficial`', command: 'follow @catcfaofficial', expectedOutput: 'Now following @catcfaofficial' },
        { instruction: 'Share your achievement: `social share --cert CMA`', command: 'social share --cert CMA', expectedOutput: 'Shared to your network' },
      ],
      quiz: [
        { question: 'How do you share a certification achievement?', options: ['social share --cert', 'share cert', 'certificate publish', 'post achievement'], correctIndex: 0, explanation: '`social share --cert <cert_id>` shares your certification to your professional network.' },
      ],
    },
  ],
}
