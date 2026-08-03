import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    dedupe: ['react', 'react-dom'],
  },
  optimizeDeps: {
    // globe.gl → three-render-objects → float-tooltip → preact
    // Preact must be excluded from Vite pre-bundling to avoid hook dispatcher conflict with React
    exclude: ['preact', 'preact/hooks', 'preact/compat', 'globe.gl'],
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts'],
        },
      },
    },
    chunkSizeWarningLimit: 200,
    cssCodeSplit: true,
    sourcemap: false,
    minify: 'esbuild',
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        ws: true,
      },
    },
  },
})
