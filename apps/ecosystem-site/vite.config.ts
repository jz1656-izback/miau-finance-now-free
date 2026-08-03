import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 5175,
    strictPort: true,
    proxy: {
      '/api/v1/marketing': {
        target: 'http://localhost:5403',
        changeOrigin: true,
      },
    },
  },
})
