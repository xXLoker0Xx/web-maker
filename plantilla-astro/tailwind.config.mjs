/** @type {import('tailwindcss').Config} */

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: '#6366F1',
        'primary-dark': '#4F46E5',
        accent: '#F59E0B',
        background: '#F8FAFC',
        surface: '#FFFFFF',
        text: '#111827',
        'text-muted': '#6B7280',
        border: '#E5E7EB',
        success: '#10B981',
      },
      spacing: {
        xs: '8px',
        sm: '16px',
        md: '24px',
        lg: '40px',
        xl: '64px',
        '2xl': '96px',
      },
      borderRadius: {
        DEFAULT: '20px',
      },
      boxShadow: {
        DEFAULT: '0 12px 40px rgba(15, 23, 42, 0.08)',
      },
      fontSize: {
        h1: ['56px', { lineHeight: '1.2', fontWeight: '700' }],
        h2: ['34px', { lineHeight: '1.2', fontWeight: '700' }],
        h3: ['24px', { lineHeight: '1.3', fontWeight: '600' }],
        body: ['18px', { lineHeight: '1.7' }],
      },
      maxWidth: {
        'content': '780px',
        'comparison': '1100px',
        'full-width': '1200px',
      },
    },
  },
  plugins: [],
};