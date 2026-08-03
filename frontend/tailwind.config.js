/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        miau: {
          green: '#00ff88',
          'text-dim': '#557755',
          amber: '#ffcc00',
          red: '#ff4444',
          text: '#c8e0c8',
          border: '#1a3a1a',
        },
      },
      width: { 'panel': '960px' },
      maxWidth: { 'panel': '95vw' },
      maxHeight: { 'panel': '92vh' },
    },
  },
  plugins: [],
}
