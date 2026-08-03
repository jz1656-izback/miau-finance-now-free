import type { Course } from '../lib/types'

export const cleantechFinance: Course = {
  id: 'cleantech-finance',
  slug: 'cleantech-renewable-energy',
  title: 'CleanTech & Renewable Energy',
  description: 'Solar, wind, battery, hydrogen, and renewable project finance — the cat powers its electronic mouse charger with clean energy.',
  category: 'ESG',
  difficulty: 'intermediate',
  icon: '☀️',
  lessonCount: 4,
  estimatedMinutes: 20,
  lessons: [
    {
      id: 'solar-energy',
      slug: 'solar-energy-economics',
      title: 'Solar Energy Economics',
      description: 'The business of solar power generation.',
      commands: ['solar', 'cleantech', 'renewable'],
      steps: [
        { instruction: 'Analyze solar project economics: `solar --project --capacity 100MW --location "Nevada" --ppA-price 0.035 --capex 80M`', command: 'solar --project --capacity 100MW --location "Nevada" --ppA-price 0.035 --capex 80M', expectedOutput: 'Solar farm 100MW: Capex $80M ($800/kW). Annual revenue: $12.3M (200 GWh x $0.035). Opex: $1.5M. IRR: 8.2%. Payback: 9 years. LCOE: $0.028/kWh' },
        { instruction: 'Solar LCOE has fallen 90% in the last decade, making it the cheapest energy source in history.' },
        { instruction: 'The cat installed solar panels on its cat house — now the electric mouse charges for free.' },
      ],
      quiz: [
        { question: 'What does LCOE (Levelized Cost of Energy) measure?', options: ['The average cost per unit of electricity over a power plant lifetime', 'The upfront installation cost', 'The retail price of electricity', 'The cost of solar panels only'], correctIndex: 0, explanation: 'LCOE represents the average cost of generating one unit of electricity over the entire lifetime of a power plant, including all costs.' },
      ],
    },
    {
      id: 'wind-energy',
      slug: 'wind-energy-economics',
      title: 'Wind Energy Economics',
      description: 'Onshore and offshore wind project finance.',
      commands: ['wind', 'cleantech', 'renewable'],
      steps: [
        { instruction: 'Compare onshore vs offshore wind: `wind --compare --onshore-capacity 200MW --offshore-capacity 1000MW`', command: 'wind --compare --onshore-capacity 200MW --offshore-capacity 1000MW', expectedOutput: 'Onshore (200MW): Capex $1,400/kW, LCOE $0.032/kWh, capacity factor 35%. Offshore (1GW): Capex $3,500/kW, LCOE $0.060/kWh, capacity factor 50%' },
        { instruction: 'Offshore wind has higher costs but better capacity factors and less intermittency.' },
        { instruction: 'The cat tried wind energy — it attached a tiny turbine to its tail and generates power while chasing it.' },
      ],
      quiz: [
        { question: 'Why does offshore wind have higher capacity factors than onshore wind?', options: ['Stronger and more consistent wind speeds at sea produce more hours of generation', 'Offshore turbines are larger', 'Offshore wind has less maintenance', 'Offshore wind uses better technology'], correctIndex: 0, explanation: 'Offshore wind farms benefit from stronger, more consistent wind speeds over the ocean, resulting in more hours of electricity generation per year.' },
      ],
    },
    {
      id: 'battery-storage',
      slug: 'battery-energy-storage',
      title: 'Battery & Energy Storage',
      description: 'The economics of energy storage systems.',
      commands: ['battery', 'cleantech', 'renewable', 'hydrogen'],
      steps: [
        { instruction: 'Analyze battery storage economics: `battery --project --capacity 100MW --duration 4hrs --capex 200M --cycles 6000`', command: 'battery --project --capacity 100MW --duration 4hrs --capex 200M --cycles 6000', expectedOutput: 'Battery storage 100MW/400MWh: Capex $200M ($500/kWh). Daily arbitrage: $15K (charge $30/MWh, discharge $80/MWh). IRR: 6.5%. Degradation: 2%/year' },
        { instruction: 'Battery storage enables renewable energy to shift generation to peak demand hours.' },
        { instruction: 'The cat battery backup keeps the automatic feeder running during power outages — priorities.' },
      ],
      quiz: [
        { question: 'What is the primary revenue stream for grid-scale battery storage?', options: ['Energy arbitrage — buying cheap power and selling during peak prices', 'Selling batteries to consumers', 'Government subsidies only', 'Charging electric vehicles'], correctIndex: 0, explanation: 'Grid-scale batteries generate revenue primarily through energy arbitrage, charging when electricity is cheap and discharging when prices are high.' },
      ],
    },
    {
      id: 'hydrogen-economy',
      slug: 'hydrogen-economy-finance',
      title: 'Hydrogen Economy & Finance',
      description: 'Green hydrogen production and project finance.',
      commands: ['hydrogen', 'cleantech', 'renewable'],
      steps: [
        { instruction: 'Evaluate green hydrogen project: `hydrogen --project --electrolyzer 100MW --cost 150M --electricity-price 0.025`', command: 'hydrogen --project --electrolyzer 100MW --cost 150M --electricity-price 0.025', expectedOutput: 'Green H2 project: 100MW PEM electrolyzer, $150M capex. Production: 15 tons H2/day at $4.50/kg. Required PPA price: $4.00/kg for 10% IRR. Grid power: $0.025/kWh' },
        { instruction: 'Green hydrogen is produced using renewable electricity and electrolysis.' },
        { instruction: 'The cat is bullish on hydrogen — it powers its own hydrogen fuel cell with catnip.' },
      ],
      quiz: [
        { question: 'What is green hydrogen?', options: ['Hydrogen produced via electrolysis using renewable electricity with zero CO2 emissions', 'Hydrogen extracted from natural gas', 'Hydrogen that is colored green', 'Hydrogen from nuclear power'], correctIndex: 0, explanation: 'Green hydrogen is produced by splitting water into hydrogen and oxygen using electrolysis powered by renewable energy sources, with no direct carbon emissions.' },
      ],
    },
  ],
}
