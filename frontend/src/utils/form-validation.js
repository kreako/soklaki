const emailRe = /[^@]+@[^@]+\.[^@]+/

// Basic email validation
export const isEmailValid = (email) => emailRe.test(email)

// Basic password validation - minimum 8 caracters
export const isPasswordValid = (password) => password.length >= 8