<template>
  <div class="my-4 px-2">
    <Loading :loading="loading">
      <div class="form-label">Élève</div>
      <div class="grid grid-cols-1 md:grid-cols-2">
        <InputTextWithLabel
          class="mt-8"
          label="Prénom"
          :value="student.firstname"
          @save="saveFirstname"
        />
        <InputTextWithLabel
          class="mt-8"
          label="Nom"
          :value="student.lastname"
          @save="saveLastname"
        />
        <InputDateWithLabel
          class="mt-8"
          label="Date d'anniversaire"
          :value="student.birthdate"
          @save="saveBirthdate"
        />
        <div></div>
        <InputDateWithLabel
          class="mt-8"
          label="Date d'entrée à l'école"
          :value="student.school_entry"
          @save="saveSchoolEntry"
        />
        <div class="mt-8">
          <div v-if="student.school_exit != null || addSchoolExit == true">
            <InputDateWithLabel
              class="mt-8"
              label="Date de sortie de l'école"
              :value="student.school_exit"
              :edit="addSchoolExit"
              :nullable="true"
              @save="saveSchoolExit"
              @cancel="addSchoolExit = false"
            />
          </div>
          <div v-else>
            <div class="form-sub-label">L'élève est toujours à l'école</div>
            <button
              @click="addSchoolExit = true"
              class="button-minor-action text-xs"
            >
              Ajouter une date de sortie
            </button>
          </div>
        </div>
      </div>
      <div class="mt-8">
        <router-link
          to="/students"
          class="text-gray-700 text-xs hover:text-teal-500"
        >
          Retourner à la liste des élèves↵
        </router-link>
      </div>
    </Loading>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import { useTitle } from "@vueuse/core";
import IconCheck from "../icons/IconCheck.vue";
import IconPencil from "../icons/IconPencil.vue";
import Loading from "../components/Loading.vue";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";
import InputDateWithLabel from "../components/InputDateWithLabel.vue";

useTitle("Élève - soklaki.fr");

const store = useStore();
const route = useRoute();
const router = useRouter();

const saveLastname = async (value) => {
  const studentId = Number(route.params.id);
  await store.dispatch("updateStudentLastname", {
    studentId: studentId,
    lastname: value,
  });
};
const saveFirstname = async (value) => {
  const studentId = Number(route.params.id);
  await store.dispatch("updateStudentFirstname", {
    studentId: studentId,
    firstname: value,
  });
};
const saveBirthdate = async (value) => {
  // TODO check date validity ?
  const studentId = Number(route.params.id);
  await store.dispatch("updateStudentBirthdate", {
    studentId: studentId,
    birthdate: value,
  });
};
const saveSchoolEntry = async (value) => {
  // TODO check date validity ?
  const studentId = Number(route.params.id);
  await store.dispatch("updateStudentSchoolEntry", {
    studentId: studentId,
    schoolEntry: value,
  });
};
const addSchoolExit = ref(false);
const saveSchoolExit = async (value) => {
  // TODO check date validity ?
  const studentId = Number(route.params.id);
  await store.dispatch("updateStudentSchoolExit", {
    studentId: studentId,
    schoolExit: value,
  });
  addSchoolExit.value = false;
};

const loading = ref(true);
const student = ref(null);

const loadStudent = async () => {
  loading.value = true;
  let id = Number(route.params.id);
  if (!id) {
    // id is not a number :(
    return;
  }
  student.value = await store.dispatch("student", id);
  loading.value = false;
};

onMounted(async () => {
  await loadStudent();
});
watch(() => route.params.id, loadStudent);
</script>
