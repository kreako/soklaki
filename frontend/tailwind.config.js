const colors = require('tailwindcss/colors')

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
      colors: {
        black: colors.black,
        white: colors.white,
        red: colors.red,
        green: colors.emerald,
        gray: colors.coolGray,
        teal: colors.teal,
        rose: colors.rose,
      },
    extend: {
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}