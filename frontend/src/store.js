import { createStore } from 'vuex'
import axios from 'axios'

const state = {
    login: {
        error : {
            invalid: false,
            knownEmail: false,
            weakPassword: false,
        },
        userId: null,
        token: null,
        groupId: null,
        groupName: null,
        paymentOk: null,
        name: null,
        email: null,
        emailConfirmed: null,
    }
}

const mutations = {
    loadFromLocalStorage(state) {
        window.console.log("loadFromLocalStorage")
        state.login.email = localStorage.getItem("email")
        state.login.token = localStorage.getItem("token")
        state.login.userId = localStorage.getItem("userId")
        state.login.groupId = localStorage.getItem("groupId")
        if (state.login.token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${state.login.token}`
        }
    },
    setLoginEmail(state, email) {
        if (state.login.token != null) {
            // Meaning the login was successful, so store data
            localStorage.setItem("email", email)
        }
        state.login.email = email
    },
    setLoginErrorInvalid(state, invalid) {
        state.login.error.invalid= invalid
    },
    setLoginErrorKnownEmail(state, errorKnownEmail) {
        state.login.error.knownEmail = errorKnownEmail
    },
    setLoginErrorWeakPassword(state, errorWeakPassword) {
        state.login.error.weakPassword = errorWeakPassword
    },
    setLoginToken(state, token) {
        state.login.token = token
        if (token) {
            localStorage.setItem("token", token)
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        }
    },
    setLoginUserId(state, userId) {
        if (state.login.token != null) {
            // Meaning the login was successful, so store data
            localStorage.setItem("userId", userId)
        }
        state.login.userId = userId
    },
    setLoginGroupId(state, groupId) {
        if (state.login.token != null) {
            // Meaning the login was successful, so store data
            localStorage.setItem("groupId", groupId)
        }
        state.login.groupId = groupId
    },
}

axios.defaults.baseURL = import.meta.env.VITE_API_URL

const actions = {
    async login({ commit }, { email, password }) {
        let answer = await axios.post('login', { email, password })
        window.console.log('answer', answer)
        commit('setLoginToken', answer.data.login.token)
        commit('setLoginErrorInvalid', answer.data.login.error)
        commit('setLoginUserId', answer.data.login.id)
        commit('setLoginGroupId', answer.data.login.group)
        commit('setLoginEmail', email)
    },

    async signup({ commit }, { email, password }) {
        let answer = await axios.post('signup', { email, password })
        commit('setLoginToken', answer.data.signup.token)
        commit('setLoginErrorKnownEmail', answer.data.signup.errorKnownEmail)
        commit('setLoginErrorWeakPassword', answer.data.signup.errorWeakPassword)
        commit('setLoginUserId', answer.data.signup.id)
        commit('setLoginGroupId', answer.data.signup.group)
        commit('setLoginEmail', email)
    },

    async resetPassword({ commit }, { email }) {
        window.console.log('dev', import.meta.env.DEV)
        window.console.log('url', import.meta.env.VITE_API_URL)
    },
}

export const store = createStore({
    state,
    mutations,
    actions,
})