import { createStore } from 'vuex'
import axios from 'axios'

const state = {
    login: {
        groupName: null,
        paymentOk: null,
        name: null,
        email: null,
        emailConfirmed: null,
    }
}

const mutations = {
    setLoginEmail(state, email) {
        state.email = email
    },
}

const url = (suffix) => import.meta.env.VITE_API_URL + suffix

const actions = {
    async login({ commit }, { email, password }) {
        commit('setLoginEmail', email)
        window.console.log('dev', import.meta.env.DEV)
        window.console.log('url', import.meta.env.VITE_API_URL)
        let answer = await axios.get(url('users'))
        window.console.log('answer', answer)
    }
}

export const store = createStore({
    state,
    mutations,
    actions,
})