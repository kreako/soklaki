<template>
  <div class="flex items-center">
    <div class="flex-grow"></div>
    <div class="px-2 w-full sm:max-w-screen-sm">
      <MascotteTip>
        <template v-slot:title>
          Vous avez oublié votre mot de passe ? 😭
        </template>
        <template v-slot:default>
          Pas de problème !
          <br />
          <a href="https://soklaki.fr/#contact" class="text-blue-600">
            Contactez moi
          </a>

          et je vous fais parvenir un lien pour le changer.
        </template>
      </MascotteTip>
    </div>
    <div class="flex-grow"></div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { computed, ref } from "vue";
import { isEmailValid } from "../utils/form-validation.js";
import MascotteTip from "../components/MascotteTip.vue";
import MyEmailInput from "../components/MyEmailInput.vue";
import { useTitle } from "@vueuse/core";

useTitle("Mot de passe perdu - soklaki.fr");

const store = useStore();

const email = ref("");

// Validation error
const emailValid = ref(true);

const reset = () => {
  // Basic validations
  emailValid.value = isEmailValid(email.value);

  if (!emailValid.value) {
    // First correct inputs
    return;
  }

  window.console.log("email", email.value);
  store.dispatch("resetPassword", { email: email.value });
};
</script>

<style scoped></style>
