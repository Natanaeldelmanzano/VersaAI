import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\./,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: {
                maxEntries: 100,
                maxAgeSeconds: 60 * 60 * 24 // 24 hours
              }
            }
          }
        ]
      },
      manifest: {
        name: 'VersaAI Enterprise Dashboard',
        short_name: 'VersaAI',
        description: 'Enterprise AI Dashboard for chatbot management and analytics',
        theme_color: '#2563eb',
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: '/icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    host: true,
    open: false,
    cors: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: 'dist',
    // Optimizaciones de performance
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: process.env.NODE_ENV === 'production',
        drop_debugger: process.env.NODE_ENV === 'production',
        pure_funcs: process.env.NODE_ENV === 'production' ? ['console.log'] : []
      },
    },
    // Configuración de chunks para mejor caching
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks para mejor caching
          vue: ['vue', 'vue-router', 'pinia'],
          ui: ['@headlessui/vue', 'vue-toastification', '@heroicons/vue'],
          charts: ['chart.js', 'vue-chartjs'],
          utils: ['axios', 'lodash', 'date-fns'],
          dashboard: [
            './src/components/dashboard/AdvancedAnalytics.vue',
            './src/components/dashboard/CustomizationSystem.vue'
          ]
        },
        // Nombres de archivos con hash para cache busting
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },
    // Configuración de sourcemaps para producción
    sourcemap: process.env.NODE_ENV !== 'production',
    // Optimización de CSS
    cssCodeSplit: true,
    // Configuración de target para mejor compatibilidad
    target: 'es2015',
    // Configuración de chunk size warnings
    chunkSizeWarningLimit: 1500,
    // Configuración de compresión
    reportCompressedSize: true,
    // Configuración de assets inline
    assetsInlineLimit: 4096
  },
  // Optimizaciones de desarrollo
  optimizeDeps: {
    include: [
      'vue', 
      'vue-router', 
      'pinia', 
      'axios',
      '@headlessui/vue',
      '@heroicons/vue/24/outline',
      '@heroicons/vue/24/solid',
      'chart.js',
      'vue-chartjs'
    ],
    exclude: ['@vite/client', '@vite/env']
  },
  // Configuración de CSS
  css: {
    devSourcemap: true,
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/styles/variables.scss";`
      }
    }
  },
  // Variables de entorno
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  },
  // Configuración de preview para producción
  preview: {
    port: 4173,
    host: true,
    cors: true
  }
})
