<template>
    <div class="flex items-center">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>Content de vous revoir ! 🙋</template>
                <template
                    v-slot:default
                >Donnez-moi votre email, votre mot de passe et on est reparti.</template>
            </MascotteTip>
            <div class="mt-10 sm:mt-16">
                <MyEmailInput @change="email = $event" :email="email" :error="!emailValid">
                    <template
                        v-slot:error
                    >Oh non ! Il semblerait que votre email ne ressemble pas à un email...</template>
                </MyEmailInput>
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Mot de passe</div>
                <input
                    @change="password = $event.target.value"
                    class="input mt-2"
                    type="password"
                    autocomplete="new-password"
                    id="new-password"
                    required
                />

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
import { isEmailValid, isPasswordValid } from '../utils/form-validation.js'
import MascotteTip from '../components/MascotteTip.vue'
import MyEmailInput from '../components/MyEmailInput.vue'

const store = useStore()

const email = ref('')
const password = ref('')

// Validation error
const emailValid = ref(true)
const passwordValid = ref(true)

const connect = () => {
    // Basic validations
    emailValid.value = isEmailValid(email.value)
    passwordValid.value = isPasswordValid(password.value)

    if (!emailValid.value || !passwordValid.value) {
        // First correct inputs
        return
    }

    window.console.log('email', email.value)
    window.console.log('password', password.value)
    store.dispatch('login', { email: email.value, password: password.value })
}

</script>

<style scoped>
</style>