<template>
    <div class="flex items-center">
        <div class="flex-grow"></div>
        <div class="px-2 w-full sm:max-w-screen-sm">
            <MascotteTip>
                <template v-slot:title>Bienvenue ! 👋</template>
                <template v-slot:default>Donnez-moi un email et un mot de passe.</template>
            </MascotteTip>
            <div class="mt-6 sm:mt-12">
                <MyEmailInput
                    @change="email = $event"
                    :email="email"
                    :error="((!emailValid) || errorKnownEmail)"
                >
                    <template v-slot:error>
                        <span
                            v-if="!emailValid"
                        >Oh non ! Il semblerait que votre email ne ressemble pas à un email...</span>
                        <div v-if="errorKnownEmail">
                            <div>Il semblerait que je connaisse déjà votre email !</div>
                            <div>
                                <router-link
                                    to="/login"
                                    class="underline text-xl text-blue-600"
                                >Je vous propose de plutôt vous identifier.</router-link>
                            </div>
                        </div>
                    </template>
                </MyEmailInput>
            </div>
            <div class="mt-6">
                <div class="text-gray-800">Votre mot de passe</div>
                <input
                    @change="password = $event.target.value"
                    @keyup.enter="signup"
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
            <div>{{ errorKnownEmail }}</div>
            <div>{{ errorWeakPassword }}</div>
        </div>
        <div class="flex-grow"></div>
    </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { computed, ref, watch } from 'vue'
import { isEmailValid, isPasswordValid } from '../utils/form-validation.js'
import MascotteTip from '../components/MascotteTip.vue'
import MyEmailInput from '../components/MyEmailInput.vue'

const store = useStore()
const router = useRouter()

// values
const email = ref('')
const password = ref('')

// Validation error
const emailValid = ref(true)
const passwordValid = ref(true)

const emailRe = /[^@]+@[^@]+\.[^@]+/

const errorKnownEmail = computed(() => store.state.login.error.knownEmail)
const errorWeakPassword = computed(() => store.state.login.error.weakPassword)

const token = computed(() => store.state.login.token)

watch(
    () => store.state.login.token,
    (token, prevToken) => {
        window.console.log("token is now", token)
        router.push("/")
    }
)

const signup = () => {
    // Basic validations
    emailValid.value = isEmailValid(email.value)
    passwordValid.value = isPasswordValid(password.value)

    if (!emailValid.value || !passwordValid.value) {
        // First correct inputs
        return
    }

    store.dispatch('signup', { email: email.value, password: password.value })
}

</script>