import { createRouter, createWebHashHistory } from 'vue-router'
import Login from './components/Login.vue'
import Signup from './components/Signup.vue'
import LostPassword from './components/LostPassword.vue'
import Home from './pages/Home.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/login', component: Login },
    { path: '/lost-password', component: LostPassword },
    { path: '/signup', component: Signup }
]

export const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
})