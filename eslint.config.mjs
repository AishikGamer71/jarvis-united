import { defineConfig } from "eslint/config";
import tseslint from "@electron-toolkit/eslint-config-ts";
import eslintConfigPrettier from "@electron-toolkit/eslint-config-prettier";
import eslintPluginReact from "eslint-plugin-react";
import eslintPluginReactHooks from "eslint-plugin-react-hooks";
import eslintPluginReactRefresh from "eslint-plugin-react-refresh";

export default defineConfig(
  { ignores: ["**/node_modules", "**/dist", "**/out", "engine/**"] },
  tseslint.configs.recommended,
  {
    files: ["apps/desktop/renderer/**/*.{ts,tsx,js,jsx}"],
    ...eslintPluginReact.configs.flat.recommended,
  },
  {
    files: ["apps/desktop/renderer/**/*.{ts,tsx,js,jsx}"],
    ...eslintPluginReact.configs.flat["jsx-runtime"],
  },
  {
    files: ["apps/desktop/renderer/**/*.{ts,tsx,js,jsx}"],
    settings: {
      react: {
        version: "18.3",
      },
    },
    plugins: {
      "react-hooks": eslintPluginReactHooks,
      "react-refresh": eslintPluginReactRefresh,
    },
    rules: {
      ...eslintPluginReactHooks.configs.recommended.rules,
      ...eslintPluginReactRefresh.configs.vite.rules,
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
    },
  },
  {
    files: ["apps/desktop/main/**/*.ts", "apps/desktop/preload/**/*.ts"],
    languageOptions: {
      globals: {
        process: "readonly",
        __dirname: "readonly",
        console: "readonly",
        require: "readonly",
        module: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        Buffer: "readonly",
      },
    },
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/explicit-function-return-type": "off",
    },
  },
  eslintConfigPrettier,
);
