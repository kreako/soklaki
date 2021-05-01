<template>
  <div class="my-4 px-2">
    <div class="form-label">Nouvel élève</div>
    <div class="mt-8">
      <div class="form-sub-label">Prénom</div>
      <input type="text" v-model="firstname" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Nom</div>
      <input type="text" v-model="lastname" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date d'anniversaire</div>
      <input type="text" v-model="birthdate" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date d'entrée à l'école</div>
      <input type="text" v-model="schoolEntry" class="mt-2 input w-full" />
    </div>
    <div class="mt-8">
      <div class="form-sub-label">Date de sortie de l'école</div>
      <input type="text" v-model="schoolExit" class="mt-2 input w-full" />
    </div>
    <div class="flex flex-row space-x-2 items-center mt-8">
      <button @click="cancel" class="button-minor-action flex-grow-0">
        Annuler
      </button>
      <button @click="save" class="button-main-action flex-grow">
        Sauvegarder
      </button>
    </div>
  </div>
</template>
<script setup>
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { computed, ref } from "vue";

const store = useStore();
const router = useRouter();

const firstname = ref("");
const lastname = ref("");
const birthdate = ref("");
const schoolEntry = ref("");
const schoolExit = ref("");

const cancel = () => {
  router.back();
};

const save = async (value) => {
  // TODO date validity check
  const id = await store.dispatch("insertStudent", {
    birthdate: birthdate.value,
    firstname: firstname.value,
    lastname: lastname.value,
    groupId: store.state.login.groupId,
    schoolEntry: schoolEntry.value,
    schoolExit: schoolExit.value == "" ? null : schoolExit.value,
  });
  router.push(`/student/${id}`);
};
</script>
