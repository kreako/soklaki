const colors = require("tailwindcss/colors");

module.exports = {
  mode: "jit",
  purge: ["./index.html", "./src/**/*.{js,jsx,ts,tsx,vue}"],
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
      orange: colors.orange,
      yellow: colors.yellow,
      blue: colors.blue,
      transparent: colors.transparent,
    },
    extend: {
      maxHeight: {
        46: "11.5rem",
      },
    },
  },
  plugins: [require("./tailwindcss-plugins/forms.cjs")],
};
