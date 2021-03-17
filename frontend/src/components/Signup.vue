<template>
    <div class="flex items-center h-screen">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>
                    Bienvenue ! 👋
                </template>
                <template v-slot:default>
                    Donnez-moi un email, un nom
                    <span
                        class="text-sm sm:text-base"
                    >(tel que vous voulez le faire apparaître sur les rapports - modifiable par la suite...)</span>
                    et un mot de passe.
                </template>
            </MascotteTip>
            <div class="mt-6 sm:mt-12">
                <div class="text-gray-800">Votre adresse email</div>
                <input
                    @change="email = $event.target.value"
                    class="input mt-2"
                    type="email"
                    placeholder="mon-email@example.com"
                />
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Votre nom</div>
                <input
                    @change="name = $event.target.value"
                    class="input mt-2"
                    type="text"
                    placeholder="Alexander Neill"
                />
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Votre mot de passe</div>
                <input @change="password = $event.target.value" class="input mt-2" type="password" />
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

const store = useStore()

// values
const name = ref('')
const email = ref('')
const password = ref('')

// Validation error
emailFormError = ref(false)

const emailRe = /[^@]+@[^@]+\.[^@]+/

const signup = () => {
    // Basic email validation
    if (!emailRe.test(email.value)) {
        emailFormError.value = true
        return
    }
    window.console.log('name', name.value)
    window.console.log('email', email.value)
    window.console.log('password', password.value)
    store.dispatch('signup', { name: name, email: email.value, password: password.value })
}

</script>