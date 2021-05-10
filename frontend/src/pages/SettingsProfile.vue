<template>
  <div class="my-4 px-2">
    <div class="form-label">Vos informations</div>
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
    <div class="form-label mt-20">Les informations de votre école</div>
    <InputTextWithLabel
      class="mt-8"
      label="Le nom de votre école"
      :value="groupName"
      @save="saveGroupName"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useStore } from "vuex";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";

const store = useStore();

const groupName = computed(() => store.state.group.name);
const saveGroupName = async (value) => {
  await store.dispatch("updateGroupName", {
    groupId: store.state.login.groupId,
    groupName: value,
  });
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
};
const saveUserLastname = async (value) => {
  await store.dispatch("saveUserName", {
    userId: store.state.login.userId,
    firstname: currentUser.value.firstname,
    lastname: value,
  });
};
</script>
