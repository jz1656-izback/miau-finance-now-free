import type { Course } from '../lib/types'

export const esgReporting: Course = {
  id: 'esg-reporting',
  slug: 'esg-reporting',
  title: 'ESG Reporting & Frameworks',
  description: 'SASB, TCFD, GRI, EU Taxonomy, ISSB — Prof. Tuna standardizes your sustainability reporting.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '📋',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'er-sasb',
      slug: 'sasb',
      title: 'SASB Standards',
      description: 'Industry-specific ESG disclosure standards.',
      commands: ['esg framework sasb', 'esg report sasb'],
      steps: [
        { instruction: 'View SASB metrics for a company: `esg framework sasb AAPL`', command: 'esg framework sasb AAPL', expectedOutput: 'SASB materiality map and metrics' },
        { instruction: 'SASB = Sustainability Accounting Standards Board. 77 industry-specific standards.' },
        { instruction: 'Generate SASB report: `esg report sasb AAPL`', command: 'esg report sasb AAPL', expectedOutput: 'SASB-aligned sustainability report' },
      ],
      quiz: [
        { question: 'How many industry standards does SASB have?', options: ['77', '50', '100', '20'], correctIndex: 0, explanation: 'SASB has 77 industry-specific sustainability accounting standards.' },
      ],
    },
    {
      id: 'er-tcfd',
      slug: 'tcfd',
      title: 'TCFD & Climate Disclosures',
      description: 'Task Force on Climate-related Financial Disclosures.',
      commands: ['esg framework tcfd', 'climate report'],
      steps: [
        { instruction: 'View TCFD framework: `esg framework tcfd`', command: 'esg framework tcfd', expectedOutput: 'TCFD pillars: governance, strategy, risk management, metrics' },
        { instruction: 'TCFD covers four areas: governance, strategy, risk management, and metrics/targets.' },
        { instruction: 'Generate TCFD report: `climate report tcfd portfolio 1`', command: 'climate report tcfd portfolio 1', expectedOutput: 'TCFD-aligned climate report' },
      ],
      quiz: [
        { question: 'How many pillars does the TCFD framework have?', options: ['4', '3', '5', '6'], correctIndex: 0, explanation: 'TCFD has four pillars: governance, strategy, risk management, and metrics and targets.' },
      ],
    },
    {
      id: 'er-gri',
      slug: 'gri',
      title: 'GRI & EU Taxonomy',
      description: 'Global Reporting Initiative and European sustainability taxonomy.',
      commands: ['esg framework gri', 'esg taxonomy'],
      steps: [
        { instruction: 'View GRI standards: `esg framework gri`', command: 'esg framework gri', expectedOutput: 'GRI universal, sector, and topic standards' },
        { instruction: 'EU Taxonomy classifies economic activities as environmentally sustainable.' },
        { instruction: 'Check EU Taxonomy alignment: `esg taxonomy AAPL`', command: 'esg taxonomy AAPL', expectedOutput: 'Taxonomy-eligible and aligned revenue percentage' },
      ],
      quiz: [
        { question: 'What does the EU Taxonomy classify?', options: ['Environmentally sustainable activities', 'Carbon credit quality', 'Green bond certification', 'Company credit ratings'], correctIndex: 0, explanation: 'The EU Taxonomy provides a classification system for environmentally sustainable economic activities.' },
      ],
    },
    {
      id: 'er-issb',
      slug: 'issb',
      title: 'ISSB & Future of Reporting',
      description: 'International Sustainability Standards Board — the global baseline.',
      commands: ['esg framework issb', 'esg report issb'],
      steps: [
        { instruction: 'View ISSB standards: `esg framework issb`', command: 'esg framework issb', expectedOutput: 'IFRS S1 and S2 overview' },
        { instruction: 'ISSB = International Sustainability Standards Board. Created by IFRS Foundation.' },
        { instruction: 'ISSB is consolidating SASB, TCFD, and CDSB into a global baseline.' },
      ],
      quiz: [
        { question: 'Which organization created the ISSB?', options: ['IFRS Foundation', 'United Nations', 'World Bank', 'SASB'], correctIndex: 0, explanation: 'The ISSB was created by the IFRS Foundation to develop a global baseline of sustainability disclosures.' },
      ],
    },
  ],
}
