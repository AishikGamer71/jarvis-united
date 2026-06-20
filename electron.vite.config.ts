import { resolve } from 'path'
import { defineConfig } from 'electron-vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  main: {
    resolve: {
      alias: {
        '@jarvis/ipc-contracts': resolve(__dirname, 'packages/ipc-contracts/index.ts')
      }
    },
    build: {
      lib: {
        entry: resolve(__dirname, 'apps/desktop/main/index.ts')
      }
    }
  },
  preload: {
    resolve: {
      alias: {
        '@jarvis/ipc-contracts': resolve(__dirname, 'packages/ipc-contracts/index.ts')
      }
    },
    build: {
      lib: {
        entry: resolve(__dirname, 'apps/desktop/preload/index.ts')
      }
    }
  },
  renderer: {
    root: resolve(__dirname, 'apps/desktop/renderer'),
    publicDir: resolve(__dirname, 'apps/desktop/renderer/src/public'),
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, 'apps/desktop/renderer/index.html')
        }
      }
    },
    resolve: {
      alias: {
        '@renderer': resolve(__dirname, 'apps/desktop/renderer/src'),
        '@jarvis/ipc-contracts': resolve(__dirname, 'packages/ipc-contracts/index.ts')
      }
    },
    plugins: [react(), tailwindcss()]
  }
})