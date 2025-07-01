/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta personalizada basada en la imagen
        primary: {
          50: '#edf2f4',   // Color beige actualizado
          100: '#d4e2e8',
          200: '#a9c5d0',
          300: '#7ea8b8',
          400: '#538ba0',
          500: '#003049',  // Azul marino principal
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
          500: '#c1121f',  // Rojo principal
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
          500: '#669bbc',  // Azul claro
          600: '#5a8aa3',
          700: '#4e798a',
          800: '#426871',
          900: '#365758',
        },
        danger: {
          50: '#7c0000',   // Rojo oscuro
          500: '#c1121f',  // Rojo principal
          600: '#a10e1a',
        },
        success: {
          50: '#edf2f4',
          500: '#669bbc',
          600: '#5a8aa3',
        },
        neutral: {
          50: '#edf2f4',   // Beige claro actualizado
          100: '#e5e7eb',
          200: '#d1d5db',
          300: '#9ca3af',
          400: '#6b7280',
          500: '#4b5563',
          600: '#374151',
          700: '#1f2937',
          800: '#111827',
          900: '#030712',
        }
      },
      backgroundColor: {
        'app-bg': '#edf2f4',      // Fondo principal de la app
        'card-bg': '#ffffff',      // Fondo de las tarjetas
        'sidebar-bg': '#003049',   // Fondo del sidebar
        'header-bg': '#ffffff',    // Fondo del header
      },
      textColor: {
        'primary-text': '#003049',    // Texto principal
        'secondary-text': '#669bbc',  // Texto secundario
        'accent-text': '#c1121f',     // Texto de acento
        'muted-text': '#6b7280',      // Texto apagado
      },
      borderColor: {
        'primary-border': '#669bbc',
        'secondary-border': '#edf2f4',
        'danger-border': '#c1121f',
      }
    },
  },
  plugins: [],
}