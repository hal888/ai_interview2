import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '2b67bf7a.r25.cpolar.top'
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    // 启用代码分割
    rollupOptions: {
      output: {
        manualChunks: {
          // 将第三方库打包成单独的 chunk
          'vue-vendor': ['vue', 'vue-router'],
          'axios-vendor': ['axios'],
          'utils-vendor': ['highlight.js', 'marked']
        },
        // 优化资源名称，便于缓存
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    },
    // 启用压缩
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    // 生成 source map 用于调试
    sourcemap: false,
    // 优化 CSS
    cssCodeSplit: true,
    // 优化资源大小
    assetsInlineLimit: 4096 // 4kb 以下的资源内联
  },
  // 优化依赖预构建
  optimizeDeps: {
    include: ['vue', 'vue-router', 'axios'],
    exclude: []
  }
})


