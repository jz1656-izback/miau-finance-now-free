import type { Course } from '../lib/types'

export const fintechPayments: Course = {
  id: 'fintech-payments',
  slug: 'fintech-payments',
  title: 'Payment Systems & Fintech',
  description: 'Payments infrastructure, neobanks, BNPL, stablecoins, and the future of money — the cat accepts Visa, Mastercard, and catnip.',
  category: 'Fintech',
  difficulty: 'intermediate',
  icon: '💳',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'payments-infra',
      slug: 'payments-infrastructure',
      title: 'Payments Infrastructure',
      description: 'How money moves through the global payments system.',
      commands: ['fintech payments', 'fintech rails'],
      steps: [
        { instruction: 'Trace a payment: `fintech payments --trace --amount 100 --from "US Bank" --to "EU Bank"`', command: 'fintech payments --trace --amount 100 --from "US Bank" --to "EU Bank"', expectedOutput: 'Payment trace: $100 USD → SWIFT (1-3 days, $25 fee) → Currency conversion (0.5% spread) → €91.50 received. Alternative: Wise ($3 fee, real-time)' },
        { instruction: 'Traditional rails: SWIFT (slow, expensive), ACH (cheap, batch), card networks (fast, 2-3% fee).' },
        { instruction: 'Check real-time payment adoption: `fintech rails --rtp --region global`', command: 'fintech rails --rtp --region global', expectedOutput: 'Real-time payment markets: India UPI (10B transactions/mo), Brazil Pix (5B/mo), EU SEPA Instant (500M/mo), US FedNow (100M/mo), UK Faster Payments (300M/mo)' },
        { instruction: 'The cat sends tuna payments via SWIFT. It takes 3 days and costs 1 can of tuna in fees.' },
      ],
      quiz: [
        { question: 'What is the main difference between SWIFT and real-time payment systems?', options: ['SWIFT is a messaging network (batch, 1-3 days) while RTP systems settle instantly, 24/7/365', 'SWIFT is free while RTP costs money', 'SWIFT only works in Europe', 'RTP only works in the US'], correctIndex: 0, explanation: 'SWIFT is a messaging network for cross-border payments that operates in batches and takes 1-3 days. Real-time payment systems (like UPI, Pix, FedNow) settle transactions instantly and operate 24/7/365.' },
      ],
    },
    {
      id: 'neobanks',
      slug: 'neobanks-digital-banking',
      title: 'Neobanks & Digital Banking',
      description: 'The rise of branchless banking.',
      commands: ['fintech neobank', 'fintech neobank --compare'],
      steps: [
        { instruction: 'Check neobank landscape: `fintech neobank --landscape`', command: 'fintech neobank --landscape', expectedOutput: 'Top neobanks: Nubank (100M users, Brazil), Revolut (45M, UK), Chime (25M, US), Monzo (9M, UK), KakaoBank (20M, Korea). Combined valuation: $150B+' },
        { instruction: 'Neobanks have lower cost bases (no branches) and use data for better risk assessment.' },
        { instruction: 'The cat banks with Meowzo — digital-only, great UX, offers overdraft in tuna.' },
        { instruction: 'Compare neobank economics: `fintech neobank --compare --banks nubank,revolut,chime`', command: 'fintech neobank --compare --banks nubank,revolut,chime', expectedOutput: 'Nubank: ARPU $8.50, Cost/account $1.20, NIM 12%. Revolut: ARPU $6.80, Cost/account $2.10, NIM 8%. Chime: ARPU $5.90, Cost/account $1.80, NIM 10%' },
      ],
      quiz: [
        { question: 'Why do neobanks have lower cost structures than traditional banks?', options: ['No physical branch network, lower IT legacy costs, automated onboarding and compliance, higher customer acquisition through digital channels', 'They pay lower wages', 'They have fewer regulations', 'They use free software'], correctIndex: 0, explanation: 'Neobanks operate without expensive branch networks, modern tech stacks reduce maintenance costs, digital onboarding automates KYC/AML, and digital marketing has lower customer acquisition costs than traditional channels.' },
      ],
    },
    {
      id: 'bnpl',
      slug: 'buy-now-pay-later',
      title: 'BNPL & Consumer Credit Innovation',
      description: 'Buy Now Pay Later and alternative credit models.',
      commands: ['fintech bnpl', 'fintech bnpl --analyze'],
      steps: [
        { instruction: 'Check BNPL market: `fintech bnpl --market --region global`', command: 'fintech bnpl --market --region global', expectedOutput: 'BNPL market 2025: $450B GMV. Players: Klarna ($80B GMV), Afterpay ($40B), Affirm ($30B), PayPal Pay Later ($60B). Growth: +15% YoY. Delinquency: 2.5% (vs credit card 3.2%)' },
        { instruction: 'BNPL economics: merchants pay 3-6% fee, consumers pay 0% interest (if on time), late fees cover losses.' },
        { instruction: 'The cat used BNPL to buy a new scratching post — 4 interest-free payments of $5.95.' },
        { instruction: 'Analyze a BNPL portfolio: `fintech bnpl --analyze --portfolio 1b --segment "prime,subprime"`', command: 'fintech bnpl --analyze --portfolio 1b --segment "prime,subprime"', expectedOutput: 'BNPL portfolio ($1B): Prime (60%) NTI 8.5%, loss rate 1.2%. Subprime (40%) NTI 14%, loss rate 6.5%. Blended NTI: 10.7%. Net margin: 4.2%' },
      ],
      quiz: [
        { question: 'How do BNPL providers make money if consumers pay 0% interest?', options: ['Merchant discount fees (3-6% of transaction value), late fees, and cross-selling financial products', 'Government subsidies', 'Advertising revenue', 'Subscription fees from consumers'], correctIndex: 0, explanation: 'BNPL revenue comes primarily from merchant discount fees (3-6% per transaction), late payment fees, and upsells to higher-margin products like installment loans and credit cards.' },
      ],
    },
    {
      id: 'stablecoins',
      slug: 'stablecoins-payments',
      title: 'Stablecoins & Payment Innovation',
      description: 'Stablecoins as a payment rail and digital dollar.',
      commands: ['fintech stablecoin', 'fintech stablecoin --flows'],
      steps: [
        { instruction: 'Check stablecoin market: `fintech stablecoin --market`', command: 'fintech stablecoin --market', expectedOutput: 'Stablecoin market cap: $180B. USDT (Tether): $120B. USDC (Circle): $42B. DAI (MakerDAO): $5B. FDUSD: $3B. Monthly transfer volume: $1.2T (vs PayPal $400B, ACH $500B)' },
        { instruction: 'Stablecoin payment volume now exceeds PayPal — they are becoming a major payment rail.' },
        { instruction: 'The cat keeps its savings in USDT because it earns yield and the cat hates bank fees.' },
        { instruction: 'Trace a stablecoin payment flow: `fintech stablecoin --trace --from "USDC wallet" --to "merchant" --amount 1000`', command: 'fintech stablecoin --trace --from "USDC wallet" --to "merchant" --amount 1000', expectedOutput: 'Payment flow: User sends 1000 USDC → Blockchain (2s, $0.01) → Merchant receives 1000 USDC → Merchant converts to $1000 USD (0.1% fee). Total: 2 seconds, $1.01 cost. vs Card: 2 days, $30 cost' },
      ],
      quiz: [
        { question: 'Why are stablecoins becoming a significant payment rail?', options: ['Lower fees than card networks, instant settlement 24/7/365, programmability, and global accessibility with only internet access needed', 'They are the only legal payment method', 'They have no fees at all', 'They are backed by the US government'], correctIndex: 0, explanation: 'Stablecoins offer near-zero fees (cents vs 2-3% for cards), instant settlement on blockchain (vs 1-3 days for traditional rails), programmable payments via smart contracts, and global accessibility.' },
      ],
    },
  ],
}
