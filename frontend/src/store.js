import { createStore } from 'vuex'
import axios from 'axios'

const state = {
    login: {
        error : {
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
    setLoginEmail(state, email) {
        state.login.email = email
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
            axios.defaults.headers.common['Authorization'] = `Bearer: ${token}`
        }
    },
    setLoginUserId(state, userId) {
        state.login.userId = userId
    },
    setLoginGroupId(state, groupId) {
        state.login.groupId = groupId
    },
}

axios.defaults.baseURL = import.meta.env.VITE_API_URL

const actions = {
    async login({ commit }, { email, password }) {
        commit('setLoginEmail', email)
        window.console.log('dev', import.meta.env.DEV)
        window.console.log('url', import.meta.env.VITE_API_URL)
        let answer = await axios.get('users')
        window.console.log('answer', answer)
    },

    async signup({ commit }, { email, password }) {
        let answer = await axios.post('signup', { email, password })
        commit('setLoginErrorKnownEmail', answer.data.signup.errorKnownEmail)
        commit('setLoginErrorWeakPassword', answer.data.signup.errorWeakPassword)
        commit('setLoginToken', answer.data.signup.token)
        commit('setLoginUserId', answer.data.signup.id)
        commit('setLoginGroupId', answer.data.signup.group)
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