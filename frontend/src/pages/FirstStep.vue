<template>
  <div class="px-2">
    <MascotteTip class="mt-4">
      <template v-slot:title>Encore quelques infos... 🙇</template>
      <template v-slot:default>
        C'est pour commencer, rien de définitif, tout sera modifiable dans la
        partie <span class="font-mono">Réglages</span>.
      </template>
    </MascotteTip>
    <div class="mt-8 form-label">Nos premiers pas ensemble...</div>
    <!-- Group name -->
    <InputTextWithLabel
      class="mt-8"
      label="Le nom de votre école"
      :value="groupName"
      @save="saveGroupName"
    />

    <!-- Firstname and lastname -->
    <InputTextWithLabel
      class="mt-8"
      label="Votre prénom"
      :value="currentUser.firstname"
      @save="saveUserFirstname"
    />
    <InputTextWithLabel
      class="mt-8"
      label="Votre nom"
      :value="currentUser.lastname"
      @save="saveUserLastname"
    />
    <div class="mt-8">
      <div class="form-sub-label">La génération du socle</div>
      <div v-if="!socleValid" class="font-serif text-red-500">En cours...</div>
      <div v-else class="flex flex-row items-center">
        <div class="font-serif">Fait !</div>
        <IconCheck class="h-4 text-green-500" />
      </div>
    </div>
    <div class="mt-8">
      <div class="form-sub-label">La création d'une période</div>
      <div v-if="!periodValid" class="font-serif text-red-500">En cours...</div>
      <div v-else class="flex flex-row items-center">
        <div class="font-serif">Fait !</div>
        <IconCheck class="h-4 text-green-500" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { searchOrCreatePeriod } from "../utils/period";
import { dateJsObj, today } from "../utils/date";
import MascotteTip from "../components/MascotteTip.vue";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";
import IconPencil from "../icons/IconPencil.vue";
import IconCheck from "../icons/IconCheck.vue";
import { useTitle } from "@vueuse/core";

useTitle("Premiers pas - soklaki.fr");

const store = useStore();
const router = useRouter();

const groupName = computed(() => store.state.group.name);
const saveGroupName = async (value) => {
  await store.dispatch("updateGroupName", {
    groupId: store.state.login.groupId,
    groupName: value,
  });
  checkEnd();
};

const currentUser = computed(() =>
  store.getters.userById(store.state.login.userId)
);
const saveUserFirstname = async (value) => {
  await store.dispatch("saveUserName", {
    userId: store.state.login.userId,
    firstname: value,
    lastname: currentUser.value.lastname,
  });
  checkEnd();
};
const saveUserLastname = async (value) => {
  await store.dispatch("saveUserName", {
    userId: store.state.login.userId,
    firstname: currentUser.value.firstname,
    lastname: value,
  });
  checkEnd();
};

const socleValid = computed(
  () => Object.keys(store.state.socle.containers).length !== 0
);

const periodValid = computed(() => store.state.currentPeriod != null);

const checkEnd = () => {
  const periods = store.state.periods;
  const group = store.state.group;
  const users = store.state.users;
  if (!periodValid.value) {
    return;
  }
  if (group.name == null) {
    return;
  }
  const userId = store.state.login.userId;
  if (!(userId in users)) {
    return;
  }
  const firstname = users[userId].firstname;
  if (firstname == null) {
    return;
  }
  const lastname = users[userId].lastname;
  if (lastname == null) {
    return;
  }
  if (!socleValid.value) {
    return;
  }
  router.push("/");
};

onMounted(async () => {
  if (!socleValid.value) {
    await store.dispatch("loadSocle");
    checkEnd();
  }
  if (!periodValid.value) {
    await searchOrCreatePeriod(today(), store.state, store.dispatch);
    checkEnd();
  }
});
</script>
