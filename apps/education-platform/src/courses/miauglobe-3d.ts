import type { Course } from '../lib/types'

export const miauGlobe3d: Course = {
  id: 'miauglobe-3d',
  slug: 'miauglobe-3d',
  title: 'MiauGlobe 3D Visualization',
  description: 'Explore the world in 3D with the WebGL globe — the cat sees everything from orbit.',
  category: 'Platform',
  difficulty: 'intermediate',
  icon: '🌍',
  lessonCount: 5,
  estimatedMinutes: 30,
  lessons: [
    {
      id: 'globe-basics', slug: 'globe-basics', title: 'Opening the 3D Globe',
      description: 'Access the interactive WebGL globe.',
      commands: ['miaumap', 'globe'],
      steps: [
        { instruction: 'Open the globe: `miaumap`', command: 'miaumap', expectedOutput: '3D WebGL globe with Earth texture' },
        { instruction: 'Drag to rotate, scroll to zoom, click points for details.' },
        { instruction: 'The cat enjoys the view from space. The Earth looks like a blue tuna.' },
      ],
      quiz: [{ question: 'Which terminal command opens the 3D globe?', options: ['miaumap', 'map', 'globe3d', 'world'], correctIndex: 0, explanation: 'Type `miaumap` or `globe` to open the WebGL 3D interactive globe.' }],
    },
    {
      id: 'globe-layers', slug: 'globe-layers', title: 'Globe Layers & Toggles',
      description: 'Different data layers on the globe.',
      commands: ['miaumap --cats', 'miaumap --aliens'],
      steps: [
        { instruction: 'Open with cats: `miaumap --cats`', command: 'miaumap --cats', expectedOutput: 'Globe with cat markers visible' },
        { instruction: 'Use the layer buttons in the toolbar to toggle Companies, Routes, Cargo, Mining, Satellites, Bases, Cats.' },
        { instruction: 'The cat prefers the cats layer. Obviously.' },
      ],
      quiz: [{ question: 'How do you unlock the aliens layer?', options: ['Type x-files while the globe is open', 'Click the aliens button', 'Complete a quest', 'Pay for premium'], correctIndex: 0, explanation: 'The aliens layer is a hidden easter egg. Type `x-files` to unlock the UFO sightings layer.' }],
    },
    {
      id: 'globe-companies', slug: 'globe-companies', title: 'Company Data on Globe',
      description: 'Visualize global companies.',
      commands: ['miaumap'],
      steps: [
        { instruction: 'Open the globe and see 10,000+ companies as colored dots.' },
        { instruction: 'Company colors indicate industry. Click any point for details.' },
        { instruction: 'The cat watches the dots move. It is like a very expensive screensaver.' },
      ],
      quiz: [{ question: 'How many companies are shown on the globe?', options: ['Up to 10,000', '500', '5,000', 'All public companies'], correctIndex: 0, explanation: 'The globe displays up to 10,000 companies from the selected continent, limited by zoom level.' }],
    },
    {
      id: 'globe-search', slug: 'globe-search', title: 'Searching the Globe',
      description: 'Find companies by name or ticker.',
      commands: ['miaumap'],
      steps: [
        { instruction: 'Use the search input in the globe toolbar to find any company by ticker or name.' },
        { instruction: 'Matching companies are highlighted in yellow and raised above the surface.' },
        { instruction: 'The cat searches for TUNA.TO. It is not listed yet, but it is only a matter of time.' },
      ],
      quiz: [{ question: 'How are search results highlighted on the globe?', options: ['They turn yellow and rise above the surface', 'They blink', 'They turn red', 'They are circled'], correctIndex: 0, explanation: 'Searched companies are highlighted in yellow and elevated above the globe surface for visibility.' }],
    },
    {
      id: 'globe-satellites', slug: 'globe-satellites', title: 'Satellite Layer & Live Tracking',
      description: 'Live satellite tracking on the globe.',
      commands: ['miaumap'],
      steps: [
        { instruction: 'Toggle the 🛰️ Satellites layer to see orbiting satellites with real-time positions.' },
        { instruction: 'The ISS is tracked as a special red marker. Spy satellites are highlighted in purple.' },
        { instruction: 'The cat believes it is being watched by satellites. It is correct.' },
      ],
      quiz: [{ question: 'What color is the ISS marker on the satellite layer?', options: ['Red (#ff4444)', 'Blue', 'Green', 'Yellow'], correctIndex: 0, explanation: 'The ISS (International Space Station) is tracked as a distinctive red marker on the satellite layer.' }],
    },
  ],
}
