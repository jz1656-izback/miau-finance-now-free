export interface Kitten {
  id: string
  name: string
  emoji: string
  role: string
  color: string
  skill: string
  level: number
  description: string
  unlocked: boolean
}

export const KITTEN_SQUAD: Kitten[] = [
  { id: 'luna', name: 'Luna', emoji: '🎓', role: 'Quant Intern', color: '#00e676', skill: 'Python & Algorithms', level: 5, unlocked: true, description: 'Knows more about quant finance than most PhDs. Purrs in numpy.' },
  { id: 'felix', name: 'Felix', emoji: '📊', role: 'Risk Analyst', color: '#a855f7', skill: 'VaR & Stress Testing', level: 4, unlocked: true, description: '9 lives of VaR experience. Has never been liquidated.' },
  { id: 'mochi', name: 'Mochi', emoji: '💻', role: 'Full-Stack Dev', color: '#22d3ee', skill: 'React & FastAPI', level: 5, unlocked: true, description: 'Codes in his sleep. Literally. The terminal compiles his dreams.' },
  { id: 'simba', name: 'Simba', emoji: '📈', role: 'M&A Kitten', color: '#f472b6', skill: 'DCF & LBO Models', level: 3, unlocked: true, description: 'Acquiring catnip futures. Hostile takeover of the treat jar.' },
  { id: 'oreo', name: 'Oreo', emoji: '🔬', role: 'Data Scientist', color: '#fb923c', skill: 'ML & Anomaly Detection', level: 4, unlocked: true, description: 'Chases laser pointers and statistical alpha. Equally entertained by both.' },
  { id: 'tigger', name: 'Tigger', emoji: '💰', role: 'DeFi Kitten', color: '#facc15', skill: 'Yield Farming & Web3', level: 3, unlocked: true, description: 'Farms yield in his sleep. Portfolio is 100% degen. No regrets.' },
  { id: 'whiskers', name: 'Whiskers', emoji: '🚀', role: 'Crypto Native', color: '#00e676', skill: 'On-Chain Analysis', level: 4, unlocked: true, description: 'Has paws on the pulse of every chain. Still buys the dip.' },
  { id: 'mittens', name: 'Mittens', emoji: '🏦', role: 'IB Kitten', color: '#6366f1', skill: 'Excel & Catnaps', level: 5, unlocked: true, description: 'Excel expert. Catnap expert. Has mastered the art of looking busy.' },
  { id: 'sasha', name: 'Sasha', emoji: '🤖', role: 'AI/ML Kitten', color: '#ec4899', skill: 'LLMs & RL Trading', level: 4, unlocked: true, description: 'Training models and purring. The models are confused by the purring.' },
  { id: 'pepper', name: 'Pepper', emoji: '📉', role: 'Short Seller', color: '#ef4444', skill: 'Short Squeeze Detection', level: 3, unlocked: true, description: 'Bear markets love this cat. Bull markets tolerate him.' },
]

export function getKitten(id: string): Kitten | undefined {
  return KITTEN_SQUAD.find(k => k.id === id || k.name.toLowerCase() === id.toLowerCase())
}

export function getKittensBySkill(skill: string): Kitten[] {
  return KITTEN_SQUAD.filter(k => k.skill.toLowerCase().includes(skill.toLowerCase()))
}
