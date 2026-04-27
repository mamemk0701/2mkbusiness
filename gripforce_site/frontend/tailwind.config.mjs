/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Neutres
        ink: {
          50: '#FAFAF7',
          100: '#F4F3EE',
          200: '#E8E6DD',
          300: '#C8C5B8',
          400: '#8E8B7E',
          500: '#5C5A52',
          600: '#3D3C36',
          700: '#2A2A26',
          800: '#1A1A18',
          900: '#0D0D0C',
        },
        // Accent électrique (signature GripForce)
        volt: {
          50: '#EFF8FF',
          100: '#DFEFFF',
          200: '#B8DEFF',
          300: '#7AC4FF',
          400: '#38A6FF',
          500: '#0F88FF',
          600: '#0067E6',
          700: '#0052BF',
          800: '#08469C',
          900: '#0D3B7F',
        },
        // Accents secondaires
        alert: '#FF4D2D',
        success: '#00B86B',
      },
      fontFamily: {
        display: ['"Fraunces"', 'Georgia', 'serif'],
        sans: ['"Manrope"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'Menlo', 'monospace'],
      },
      fontSize: {
        'display-xl': ['clamp(3.5rem, 8vw, 7rem)', { lineHeight: '0.92', letterSpacing: '-0.04em' }],
        'display-lg': ['clamp(2.5rem, 5vw, 4.5rem)', { lineHeight: '0.95', letterSpacing: '-0.03em' }],
        'display-md': ['clamp(2rem, 4vw, 3rem)', { lineHeight: '1.05', letterSpacing: '-0.02em' }],
      },
      animation: {
        'slide-up': 'slideUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards',
        'fade-in': 'fadeIn 0.8s ease-out forwards',
        'marquee': 'marquee 40s linear infinite',
        'pulse-slow': 'pulseSlow 3s ease-in-out infinite',
      },
      keyframes: {
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        pulseSlow: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.6' },
        },
      },
      backgroundImage: {
        'grid-light': "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath d='M0 0h40v40H0z' fill='none' stroke='%23000' stroke-opacity='0.04'/%3E%3C/svg%3E\")",
        'grid-dark': "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cpath d='M0 0h40v40H0z' fill='none' stroke='%23fff' stroke-opacity='0.04'/%3E%3C/svg%3E\")",
      },
    },
  },
  plugins: [],
};
