import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Database,
  Briefcase,
  TrendingUp,
  ArrowLeftRight,
  Search,
  Workflow,
  Settings,
  Building2,
} from 'lucide-react'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/objects', label: 'Object Explorer', icon: Database },
  { to: '/workspace', label: 'Workspace', icon: Workflow },
  { to: '/trades', label: 'Trades', icon: ArrowLeftRight },
  { to: '/search', label: 'Search', icon: Search },
]

const resourceItems = [
  { to: '/portfolios', label: 'Portfolios', icon: Briefcase },
  { to: '/instruments', label: 'Instruments', icon: TrendingUp },
  { to: '/counterparties', label: 'Counterparties', icon: Building2 },
]

export default function Sidebar() {
  return (
    <aside className="w-56 bg-slate-900 border-r border-slate-800 flex flex-col flex-shrink-0">
      <div className="h-14 flex items-center gap-2 px-4 border-b border-slate-800">
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-miau-500 to-purple-600 flex items-center justify-center">
          <span className="text-xs font-bold text-white">A</span>
        </div>
        <span className="font-bold text-base text-slate-100">Miau Finance</span>
      </div>

      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        <div className="text-xs font-medium text-slate-500 uppercase tracking-wider px-3 py-2">
          Platform
        </div>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <item.icon size={16} />
            {item.label}
          </NavLink>
        ))}

        <div className="text-xs font-medium text-slate-500 uppercase tracking-wider px-3 py-2 mt-4">
          Resources
        </div>
        {resourceItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <item.icon size={16} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-slate-800">
        <NavLink to="/settings" className="nav-link">
          <Settings size={16} />
          Settings
        </NavLink>
      </div>
    </aside>
  )
}
