/**
 * 🏆 CAT ACHIEVEMENTS SYSTEM
 * Gamified achievement tracking for user engagement and retention.
 * Persists to localStorage. Unlock triggers cat sound effects.
 */

export interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  category: 'trading' | 'portfolio' | 'analytics' | 'community' | 'secret'
  rarity: 'common' | 'rare' | 'epic' | 'legendary' | 'mythic'
  condition: (state: AchievementState) => boolean
  /** Points toward the overall cat ranking */
  points: number
}

export interface AchievementState {
  numTrades: number
  numPortfolios: number
  numInstruments: number
  numCommandsExecuted: number
  numAnalyticsRuns: number
  highestSharpe: number
  totalAum: number
  totalPnL: number
  consecutiveDaysActive: number
  numSocialShares: number
  numFollowers: number
}

export interface UnlockedAchievement extends Achievement {
  unlockedAt: string
}

const ACHIEVEMENTS: Achievement[] = [
  // ── Trading ──
  {
    id: 'first-trade',
    title: 'First Trade',
    description: 'Execute your very first trade',
    icon: '🐾',
    category: 'trading',
    rarity: 'common',
    points: 10,
    condition: (s) => s.numTrades >= 1,
  },
  {
    id: 'ten-trades',
    title: 'Cat Trader',
    description: 'Execute 10 trades',
    icon: '🐱',
    category: 'trading',
    rarity: 'common',
    points: 30,
    condition: (s) => s.numTrades >= 10,
  },
  {
    id: 'hundred-trades',
    title: 'Market Meow',
    description: 'Execute 100 trades',
    icon: '😼',
    category: 'trading',
    rarity: 'rare',
    points: 100,
    condition: (s) => s.numTrades >= 100,
  },
  {
    id: 'five-hundred-trades',
    title: 'Whisker Warrior',
    description: 'Execute 500 trades',
    icon: '⚔️',
    category: 'trading',
    rarity: 'epic',
    points: 500,
    condition: (s) => s.numTrades >= 500,
  },

  // ── Portfolio ──
  {
    id: 'first-portfolio',
    title: 'Your First Litter',
    description: 'Create your first portfolio',
    icon: '📦',
    category: 'portfolio',
    rarity: 'common',
    points: 10,
    condition: (s) => s.numPortfolios >= 1,
  },
  {
    id: 'portfolio-master',
    title: 'Portfolio Master',
    description: 'Create 5 portfolios',
    icon: '👑',
    category: 'portfolio',
    rarity: 'rare',
    points: 50,
    condition: (s) => s.numPortfolios >= 5,
  },
  {
    id: 'fish-feast',
    title: 'Fish Feast',
    description: 'Reach $100K+ in assets under management',
    icon: '🐟',
    category: 'portfolio',
    rarity: 'epic',
    points: 200,
    condition: (s) => s.totalAum >= 100_000,
  },
  {
    id: 'whale-pod',
    title: 'Whale Pod',
    description: 'Reach $1M+ in assets under management',
    icon: '🐋',
    category: 'portfolio',
    rarity: 'legendary',
    points: 1000,
    condition: (s) => s.totalAum >= 1_000_000,
  },
  {
    id: 'profit-purr',
    title: 'Profit Purr',
    description: 'Achieve positive total P&L',
    icon: '💚',
    category: 'portfolio',
    rarity: 'common',
    points: 20,
    condition: (s) => s.totalPnL > 0,
  },
  {
    id: 'mega-profit',
    title: 'Mega Profit',
    description: 'Achieve $10K+ total P&L',
    icon: '💰',
    category: 'portfolio',
    rarity: 'rare',
    points: 150,
    condition: (s) => s.totalPnL >= 10_000,
  },

  // ── Analytics ──
  {
    id: 'first-analytics',
    title: 'Curious Kitten',
    description: 'Run your first analytics report',
    icon: '🔍',
    category: 'analytics',
    rarity: 'common',
    points: 10,
    condition: (s) => s.numAnalyticsRuns >= 1,
  },
  {
    id: 'sharp-kitty',
    title: 'Sharpe Kitty',
    description: 'Achieve Sharpe ratio above 2.0',
    icon: '📈',
    category: 'analytics',
    rarity: 'rare',
    points: 100,
    condition: (s) => s.highestSharpe >= 2.0,
  },
  {
    id: 'god-mode',
    title: 'Cat Burglar',
    description: 'Achieve Sharpe ratio above 5.0',
    icon: '💎',
    category: 'analytics',
    rarity: 'legendary',
    points: 500,
    condition: (s) => s.highestSharpe >= 5.0,
  },
  {
    id: 'cat-army',
    title: 'Cat Army',
    description: 'Execute 50+ terminal commands',
    icon: '🐈',
    category: 'analytics',
    rarity: 'common',
    points: 25,
    condition: (s) => s.numCommandsExecuted >= 50,
  },
  {
    id: 'power-user',
    title: 'Terminal Power User',
    description: 'Execute 500+ terminal commands',
    icon: '⚡',
    category: 'analytics',
    rarity: 'rare',
    points: 150,
    condition: (s) => s.numCommandsExecuted >= 500,
  },
  {
    id: 'ninja-kitty',
    title: 'Ninja Kitty',
    description: 'Execute 5000+ terminal commands',
    icon: '🥷',
    category: 'analytics',
    rarity: 'epic',
    points: 1000,
    condition: (s) => s.numCommandsExecuted >= 5000,
  },

  // ── Community ──
  {
    id: 'social-paws',
    title: 'Social Paws',
    description: 'Share your first portfolio',
    icon: '🤝',
    category: 'community',
    rarity: 'common',
    points: 15,
    condition: (s) => s.numSocialShares >= 1,
  },
  {
    id: 'influencer',
    title: 'Catfluencer',
    description: 'Gain 10 followers',
    icon: '🌟',
    category: 'community',
    rarity: 'rare',
    points: 75,
    condition: (s) => s.numFollowers >= 10,
  },
  {
    id: 'celebrity',
    title: 'Celebrity Cat',
    description: 'Gain 100 followers',
    icon: '🎭',
    category: 'community',
    rarity: 'epic',
    points: 500,
    condition: (s) => s.numFollowers >= 100,
  },

  // ── Secret/Streak ──
  {
    id: 'seven-day-streak',
    title: 'Seven Lives Streak',
    description: 'Stay active 7 consecutive days',
    icon: '📅',
    category: 'secret',
    rarity: 'rare',
    points: 100,
    condition: (s) => s.consecutiveDaysActive >= 7,
  },
  {
    id: 'thirty-day-streak',
    title: 'Nine Lives Club',
    description: 'Stay active 30 consecutive days',
    icon: '🔥',
    category: 'secret',
    rarity: 'legendary',
    points: 500,
    condition: (s) => s.consecutiveDaysActive >= 30,
  },
  {
    id: 'hundred-day-streak',
    title: 'Immortal Cat',
    description: 'Stay active 100 consecutive days',
    icon: '♾️',
    category: 'secret',
    rarity: 'mythic',
    points: 2000,
    condition: (s) => s.consecutiveDaysActive >= 100,
  },
  {
    id: 'data-sleuth',
    title: 'Data Sleuth',
    description: 'Analyze 50+ different instruments',
    icon: '🕵️',
    category: 'analytics',
    rarity: 'rare',
    points: 100,
    condition: (s) => s.numInstruments >= 50,
  },
]

