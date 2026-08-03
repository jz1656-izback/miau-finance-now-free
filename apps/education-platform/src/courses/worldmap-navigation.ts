import type { Course } from '../lib/types'

export const worldmapNavigation: Course = {
  id: 'worldmap-navigation',
  slug: 'worldmap-navigation',
  title: 'WorldMap Navigation & Layers',
  description: 'Explore the interactive 2D world map with companies, trade routes, cats, and weather — the cat explores the globe one paw at a time.',
  category: 'Platform',
  difficulty: 'beginner',
  icon: '🗺️',
  lessonCount: 4,
  estimatedMinutes: 25,
  lessons: [
    {
      id: 'wm-basics', slug: 'wm-basics', title: 'WorldMap Basics',
      description: 'Opening and navigating the map.',
      commands: ['map'],
      steps: [
        { instruction: 'Open the map: type `map`', command: 'map', expectedOutput: 'Leaflet world map with markers and overlays' },
        { instruction: 'Drag to pan, scroll to zoom. Click markers for details.' },
        { instruction: 'The cat uses the map to find the nearest tuna can. Geographically.' },
      ],
      quiz: [{ question: 'How do you toggle the WorldMap?', options: ['Type `map` in the terminal', 'Click the map icon', 'Press Ctrl+M', 'It opens automatically'], correctIndex: 0, explanation: 'The `map` command toggles the Leaflet-based interactive world map overlay.' }],
    },
    {
      id: 'wm-markers', slug: 'wm-markers', title: 'Map Markers & Data Layers',
      description: 'Understanding map markers and overlays.',
      commands: ['map'],
      steps: [
        { instruction: 'Open the map and explore different markers.', command: 'map', expectedOutput: 'Company markers, trade routes, cat markers, hairballs' },
        { instruction: 'Green markers = stock exchanges. Cat emojis = company locations.' },
        { instruction: 'Each cat on the map has a net worth. Some are surprisingly wealthy.' },
      ],
      quiz: [{ question: 'What do the cat emoji markers represent on the WorldMap?', options: ['Real companies categorized by industry', 'Random cat locations', 'Trading signals', 'Weather patterns'], correctIndex: 0, explanation: 'Cat emojis on the map represent company locations, with different cat expressions for different industries.' }],
    },
    {
      id: 'wm-toolbar', slug: 'wm-toolbar', title: 'Toolbar Controls & Filters',
      description: 'Toggle data layers on the map.',
      commands: ['map'],
      steps: [
        { instruction: 'Use the toolbar buttons to toggle: Boats, Jets, Cats, Hairballs, ISS, Commodities, Bonds, Weather, Companies, DeFi.' },
        { instruction: 'The search bar lets you find any company by name or ticker.' },
        { instruction: 'The cat likes the hairball layer best. It is like easter eggs, but furrier.' },
      ],
      quiz: [{ question: 'How do you change the map tile style?', options: ['Click the Map/Satellite/Dark button in the toolbar', 'Type `tiles`', 'Right-click the map', 'It is not possible'], correctIndex: 0, explanation: 'The map layer button cycles through Street, Satellite, and Dark tile styles.' }],
    },
    {
      id: 'wm-company-detail', slug: 'wm-company-detail', title: 'Company Detail Panel',
      description: 'Research companies by clicking on the map.',
      commands: ['map'],
      steps: [
        { instruction: 'Click any company marker to open the detail panel with info, chart, stats, peers, IB data, and news.' },
        { instruction: 'The Investment Banking tab shows DCF, WACC, Comps, and LBO models.' },
        { instruction: 'The cat reads the news tab while ignoring the fundamentals. Priorities.' },
      ],
      quiz: [{ question: 'What tabs are available in the company detail panel?', options: ['Info, Chart, Stats, Peers, IB, News', 'Buy, Sell, Hold', 'Overview, History, Forecast', 'Price, Volume, Market Cap'], correctIndex: 0, explanation: 'The detail panel provides six tabs: Info (company overview), Chart (price history), Stats (fundamentals), Peers (comparable companies), IB (investment banking models), and News.' }],
    },
  ],
}
