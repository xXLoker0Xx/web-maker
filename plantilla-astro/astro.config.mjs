import { defineConfig } from 'astro/config';

export default defineConfig({
  // Configuración general
  site: 'https://example.com',
  output: 'static', // SSG: Static Site Generation
  
  // Soporte para componentes que usan JSX
  vite: {
    ssr: {
      external: ['node-modules']
    }
  },

  // Compresión y optimización
  compressHTML: true,
  
  // Rutas y prefijo
  base: '/',
  trailingSlash: 'never',

  // Build output
  build: {
    assets: 'assets'
  }
});
