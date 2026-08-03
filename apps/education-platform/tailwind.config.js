/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        miau: {
          bg: '#0a0a0a',
          surface: '#111111',
          border: '#1a3a1a',
          green: '#00ff88',
          'green-dim': '#006622',
          yellow: '#ffcc00',
          amber: '#ffaa00',
          red: '#ff4444',
          text: '#c8e0c8',
          'text-dim': '#557755',
        },
      },
      fontFamily: {
        mono: ['"Fira Code"', '"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}
