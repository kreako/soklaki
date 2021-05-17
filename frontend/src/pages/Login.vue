<template>
  <div class="flex items-center">
    <div class="flex-grow"></div>
    <div class="px-2 w-full sm:max-w-screen-sm">
      <MascotteTip>
        <template v-slot:title>Content de vous revoir ! 🙋</template>
        <template v-slot:default
          >Donnez-moi votre email, votre mot de passe et on est
          reparti.</template
        >
      </MascotteTip>
      <div class="mt-10 sm:mt-16">
        <MyEmailInput
          @change="email = $event"
          :email="email"
          :error="!emailValid || invalidLogin"
        >
          <template v-slot:error
            ><span v-if="!emailValid">
              Oh non ! Il semblerait que votre email ne ressemble pas à un
              email...
            </span>
            <div v-if="invalidLogin">
              Je ne reconnais pas votre email ou votre mot de passe. 😭
            </div>
          </template>
        </MyEmailInput>
      </div>
      <div class="mt-6">
        <div class="text-gray-800">Mot de passe</div>
        <input
          @change="password = $event.target.value"
          @keyup.enter="connect"
          class="input w-full mt-2"
          type="password"
          autocomplete="new-password"
          id="new-password"
          required
        />
        <div v-if="invalidLogin" class="text-right text-red-600">
          Je ne reconnais pas votre email ou votre mot de passe. 😭
        </div>

        <div class="text-right">
          <router-link to="/lost-password" class="text-gray-600 mt-1 text-sm"
            >Mot de passe perdu ?</router-link
          >
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
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed, ref, watch } from "vue";
import { isEmailValid, isPasswordValid } from "../utils/form-validation.js";
import MascotteTip from "../components/MascotteTip.vue";
import MyEmailInput from "../components/MyEmailInput.vue";
import { useTitle } from "@vueuse/core";

useTitle("Connexion - soklaki.fr");

const store = useStore();
const router = useRouter();

const email = ref("");
const password = ref("");

// Validation error
const emailValid = ref(true);
const passwordValid = ref(true);

const invalidLogin = computed(() => store.state.login.error.invalid);

const token = computed(() => store.state.login.token);

watch(
  () => store.state.login.token,
  (token, prevToken) => {
    router.push("/");
  }
);

const connect = () => {
  // Basic validations
  emailValid.value = isEmailValid(email.value);
  passwordValid.value = isPasswordValid(password.value);

  if (!emailValid.value || !passwordValid.value) {
    // First correct inputs
    return;
  }

  store.dispatch("login", { email: email.value, password: password.value });
};
</script>

<style scoped></style>