// ── Storage ──
const STORAGE_KEY = 'miau_achievements'

interface StoredData {
  unlocked: Record<string, string> // achievement id → ISO timestamp
  state: AchievementState
  lastActive: string
}

function load(): StoredData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    /* corrupt data — reset */
  }
  return {
    unlocked: {},
    state: {
      numTrades: 0,
      numPortfolios: 0,
      numInstruments: 0,
      numCommandsExecuted: 0,
      numAnalyticsRuns: 0,
      highestSharpe: 0,
      totalAum: 0,
      totalPnL: 0,
      consecutiveDaysActive: 1,
      numSocialShares: 0,
      numFollowers: 0,
    },
    lastActive: new Date().toISOString(),
  }
}

function save(data: StoredData): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

// ── Public API ──

export function getAchievementState(): AchievementState {
  return load().state
}

export function updateAchievementState(partial: Partial<AchievementState>): UnlockedAchievement[] {
  const data = load()
  Object.assign(data.state, partial)
  // Track streaks
  const today = new Date().toISOString().slice(0, 10)
  const lastActive = data.lastActive.slice(0, 10)
  if (today !== lastActive) {
    const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10)
    if (lastActive === yesterday) {
      data.state.consecutiveDaysActive += 1
    } else if (lastActive !== today) {
      data.state.consecutiveDaysActive = 1
    }
    data.lastActive = new Date().toISOString()
  }

  // Check for newly unlocked achievements
  const newlyUnlocked: UnlockedAchievement[] = []
  for (const ach of ACHIEVEMENTS) {
    if (!data.unlocked[ach.id] && ach.condition(data.state)) {
      const timestamp = new Date().toISOString()
      data.unlocked[ach.id] = timestamp
      newlyUnlocked.push({ ...ach, unlockedAt: timestamp })
    }
  }

  save(data)
  return newlyUnlocked
}

