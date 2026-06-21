import { resolve } from "path";
import { defineConfig } from "electron-vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  main: {
    resolve: {
      alias: {
        "@jarvis/ipc-contracts": resolve(
          __dirname,
          "../../packages/ipc-contracts/src/index.ts",
        ),
      },
    },
    build: {
      lib: {
        entry: resolve(__dirname, "src/main/index.ts"),
      },
    },
  },
  preload: {
    resolve: {
      alias: {
        "@jarvis/ipc-contracts": resolve(
          __dirname,
          "../../packages/ipc-contracts/src/index.ts",
        ),
      },
    },
    build: {
      lib: {
        entry: resolve(__dirname, "src/preload/index.ts"),
      },
    },
  },
  renderer: {
    root: resolve(__dirname, "src/renderer"),
    publicDir: resolve(__dirname, "src/renderer/src/public"),
    build: {
      rollupOptions: {
        input: {
          index: resolve(__dirname, "src/renderer/index.html"),
        },
      },
    },
    resolve: {
      alias: {
        "@renderer": resolve(__dirname, "src/renderer/src"),
        "@jarvis/ipc-contracts": resolve(
          __dirname,
          "../../packages/ipc-contracts/src/index.ts",
        ),
      },
    },
    plugins: [react(), tailwindcss()],
  },
});
