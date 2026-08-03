import type { Course } from '../lib/types'

export const monetaryTheory: Course = {
  id: 'monetary-theory-policy',
  slug: 'monetary-theory-and-policy',
  title: 'Monetary Theory & Policy',
  description: 'Money supply, quantitative easing, and modern monetary theory — the cat prints its own tuna currency.',
  category: 'Economics',
  difficulty: 'advanced',
  icon: '🏛️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'monet-money',
      slug: 'money-supply-velocity',
      title: 'Money Supply & Velocity',
      description: 'M0, M1, M2, and how money moves.',
      commands: ['money-supply', 'money-supply chart'],
      steps: [
        { instruction: 'Chart money supply trends: `money-supply chart --measure M2 --country US --period 10y`', command: 'money-supply chart --measure M2 --country US --period 10y', expectedOutput: 'M2 money supply chart (2016-2026): 12T → 22T, velocity declining from 1.5 to 1.1' },
        { instruction: 'Money supply measures the total amount of money in the economy.' },
        { instruction: 'The cat\'s personal money supply (M1-tuna) has been growing steadily.' },
      ],
      quiz: [
        { question: 'What is the velocity of money?', options: ['The rate at which money circulates through the economy', 'The speed of electronic transactions', 'How fast prices increase', 'The speed of bank transfers'], correctIndex: 0, explanation: 'Velocity measures how frequently each unit of currency is used to purchase goods and services within a period.' },
      ],
    },
    {
      id: 'monet-qe',
      slug: 'quantitative-easing',
      title: 'Quantitative Easing',
      description: 'Central banks buying assets.',
      commands: ['qe', 'qe impact'],
      steps: [
        { instruction: 'Simulate QE impact on bond yields: `qe impact --amount 500B --duration 12m`', command: 'qe impact --amount 500B --duration 12m', expectedOutput: 'QE simulation: 10y yield -45bps, equity +8%, inflation +0.3% over 12 months' },
        { instruction: 'QE injects liquidity by central banks purchasing government bonds and other assets.' },
        { instruction: 'The cat conducted QE on its treat stash — expanding the supply by 200%.' },
      ],
      quiz: [
        { question: 'How does Quantitative Easing lower long-term interest rates?', options: ['Central bank bond purchases reduce supply and push prices up', 'It directly sets the federal funds rate', 'It increases bank reserve requirements', 'It raises inflation expectations'], correctIndex: 0, explanation: 'By buying long-term bonds, the central bank reduces available supply, pushing bond prices up and yields down.' },
      ],
    },
    {
      id: 'monet-mmt',
      slug: 'modern-monetary-theory',
      title: 'Modern Monetary Theory',
      description: 'A controversial approach to fiscal policy.',
      commands: ['mmt', 'mmt simulate'],
      steps: [
        { instruction: 'Simulate MMT-style fiscal policy: `mmt simulate --spending 2T --tax-revenue 1.5T --unemployment 4`', command: 'mmt simulate --spending 2T --tax-revenue 1.5T --unemployment 4', expectedOutput: 'MMT simulation: inflation +2.1%, GDP +3.5%, unemployment 3.2% after 2 years' },
        { instruction: 'MMT argues sovereign currency issuers cannot involuntarily default.' },
        { instruction: 'The cat supports MMT — it believes in unlimited tuna printing.' },
      ],
      quiz: [
        { question: 'What is a key claim of Modern Monetary Theory?', options: ['A sovereign currency issuer can never run out of money', 'Governments must always balance budgets', 'Gold backs all currency', 'Central banks should be abolished'], correctIndex: 0, explanation: 'MMT posits that countries issuing their own currency can create more money at will and cannot default on domestic currency debt.' },
      ],
    },
    {
      id: 'monet-inflation',
      slug: 'inflation-deflation',
      title: 'Inflation & Deflation',
      description: 'Causes, effects, and policy responses.',
      commands: ['inflation', 'inflation forecast'],
      steps: [
        { instruction: 'Forecast inflation using macro indicators: `inflation forecast --model phillips --unemployment 3.8 --expectations 2.5`', command: 'inflation forecast --model phillips --unemployment 3.8 --expectations 2.5', expectedOutput: 'Inflation forecast: CPI 3.2% (1y), core PCE 2.8% (1y) — Phillips curve suggests above-target inflation' },
        { instruction: 'Central banks target 2% inflation as a sign of healthy economy.' },
        { instruction: 'The cat measured inflation in the tuna market — prices have increased 5 whiskers per can.' },
      ],
      quiz: [
        { question: 'What is the Phillips Curve?', options: ['The inverse relationship between unemployment and inflation', 'The relationship between money supply and prices', 'The yield curve shape and recession probability', 'The trade-off between growth and debt'], correctIndex: 0, explanation: 'The Phillips Curve suggests that low unemployment tends to come with higher inflation, and vice versa.' },
      ],
    },
  ],
}
