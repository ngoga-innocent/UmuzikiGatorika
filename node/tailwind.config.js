/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../**/*.{html,py}"],
  theme: {
    extend: {
      colors:{
        "dark":"#170e09",
        "white":"#ffffff"
      },fontFamily:{
        "staff": "Parkinsans",

      }
    },
  },
  plugins: [],
}

