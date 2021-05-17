<template>
  <div class="flex items-center">
    <div class="flex-grow"></div>
    <div v-if="tokenValid == null" class="px-2 w-full sm:max-w-screen-sm">
      <MascotteTip>
        <template v-slot:title>Bienvenue ! 👋</template>
        <template v-slot:default>
          Veuillez patienter pendant que je vérifie tout ça...
        </template>
      </MascotteTip>
    </div>
    <div v-else-if="tokenValid == false" class="px-2 w-full sm:max-w-screen-sm">
      <MascotteTip>
        <template v-slot:title>Bienvenue ! 👋</template>
        <template v-slot:default>
          <div v-if="tokenTooOld == true">
            Désolé mais le lien que vous avez utilisé n'est plus valide. Il a
            plus de 3 jours... 😥
            <br />
            Il vous faut en demander un autre à {{ tokenUserFirstname }}
            {{ tokenUserLastname }}...
          </div>
          <div v-else>
            Désolé mais le lien que vous avez utilisé n'est pas valide.
            <br />
            Il n'est peut-être pas entier ?
          </div>
        </template>
      </MascotteTip>
    </div>
    <div v-else-if="tokenValid == true" class="px-2 w-full sm:max-w-screen-sm">
      <MascotteTip>
        <template v-slot:title>Bienvenue ! 👋</template>
        <template v-slot:default>
          <div class="mt-4">
            Vous avez été invité par
            <span class="font-bold">
              {{ tokenUserFirstname }} {{ tokenUserLastname }}
            </span>
            à rejoindre le groupe
            <span class="font-bold">
              {{ tokenGroupName }}
            </span>
            pour participer à l'évaluation du socle.
          </div>
          <div class="mt-4">Donnez-moi un email et un mot de passe !</div>
        </template>
      </MascotteTip>
      <div class="mt-6 sm:mt-12">
        <MyEmailInput
          @change="email = $event"
          :email="email"
          :error="!emailValid"
        >
          <template v-slot:error>
            <span v-if="!emailValid">
              Oh non ! Il semblerait que votre email ne ressemble pas à un
              email...
            </span>
          </template>
        </MyEmailInput>
      </div>
      <div class="mt-6">
        <div class="text-gray-800">Votre mot de passe</div>
        <input
          @change="password = $event.target.value"
          @keyup.enter="signup"
          class="input w-full mt-2"
          :class="{ 'input-error': !passwordValid }"
          type="password"
          autocomplete="new-password"
          id="new-password"
          required
        />
        <div v-if="!passwordValid" class="text-right text-red-600">
          Oh non ! Il semblerait que votre mot de passe soit trop court. 8
          caractères minimum !
        </div>
      </div>
      <div class="mt-8">
        <button @click="signup" class="button-main-action">Inscription</button>
      </div>
    </div>
    <div class="flex-grow"></div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { useRouter, useRoute } from "vue-router";
import { computed, ref, watch, onMounted } from "vue";
import { isEmailValid, isPasswordValid } from "../utils/form-validation.js";
import MascotteTip from "../components/MascotteTip.vue";
import MyEmailInput from "../components/MyEmailInput.vue";
import { useTitle } from "@vueuse/core";

useTitle("Invitation - soklaki.fr");

const store = useStore();
const router = useRouter();
const route = useRoute();

// values
const email = ref("");
const password = ref("");

// Validation error
const emailValid = ref(true);
const passwordValid = ref(true);

const errorWeakPassword = computed(() => store.state.login.error.weakPassword);

const token = computed(() => store.state.login.token);

watch(
  () => store.state.login.token,
  (token, prevToken) => {
    router.push("/");
  }
);

const signup = () => {
  // Basic validations
  emailValid.value = isEmailValid(email.value);
  passwordValid.value = isPasswordValid(password.value);

  if (!emailValid.value || !passwordValid.value) {
    // First correct inputs
    return;
  }

  store.dispatch("invitationSignupToken", {
    email: email.value,
    password: password.value,
    token: route.query.token,
  });
};

const tokenValid = ref(null);
const tokenTooOld = ref(null);
const tokenUserFirstname = ref(null);
const tokenUserLastname = ref(null);
const tokenGroupName = ref(null);

onMounted(async () => {
  const answer = await store.dispatch(
    "invitationVerifyToken",
    route.query.token
  );
  tokenValid.value = answer.valid;
  tokenTooOld.value = answer.too_old;
  tokenUserFirstname.value = answer.user_firstname;
  tokenUserLastname.value = answer.user_lastname;
  tokenGroupName.value = answer.group_name;
});
</script>
