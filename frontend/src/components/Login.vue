<template>
    <div class="flex items-center h-screen">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>Content de vous revoir ! 🙋</template>
                <template
                    v-slot:default
                >Donnez-moi votre email, votre mot de passe et on est reparti.</template>
            </MascotteTip>
            <div class="mt-10 sm:mt-16">
                <div class="text-gray-800">Adresse e-mail</div>
                <input
                    @change="email = $event.target.value"
                    class="input mt-2"
                    type="email"
                    placeholder="mon-email@example.com"
                />
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Mot de passe</div>
                <input @change="password = $event.target.value" class="input mt-2" type="password" />
                <div class="text-right">
                    <router-link
                        to="/lost-password"
                        class="text-gray-600 mt-1 text-sm"
                    >Mot de passe perdu ?</router-link>
                </div>
            </div>
            <div class="mt-8">
                <button @click="connect" class="button-main-action">Connexion</button>
            </div>
            <div class="mt-10 flex justify-end">
                <router-link to="/signup" class="text-sm text-right">
                    Pas encore de compte ?
                    <br />Enregistrez-vous !
                </router-link>
            </div>
        </div>
        <div class="flex-grow"></div>
    </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { computed, ref } from 'vue'
import MascotteTip from './MascotteTip.vue'

const store = useStore()

const loginInProgress = ref(false)
const email = ref('')
const password = ref('')

const connect = () => {
    window.console.log('email', email.value)
    window.console.log('password', password.value)
    loginInProgress.value = true
    store.dispatch('login', { email: email.value, password: password.value })
}

</script>

<style scoped>
</style>