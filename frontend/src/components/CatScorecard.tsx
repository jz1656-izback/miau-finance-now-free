import { useState, useEffect } from 'react'
import { Award } from 'lucide-react'

interface CatMetrics {
  fishEarned: number // LoC, tests, features
  purrMeter: number // 0-100 team velocity
  catLives: number // error recovery
  whiskerQuality: number // code quality %
  pawPrints: number // feature adoption
}

interface CatScorecardProps {
  metrics?: Partial<CatMetrics>
  hideAnimation?: boolean
}

const DEFAULT_METRICS: CatMetrics = {
  fishEarned: 42,
  purrMeter: 78,
  catLives: 9,
  whiskerQuality: 89,
  pawPrints: 234,
}

export default function CatScorecard({ metrics = {}, hideAnimation = false }: CatScorecardProps) {
  const [animatedMetrics, setAnimatedMetrics] = useState<CatMetrics>(DEFAULT_METRICS)
  const [catMood, setCatMood] = useState<'happy' | 'excited' | 'focused' | 'napping'>('happy')
  const [meowCount, setMeowCount] = useState(0)

  const mergedMetrics = { ...DEFAULT_METRICS, ...metrics }

  useEffect(() => {
    if (!hideAnimation) {
      const interval = setInterval(() => {
        setAnimatedMetrics((prev) => ({
          ...prev,
          purrMeter: Math.min(mergedMetrics.purrMeter, prev.purrMeter + 2),
          whiskerQuality: Math.min(mergedMetrics.whiskerQuality, prev.whiskerQuality + 1),
          pawPrints: Math.min(mergedMetrics.pawPrints, prev.pawPrints + 5),
        }))
      }, 50)
      return () => clearInterval(interval)
    }
    return
  }, [mergedMetrics, hideAnimation])

  // Determine cat mood based on metrics
  useEffect(() => {
    if (animatedMetrics.purrMeter >= 90) setCatMood('excited')
    else if (animatedMetrics.purrMeter >= 70) setCatMood('happy')
    else if (animatedMetrics.purrMeter >= 40) setCatMood('focused')
    else setCatMood('napping')
  }, [animatedMetrics.purrMeter])

  const getCatEmoji = () => {
    switch (catMood) {
      case 'excited':
        return '😻'
      case 'happy':
        return '😸'
      case 'focused':
        return '😼'
      case 'napping':
        return '😴'
    }
  }

  const getMoodText = () => {
    switch (catMood) {
      case 'excited':
        return 'TURBO MODE! 🚀'
      case 'happy':
        return 'Purring along nicely'
      case 'focused':
        return 'Focused on the hunt'
      case 'napping':
        return 'Time for a catnap'
    }
  }

  const playMeow = () => {
    setMeowCount((prev) => prev + 1)
    // In a real app, play audio here
    const meows = ['Meow~', 'MEOW!', 'mrrrow...', 'prrrr']
    console.log(meows[meowCount % meows.length])
  }

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-lg p-6 border border-slate-700 shadow-lg">
      {/* Header with Cat */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            🐱 CAT PRODUCTIVITY SCORECARD
          </h2>
          <p className="text-sm text-slate-400 mt-1">{getMoodText()}</p>
        </div>
        <button
          onClick={playMeow}
          className="text-4xl hover:scale-110 transition cursor-pointer"
          title="Meow!"
        >
          {getCatEmoji()}
        </button>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {/* Fish Earned */}
        <div className="bg-slate-800 rounded p-3 border border-emerald-600/30 hover:border-emerald-500 transition">
          <div className="text-xs text-emerald-400 uppercase font-bold">Fish Earned</div>
          <div className="text-2xl font-bold text-emerald-300 mt-2">🐟 {animatedMetrics.fishEarned}</div>
          <div className="text-xs text-slate-500 mt-1">Features shipped</div>
        </div>

        {/* Purr Meter */}
        <div className="bg-slate-800 rounded p-3 border border-pink-600/30 hover:border-pink-500 transition">
          <div className="text-xs text-pink-400 uppercase font-bold">Purr Meter</div>
          <div className="text-2xl font-bold text-pink-300 mt-2">{animatedMetrics.purrMeter}%</div>
          <div className="mt-2 bg-slate-700 rounded h-2 overflow-hidden">
            <div
              className="bg-pink-500 h-full transition-all duration-300"
              style={{ width: `${animatedMetrics.purrMeter}%` }}
            />
          </div>
        </div>

        {/* Cat Lives */}
        <div className="bg-slate-800 rounded p-3 border border-red-600/30 hover:border-red-500 transition">
          <div className="text-xs text-red-400 uppercase font-bold">Cat Lives</div>
          <div className="text-2xl font-bold text-red-300 mt-2">
            {Array(Math.max(1, animatedMetrics.catLives))
              .fill(0)
              .map((_, i) => (
                <span key={i}>❤️</span>
              ))}
          </div>
          <div className="text-xs text-slate-500 mt-1">Error recovery</div>
        </div>

        {/* Whisker Quality */}
        <div className="bg-slate-800 rounded p-3 border border-blue-600/30 hover:border-blue-500 transition">
          <div className="text-xs text-blue-400 uppercase font-bold">Whisker Quality</div>
          <div className="text-2xl font-bold text-blue-300 mt-2">{animatedMetrics.whiskerQuality}%</div>
          <div className="mt-2 bg-slate-700 rounded h-2 overflow-hidden">
            <div
              className="bg-blue-500 h-full transition-all duration-300"
              style={{ width: `${animatedMetrics.whiskerQuality}%` }}
            />
          </div>
        </div>

        {/* Paw Prints */}
        <div className="bg-slate-800 rounded p-3 border border-amber-600/30 hover:border-amber-500 transition">
          <div className="text-xs text-amber-400 uppercase font-bold">Paw Prints</div>
          <div className="text-2xl font-bold text-amber-300 mt-2">👣 {animatedMetrics.pawPrints}</div>
          <div className="text-xs text-slate-500 mt-1">Users engaged</div>
        </div>
      </div>

      {/* Achievement Status */}
      <div className="bg-slate-800 rounded p-4 border border-slate-600 mb-4">
        <div className="text-sm font-bold text-slate-300 mb-3 flex items-center gap-2">
          <Award size={16} className="text-amber-400" />
          ACHIEVEMENTS UNLOCKED
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 text-xs">
          {animatedMetrics.purrMeter >= 70 && (
            <div className="bg-emerald-900/30 border border-emerald-600 rounded px-2 py-1 text-emerald-400">
              🏅 First Purr
            </div>
          )}
          {animatedMetrics.whiskerQuality >= 85 && (
            <div className="bg-blue-900/30 border border-blue-600 rounded px-2 py-1 text-blue-400">
              🏅 Clean Code
            </div>
          )}
          {animatedMetrics.fishEarned >= 10 && (
            <div className="bg-amber-900/30 border border-amber-600 rounded px-2 py-1 text-amber-400">
              🏅 Fish Feast
            </div>
          )}
          {animatedMetrics.pawPrints >= 100 && (
            <div className="bg-pink-900/30 border border-pink-600 rounded px-2 py-1 text-pink-400">
              🏅 Popular Cat
            </div>
          )}
          {animatedMetrics.catLives === 9 && (
            <div className="bg-red-900/30 border border-red-600 rounded px-2 py-1 text-red-400">
              🏅 Nine Lives
            </div>
          )}
        </div>
      </div>

      {/* Mood Message */}
      <div className="text-center text-xs text-slate-400 italic">
        {catMood === 'excited' &&
          '🐱 The team is ON FIRE! Keep up the amazing work, meow!'}
        {catMood === 'happy' &&
          '😸 Things are looking good! Keep pushing forward!'}
        {catMood === 'focused' &&
          '😼 Focus mode activated. The team is hunting for bugs!'}
        {catMood === 'napping' &&
          '😴 Time to rest and recharge. Take a break!'}
      </div>
    </div>
  )
}
