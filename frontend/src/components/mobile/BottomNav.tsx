import { useState } from 'react'

interface NavItem {
  id: string
  label: string
  icon: string
  action: () => void
}

interface BottomNavProps {
  items: NavItem[]
}

export default function BottomNav({ items }: BottomNavProps) {
  const [active, setActive] = useState<string | null>(null)

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#0a1a14] border-t border-green-800/40 flex justify-around items-center h-14 px-2 z-50 md:hidden">
      {items.map(item => (
        <button
          key={item.id}
          onClick={() => { setActive(item.id); item.action() }}
          className={`flex flex-col items-center justify-center px-3 py-1 rounded transition-colors ${
            active === item.id ? 'text-green-400' : 'text-green-700'
          }`}
        >
          <span className="text-lg">{item.icon}</span>
          <span className="text-[10px] font-mono mt-0.5">{item.label}</span>
        </button>
      ))}
    </nav>
  )
}
