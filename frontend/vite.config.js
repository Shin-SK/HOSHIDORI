// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',    // SW が自動で更新チェック
      devOptions: { enabled: true }, // `vite dev` でも SW を動かす
      manifest: {
        name:          'Hoshidori',
        short_name:    'Hoshidori',
        description:   '観劇ログ',
        start_url:     '/stage',
        display:       'standalone',
        theme_color:   '#ffffff',
        background_color: '#ffffff',
        icons: [
          // 512×512 は必須。96 / 192 も推奨
          { src: 'ogp.png', sizes: '192x192', type: 'image/png' },
          { src: 'ogp.png', sizes: '512x512', type: 'image/png' },
          // mask-able 付きにすると iOS で丸く切られない
          { src: 'ogp.png', sizes: '192x192', type: 'image/png', purpose: 'maskable any' }
        ]
      },
      workbox: {
        // ↑より高度なキャッシュ設定をしたくなったらここに workbox オプション
        globPatterns: ['**/*.{js,css,html,png,svg,ico,json}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/admin\.hoshidori\.com\/api\//,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              networkTimeoutSeconds: 10
            }
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // ← これで '@/...' が使える
    },
  },
})