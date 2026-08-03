export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: 'var(--bg)',
        foreground: 'var(--fg)',
        dim: 'var(--dim)',
        surface: 'var(--surface)',
        'surface-alt': 'var(--surface-alt)',
        border: 'var(--border)',
        green: '#00e676',
        'green-dark': '#00c853',
        'green-dim': '#1b5e20',
        purple: '#a855f7',
        cyan: '#22d3ee',
        pink: '#f472b6',
        orange: '#fb923c',
      },
      fontFamily: {
        sans: ['Geist', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
