import type { Course } from '../lib/types'

export const cybersecurityFinance: Course = {
  id: 'cybersecurity-finance',
  slug: 'cybersecurity-for-finance',
  title: 'Cybersecurity for Finance',
  description: 'Securing assets, 2FA, phishing, and wallet security — the cat guards your portfolio like a lion.',
  category: 'Security',
  difficulty: 'intermediate',
  icon: '🔒',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'sec-basics',
      slug: 'security-fundamentals',
      title: 'Security Fundamentals',
      description: 'Threat landscape in financial services.',
      commands: ['security', 'security scan'],
      steps: [
        { instruction: 'Run a security scan on your system: `security scan --level full`', command: 'security scan --level full', expectedOutput: 'Security scan complete: 0 critical, 2 medium, 5 low findings' },
        { instruction: 'Financial accounts are the #1 target for cybercriminals.' },
        { instruction: 'The cat uses a 128-character password that it memorized in one try.' },
      ],
      quiz: [
        { question: 'Why are financial accounts prime targets for hackers?', options: ['They offer direct monetary gain and sensitive data', 'They have the weakest security', 'They are the most common accounts', 'They lack any encryption'], correctIndex: 0, explanation: 'Financial accounts combine monetary access with sensitive personal data, making them the most valuable target.' },
      ],
    },
    {
      id: 'sec-2fa',
      slug: 'two-factor-authentication',
      title: 'Two-Factor Authentication',
      description: 'Adding layers of protection.',
      commands: ['audit', 'audit 2fa'],
      steps: [
        { instruction: 'Audit 2FA status on your accounts: `audit 2fa --check-all`', command: 'audit 2fa --check-all', expectedOutput: '2FA audit: 12/15 accounts secured, 3 accounts at risk' },
        { instruction: 'Use authenticator apps over SMS — SIM swapping is real.' },
        { instruction: 'The cat has 2FA on its tuna delivery account. Priorities.' },
      ],
      quiz: [
        { question: 'Why is app-based 2FA safer than SMS?', options: ['SMS can be intercepted via SIM swapping attacks', 'SMS is encrypted by default', 'Apps are slower and less convenient', 'SMS requires a phone number'], correctIndex: 0, explanation: 'SIM swapping lets attackers redirect SMS messages to their device, bypassing SMS-based 2FA entirely.' },
      ],
    },
    {
      id: 'sec-phishing',
      slug: 'phishing-social-engineering',
      title: 'Phishing & Social Engineering',
      description: 'Recognizing and avoiding scams.',
      commands: ['encrypt', 'encrypt file'],
      steps: [
        { instruction: 'Encrypt sensitive files: `encrypt file --path portfolio.xlsx --algorithm aes256`', command: 'encrypt file --path portfolio.xlsx --algorithm aes256', expectedOutput: 'portfolio.xlsx encrypted with AES-256 — key stored in vault' },
        { instruction: 'Never click links in unsolicited emails about account problems.' },
        { instruction: 'The cat received a phishing email — it was from "TunaBank." Very suspicious.' },
      ],
      quiz: [
        { question: 'What is a common sign of a phishing email?', options: ['Urgent language and requests for credentials', 'Professional formatting', 'Being sent during business hours', 'Coming from a known contact'], correctIndex: 0, explanation: 'Phishing emails create urgency and pressure you to share credentials or click malicious links immediately.' },
      ],
    },
    {
      id: 'sec-wallet',
      slug: 'wallet-security-crypto',
      title: 'Wallet & Crypto Security',
      description: 'Protecting digital assets.',
      commands: ['backup', 'backup wallet'],
      steps: [
        { instruction: 'Back up your crypto wallet: `backup wallet --type hardware --destination offline`', command: 'backup wallet --type hardware --destination offline', expectedOutput: 'Wallet backup created — seed phrase stored in fireproof safe' },
        { instruction: 'Hardware wallets are the gold standard for cryptocurrency storage.' },
        { instruction: 'The cat keeps its seed phrase buried in the garden — very secure, very muddy.' },
      ],
      quiz: [
        { question: 'What is the safest way to store cryptocurrency?', options: ['Hardware wallet with offline seed phrase backup', 'Keeping keys on the exchange', 'Storing keys in a cloud document', 'Writing passwords in a notebook'], correctIndex: 0, explanation: 'Hardware wallets keep private keys offline, and a physical seed phrase backup provides recovery without digital exposure.' },
      ],
    },
  ],
}
