import type { Course } from '../lib/types'

export const agricultureFinance: Course = {
  id: 'agriculture-finance',
  slug: 'agriculture-commodity-finance',
  title: 'Agriculture & Commodity Finance',
  description: 'Crop insurance, commodity hedging, and farmland valuation — the cat manages the financial side of its catnip farm.',
  category: 'Commodities',
  difficulty: 'intermediate',
  icon: '🌾',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'crop-insurance',
      slug: 'crop-insurance-basics',
      title: 'Crop Insurance Fundamentals',
      description: 'Protecting agricultural production against losses.',
      commands: ['crop', 'agri', 'hedge'],
      steps: [
        { instruction: 'Analyze crop insurance options: `crop --insurance --crop corn --acres 1000 --APH 180 --coverage-level 0.80`', command: 'crop --insurance --crop corn --acres 1000 --APH 180 --coverage-level 0.80', expectedOutput: 'Crop insurance (corn): 1,000 acres, APH 180 bu/acre, 80% coverage. Revenue guarantee: $720/acre ($144K total). Premium: $18/acre ($18K). Subsidy: 62%' },
        { instruction: 'Crop insurance protects farmers against yield losses and price declines.' },
        { instruction: 'The cat catnip farm has crop insurance — if the catnip fails, the cat gets compensated in tuna.' },
      ],
      quiz: [
        { question: 'What is APH (Actual Production History) in crop insurance?', options: ['The historical average yield per acre used to calculate coverage guarantees', 'The price of the crop at harvest', 'The insurance premium amount', 'The number of acres insured'], correctIndex: 0, explanation: 'APH is the average yield per acre over a historical period (typically 10 years) used as the basis for calculating crop insurance guarantees.' },
      ],
    },
    {
      id: 'commodity-hedging',
      slug: 'commodity-hedging-agriculture',
      title: 'Commodity Hedging for Agriculture',
      description: 'Using futures and options to hedge crop prices.',
      commands: ['hedge', 'crop', 'agri'],
      steps: [
        { instruction: 'Hedge corn price risk: `hedge --crop corn --price 4.50 --target 4.20 --protection 100000-bushels`', command: 'hedge --crop corn --price 4.50 --target 4.20 --protection 100000-bushels', expectedOutput: 'Corn hedge: Sell 20 Dec futures contracts at $4.50. Put option strike $4.20, premium $0.15/bu. Floor price: $4.05 ($4.20 - $0.15). Max hedge cost: $15,000' },
        { instruction: 'Commodity hedging uses futures and options to lock in prices and manage risk.' },
        { instruction: 'The cat hedges its catnip crop every season — it knows that catnip prices are volatile.' },
      ],
      quiz: [
        { question: 'What is the purpose of a short hedge for a farmer?', options: ['To lock in a selling price for a crop that has not yet been harvested', 'To speculate on rising prices', 'To buy more land', 'To reduce insurance costs'], correctIndex: 0, explanation: 'A short hedge involves selling futures contracts to lock in a price for crops that will be harvested in the future, protecting against price declines.' },
      ],
    },
    {
      id: 'farmland-valuation',
      slug: 'farmland-valuation-methods',
      title: 'Farmland Valuation',
      description: 'Methods for valuing agricultural land.',
      commands: ['farmland', 'agri', 'crop'],
      steps: [
        { instruction: 'Value farmland: `farmland --value --acres 500 --county "Story County IA" --crop-rotation "corn/soy"`', command: 'farmland --value --acres 500 --county "Story County IA" --crop-rotation "corn/soy"', expectedOutput: 'Farmland value: $12,000/acre ($6M total). Income approach: $850/acre NOI, 7.1% cap rate. Sales comp: $11,500-$12,500/acre. CSR2 rating: 85 (excellent quality)' },
        { instruction: 'Farmland valuation uses income, sales comparison, and soil quality approaches.' },
        { instruction: 'The cat farmland is prime catnip-growing soil — CSR2 rating of 95 out of 100.' },
      ],
      quiz: [
        { question: 'What is a cap rate in farmland valuation?', options: ['Net operating income per acre divided by land value per acre', 'The maximum crop yield', 'The capitalization of the farming company', 'The interest rate on farm loans'], correctIndex: 0, explanation: 'The capitalization rate for farmland is calculated by dividing the net operating income per acre by the market value per acre.' },
      ],
    },
    {
      id: 'agri-investing',
      slug: 'agriculture-investing-strategies',
      title: 'Agriculture Investing Strategies',
      description: 'Direct and indirect agriculture investments.',
      commands: ['agri', 'farmland', 'hedge'],
      steps: [
        { instruction: 'Build an agriculture allocation: `agri --allocate --capital 200000 --vehicles "farmland:40,commodity-etfs:30,agri-stocks:20,timber:10"`', command: 'agri --allocate --capital 200000 --vehicles "farmland:40,commodity-etfs:30,agri-stocks:20,timber:10"', expectedOutput: 'Agri portfolio: $80K farmland (7-10% return, illiquid), $60K DBA (commodity ETF), $40K Deere/ADM (stocks), $20K timber (8-12%, 15yr horizon)' },
        { instruction: 'Agriculture offers inflation protection and low correlation to equities.' },
        { instruction: 'The cat agriculture portfolio is overweight catnip and tuna fishing — a concentrated but delicious bet.' },
      ],
      quiz: [
        { question: 'What makes agriculture an attractive portfolio diversifier?', options: ['Low correlation with equity and bond markets plus inflation hedging characteristics', 'High correlation with technology stocks', 'Guaranteed 15% annual returns', 'Government price supports'], correctIndex: 0, explanation: 'Agriculture investments have historically shown low correlation to traditional financial assets and provide a hedge against inflation.' },
      ],
    },
  ],
}
