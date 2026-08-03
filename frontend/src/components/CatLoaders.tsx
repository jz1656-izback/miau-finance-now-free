import React from 'react'

interface CatLoaderProps {
  type?: 'paws' | 'walking' | 'yarn' | 'napping' | 'hunting'
  message?: string
  size?: 'sm' | 'md' | 'lg'
}

const CAT_WALKING = [
  `  │                    
  │  ╱╲_╱╲              
  │ ( o.o )             
  └─ > ^ <              `,

  `    │                 
    │  ╱╲_╱╲             
    │ ( o.o )            
    └─ > ^ <             `,

  `     │                
     │  ╱╲_╱╲            
     │ ( o.o )           
     └─ > ^ <            `,
]

const CAT_NAPPING = `
  ■──╯═════════════════╭■
  ■─╭╮ ╔═══════╗ ╭╮───╭■
  ■─╰╯ ║ (~)~) ║ ╰╯───╭■
  ■────╚═══════╝──────╭■
  ╚════════════════════╯
   (sleeping peacefully)
`

const PAW_ANIMATION = [
  '🐾 ⊙',
  '⊙ 🐾',
  '🐾 ⊙',
  '⊙ 🐾',
]

const YARN_ANIMATION = [
  '🧶→',
  '→🧶',
  '🧶→',
  '→🧶',
]

export default function CatLoader({ type = 'paws', message = 'Loading...', size = 'md' }: CatLoaderProps) {
  const [frame, setFrame] = React.useState(0)

  React.useEffect(() => {
    const interval = setInterval(() => {
      setFrame((prev) => (prev + 1) % (type === 'walking' ? CAT_WALKING.length : 4))
    }, 500)
    return () => clearInterval(interval)
  }, [type])

  const getSizeClass = () => {
    switch (size) {
      case 'sm':
        return 'text-xs'
      case 'lg':
        return 'text-2xl'
      default:
        return 'text-lg'
    }
  }

  return (
    <div className="flex flex-col items-center gap-3 py-6">
      <div className={`font-mono ${getSizeClass()} text-glow-green`}>
        {type === 'paws' && (
          <div className="animate-pulse">
            {PAW_ANIMATION[frame]}
          </div>
        )}
        {type === 'walking' && (
          <pre className="text-[#00ff88] leading-tight">
            {CAT_WALKING[frame]}
          </pre>
        )}
        {type === 'yarn' && (
          <div className="animate-pulse">
            {YARN_ANIMATION[frame]}
          </div>
        )}
        {type === 'napping' && (
          <pre className="text-[#00ff88] text-center leading-tight">
            {CAT_NAPPING}
          </pre>
        )}
        {type === 'hunting' && (
          <div className="text-4xl animate-bounce">
            🐱
          </div>
        )}
      </div>
      <div className="text-center text-sm text-slate-400">
        {message}
      </div>
    </div>
  )
}
