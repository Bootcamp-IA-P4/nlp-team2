/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Paleta principal basada en tu imagen
        primary: {
          50: '#f8f9fa',           // Gris muy claro para fondos
          100: '#e9ecef',          // Gris claro
          200: '#dee2e6',          // Gris medio claro
          300: '#ced4da',          // Gris medio
          400: '#6c757d',          // Gris
          500: '#003049',          // Azul marino oscuro (principal)
          600: '#002639',          // Azul marino más oscuro
          700: '#001d2a',          // Azul marino muy oscuro
          800: '#00131c',          // Azul marino casi negro
          900: '#000a0d',          // Negro azulado
        },
        secondary: {
          50: '#fef7f7',           // Rojo muy claro
          100: '#fdeaea',          // Rojo claro
          200: '#fbd5d5',          // Rojo medio claro
          300: '#f8b4b4',          // Rojo medio
          400: '#f87171',          // Rojo vivo
          500: '#c1121f',          // Rojo principal (de tu paleta)
          600: '#a10e1a',          // Rojo oscuro
          700: '#7f0a14',          // Rojo muy oscuro
          800: '#65080f',          // Rojo casi negro
          900: '#4c060b',          // Rojo negro
        },
        accent: {
          50: '#f0f9ff',           // Azul muy claro
          100: '#e0f2fe',          // Azul claro
          200: '#bae6fd',          // Azul medio claro
          300: '#7dd3fc',          // Azul medio
          400: '#38bdf8',          // Azul vivo
          500: '#669bbc',          // Azul gris (de tu paleta)
          600: '#5a8aa3',          // Azul gris oscuro
          700: '#4e798a',          // Azul gris muy oscuro
          800: '#426871',          // Azul gris casi negro
          900: '#365758',          // Verde azulado oscuro
        },
        // Nuevos colores de tu paleta
        wine: {
          50: '#fef2f2',           // Vino muy claro
          100: '#fee2e2',          // Vino claro
          200: '#fecaca',          // Vino medio claro
          300: '#fca5a5',          // Vino medio
          400: '#f87171',          // Vino vivo
          500: '#780000',          // Vino principal (de tu paleta)
          600: '#650000',          // Vino oscuro
          700: '#520000',          // Vino muy oscuro
          800: '#3f0000',          // Vino casi negro
          900: '#2c0000',          // Vino negro
        },
        cream: {
          50: '#fefefe',           // Blanco puro
          100: '#fdfdf9',          // Crema muy claro
          200: '#faf9f0',          // Crema claro
          300: '#f7f5e7',          // Crema medio
          400: '#f4f1de',          // Crema (gris hueso de tu paleta)
          500: '#f1edda',          // Crema principal
          600: '#e8e0c7',          // Crema oscuro
          700: '#d9cdb0',          // Crema muy oscuro
          800: '#c4b896',          // Beige
          900: '#a89d7a',          // Beige oscuro
        },
        navy: {
          50: '#f0f4f8',           // Azul marino muy claro
          100: '#d9e2ec',          // Azul marino claro
          200: '#bcccdc',          // Azul marino medio claro
          300: '#9fb3c8',          // Azul marino medio
          400: '#829ab1',          // Azul marino
          500: '#003049',          // Azul marino principal (mantener original)
          600: '#002a3f',          // Azul marino oscuro
          700: '#002235',          // Azul marino muy oscuro
          800: '#001a2b',          // Azul marino casi negro
          900: '#001221',          // Azul marino negro
        }
      },
      // Mejores fondos para modo oscuro/claro
      backgroundColor: {
        'light': '#fefefe',       // Fondo claro (casi blanco)
        'dark': '#0f1419',        // Fondo oscuro
        'card-light': '#ffffff',  // Cards en modo claro
        'card-dark': '#1a202c',   // Cards en modo oscuro
      }
    },
  },
  plugins: [],
}