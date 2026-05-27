/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#C6F7D0',
          DEFAULT: '#A3E4A3',
          dark: '#2D5016',
        },
        sidebar: {
          bg: '#C6F7D0',
          item: '#A3E4A3',
          active: '#2D5016',
        },
        bg: {
          light: '#F5FBF5',
          white: '#FFFFFF',
        }
      },
      fontFamily: {
        sans: ['Noto Sans SC', '思源黑体', 'sans-serif'],
        mono: ['Roboto Mono', 'monospace'],
      },
      borderRadius: {
        'card': '8px',
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0,0,0,0.06)',
      }
    },
  },
  plugins: [],
}
