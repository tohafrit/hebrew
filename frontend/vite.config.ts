import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
import path from "path";

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "prompt",
      includeAssets: ["**/*.{ico,png,svg,woff2}"],
      manifest: false, // Use existing manifest.json
      workbox: {
        globPatterns: ["**/*.{js,css,html,ico,png,svg,woff2}"],
        runtimeCaching: [
          {
            urlPattern: /\/api\/(words|lessons|grammar|culture)/,
            handler: "StaleWhileRevalidate",
            options: {
              cacheName: "api-content",
              expiration: { maxAgeSeconds: 7 * 24 * 60 * 60 },
            },
          },
          {
            urlPattern: /\/api\/(stats|srs|recommendations)/,
            handler: "NetworkFirst",
            options: {
              cacheName: "api-dynamic",
              expiration: { maxAgeSeconds: 24 * 60 * 60 },
            },
          },
          {
            urlPattern: /\/api\/auth/,
            handler: "NetworkOnly",
          },
          {
            urlPattern: /\/api\/tts/,
            handler: "CacheFirst",
            options: {
              cacheName: "api-tts",
              expiration: { maxAgeSeconds: 30 * 24 * 60 * 60 },
            },
          },
        ],
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true,
    },
    hmr: {
      clientPort: 80,
    },
  },
});