export function getUnlockedAchievements(): UnlockedAchievement[] {
  const data = load()
  return ACHIEVEMENTS
    .filter((a) => data.unlocked[a.id])
    .map((a) => ({ ...a, unlockedAt: data.unlocked[a.id] }))
}

export function getAllAchievements(): Achievement[] {
  return ACHIEVEMENTS
}

export function getUnlockedCount(): number {
  return Object.keys(load().unlocked).length
}

export function getTotalPoints(): number {
  const data = load()
  let points = 0
  for (const id of Object.keys(data.unlocked)) {
    const ach = ACHIEVEMENTS.find((a) => a.id === id)
    if (ach) points += ach.points
  }
  return points
}

export function getRank(): { title: string; icon: string; emoji: string } {
  const points = getTotalPoints()
  if (points >= 5000) return { title: 'Mythic Meowster', icon: '👑', emoji: '😻' }
  if (points >= 2000) return { title: 'Legendary Lion', icon: '🦁', emoji: '😸' }
  if (points >= 1000) return { title: 'Epic Panther', icon: '🐆', emoji: '😼' }
  if (points >= 500) return { title: 'Rare Lynx', icon: '🐱', emoji: '😺' }
  if (points >= 200) return { title: 'Savvy Siamese', icon: '🐈', emoji: '😽' }
  if (points >= 50) return { title: 'Tabby Trainee', icon: '🐾', emoji: '😿' }
  return { title: 'Newborn Kitten', icon: '🐣', emoji: '🥺' }
}

export function getProgress(achievementId: string): number {
  const stored = load()
  const ach = ACHIEVEMENTS.find((a) => a.id === achievementId)
  if (!ach || stored.unlocked[achievementId]) return 100

  const s = stored.state
  // Heuristic progress for each achievement
  switch (achievementId) {
    case 'first-trade': return Math.min(100, s.numTrades * 100)
    case 'ten-trades': return Math.min(100, (s.numTrades / 10) * 100)
    case 'hundred-trades': return Math.min(100, (s.numTrades / 100) * 100)
    case 'five-hundred-trades': return Math.min(100, (s.numTrades / 500) * 100)
    case 'first-portfolio': return Math.min(100, s.numPortfolios * 100)
    case 'portfolio-master': return Math.min(100, (s.numPortfolios / 5) * 100)
    case 'fish-feast': return Math.min(100, (s.totalAum / 100_000) * 100)
    case 'whale-pod': return Math.min(100, (s.totalAum / 1_000_000) * 100)
    case 'profit-purr': return s.totalPnL > 0 ? 100 : Math.min(100, (s.totalPnL + 1000) / 10)
    case 'mega-profit': return Math.min(100, (s.totalPnL / 10_000) * 100)
    case 'first-analytics': return Math.min(100, s.numAnalyticsRuns * 100)
    case 'sharp-kitty': return Math.min(100, (s.highestSharpe / 2.0) * 100)
    case 'god-mode': return Math.min(100, (s.highestSharpe / 5.0) * 100)
    case 'cat-army': return Math.min(100, (s.numCommandsExecuted / 50) * 100)
    case 'power-user': return Math.min(100, (s.numCommandsExecuted / 500) * 100)
    case 'ninja-kitty': return Math.min(100, (s.numCommandsExecuted / 5000) * 100)
    case 'social-paws': return Math.min(100, s.numSocialShares * 100)
    case 'influencer': return Math.min(100, (s.numFollowers / 10) * 100)
    case 'celebrity': return Math.min(100, (s.numFollowers / 100) * 100)
    case 'seven-day-streak': return Math.min(100, (s.consecutiveDaysActive / 7) * 100)
    case 'thirty-day-streak': return Math.min(100, (s.consecutiveDaysActive / 30) * 100)
    case 'hundred-day-streak': return Math.min(100, (s.consecutiveDaysActive / 100) * 100)
    case 'data-sleuth': return Math.min(100, (s.numInstruments / 50) * 100)
    default: return 0
  }
}

/** Reset all achievements (for testing) */
export function resetAchievements(): void {
  localStorage.removeItem(STORAGE_KEY)
}
