<template>
  <div class="my-4 px-2">
    <div class="form-label">Élève</div>
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
    <InputTextWithLabel
      class="mt-8"
      label="Date d'anniversaire"
      :value="student.birthdate"
      @save="saveBirthdate"
    />
    <InputTextWithLabel
      class="mt-8"
      label="Date d'entrée à l'école"
      :value="student.school_entry"
      @save="saveSchoolEntry"
    />
    <div class="mt-8">
      <div v-if="student.school_exit != null || addSchoolExit == true">
        <InputTextWithLabel
          class="mt-8"
          label="Date de sortie de l'école"
          :value="student.school_exit"
          :edit="addSchoolExit"
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
    <div class="mt-8">
      <button
        @click="router.back()"
        class="text-gray-700 text-xs hover:text-teal-500"
      >
        Retourner à la liste des élèves↵
      </button>
    </div>
  </div>
</template>

<script setup>
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import { computed, ref, onMounted, watch } from "vue";
import IconCheck from "../icons/IconCheck.vue";
import IconPencil from "../icons/IconPencil.vue";
import InputTextWithLabel from "../components/InputTextWithLabel.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const student = computed(() => store.getters.studentById(route.params.id));

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
</script>
