/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        blue: {
          900: '#1e3a8a', // Mantendo a cor principal do design anterior
        }
      },
    },
  },
  plugins: [],
}
