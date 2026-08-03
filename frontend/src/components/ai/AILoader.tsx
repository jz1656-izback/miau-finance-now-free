import { useState, useEffect } from 'react'

const CAT_FRAMES = [
  '  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ',
  '  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ  🤔',
  '  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ  🧐',
  '  ╱|、\n (˚ˎ 。7\n  |、˜〵\n  じしˍ,)ノ  💭',
]

const LOADING_TEXTS = [
  'analyzing markets...',
  'consulting the cat oracle...',
  'sharpening claws on data...',
  'chasing outliers...',
  'pouncing on insights...',
  'purring over probabilities...',
  'stalking opportunities...',
  'napping on the big red button...',
]

interface AILoaderProps {
  text?: string
}

export default function AILoader({ text }: AILoaderProps) {
  const [frame, setFrame] = useState(0)
  const [textIndex, setTextIndex] = useState(0)

  useEffect(() => {
    const frameInterval = setInterval(() => {
      setFrame(prev => (prev + 1) % CAT_FRAMES.length)
    }, 300)
    return () => clearInterval(frameInterval)
  }, [])

  useEffect(() => {
    const textInterval = setInterval(() => {
      setTextIndex(prev => (prev + 1) % LOADING_TEXTS.length)
    }, 2000)
    return () => clearInterval(textInterval)
  }, [])

  return (
    <div className="flex flex-col items-center justify-center p-4 gap-2">
      <pre className="text-green-400 text-xs leading-tight m-0 font-mono">
        {CAT_FRAMES[frame]}
      </pre>
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
        <span className="text-green-400 text-sm font-mono">
          {text || LOADING_TEXTS[textIndex]}
        </span>
      </div>
    </div>
  )
}
