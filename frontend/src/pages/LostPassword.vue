<template>
    <div class="flex items-center">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>
                   Vous avez oublié votre mot de passe ? 😭</template>
                <template
                    v-slot:default
                >Pas de problèmes ! Renseignez votre email et je vous fais parvenir un lien pour le changer.</template>
            </MascotteTip>
            <div class="mt-8 sm:mt-16">
                <MyEmailInput @change="email = $event" :email="email" :error="!emailValid">
                    <template
                        v-slot:error
                    >Oh non ! Il semblerait que votre email ne ressemble pas à un email...</template>
                </MyEmailInput>
            </div>
            <div class="mt-8">
                <button @click="reset" class="button-main-action">Recevoir un email !</button>
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
import { isEmailValid } from '../utils/form-validation.js'
import MascotteTip from './MascotteTip.vue'
import MyEmailInput from './MyEmailInput.vue'

const store = useStore()

const email = ref('')

// Validation error
const emailValid = ref(true)

const reset = () => {
    // Basic validations
    emailValid.value = isEmailValid(email.value)

    if (!emailValid.value) {
        // First correct inputs
        return
    }

    window.console.log('email', email.value)
    store.dispatch('resetPassword', { email: email.value })
}

</script>

<style scoped>
</style>