import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    // Otimizações de build
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          // Separar bibliotecas grandes em chunks
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-accordion', '@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          router: ['react-router-dom'],
          charts: ['recharts'],
          utils: ['date-fns', 'clsx', 'tailwind-merge']
        },
      },
    },
    // Aumentar limite de aviso de chunk
    chunkSizeWarningLimit: 1000,
  },
  server: {
    // Configurações do servidor de desenvolvimento
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  preview: {
    port: 3000,
    host: true,
  },
  optimizeDeps: {
    // Pré-bundling de dependências
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'recharts',
      'date-fns',
      'clsx',
      'tailwind-merge'
    ],
  },
})
