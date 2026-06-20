// electron.vite.config.ts
import { resolve } from "path";
import { defineConfig } from "electron-vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
var __electron_vite_injected_dirname =
  "E:\\Projects\\ui test\\jarvis-unified - Copy";
var electron_vite_config_default = defineConfig({
  main: {
    resolve: {
      alias: {
        "@jarvis/ipc-contracts": resolve(
          __electron_vite_injected_dirname,
          "packages/ipc-contracts/index.ts",
        ),
      },
    },
    build: {
      lib: {
        entry: resolve(
          __electron_vite_injected_dirname,
          "apps/desktop/main/index.ts",
        ),
      },
      rollupOptions: {
        external: ["vectordb", "apache-arrow"],
      },
    },
  },
  preload: {
    resolve: {
      alias: {
        "@jarvis/ipc-contracts": resolve(
          __electron_vite_injected_dirname,
          "packages/ipc-contracts/index.ts",
        ),
      },
    },
    build: {
      lib: {
        entry: {
          ai: resolve(
            __electron_vite_injected_dirname,
            "apps/desktop/preload/ai.ts",
          ),
          fs: resolve(
            __electron_vite_injected_dirname,
            "apps/desktop/preload/fs.ts",
          ),
          system: resolve(
            __electron_vite_injected_dirname,
            "apps/desktop/preload/system.ts",
          ),
        },
      },
    },
  },
  renderer: {
    root: resolve(__electron_vite_injected_dirname, "apps/desktop/renderer"),
    publicDir: resolve(
      __electron_vite_injected_dirname,
      "apps/desktop/renderer/src/public",
    ),
    build: {
      rollupOptions: {
        input: {
          index: resolve(
            __electron_vite_injected_dirname,
            "apps/desktop/renderer/index.html",
          ),
        },
      },
    },
    resolve: {
      alias: {
        "@renderer": resolve(
          __electron_vite_injected_dirname,
          "apps/desktop/renderer/src",
        ),
        "@jarvis/ipc-contracts": resolve(
          __electron_vite_injected_dirname,
          "packages/ipc-contracts/index.ts",
        ),
      },
    },
    plugins: [react(), tailwindcss()],
  },
});
export { electron_vite_config_default as default };
