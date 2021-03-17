import { createRouter, createWebHashHistory } from 'vue-router'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import LostPassword from './components/LostPassword.vue'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/lost-password', component: LostPassword },
    { path: '/signup', component: Signup }
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
})