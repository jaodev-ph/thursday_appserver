import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// HMR when using Docker + Nginx (browser hits host:5188 → spa:5173):
// set VITE_HMR_CLIENT_PORT=5188 (and optionally VITE_HMR_HOST=localhost).
// Direct `npm run dev` on :5173: omit these — Vite defaults work.
const hmrClientPort = process.env.VITE_HMR_CLIENT_PORT
const hmrHost = process.env.VITE_HMR_HOST ?? 'localhost'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    allowedHosts: ['frontend'],
    // Never use `frontend` as HMR host — that is an Nginx upstream name, not a DNS name in the browser.
    hmr: hmrClientPort
      ? {
          host: hmrHost,
          protocol: 'ws',
          clientPort: Number(hmrClientPort),
        }
      : true,
  },
})
