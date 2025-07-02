/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Habilitar modo oscuro con clase
  theme: {
    extend: {
      colors: {
        // Paleta personalizada
        primary: {
          50: '#edf2f4',
          100: '#d4e2e8',
          200: '#a9c5d0',
          300: '#7ea8b8',
          400: '#538ba0',
          500: '#003049',
          600: '#002639',
          700: '#001d2a',
          800: '#00131c',
          900: '#000a0d',
        },
        secondary: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#c1121f',
          600: '#a10e1a',
          700: '#7f0a14',
          800: '#65080f',
          900: '#4c060b',
        },
        accent: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#669bbc',
          600: '#5a8aa3',
          700: '#4e798a',
          800: '#426871',
          900: '#365758',
        }
      }
    },
  },
  plugins: [],
}