interface SidebarSection {
  title: string
  items: { label: string; action: () => void }[]
}

interface SidebarProps {
  sections: SidebarSection[]
  isOpen: boolean
  onClose: () => void
}

export default function CollapsibleSidebar({ sections, isOpen, onClose }: SidebarProps) {
  if (!isOpen) return null

  return (
    <>
      <div className="fixed inset-0 bg-black/50 z-40 md:hidden" onClick={onClose} />
      <aside className="fixed top-0 left-0 bottom-0 w-64 bg-[#0a1a14] border-r border-green-800/40 z-50 overflow-y-auto md:relative md:w-56">
        <div className="flex items-center justify-between p-3 border-b border-green-800/40">
          <span className="text-green-400 font-mono text-sm">🐱 Menu</span>
          <button onClick={onClose} className="text-green-600 hover:text-green-400 text-lg md:hidden">✕</button>
        </div>
        {sections.map(section => (
          <div key={section.title} className="border-b border-green-900/20">
            <div className="px-3 py-2 text-green-600 text-xs font-mono uppercase tracking-wider">{section.title}</div>
            {section.items.map(item => (
              <button
                key={item.label}
                onClick={() => { item.action(); onClose() }}
                className="w-full text-left px-3 py-2 text-green-400 hover:bg-green-900/20 font-mono text-sm transition-colors"
              >
                {item.label}
              </button>
            ))}
          </div>
        ))}
      </aside>
    </>
  )
}
