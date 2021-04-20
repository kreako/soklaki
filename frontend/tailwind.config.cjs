const colors = require("tailwindcss/colors");

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
      blue: colors.blue,
    },
    extend: {
      maxHeight: {
        46: "11.5rem",
      },
    },
  },
  variants: {
    extend: {
      textColor: ["group-hover", "disabled"],
      backgroundColor: ["disabled"],
      cursor: ["disabled"],
    },
  },
  plugins: [require("./tailwindcss-plugins/forms.cjs")],
};
