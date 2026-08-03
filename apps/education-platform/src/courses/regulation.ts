import type { Course } from '../lib/types'

export const regulationCompliance: Course = {
  id: 'regulation-compliance',
  slug: 'regulation-and-compliance',
  title: 'Regulation & Compliance',
  description: 'SEC, FINRA, MiFID II, GDPR, KYC/AML — the cat keeps its paperwork purrfectly in order.',
  category: 'Regulation',
  difficulty: 'intermediate',
  icon: '📋',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'reg-sec',
      slug: 'sec-regulations',
      title: 'SEC Regulations',
      description: 'Key SEC rules for investors and firms.',
      commands: ['compliance', 'compliance sec'],
      steps: [
        { instruction: 'Check SEC compliance requirements: `compliance sec --entity hedge-fund`', command: 'compliance sec --entity hedge-fund', expectedOutput: 'SEC compliance checklist for hedge funds: 13F filings, Form ADV, accredited investor verification' },
        { instruction: 'The SEC requires regular filings from institutional investment managers.' },
        { instruction: 'The cat files its 13F quarterly — it only discloses long positions in tuna futures.' },
      ],
      quiz: [
        { question: 'What is Form 13F?', options: ['Quarterly report of equity holdings by institutional managers', 'Annual tax filing for investment firms', 'Registration form for new broker-dealers', 'Disclosure of short positions'], correctIndex: 0, explanation: 'Form 13F must be filed quarterly by institutional investment managers with over $100M in equity assets.' },
      ],
    },
    {
      id: 'reg-mifid',
      slug: 'mifid-ii-gdpr',
      title: 'MiFID II & GDPR',
      description: 'European financial regulations.',
      commands: ['mifid', 'mifid report'],
      steps: [
        { instruction: 'Generate a MiFID II transaction report: `mifid report --date 2025-04-01 --format xml`', command: 'mifid report --date 2025-04-01 --format xml', expectedOutput: 'MiFID II transaction report generated for 2025-04-01: 1,234 transactions' },
        { instruction: 'MiFID II requires trade reporting, best execution, and investor protection.' },
        { instruction: 'GDPR means the cat must ask permission before storing your name in its database.' },
      ],
      quiz: [
        { question: 'What is the main goal of MiFID II?', options: ['Increase transparency and investor protection in EU markets', 'Eliminate all high-frequency trading', 'Create a single European exchange', 'Ban cryptocurrency trading'], correctIndex: 0, explanation: 'MiFID II aims to make EU financial markets more transparent, efficient, and fair for investors.' },
      ],
    },
    {
      id: 'reg-kyc',
      slug: 'kyc-aml-compliance',
      title: 'KYC & AML Compliance',
      description: 'Know Your Customer and Anti-Money Laundering.',
      commands: ['aml', 'aml screen'],
      steps: [
        { instruction: 'Screen a client for AML compliance: `aml screen --client --risk-level high`', command: 'aml screen --client --risk-level high', expectedOutput: 'AML screening complete: client cleared — enhanced due diligence recommended' },
        { instruction: 'KYC requires verifying client identity before doing business.' },
        { instruction: 'The cat performs KYC on every new mouse in the house.' },
      ],
      quiz: [
        { question: 'What does KYC aim to prevent?', options: ['Identity fraud, money laundering, and terrorist financing', 'Insider trading exclusively', 'Market manipulation only', 'Tax evasion exclusively'], correctIndex: 0, explanation: 'KYC procedures verify identity to prevent fraud, money laundering, and terrorist financing through the financial system.' },
      ],
    },
    {
      id: 'reg-fintech',
      slug: 'fintech-regulatory-landscape',
      title: 'FinTech Regulatory Landscape',
      description: 'Regulations for modern financial services.',
      commands: ['sec', 'sec filing'],
      steps: [
        { instruction: 'Check upcoming SEC filing deadlines: `sec filing --calendar Q1-2026`', command: 'sec filing --calendar Q1-2026', expectedOutput: 'Q1 2026 SEC filing calendar: 13F due Feb 15, 10-K due Mar 31' },
        { instruction: 'FinTech firms must navigate both financial and technology regulations.' },
        { instruction: 'The cat hired a compliance officer — it is also a cat. Conflicts of interest? Never.' },
      ],
      quiz: [
        { question: 'Why do FinTech companies face complex regulatory challenges?', options: ['They operate at the intersection of finance and technology regulations', 'They are exempt from all regulations', 'They only follow one regulator', 'Technology regulations do not apply to them'], correctIndex: 0, explanation: 'FinTech firms must comply with financial services regulations plus technology and data protection laws simultaneously.' },
      ],
    },
  ],
}
