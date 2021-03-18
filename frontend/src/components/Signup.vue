<template>
    <div class="flex items-center">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>Bienvenue ! 👋</template>
                <template v-slot:default>
                    Donnez-moi un email et un mot de passe.
                </template>
            </MascotteTip>
            <div class="mt-6 sm:mt-12">
                <MyEmailInput @change="email = $event" :email="email" :error="!emailValid">
                    <template
                        v-slot:error
                    >Oh non ! Il semblerait que votre email ne ressemble pas à un email...</template>
                </MyEmailInput>
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Votre mot de passe</div>
                <input
                    @change="password = $event.target.value"
                    class="input mt-2"
                    :class="{ 'input-error': !passwordValid }"
                    type="password"
                    autocomplete="new-password"
                    id="new-password"
                    required
                />
                <div
                    v-if="!passwordValid"
                    class="text-right text-red-600"
                >Oh non ! Il semblerait que votre mot de passe soit trop court. 8 caractères minimum !</div>
            </div>
            <div class="mt-8">
                <button @click="signup" class="button-main-action">Inscription</button>
            </div>
            <div class="mt-10 flex justify-end">
                <router-link to="/login" class="text-sm text-right">
                    Vous avez déjà un compte ?
                    <br />Identifiez-vous !
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
import { isEmailValid, isPasswordValid } from '../utils/form-validation.js'
import MyEmailInput from './MyEmailInput.vue'

const store = useStore()

// values
const email = ref('')
const password = ref('')

// Validation error
const emailValid = ref(true)
const passwordValid = ref(true)

const emailRe = /[^@]+@[^@]+\.[^@]+/

const signup = () => {
    // Basic validations
    emailValid.value = isEmailValid(email.value)
    passwordValid.value = isPasswordValid(password.value)

    if (!emailValid.value || !passwordValid.value) {
        // First correct inputs
        return
    }

    window.console.log('email', email.value)
    window.console.log('password', password.value)
    store.dispatch('signup', { email: email.value, password: password.value })
}

</script>